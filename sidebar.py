# sidebar.py
import streamlit as st
from constants import DEFAULT_W_TEXT, DEFAULT_W_FACE, DEFAULT_W_QUEST, DEFAULT_THRESHOLD

def render_sidebar(metrics: dict):
    st.sidebar.header("⚙️ Fusion Settings")
    w_text = st.sidebar.slider("Text weight", 0.0, 1.0, DEFAULT_W_TEXT, 0.05)
    w_face = st.sidebar.slider("Face weight", 0.0, 1.0, DEFAULT_W_FACE, 0.05)
    w_quest = st.sidebar.slider("Questionnaire weight", 0.0, 1.0, DEFAULT_W_QUEST, 0.05)
    thresh = st.sidebar.slider("Decision threshold", 0.50, 0.90, DEFAULT_THRESHOLD, 0.01)
    if abs(w_text + w_face + w_quest - 1.0) > 1e-6:
        st.sidebar.caption("Weights are normalized internally if not summing to 1.")
    return w_text, w_face, w_quest, thresh