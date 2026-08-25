def generate_recruiter_notes(report):

    score = report["analysis"]["score"]

    fluency = report["analysis"]["fluency"]

    professionalism = report["analysis"]["professionalism"]

    eye = report["vision"].get("eye_contact", 0)

    transcript = report["transcript"]


    notes = []


    if score >= 85:
        notes.append("Candidate performed confidently throughout the interview.")

    elif score >= 70:
        notes.append("Candidate showed potential but needs polishing.")

    else:
        notes.append("Candidate requires significant communication improvement.")


    if professionalism < 75:
        notes.append("Professional language could be improved.")

    if fluency < 75:
        notes.append("Speech contained hesitations or lacked smooth delivery.")

    if eye < 70:
        notes.append("Limited eye contact may reduce perceived confidence.")

    if len(transcript.split()) < 40:
        notes.append("Answers were shorter than expected.")

    elif len(transcript.split()) > 180:
        notes.append("Answers were slightly too lengthy.")

    notes.append("Overall communication assessment completed.")

    return notes