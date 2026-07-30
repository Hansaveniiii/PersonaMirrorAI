import json
import os

DATA_FILE = "data/analysis.json"


def save_results(result):

    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump(result, f, indent=4)


def load_results():

    default = {
        "frames": 0,
        "faces": 0,
        "average_faces": 0,
        "visibility": 0,

        "confidence": 0,
        "emotion": "Not Analyzed",
        "eye_contact": 0,
        "speech": 0,
        "leadership": 0,

        "transcript": "",
        "word_count": 0,

        "voice_energy": 0,
        "pause_score": 0,
        "voice_confidence": 0,

        "posture": 0,
        "smile": 0,
        "gesture_score": 0,

        "interview_score": 0,
        "presentation_score": 0,
        "executive_presence": 0,

        "feedback": {
            "strengths": [],
            "improvements": [],
            "suggestions": []
        }
    }

    if not os.path.exists(DATA_FILE):
        return default

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    for key, value in default.items():
        data.setdefault(key, value)

    return data