from pathlib import Path
import streamlit as st
from core.model_loader import load_models, check_model_files

ROOT_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Community Waste AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session-based visual theme. This styles the app; Streamlit's native
# widget theme can be refined later after the first UI pass.
if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "Dark"

with st.sidebar:
    st.title("♻️ Community Waste AI")
    st.caption("AI-powered waste collection assistant")
    st.selectbox(
        "Appearance",
        ["Dark", "Light"],
        key="ui_theme",
    )
    st.divider()
    st.caption("Navigation")
    st.page_link("app.py", label="Overview", icon="🏠")
    st.page_link("pages/1_Manual_AI.py", label="Manual AI", icon="🧠")
    st.page_link("pages/2_Material_Recognition.py", label="Material Recognition", icon="🖼️")
    st.page_link("pages/3_Analytics.py", label="Analytics", icon="📊")
    st.page_link("pages/4_System_Settings.py", label="System Settings", icon="⚙️")

if st.session_state.ui_theme == "Dark":
    st.markdown("""
    <style>
    .stApp { background: #0b1220; color: #e5edf7; }
    [data-testid="stSidebar"] { background: #111c2e; }
    [data-testid="stMetric"] {
        background: #142238; padding: 16px; border-radius: 14px;
        border: 1px solid #263b56;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp { background: #f5f8fc; color: #172033; }
    [data-testid="stSidebar"] { background: #eaf0f8; }
    [data-testid="stMetric"] {
        background: #ffffff; padding: 16px; border-radius: 14px;
        border: 1px solid #dce5f0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Community Waste Collection & Sorting Assistant")
st.caption("AI models, operational insights and IoT monitoring in one workspace.")

st.info(
    "This is the initial application shell. The next development step is to "
    "connect and test each model workflow before enabling live controls."
)

# Check files without loading the large models on every page rerun.
checks = check_model_files(ROOT_DIR / "models")
c1, c2, c3, c4 = st.columns(4)
for col, label, filename in [
    (c1, "Decision / baseline", "baseline.joblib"),
    (c2, "Supervised pipeline", "supervised.joblib"),
    (c3, "KMeans pipeline", "clusters.joblib"),
    (c4, "CNN image model", "images.keras"),
]:
    col.metric(label, "Found" if checks.get(filename, False) else "Missing")

mobile = checks.get("mobilenetv2_waste.keras", False)
st.metric("MobileNetV2", "Found" if mobile else "Not found")

with st.expander("Load and verify saved models"):
    if st.button("Load models now", type="primary"):
        with st.spinner("Loading saved models..."):
            try:
                loaded = load_models(ROOT_DIR / "models")
                st.success("Available models loaded successfully.")
                st.write("Loaded components:", list(loaded.keys()))
            except Exception as exc:
                st.error(f"Model loading failed: {exc}")

st.subheader("System modules")
cols = st.columns(3)
modules = [
    ("Manual AI", "Collection decision support"),
    ("Material Recognition", "Paper, plastic and metal image classification"),
    ("Analytics", "Clustering, trends and model evaluation"),
]
for col, (name, description) in zip(cols, modules):
    with col:
        st.markdown(f"### {name}")
        st.write(description)
        st.caption("Module scaffold — implementation follows in the next phase.")
