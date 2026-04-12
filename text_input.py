# render text
import streamlit as st

def render_text_input():
    st.subheader("💬 Text Input (optional)")
    return st.text_area(
        "Describe what you're experiencing (optional):",
        height=120,
        placeholder="Example: I have two midterms next week and I’m exhausted."
    )