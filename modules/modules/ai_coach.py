def generate_ai_feedback(result):

    strengths = []
    improvements = []
    suggestions = []

    # Confidence
    if result["confidence"] >= 80:
        strengths.append("You appear confident and comfortable while speaking.")
    else:
        improvements.append("Your confidence appears low.")
        suggestions.append(
            "Practice speaking in front of a mirror for 10 minutes every day."
        )

    # Eye Contact
    if result["eye_contact"] >= 70:
        strengths.append("Good eye contact keeps the audience engaged.")
    else:
        improvements.append("Eye contact needs improvement.")
        suggestions.append(
            "Look directly at the camera instead of the screen."
        )

    # Speech Speed
    if 110 <= result["speech"] <= 170:
        strengths.append("Your speaking pace is easy to follow.")
    elif result["speech"] > 170:
        improvements.append("You are speaking too fast.")
        suggestions.append(
            "Slow down slightly and pause after important sentences."
        )
    else:
        improvements.append("Your speaking pace is a little slow.")
        suggestions.append(
            "Speak with more energy and maintain a consistent rhythm."
        )

    # Face Visibility
    if result["visibility"] >= 90:
        strengths.append("Your face stayed visible throughout the recording.")
    else:
        improvements.append("Your face was not consistently visible.")
        suggestions.append(
            "Stay centered in front of the camera."
        )

    # Leadership
    if result["leadership"] >= 80:
        strengths.append("You display strong leadership presence.")
    else:
        improvements.append("Leadership presence can be improved.")
        suggestions.append(
            "Use stronger posture and speak with conviction."
        )

    return {
        "strengths": strengths,
        "improvements": improvements,
        "suggestions": suggestions
    }