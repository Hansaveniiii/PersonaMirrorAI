def detect_emotion(result):

    if result["visibility"] > 90:
        return "Confident"

    elif result["visibility"] > 70:
        return "Calm"

    elif result["visibility"] > 50:
        return "Neutral"

    return "Low Engagement"