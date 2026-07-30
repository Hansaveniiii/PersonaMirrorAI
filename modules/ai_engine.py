def clamp(value):
    return max(0, min(100, int(value)))


def calculate_confidence(result):
    score = (
        result.get("eye_contact", 0) * 0.25
        + result.get("voice_confidence", 0) * 0.20
        + result.get("smile", 0) * 0.10
        + result.get("posture", 0) * 0.15
        + result.get("gesture_score", 0) * 0.10
        + result.get("visibility", 0) * 0.10
        + result.get("pause_score", 0) * 0.10
    )

    return clamp(score)


def calculate_leadership(result):
    score = (
        result.get("confidence", 0) * 0.30
        + result.get("voice_energy", 0) * 0.20
        + result.get("speech", 0) * 0.10
        + result.get("posture", 0) * 0.15
        + result.get("gesture_score", 0) * 0.15
        + result.get("executive_presence", 0) * 0.10
    )

    return clamp(score)


def calculate_interview_score(result):
    score = (
        result.get("confidence", 0) * 0.25
        + result.get("leadership", 0) * 0.20
        + result.get("eye_contact", 0) * 0.15
        + result.get("voice_confidence", 0) * 0.15
        + result.get("speech", 0) * 0.10
        + result.get("posture", 0) * 0.15
    )

    return clamp(score)


def calculate_presentation_score(result):
    score = (
        result.get("confidence", 0) * 0.25
        + result.get("gesture_score", 0) * 0.20
        + result.get("voice_energy", 0) * 0.20
        + result.get("eye_contact", 0) * 0.15
        + result.get("speech", 0) * 0.20
    )

    return clamp(score)


def calculate_executive_presence(result):
    score = (
        result.get("confidence", 0) * 0.35
        + result.get("leadership", 0) * 0.25
        + result.get("posture", 0) * 0.20
        + result.get("voice_confidence", 0) * 0.20
    )

    return clamp(score)