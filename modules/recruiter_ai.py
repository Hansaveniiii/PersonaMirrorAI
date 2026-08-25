def recruiter_decision(report):

    analysis = report.get("analysis", {})
    voice = report.get("voice", {})

    score = analysis.get("score", 0)
    professionalism = analysis.get("professionalism", 0)
    fluency = analysis.get("fluency", 0)

    # Eye contact may not exist
    eye = analysis.get("eye_contact", 0)

    # Convert "145 WPM" -> 145
    speech_rate = voice.get("speech_rate", "120 WPM")

    try:
        speech = int(str(speech_rate).split()[0])
    except Exception:
        speech = 120

    strengths = []
    concerns = []

    if score >= 85:
        strengths.append("Strong interview performance")
    elif score >= 70:
        strengths.append("Good overall communication")
    else:
        concerns.append("Interview performance needs improvement")

    if professionalism >= 80:
        strengths.append("Professional communication")
    else:
        concerns.append("Professional tone can improve")

    if fluency >= 80:
        strengths.append("Fluent speaking")
    else:
        concerns.append("Improve speaking fluency")

    if eye > 0:
        if eye >= 75:
            strengths.append("Maintained good eye contact")
        else:
            concerns.append("Eye contact needs improvement")

    if 110 <= speech <= 160:
        strengths.append("Speaking pace is ideal")
    elif speech < 110:
        concerns.append("Speaking too slowly")
    else:
        concerns.append("Speaking too fast")

    if score >= 85:
        decision = "✅ Recommended for Next Round"
    elif score >= 70:
        decision = "🟡 Borderline Candidate"
    else:
        decision = "❌ Not Recommended"

    return {
        "decision": decision,
        "strengths": strengths,
        "concerns": concerns,
    }