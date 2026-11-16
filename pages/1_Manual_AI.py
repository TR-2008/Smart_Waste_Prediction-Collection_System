import streamlit as st

st.title("Manual AI Mode")
st.caption("Manual bin assessment and collection decision support.")

st.warning(
    "The form and prediction service will be connected after we confirm "
    "the exact feature schema and categorical values used during training."
)
st.write("Expected model features:")
st.code(
    "fill_pct, days_since_collection, footfall, capacity_l, location_type"
)
