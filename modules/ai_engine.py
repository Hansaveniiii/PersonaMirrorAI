def calculate_confidence(result):

    score = 0

    visibility = result.get("visibility", 0)
    score += min(visibility * 0.4, 40)

    eye = result.get("eye_contact", 0)
    score += eye * 0.3

    speech = result.get("speech", 0)
    score += speech * 0.2

    leadership = result.get("leadership", 0)
    score += leadership * 0.1

    return round(score)