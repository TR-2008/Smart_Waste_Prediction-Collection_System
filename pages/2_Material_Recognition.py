import streamlit as st

st.title("Material Recognition")
st.caption("Classify an uploaded image as paper, plastic or metal.")

uploaded = st.file_uploader(
    "Upload a waste image",
    type=["png", "jpg", "jpeg"],
)

if uploaded:
    st.image(uploaded, caption="Uploaded image", use_container_width=True)
    st.info(
        "Image preprocessing and CNN/MobileNetV2 inference will be added "
        "after model input and preprocessing parity tests."
    )
