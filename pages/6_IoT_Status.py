from pathlib import Path
import streamlit as st
from core.ui import render_sidebar, apply_theme, section_header

ROOT = Path(__file__).resolve().parents[1]
st.set_page_config(page_title="IoT Status", page_icon="📡", layout="wide")
render_sidebar(ROOT)
apply_theme(st.session_state.get("ui_theme", "Dark"))
section_header("IoT Device Status", "Hardware integration readiness.")

st.warning("No ESP32 telemetry transport or device credentials were included in the supplied source ZIP. Live readings are therefore not connected.")
a, b, c = st.columns(3)
a.metric("Device connection", "Not configured")
b.metric("Sensor stream", "Offline")
c.metric("Last reading", "—")
st.markdown("#### Required hardware integration details")
st.write("- ESP32 board and firmware")
st.write("- Ultrasonic sensor model and GPIO pin mapping")
st.write("- Communication method: HTTP, MQTT or serial")
st.write("- Wi-Fi/network endpoint and payload format")
st.caption("Do not treat demo/simulated readings as actual sensor measurements.")
