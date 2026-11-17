from pathlib import Path
import streamlit as st
from core.ui import render_sidebar, apply_theme, section_header

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="System Settings", page_icon="⚙️", layout="wide")
render_sidebar(ROOT)
apply_theme(st.session_state.get("ui_theme", "Dark"))
section_header("System Settings", "Session preferences and integration controls.")

st.radio("Operating mode", ["Manual", "Advanced IoT"], key="operating_mode", horizontal=True)
st.selectbox("Default image classifier", ["MobileNetV2", "CNN"], key="image_model_choice")
st.toggle("Enable AI-generated summaries", value=False, key="ai_summaries")
st.toggle("Enable notifications", value=False, key="notifications")
st.info("These preferences are session-level UI settings. Persistent user accounts, email/SMS delivery and live device control require additional services.")
st.warning("Do not paste API keys into this page or commit them to GitHub. Store secrets in .streamlit/secrets.toml locally or the hosting platform's secrets manager.")
