import datetime
import streamlit as st
from text_input import render_text_input
from questionnaire import render_questionnaire
from camera_input import render_camera



# Text input
user_text = render_text_input()

# Questionnaire (modularized)
p_q, subscales, questionnaire_payload = render_questionnaire()
questionnaire_payload = {"consent": False, "subscales": {}, "overall": None}

# Camera input
pil_image = render_camera()


if st.button("Analyze"):
    cfg = AnalyzeInputs(
        vectorizer=vectorizer,
        text_model=text_model,
        face_model=face_model,
        face_cascade=face_cascade,
        user_text=user_text,
        pil_image=pil_image,
        p_q=p_q,
        questionnaire_payload=questionnaire_payload,
        w_text=W_TEXT, w_face=W_FACE, w_quest=W_QUEST,
        threshold=THRESH,
        enable_log=True,
    )

    outputs = analyze_inputs(cfg)           # pure compute
    render_results(outputs, user_text)      # UI render
    #maybe_log(outputs, enable_log=True)     # optional persistence + trend