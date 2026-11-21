from pathlib import Path
import streamlit as st
from core.settings_manager import load_settings
from core.ui import apply_theme, render_brand
ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title="Smart Waste Management & Prediction System",page_icon="♻️",layout="wide",initial_sidebar_state="expanded")
settings=load_settings()
st.session_state["operating_mode"]=settings["system_mode"]
st.session_state["ui_theme"]=settings["theme"]
st.session_state["image_model_choice"]=settings["image_model"]
apply_theme(settings["theme"])
manual=[st.Page("pages/1_Manual_AI.py",title="Bin Overview & Collection Review",icon="🧠",url_path="bin-overview"),st.Page("pages/2_Material_Recognition.py",title="Material Recognition",icon="♻️",url_path="material-recognition"),st.Page("pages/3_Analytics.py",title="Bin Profiles",icon="📊",url_path="bin-profiles"),st.Page("pages/4_Feedback_NLP.py",title="Collection Comments",icon="💬",url_path="collection-comments"),st.Page("pages/5_Facilities_Summary.py",title="Facilities Summary",icon="🏢",url_path="facilities-summary")]
nav={"MAIN WORKSPACE":[st.Page("pages/0_Overview.py",title="Home",icon="🏠",url_path="home")]+manual,"PREFERENCES":[st.Page("pages/5_System_Settings.py",title="System Settings",icon="⚙️",url_path="system-settings")]}
if settings["system_mode"]=="Advanced": nav["ADVANCED WORKSPACE"]=[st.Page("pages/9_Advanced_Analytics.py",title="Advanced Analytics",icon="📈",url_path="advanced-analytics"),st.Page("pages/7_Model_Comparison.py",title="Model Comparison",icon="🧪",url_path="model-comparison"),st.Page("pages/6_IoT_Status.py",title="IoT Monitoring",icon="📡",url_path="iot-monitoring"),st.Page("pages/8_AI_Summary.py",title="AI Summary",icon="✨",url_path="ai-summary")]
render_brand(settings["system_mode"])
page=st.navigation(nav,position="sidebar",expanded=True)
page.run()
