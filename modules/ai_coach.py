import re


def clean_text(text):
    if not text:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(text)
    ).strip()


def count_words(text):
    return len(
        re.findall(
            r"\b[\w']+\b",
            text
        )
    )


def find_fillers(text):

    filler_words = [
        "um",
        "uh",
        "like",
        "basically",
        "actually",
        "literally",
        "you know",
        "i mean",
        "sort of",
        "kind of",
        "so yeah",
    ]

    text_lower = text.lower()

    found = {}

    for filler in filler_words:

        pattern = r"\b" + re.escape(filler) + r"\b"

        count = len(
            re.findall(
                pattern,
                text_lower
            )
        )

        if count > 0:
            found[filler] = count

    return found


def analyze_transcript(text, analysis_type):

    text = clean_text(text)

    if not text:

        return {
            "word_count": 0,
            "filler_count": 0,
            "fillers": {},
            "opening": "",
            "conclusion": "",
            "structure_score": None,
            "clarity_score": None,
            "repetition_score": None,
        }

    words = count_words(text)

    fillers = find_fillers(text)

    filler_count = sum(
        fillers.values()
    )

    sentences = re.split(
        r"[.!?]+",
        text
    )

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    # ---------------------------------------------------------
    # OPENING
    # ---------------------------------------------------------

    opening = ""

    if sentences:

        opening = sentences[0]

    # ---------------------------------------------------------
    # CONCLUSION
    # ---------------------------------------------------------

    conclusion = ""

    if sentences:

        conclusion = sentences[-1]

    # ---------------------------------------------------------
    # FILLER SCORE
    # ---------------------------------------------------------

    filler_ratio = 0

    if words > 0:

        filler_ratio = (
            filler_count / words
        ) * 100

    # ---------------------------------------------------------
    # STRUCTURE
    # ---------------------------------------------------------

    structure_score = 70

    if len(sentences) >= 5:

        structure_score += 10

    if len(sentences) >= 10:

        structure_score += 5

    # Look for transition language

    transition_words = [
        "first",
        "second",
        "finally",
        "however",
        "therefore",
        "because",
        "for example",
        "in addition",
        "on the other hand",
        "in conclusion",
        "to conclude",
    ]

    transition_count = 0

    lower_text = text.lower()

    for word in transition_words:

        if word in lower_text:

            transition_count += 1

    structure_score += min(
        transition_count * 2,
        10
    )

    structure_score = min(
        structure_score,
        100
    )

    # ---------------------------------------------------------
    # CLARITY
    # ---------------------------------------------------------

    clarity_score = 85

    if filler_ratio > 5:

        clarity_score -= 15

    elif filler_ratio > 2:

        clarity_score -= 7

    # ---------------------------------------------------------
    # REPETITION
    # ---------------------------------------------------------

    words_list = re.findall(
        r"\b[a-zA-Z']+\b",
        text.lower()
    )

    word_frequency = {}

    for word in words_list:

        if len(word) < 4:
            continue

        word_frequency[word] = (
            word_frequency.get(
                word,
                0
            ) + 1
        )

    repeated_words = {
        word: count
        for word, count
        in word_frequency.items()
        if count >= 5
    }

    repetition_score = 90

    if len(repeated_words) >= 5:

        repetition_score = 65

    elif len(repeated_words) >= 3:

        repetition_score = 75

    elif len(repeated_words) >= 1:

        repetition_score = 85

    return {
        "word_count": words,
        "filler_count": filler_count,
        "fillers": fillers,
        "opening": opening,
        "conclusion": conclusion,
        "structure_score": structure_score,
        "clarity_score": clarity_score,
        "repetition_score": repetition_score,
        "repeated_words": repeated_words,
    }


def generate_ai_feedback(
    result,
    analysis_type="General Speech"
):

    transcript = clean_text(
        result.get(
            "transcript",
            ""
        )
    )

    transcript_analysis = analyze_transcript(
        transcript,
        analysis_type
    )

    strengths = []
    improvements = []
    suggestions = []

    confidence = result.get(
        "confidence"
    )

    leadership = result.get(
        "leadership"
    )

    speech = result.get(
        "speech"
    )

    voice_energy = result.get(
        "voice_energy"
    )

    voice_confidence = result.get(
        "voice_confidence"
    )

    posture = result.get(
        "posture"
    )

    gesture = result.get(
        "gesture_score"
    )

    structure = transcript_analysis.get(
        "structure_score"
    )

    clarity = transcript_analysis.get(
        "clarity_score"
    )

    repetition = transcript_analysis.get(
        "repetition_score"
    )

    fillers = transcript_analysis.get(
        "fillers",
        {}
    )

    filler_count = transcript_analysis.get(
        "filler_count",
        0
    )

    # =========================================================
    # SPEECH / PRESENTATION
    # =========================================================

    if (
        "Speech" in analysis_type
        or "Presentation" in analysis_type
        or "General" in analysis_type
    ):

        # -----------------------------
        # CONFIDENCE
        # -----------------------------

        if (
            confidence is not None
            and confidence >= 75
        ):

            strengths.append(
                "Your delivery shows a confident foundation, particularly in the way you maintain your overall presence while speaking."
            )

        elif (
            confidence is not None
            and confidence < 60
        ):

            improvements.append(
                "Your delivery could communicate confidence more consistently."
            )

            suggestions.append(
                "Focus on a deliberate opening, controlled pauses and finishing each major point before moving to the next."
            )

        # -----------------------------
        # LEADERSHIP
        # -----------------------------

        if (
            leadership is not None
            and leadership >= 75
        ):

            strengths.append(
                "You project a positive speaking presence and your delivery has the potential to hold an audience's attention."
            )

        # -----------------------------
        # STRUCTURE
        # -----------------------------

        if (
            structure is not None
            and structure >= 85
        ):

            strengths.append(
                "Your speech shows a reasonably clear progression of ideas rather than sounding like a collection of disconnected points."
            )

        elif (
            structure is not None
            and structure < 75
        ):

            improvements.append(
                "The movement between ideas could be more clearly signposted for the listener."
            )

            suggestions.append(
                "Use short transition phrases when moving from one major idea to another so the audience always knows where your argument is going."
            )

        # -----------------------------
        # CLARITY
        # -----------------------------

        if (
            clarity is not None
            and clarity >= 85
        ):

            strengths.append(
                "Your language is generally clear and understandable without excessive verbal clutter."
            )

        elif (
            clarity is not None
            and clarity < 75
        ):

            improvements.append(
                "Some verbal habits may be reducing the clarity of your delivery."
            )

        # -----------------------------
        # FILLERS
        # -----------------------------

        if filler_count > 0:

            filler_names = ", ".join(
                fillers.keys()
            )

            improvements.append(
                f"I noticed repeated filler expressions such as {filler_names}. These can make otherwise strong ideas sound less deliberate."
            )

            suggestions.append(
                "Instead of replacing every filler with another word, allow yourself a short silent pause. Silence will usually sound more confident than filling the space."
            )

        # -----------------------------
        # REPETITION
        # -----------------------------

        if (
            repetition is not None
            and repetition < 80
        ):

            repeated = list(
                transcript_analysis.get(
                    "repeated_words",
                    {}
                ).keys()
            )

            repeated_preview = ", ".join(
                repeated[:5]
            )

            improvements.append(
                f"Some ideas or words appear repeatedly{': ' + repeated_preview if repeated_preview else ''}, which can reduce the impact of your strongest points."
            )

            suggestions.append(
                "After making your main point once, move forward with an example, explanation or consequence instead of restating the same idea."
            )

        # -----------------------------
        # VOICE
        # -----------------------------

        if (
            voice_energy is not None
            and voice_energy >= 75
        ):

            strengths.append(
                "Your vocal energy supports your message and helps prevent the speech from becoming flat."
            )

        elif (
            voice_energy is not None
            and voice_energy < 60
        ):

            improvements.append(
                "Your vocal energy could vary more between important and supporting points."
            )

            suggestions.append(
                "Use stronger emphasis on your key message and slightly lower energy during supporting details to create contrast."
            )

        # -----------------------------
        # PACE
        # -----------------------------

        if speech is not None and speech > 0:

            if speech > 175:

                improvements.append(
                    f"Your average speaking rate is around {speech} words per minute, which is relatively fast for a speech."
                )

                suggestions.append(
                    "Slow down particularly before important ideas and allow the audience a moment to process them."
                )

            elif speech < 105:

                improvements.append(
                    f"Your average speaking rate is around {speech} words per minute, which may make parts of the speech feel less energetic."
                )

                suggestions.append(
                    "Increase your rhythm slightly while preserving the clarity that comes from your slower delivery."
                )

            else:

                strengths.append(
                    f"Your speaking pace of approximately {speech} words per minute is within a comfortable range for clear communication."
                )

        # -----------------------------
        # POSTURE
        # -----------------------------

        if (
            posture is not None
            and posture >= 80
        ):

            strengths.append(
                "Your posture supports a composed and professional speaking presence."
            )

        # -----------------------------
        # GESTURES
        # -----------------------------

        if (
            gesture is not None
            and gesture >= 75
        ):

            strengths.append(
                "Your physical delivery appears to complement your spoken communication rather than distracting from it."
            )

        elif (
            gesture is not None
            and gesture < 60
        ):

            improvements.append(
                "Your physical delivery could do more to reinforce your strongest spoken points."
            )

            suggestions.append(
                "Use a small number of purposeful gestures when emphasizing key ideas rather than keeping the same physical movement throughout."
            )

    # =========================================================
    # MOCK INTERVIEW
    # =========================================================

    elif "Mock Interview" in analysis_type:

        strengths.append(
            "Your analysis is being evaluated specifically for interview-style communication."
        )

        suggestions.append(
            "Give the main answer first, then support it with evidence, experience or a specific example."
        )

    # =========================================================
    # DEBATE
    # =========================================================

    elif (
        "Debate" in analysis_type
        or "Public Speaking" in analysis_type
    ):

        strengths.append(
            "Your delivery is being evaluated with emphasis on persuasion, argument clarity and speaking presence."
        )

        suggestions.append(
            "Make each major claim explicit, support it with evidence and finish important arguments with a clear takeaway."
        )

    # =========================================================
    # PERSONALIZED TRANSCRIPT OBSERVATION
    # =========================================================

    if transcript:

        opening = transcript_analysis.get(
            "opening",
            ""
        )

        conclusion = transcript_analysis.get(
            "conclusion",
            ""
        )

        if opening:

            strengths.append(
                f"Your opening begins with: “{opening[:180]}”. This gives us a concrete starting point for improving how you establish the speech."
            )

        if conclusion:

            suggestions.append(
                f"Your final sentence was: “{conclusion[:180]}”. For your next recording, consider ending with a deliberate takeaway rather than simply stopping after the final sentence."
            )

    # =========================================================
    # FALLBACKS
    # =========================================================

    if not strengths:

        strengths.append(
            "The recording provides a useful baseline of your current communication style, which we can use to track improvement over future recordings."
        )

    if not improvements:

        improvements.append(
            "No major weakness was identified from the measurements currently available."
        )

    if not suggestions:

        suggestions.append(
            "Keep your current strengths and make one focused improvement in your next recording rather than changing your entire speaking style."
        )

    # Remove duplicates

    strengths = list(
        dict.fromkeys(strengths)
    )

    improvements = list(
        dict.fromkeys(improvements)
    )

    suggestions = list(
        dict.fromkeys(suggestions)
    )

    return {

        "analysis_type": analysis_type,

        "strengths": strengths,

        "improvements": improvements,

        "suggestions": suggestions,

        "transcript_analysis": transcript_analysis,
    }