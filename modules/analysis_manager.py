import json
import os

DATA_FILE = "data/analysis.json"


def save_results(result):
    """
    Save the latest completed analysis.

    Only the latest analysis is stored.
    """

    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)


def clear_results():
    """
    Delete the previous analysis completely.
    """

    if os.path.exists(DATA_FILE):

        try:
            os.remove(DATA_FILE)

        except Exception as e:
            print("Could not clear previous analysis:", e)


def load_results():

    default = {
        "analysis_ready": False,

        "frames": 0,
        "faces": 0,
        "average_faces": 0,
        "visibility": None,

        "confidence": None,
        "emotion": "Not Analyzed",
        "eye_contact": None,
        "speech": None,
        "leadership": None,

        "transcript": "",
        "original_transcript": "",
        "word_count": 0,

        "voice_energy": None,
        "pause_score": None,
        "voice_confidence": None,

        "posture": None,
        "smile": None,
        "gesture_score": None,

        "interview_score": None,
        "presentation_score": None,
        "executive_presence": None,
        "overall_score": None,

        "transcription_confidence": None,
        "high_confidence_segments": 0,
        "review_segments": 0,
        "low_confidence_segments": 0,

        "hallucination_flags": [],

        "feedback": {
            "strengths": [],
            "improvements": [],
            "suggestions": []
        }
    }

    if not os.path.exists(DATA_FILE):
        return default

    try:

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        if not isinstance(data, dict):
            return default

        for key, value in default.items():
            data.setdefault(key, value)

        return data

    except Exception as e:

        print("Error loading analysis:", e)

        return default