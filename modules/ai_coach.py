def generate_ai_feedback(result):

    strengths = []
    improvements = []
    suggestions = []

    if result["confidence"] >= 80:
        strengths.append("You appear confident while speaking.")
    else:
        improvements.append("Confidence needs improvement.")
        suggestions.append("Practice speaking in front of a mirror daily.")

    if result["eye_contact"] >= 70:
        strengths.append("Good eye contact.")
    else:
        improvements.append("Eye contact needs improvement.")
        suggestions.append("Look directly at the camera.")

    if result["speech"] > 170:
        improvements.append("Speaking speed is too fast.")
        suggestions.append("Slow down and pause between sentences.")
    elif result["speech"] < 110:
        improvements.append("Speaking speed is too slow.")
        suggestions.append("Maintain a more energetic pace.")
    else:
        strengths.append("Speaking speed is appropriate.")

    if result["visibility"] >= 90:
        strengths.append("Excellent face visibility.")
    else:
        improvements.append("Stay centered in front of the camera.")
        suggestions.append("Keep your face visible throughout the recording.")

    if result["leadership"] >= 80:
        strengths.append("Strong leadership presence.")
    else:
        improvements.append("Leadership presence can improve.")
        suggestions.append("Speak confidently and maintain good posture.")

    return {
        "strengths": strengths,
        "improvements": improvements,
        "suggestions": suggestions,
    }