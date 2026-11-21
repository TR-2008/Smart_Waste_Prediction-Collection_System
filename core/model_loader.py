from pathlib import Path
import joblib
import tensorflow as tf

MODEL_FILES = {"baseline":"baseline.joblib","supervised":"supervised.joblib","clusters":"clusters.joblib","cnn":"images.keras","mobilenet":"mobilenetv2_waste.keras"}

def check_model_files(model_dir):
    p=Path(model_dir)
    return {filename:(p/filename).is_file() for filename in MODEL_FILES.values()}

def load_models(model_dir):
    """Load whichever artifacts exist; do not train or silently fake missing models."""
    p=Path(model_dir); loaded={}; errors={}
    for key, filename in MODEL_FILES.items():
        path=p/filename
        if not path.is_file(): continue
        try:
            loaded[key] = joblib.load(path) if filename.endswith('.joblib') else tf.keras.models.load_model(path)
        except Exception as exc:
            errors[key] = f"{type(exc).__name__}: {exc}"
    if errors: loaded["_load_errors"] = errors
    return loaded

def require_models(models, *keys):
    missing=[k for k in keys if k not in models]
    if missing:
        details=models.get('_load_errors',{})
        extra='; '.join(f'{k}: {details[k]}' for k in missing if k in details)
        raise RuntimeError('Required model(s) are not loaded: '+', '.join(missing)+(('. '+extra) if extra else '. Check models/ and package versions.'))
