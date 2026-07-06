# loading_artifacts.py
import json
from joblib import load
import streamlit as st
import cv2
from constants import ART_DIR

VEC_PATH        = ART_DIR / "tfidf_vectorizer.pkl"
TEXT_MODEL_PATH = ART_DIR / "baseline_model.pkl"
METRICS_PATH    = ART_DIR / "metrics.json"
FACE_MODEL_PATH = ART_DIR / "face_emotion_svc.pkl"

@st.cache_resource
def load_text_artifacts():
    vec = load(VEC_PATH)
    clf = load(TEXT_MODEL_PATH)
    try:
        with open(METRICS_PATH) as f: metrics = json.load(f)
    except Exception: metrics = {}
    return vec, clf, metrics

@st.cache_resource
def load_face_artifacts():
    try: face_clf = load(FACE_MODEL_PATH)
    except Exception: face_clf = None
    haar = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    return face_clf, haar