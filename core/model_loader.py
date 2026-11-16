from pathlib import Path
import joblib
import tensorflow as tf


def check_model_files(model_dir):
    model_dir = Path(model_dir)
    filenames = [
        "baseline.joblib",
        "supervised.joblib",
        "clusters.joblib",
        "images.keras",
        "mobilenetv2_waste.keras",
    ]
    return {name: (model_dir / name).is_file() for name in filenames}


def load_models(model_dir):
    """Load persisted models. No training takes place in this function."""
    model_dir = Path(model_dir)
    required = [
        "baseline.joblib",
        "supervised.joblib",
        "clusters.joblib",
        "images.keras",
    ]
    missing = [name for name in required if not (model_dir / name).is_file()]
    if missing:
        raise FileNotFoundError(
            "Required model file(s) missing from "
            f"{model_dir}: {', '.join(missing)}"
        )

    loaded = {
        "baseline": joblib.load(model_dir / "baseline.joblib"),
        "supervised": joblib.load(model_dir / "supervised.joblib"),
        "clusters": joblib.load(model_dir / "clusters.joblib"),
        "cnn": tf.keras.models.load_model(model_dir / "images.keras"),
    }

    # MobileNetV2 is optional until its final filename is confirmed.
    mobile_path = model_dir / "mobilenetv2_waste.keras"
    if mobile_path.is_file():
        loaded["mobilenet"] = tf.keras.models.load_model(mobile_path)

    return loaded
