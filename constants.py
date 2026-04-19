from pathlib import Path

ART_DIR = Path("artifacts")

EMO_LABELS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

# emotion -> stress weight
STRESS_W = {
    "fear": 1.00,
    "sad": 0.90, 
    "angry": 0.85, 
    "disgust": 0.75,
    "surprise": 0.50, 
    "neutral": 0.40,
    "happy": 0.10
}

# UI defaults
DEFAULT_W_TEXT = 0.50
DEFAULT_W_FACE = 0.30
DEFAULT_W_QUEST = 0.20
DEFAULT_THRESHOLD = 0.65