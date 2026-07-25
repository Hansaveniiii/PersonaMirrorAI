def calculate_confidence(result):

    score = 0

    # Face visibility (40 marks)
    visibility = result.get("visibility", 0)

    score += min(visibility * 0.4, 40)

    # Eye contact (30 marks)
    eye = result.get("eye_contact", 0)

    score += eye * 0.3

    # Speech (20 marks)
    speech = result.get("speech", 0)

    score += speech * 0.2

    # Leadership (10 marks)
    leader = result.get("leadership", 0)

    score += leader * 0.1

    return round(score)