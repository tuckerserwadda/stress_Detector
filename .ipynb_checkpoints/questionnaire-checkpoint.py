import streamlit as st
from helper import questionnaire_score_from_subscales 

LIKERT = ["Not at all (0)", "Slightly (1)", "Somewhat (2)", "Very (3)", "Extremely (4)"]
LIKERT_TO_INT = {lab: i for i, lab in enumerate(LIKERT)}

def _pick(label, help_text=""):
    return st.select_slider(label, options=LIKERT, value="Somewhat (2)", help=help_text)

def render_questionnaire():
    st.subheader("📝 Brief Check-in (1 minute)")
    with st.expander("Why we ask this"):
        st.caption(
            "These questions are not diagnostic. They help the model contextualize text and facial signals. "
            "You can skip any item; the system fuses whatever you provide."
        )

    consent_save_q = st.checkbox("I consent to store my questionnaire answers for research/evaluation.", value=False)
    skip_q = st.toggle("Skip questionnaire", value=False, help="If on, the questionnaire will be excluded from the final score.")

    if skip_q:
        subscales = {}
        p_q = None
    else:
        colA, colB, colC = st.columns(3)
        with colA:
            st.markdown("**Workload / Demands**")
            q1 = _pick("Deadlines feel unmanageable.", "Time pressure / due dates.")
            q2 = _pick("My workload feels overwhelming.", "Overall task load.")
        with colB:
            st.markdown("**Sleep / Recovery**")
            q3 = _pick("I'm losing sleep due to school worries.", "Sleep disturbance.")
            q4 = _pick("I'm skipping breaks or meals.", "Recovery habits.")
        with colC:
            st.markdown("**Control / Emotions**")
            q5 = _pick("I feel anxious about grades or failure.", "Worry/rumination.")
            q6 = _pick("I feel unable to control my study plan.", "Low control / planning.")

        def norm2(vals): return float(sum(vals) / (4 * len(vals))) if vals else 0.0

        subscales = {
            "Workload": norm2([LIKERT_TO_INT[q1], LIKERT_TO_INT[q2]]),
            "Recovery": norm2([LIKERT_TO_INT[q3], LIKERT_TO_INT[q4]]),
            "Emotions": norm2([LIKERT_TO_INT[q5], LIKERT_TO_INT[q6]]),
        }
        p_q = questionnaire_score_from_subscales(subscales)

    # summary tiles
    st.markdown("**Questionnaire Summary**")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Workload", f"{subscales.get('Workload', 0):.2f}")
    c2.metric("Recovery", f"{subscales.get('Recovery', 0):.2f}")
    c3.metric("Emotions", f"{subscales.get('Emotions', 0):.2f}")
    c4.metric("Overall Risk", f"{(p_q if p_q is not None else 0):.2f}")

    payload = {"skip": bool(skip_q), "consent": bool(consent_save_q), "subscales": subscales, "overall": p_q}
    return p_q, subscales, payload