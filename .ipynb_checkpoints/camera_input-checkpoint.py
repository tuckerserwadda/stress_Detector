# camera input
import streamlit as st
from PIL import Image

def render_camera():
    st.subheader("📷 Capture a Selfie")
    photo_file = st.camera_input("Take a clear, well-lit selfie (front-facing).")
    return (Image.open(photo_file) if photo_file is not None else None)