from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import os

# Save this script in your project ROOT folder and run:
# python prepare_dashboard_bundle.py

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT.parent / f"{ROOT.name}_dashboard_review.zip"

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "env", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".idea", ".vscode", "node_modules",
    "models", "model", "nltk_data", ".ipynb_checkpoints",
    "wandb", "runs", "logs", "artifacts", "uploads",
}
EXCLUDED_NAMES = {
    ".env", ".env.local", ".env.production",
    "secrets.toml", "credentials.json", "token.json",
}
ALLOWED_TEXT = {
    ".py", ".md", ".txt", ".toml", ".yaml", ".yml", ".json",
    ".ini", ".cfg", ".css", ".js", ".html", ".sql",
}
ALLOWED_DATA = {".csv"}
ALLOWED_UI_IMAGES = {
    ".png", ".jpg", ".jpeg", ".webp", ".svg", ".ico"
}
MAX_UI_IMAGE_BYTES = 8 * 1024 * 1024
MAX_CSV_BYTES = 15 * 1024 * 1024

def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = set(rel.parts)

    if any(part in EXCLUDED_DIRS for part in parts):
        return False
    lower_name = path.name.lower()
    if lower_name in EXCLUDED_NAMES or lower_name.startswith(".env"):
        return False
    if any(term in lower_name for term in ("secret", "credential", "token", "api_key", "apikey")):
        return False
    if path.suffix.lower() in {".joblib", ".pkl", ".pickle", ".keras", ".h5",
                               ".hdf5", ".npz", ".npy", ".pt", ".pth",
                               ".onnx", ".parquet", ".db", ".sqlite"}:
        return False

    suffix = path.suffix.lower()
    if suffix in ALLOWED_TEXT:
        return True

    if suffix in ALLOWED_DATA and "data" in parts:
        return path.stat().st_size <= MAX_CSV_BYTES

    # Include only interface assets, not training/dataset images.
    if suffix in ALLOWED_UI_IMAGES and ({"assets", "static"} & parts):
        return path.stat().st_size <= MAX_UI_IMAGE_BYTES

    return False

def main():
    if not (ROOT / "app.py").exists():
        print("ERROR: app.py nahi mila.")
        print("Is script ko project ke ROOT folder mein rakhein, jahan app.py mojood hai.")
        raise SystemExit(1)

    files = []
    for current, dirs, names in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        current_path = Path(current)
        for name in names:
            path = current_path / name
            if path.is_file() and should_include(path):
                files.append(path)

    files = sorted(set(files))
    if not files:
        print("ERROR: Koi source files nahi milin.")
        raise SystemExit(1)

    tree_lines = ["Source bundle contents (models, virtual environments and secrets excluded):"]
    for path in files:
        tree_lines.append(f"- {path.relative_to(ROOT).as_posix()}")

    with ZipFile(OUTPUT, "w", ZIP_DEFLATED, compresslevel=6) as zf:
        for path in files:
            zf.write(path, arcname=path.relative_to(ROOT).as_posix())
        zf.writestr("BUNDLE_MANIFEST.txt", "\n".join(tree_lines) + "\n")

    size_mb = OUTPUT.stat().st_size / (1024 * 1024)
    print("\nSUCCESS: Dashboard review ZIP create ho gayi.")
    print(f"Project: {ROOT}")
    print(f"ZIP: {OUTPUT}")
    print(f"Files included: {len(files)}")
    print(f"ZIP size: {size_mb:.2f} MB")
    print("\nIncluded: Python source, pages, core, requirements, configuration/templates,")
    print("CSV data files, documentation and UI assets from assets/ or static/.")
    print("Excluded: model binaries, virtual environments, Git history, caches,")
    print("large image datasets, .env files and secrets.")

if __name__ == "__main__":
    main()