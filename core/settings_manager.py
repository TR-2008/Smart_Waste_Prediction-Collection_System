"""Atomic persistence for application preferences."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config"
SETTINGS_FILE = CONFIG_DIR / "user_settings.json"
DEFAULT_SETTINGS = {"system_mode":"Manual","theme":"Dark","image_model":"CNN","summary_mode":"Offline","dashboard_layout":"Expanded","notifications":True,"auto_model_loading":True}

def load_settings():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        saved = json.loads(SETTINGS_FILE.read_text(encoding="utf-8")) if SETTINGS_FILE.exists() else {}
        if not isinstance(saved, dict): saved = {}
    except (OSError, json.JSONDecodeError): saved = {}
    clean = {**DEFAULT_SETTINGS, **{k:v for k,v in saved.items() if k in DEFAULT_SETTINGS}}
    if clean["system_mode"] not in ("Manual","Advanced"): clean["system_mode"]="Manual"
    if clean["theme"] not in ("Dark","Light"): clean["theme"]="Dark"
    if clean["image_model"] not in ("CNN","MobileNetV2"): clean["image_model"]="CNN"
    return clean

def save_settings(settings):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    clean = {**DEFAULT_SETTINGS, **{k:v for k,v in settings.items() if k in DEFAULT_SETTINGS}}
    tmp = SETTINGS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(clean, indent=2), encoding="utf-8")
    tmp.replace(SETTINGS_FILE)
    return clean
