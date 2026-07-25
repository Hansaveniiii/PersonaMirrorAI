import json
import os

DATA_FILE = "data/analysis.json"


def save_results(result):

    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w") as f:
        json.dump(result, f, indent=4)


def load_results():

    if not os.path.exists(DATA_FILE):
        return {
            "frames": 0,
            "faces": 0,
            "confidence": 0,
            "emotion": "Not Analyzed",
            "eye_contact": 0,
            "speech": 0,
            "leadership": 0
        }

    with open(DATA_FILE, "r") as f:
        return json.load(f)