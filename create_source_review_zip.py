from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import os

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "source_review.zip"

# Include source/configuration and small metadata only.
ALLOWED_ROOT_FILES = {
    "app.py", "main.py", "requirements.txt", "pyproject.toml",
    "Pipfile", "Pipfile.lock", "README.md", ".gitignore",
    ".gitattributes", ".env.example"
}
SOURCE_DIRS = ["core", "pages", "iot", "IOT", ".streamlit", "licenses", "reports"]
MAX_SMALL_ASSET = 3 * 1024 * 1024
MAX_NOTEBOOK = 20 * 1024 * 1024

def should_exclude(path: Path):
    parts = {p.lower() for p in path.parts}
    if any(p in parts for p in [".git", ".venv", "venv", "__pycache__", "backup", "backups"]):
        return True
    if path.name.lower() in {".env", "secrets.toml", "credentials.json"}:
        return True
    if path.suffix.lower() in {
        ".keras", ".h5", ".joblib", ".pkl", ".pickle", ".npz",
        ".npy", ".zip", ".7z", ".rar", ".parquet", ".db", ".sqlite"
    }:
        return True
    return False

selected = set()

# Root-level source/config files.
for name in ALLOWED_ROOT_FILES:
    p = ROOT / name
    if p.is_file():
        selected.add(p)

# Python and configuration files in source folders.
for dirname in SOURCE_DIRS:
    folder = ROOT / dirname
    if folder.is_dir():
        for p in folder.rglob("*"):
            if p.is_file() and not should_exclude(p):
                if p.suffix.lower() in {".py", ".toml", ".yaml", ".yml", ".md", ".txt", ".json"}:
                    selected.add(p)
                elif dirname == "assets" and p.stat().st_size <= MAX_SMALL_ASSET:
                    selected.add(p)

# Model metadata only (never model binaries).
models = ROOT / "models"
if models.is_dir():
    for p in models.glob("*.json"):
        if not should_exclude(p):
            selected.add(p)

# Small tabular and JSON project data, but no image arrays or sample-image folders.
data = ROOT / "data"
if data.is_dir():
    for p in data.iterdir():
        if p.is_file() and p.suffix.lower() in {".csv", ".json"} and not should_exclude(p):
            selected.add(p)
    # Include the VADER lexicon text if present; no other downloaded corpora.
    for p in data.rglob("vader_lexicon.txt"):
        if not should_exclude(p):
            selected.add(p)

# Include JSON evaluation reports if present.\nreports = ROOT / "reports"\nif reports.is_dir():\n    for p in reports.rglob("*.json"):\n        if not should_exclude(p):\n            selected.add(p)\n\n# Include the training notebook only if reasonably small.
notebook_dir = ROOT / "notebooks"
if notebook_dir.is_dir():
    for p in notebook_dir.rglob("*.ipynb"):
        if p.stat().st_size <= MAX_NOTEBOOK and not should_exclude(p):
            selected.add(p)

# Add small visual assets if present.
assets = ROOT / "assets"
if assets.is_dir():
    for p in assets.rglob("*"):
        if p.is_file() and p.stat().st_size <= MAX_SMALL_ASSET and not should_exclude(p):
            selected.add(p)

with ZipFile(OUTPUT, "w", ZIP_DEFLATED, compresslevel=6) as zf:
    for p in sorted(selected):
        zf.write(p, p.relative_to(ROOT))

print(f"Created: {OUTPUT}")
print(f"Files included: {len(selected)}")
print(f"ZIP size: {OUTPUT.stat().st_size / (1024 * 1024):.2f} MB")
print("Excluded: model binaries, NPZ/NPY arrays, backup archives, virtual environments, .git and secrets.")
