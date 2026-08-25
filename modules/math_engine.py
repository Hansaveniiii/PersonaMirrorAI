from typing import Dict


FEATURE_WEIGHTS = {
    "relevance": 0.30,
    "answer_quality": 0.20,
    "confidence": 0.15,
    "eye_contact": 0.10,
    "voice": 0.10,
    "body_language": 0.10,
    "professionalism": 0.05,
}


def clamp(value):
    return max(0, min(100, float(value)))


def weighted_score(scores: Dict):

    relevance = clamp(
        scores.get("relevance", 0)
    )

    answer_quality = clamp(
        scores.get("answer_quality", 0)
    )

    confidence = clamp(
        scores.get("confidence", 0)
    )

    eye_contact = clamp(
        scores.get("eye_contact", 0)
    )

    voice = clamp(
        scores.get("voice", 0)
    )

    body_language = clamp(
        scores.get("body_language", 0)
    )

    professionalism = clamp(
        scores.get("professionalism", 0)
    )

    score = (
        relevance * FEATURE_WEIGHTS["relevance"]
        + answer_quality * FEATURE_WEIGHTS["answer_quality"]
        + confidence * FEATURE_WEIGHTS["confidence"]
        + eye_contact * FEATURE_WEIGHTS["eye_contact"]
        + voice * FEATURE_WEIGHTS["voice"]
        + body_language * FEATURE_WEIGHTS["body_language"]
        + professionalism * FEATURE_WEIGHTS["professionalism"]
    )

    # Strong penalty for irrelevant answers

    if relevance < 25:
        score *= 0.45

    elif relevance < 45:
        score *= 0.70

    elif relevance < 60:
        score *= 0.85

    return round(
        clamp(score),
        2
    )


def confidence_label(score):

    score = clamp(score)

    if score >= 90:
        return "Outstanding"

    elif score >= 80:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 60:
        return "Average"

    elif score >= 50:
        return "Needs Improvement"

    else:
        return "Poor"


def recommendation(score):

    score = clamp(score)

    if score >= 90:
        return "Strong Hire"

    elif score >= 80:
        return "Hire"

    elif score >= 70:
        return "Consider"

    elif score >= 60:
        return "Needs Improvement"

    else:
        return "Not Recommended"


def fuzzy_level(score):

    score = clamp(score)

    if score >= 90:
        return "Very High"

    elif score >= 75:
        return "High"

    elif score >= 60:
        return "Medium"

    elif score >= 40:
        return "Low"

    else:
        return "Very Low"


def interview_readiness(
    confidence,
    eye_contact,
    leadership,
    relevance=100
):

    confidence_level = fuzzy_level(
        confidence
    )

    eye_level = fuzzy_level(
        eye_contact
    )

    leadership_level = fuzzy_level(
        leadership
    )

    relevance_level = fuzzy_level(
        relevance
    )

    # Completely irrelevant answer

    if relevance < 25:

        return "Poor"

    # Very weak relevance

    if relevance < 45:

        return "Needs Improvement"

    # Strong performance

    if (
        confidence_level == "Very High"
        and eye_level == "Very High"
        and leadership_level == "Very High"
        and relevance_level in [
            "High",
            "Very High"
        ]
    ):

        return "Outstanding"

    # Excellent performance

    if (
        confidence_level == "High"
        and leadership_level == "High"
        and relevance >= 70
    ):

        return "Excellent"

    # Good performance

    if (
        confidence_level in [
            "Medium",
            "High"
        ]
        and relevance >= 60
    ):

        return "Good"

    # Weak confidence

    if confidence < 50:

        return "Needs Improvement"

    return "Average"