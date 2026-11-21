import streamlit as st
from core.ui import apply_theme,section_header
apply_theme(st.session_state.get('ui_theme','Dark')); section_header('IoT Monitoring','Hardware integration readiness — live readings are not connected.')
st.warning('No ESP32 firmware, sensor pin mapping or telemetry contract was included. This page intentionally does not show simulated values as live readings.')
a,b,c=st.columns(3); a.metric('Device connection','Not configured'); b.metric('Sensor stream','Offline'); c.metric('Last reading','—')
st.markdown('### Required before integration'); st.write('- ESP32 board and firmware version\n- Ultrasonic sensor model and GPIO pins\n- Bin/device identifier\n- Transport: HTTP, MQTT or serial\n- Example payload and authentication method')
st.caption('Never commit Wi-Fi passwords or broker credentials.')
