def clamp(value, default=None):
    """
    Keep a score between 0 and 100.

    None means the measurement is unavailable.
    We do NOT convert unavailable measurements into 0.
    """

    if value is None:
        return default

    try:
        return max(0, min(100, round(float(value))))
    except (TypeError, ValueError):
        return default


def available(result, key):
    """
    Return True only when a metric is genuinely available.
    """

    value = result.get(key)

    return value is not None


def weighted_score(result, weights):
    """
    Calculate a weighted score using ONLY measurements
    that are actually available.

    This prevents unavailable metrics from unfairly
    dragging the user's score down to zero.
    """

    total = 0
    weight_total = 0

    for key, weight in weights.items():

        value = result.get(key)

        if value is None:
            continue

        try:
            value = float(value)
        except (TypeError, ValueError):
            continue

        value = max(0, min(100, value))

        total += value * weight
        weight_total += weight

    if weight_total == 0:
        return None

    return clamp(total / weight_total)


# =========================================================
# CONFIDENCE
# =========================================================

def calculate_confidence(result):

    return weighted_score(
        result,
        {
            "voice_confidence": 0.35,
            "voice_energy": 0.20,
            "pause_score": 0.15,
            "speech_quality": 0.15,
            "clarity": 0.15,
        }
    )


# =========================================================
# LEADERSHIP
# =========================================================

def calculate_leadership(result):

    return weighted_score(
        result,
        {
            "voice_energy": 0.30,
            "voice_confidence": 0.25,
            "speech_quality": 0.20,
            "clarity": 0.15,
            "posture": 0.10,
        }
    )


# =========================================================
# INTERVIEW SCORE
# =========================================================

def calculate_interview_score(result):

    return weighted_score(
        result,
        {
            "confidence": 0.20,
            "leadership": 0.15,
            "voice_confidence": 0.15,
            "speech_quality": 0.20,
            "answer_relevance": 0.20,
            "clarity": 0.10,
        }
    )


# =========================================================
# PRESENTATION SCORE
# =========================================================

def calculate_presentation_score(result):

    return weighted_score(
        result,
        {
            "confidence": 0.20,
            "leadership": 0.15,
            "gesture_score": 0.15,
            "voice_energy": 0.20,
            "speech_quality": 0.15,
            "clarity": 0.15,
        }
    )


# =========================================================
# EXECUTIVE PRESENCE
# =========================================================

def calculate_executive_presence(result):

    return weighted_score(
        result,
        {
            "confidence": 0.30,
            "leadership": 0.25,
            "voice_confidence": 0.20,
            "speech_quality": 0.15,
            "posture": 0.10,
        }
    )


# =========================================================
# OVERALL SCORE
# =========================================================

def calculate_overall_score(result):

    scores = [
        result.get("confidence"),
        result.get("leadership"),
        result.get("interview_score"),
        result.get("presentation_score"),
        result.get("executive_presence"),
    ]

    valid_scores = []

    for score in scores:

        if score is None:
            continue

        try:
            valid_scores.append(float(score))
        except (TypeError, ValueError):
            continue

    if not valid_scores:
        return None

    return clamp(
        sum(valid_scores) / len(valid_scores)
    )