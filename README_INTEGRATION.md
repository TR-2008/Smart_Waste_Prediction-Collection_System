# Smart Waste integration update

This package adds integrated Streamlit pages and backend functions based on the
source review ZIP. It does NOT include model binaries. Keep your existing
`models/*.keras` and `models/*.joblib` files in the project.

## Merge
Back up the current project first. Copy the package files into the project root,
preserving the existing `models/`, `data/`, `notebooks/`, `reports/`, and `licenses/`.
Review same-name files before overwriting.

## Run
Use the existing project virtual environment. Compare package versions with the
Colab training runtime before changing TensorFlow, NumPy, or scikit-learn.

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Model paths expected
- models/baseline.joblib
- models/supervised.joblib
- models/clusters.joblib
- models/images.keras
- models/mobilenetv2_waste.keras (optional but supported)

## Notes
- CNN and MobileNetV2 are expected to receive RGB uint8 image batches of shape
  `(N, 96, 96, 3)`. Both models contain their own preprocessing layers.
- MobileNetV2 resizes internally to 160x160 and scales to [-1, 1].
- VADER lexicon is loaded from `data/nltk_data/sentiment/vader_lexicon/vader_lexicon.txt`.
- IoT live telemetry is not implemented until the ESP32 transport and payload are supplied.
- Groq API integration is not included in this first integration bundle. Add it only
  after a key is configured securely and the desired summary workflow is confirmed.
- Reported metrics are read from the saved JSON reports; they are not recomputed by the app.
