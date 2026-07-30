def generate_coaching(result):

    coaching = []

    if result["confidence"] < 80:
        coaching.append(
            "Stand straight and begin speaking with a smile."
        )

    if result["eye_contact"] < 80:
        coaching.append(
            "Look into the camera instead of the screen."
        )

    if result["speech"] > 170:
        coaching.append(
            "Slow your speech slightly."
        )

    elif result["speech"] < 110:
        coaching.append(
            "Increase your speaking speed."
        )

    if result["voice_confidence"] < 70:
        coaching.append(
            "Speak louder and vary your voice tone."
        )

    if result["posture"] < 80:
        coaching.append(
            "Keep your shoulders straight."
        )

    if result["smile"] < 60:
        coaching.append(
            "Smile naturally while introducing yourself."
        )

    if len(coaching) == 0:
        coaching.append(
            "Outstanding communication! Keep practicing."
        )

    return coaching