# main_ui.py
import streamlit as st

def render_main_header():
    st.title("🎓 Multimodal Academic Stress Detection")
    st.markdown("Answer a brief check-in, (optionally) type what you’re experiencing, and **capture a selfie**. We’ll combine all signals to estimate stress.")