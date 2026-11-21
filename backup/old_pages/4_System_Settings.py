import streamlit as st

st.title("System Settings")
st.caption("Application preferences and operating modes.")

if "operating_mode" not in st.session_state:
    st.session_state.operating_mode = "Manual"

st.radio(
    "Operating mode",
    ["Manual", "Advanced IoT"],
    key="operating_mode",
    horizontal=True,
)

st.selectbox(
    "Image classification model",
    ["CNN", "MobileNetV2"],
    key="image_model_choice",
)

st.toggle("Enable AI-generated summaries", value=False, key="ai_summaries")
st.toggle("Enable notifications", value=True, key="notifications")

st.warning(
    "These are initial UI settings. IoT connectivity, notification delivery "
    "and summary-provider integration are not active yet."
)
