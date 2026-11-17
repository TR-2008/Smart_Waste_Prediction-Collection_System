from pathlib import Path
import json
import numpy as np
import pandas as pd
from PIL import Image

def read_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return {} if default is None else default
    return json.loads(path.read_text(encoding="utf-8"))

def predict_collection(models, model_dir, fill_pct, days_since_collection, footfall, capacity_l, location_type):
    metadata = read_json(Path(model_dir) / "supervised_metadata.json")
    features = metadata.get("features", [
        "fill_pct", "days_since_collection", "footfall", "capacity_l", "location_type"
    ])
    values = {
        "fill_pct": float(fill_pct),
        "days_since_collection": int(days_since_collection),
        "footfall": int(footfall),
        "capacity_l": int(capacity_l),
        "location_type": str(location_type),
    }
    row = pd.DataFrame([{name: values[name] for name in features}])
    model = models["supervised"]
    prediction = int(model.predict(row)[0])
    probabilities = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(row)[0]
        classes = list(model.classes_)
        probabilities = {str(int(cls)): float(prob) for cls, prob in zip(classes, probs)}
    baseline_prediction = int(models["baseline"].predict(row)[0])
    return {
        "prediction": prediction,
        "label": metadata.get("class_labels", {}).get(str(prediction), "Collection review" if prediction else "No collection review"),
        "probabilities": probabilities,
        "baseline_prediction": baseline_prediction,
        "baseline_label": "Collection review" if baseline_prediction else "No collection review",
        "features": values,
    }

def predict_cluster(models, model_dir, fill_pct, days_since_collection, footfall, capacity_l):
    metadata = read_json(Path(model_dir) / "cluster_metadata.json")
    features = metadata.get("features", ["fill_pct", "days_since_collection", "footfall", "capacity_l"])
    values = {
        "fill_pct": float(fill_pct),
        "days_since_collection": int(days_since_collection),
        "footfall": int(footfall),
        "capacity_l": int(capacity_l),
    }
    row = pd.DataFrame([{name: values[name] for name in features}])
    cluster_id = int(models["clusters"].predict(row)[0])
    description = metadata.get("group_descriptions", {}).get(str(cluster_id), "Cluster profile")
    return {"cluster": cluster_id, "description": description, "features": values}

def prepare_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB").resize((96, 96))
    array = np.asarray(image, dtype=np.uint8)
    return image, np.expand_dims(array, axis=0)

def predict_material(models, image_batch, model_choice="MobileNetV2", metadata_dir=None):
    key = "mobilenet" if model_choice == "MobileNetV2" else "cnn"
    if key not in models:
        raise FileNotFoundError(f"{model_choice} model is not loaded. Check its .keras file.")
    probabilities = np.asarray(models[key].predict(image_batch, verbose=0))[0]
    classes = ["paper", "plastic", "metal"]
    index = int(np.argmax(probabilities))
    return {
        "model": model_choice,
        "class": classes[index],
        "confidence": float(probabilities[index]),
        "probabilities": {name: float(prob) for name, prob in zip(classes, probabilities)},
    }
