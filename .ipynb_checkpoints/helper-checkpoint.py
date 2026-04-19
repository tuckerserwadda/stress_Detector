# fuctions to  helper to get the scores  

import re, numpy as np, pandas as pd, cv2
from PIL import Image
from skimage.feature import local_binary_pattern
from sklearn.exceptions import NotFittedError
from constants import EMO_LABELS, STRESS_W

def questionnaire_score_from_subscales(subscales, weights=None):
    if not subscales:
        return None
    if weights is None:
        weights = {k: 1/len(subscales) for k in subscales}
    total_w = sum(weights.values()) or 1.0
    val = sum(weights[k] * subscales[k] for k in subscales) / total_w
    return float(val)

def highlight_contributors(text, vectorizer, model, top_k=8):
    try:
        vocab = {w: i for i, w in enumerate(vectorizer.get_feature_names_out())}
        coefs = model.coef_.ravel()
    except Exception:
        return text, []
    tokens = re.findall(r"[a-zA-Z]+", text.lower())
    contrib = {}
    for t in tokens:
        if t in vocab: contrib[t] = contrib.get(t, 0.0) + float(coefs[vocab[t]])
    for i in range(len(tokens)-1):
        bg = tokens[i] + " " + tokens[i+1]
        if bg in vocab: contrib[bg] = contrib.get(bg, 0.0) + float(coefs[vocab[bg]])
    top = sorted(contrib.items(), key=lambda x: x[1], reverse=True)[:top_k]
    top_terms = {k for k, v in top if v > 0}
    def style_word(w):
        lw = re.sub(r"[^a-zA-Z]+","",w).lower()
        return f"<mark style='background-color:#ffd1d1'>{w}</mark>" if lw in top_terms else w
    words = re.split(r"(\W+)", text)
    styled = "".join(style_word(w) if w.strip() else w for w in words)
    return styled, top

def face_to_stress_score(pil_image: Image.Image, face_clf, cascade):
    if pil_image is None: return None, "No image."
    if face_clf is None:  return None, "Facial emotion model not available."
    img_rgb = np.array(pil_image.convert("RGB"))
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(48,48))
    if len(faces)==0: return None, "No face detected. Ensure good lighting and face the camera."
    (x,y,w,h) = max(faces, key=lambda b: b[2]*b[3])
    face = cv2.resize(gray[y:y+h, x:x+w], (48,48))
    lbp = local_binary_pattern(face, P=8, R=1, method='uniform')
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0, 8*1+4), range=(0, 8*1+3), density=True)
    feat = hist.reshape(1,-1)
    try:
        proba = face_clf.predict_proba(feat)[0]
    except NotFittedError:
        return None, "Face model not fitted."
    except Exception as e:
        return None, f"Face model error: {e}"
    top_idx = int(np.argmax(proba))
    top_emo, top_conf = EMO_LABELS[top_idx], float(proba[top_idx])
    stress_score = float(sum(STRESS_W[e]*float(p) for e,p in zip(EMO_LABELS, proba)))
    return {"stress": stress_score, "emo": top_emo, "conf": top_conf}, None