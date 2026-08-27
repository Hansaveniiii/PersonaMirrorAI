import re
import math


# =========================================================
# TEXT UTILITIES
# =========================================================

def clean_text(text):
    if not text:
        return ""

    return re.sub(r"\s+", " ", str(text)).strip()


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


# =========================================================
# SENTENCE ANALYSIS
# =========================================================

def get_sentences(text):

    sentences = re.split(
        r"[.!?]+",
        text
    )

    return [
        s.strip()
        for s in sentences
        if s.strip()
    ]


# =========================================================
# STRUCTURE SCORE
# =========================================================

def calculate_structure(text, sentences):

    if not text or not sentences:
        return None

    score = 45.0

    sentence_count = len(sentences)

    # Reasonable number of sentences
    if sentence_count >= 2:
        score += 8

    if sentence_count >= 4:
        score += 7

    if sentence_count >= 7:
        score += 5

    # Transition language
    transition_phrases = [
        "first",
        "firstly",
        "second",
        "secondly",
        "third",
        "finally",
        "however",
        "therefore",
        "because",
        "for example",
        "for instance",
        "in addition",
        "on the other hand",
        "in conclusion",
        "to conclude",
        "overall",
        "next",
        "then",
    ]

    lower_text = text.lower()

    transition_count = 0

    for phrase in transition_phrases:

        if re.search(
            r"\b" + re.escape(phrase) + r"\b",
            lower_text
        ):
            transition_count += 1

    score += min(
        transition_count * 5,
        20
    )

    # Opening and conclusion indicators
    opening_words = [
        "hello",
        "hi",
        "today",
        "i am",
        "my name",
        "respected",
        "good morning",
        "good afternoon",
        "good evening",
    ]

    conclusion_words = [
        "thank you",
        "in conclusion",
        "to conclude",
        "finally",
        "overall",
        "jai hind",
    ]

    if any(
        phrase in lower_text[:180]
        for phrase in opening_words
    ):
        score += 5

    if any(
        phrase in lower_text[-180:]
        for phrase in conclusion_words
    ):
        score += 5

    return round(
        max(0, min(100, score))
    )


# =========================================================
# CLARITY SCORE
# =========================================================

def calculate_clarity(
    text,
    words,
    sentences,
    filler_count,
    repeated_words
):

    if not text or words == 0:
        return None

    score = 100.0

    # -----------------------------------------------------
    # Filler penalty
    # -----------------------------------------------------

    filler_ratio = (
        filler_count / words
    ) * 100

    score -= min(
        filler_ratio * 3.0,
        25
    )

    # -----------------------------------------------------
    # Extremely long sentences
    # -----------------------------------------------------

    if sentences:

        sentence_lengths = [
            count_words(sentence)
            for sentence in sentences
        ]

        average_length = (
            sum(sentence_lengths)
            / len(sentence_lengths)
        )

        if average_length > 35:
            score -= 12

        elif average_length > 28:
            score -= 7

        elif average_length < 5 and len(sentences) >= 3:
            score -= 5

    # -----------------------------------------------------
    # Repetition penalty
    # -----------------------------------------------------

    if repeated_words:

        repetition_penalty = min(
            len(repeated_words) * 3,
            18
        )

        score -= repetition_penalty

    return round(
        max(0, min(100, score))
    )


# =========================================================
# REPETITION ANALYSIS
# =========================================================

def calculate_repetition(text):

    words_list = re.findall(
        r"\b[a-zA-Z']+\b",
        text.lower()
    )

    word_frequency = {}

    # Common words are ignored because repetition of
    # "the", "and", "is", etc. is not useful feedback.

    ignored_words = {
        "this",
        "that",
        "with",
        "from",
        "have",
        "will",
        "your",
        "they",
        "them",
        "their",
        "there",
        "about",
        "which",
        "would",
        "could",
        "should",
        "because",
        "what",
        "when",
        "where",
        "were",
        "been",
        "being",
        "into",
        "also",
        "very",
        "more",
        "than",
        "then",
    }

    for word in words_list:

        if len(word) < 4:
            continue

        if word in ignored_words:
            continue

        word_frequency[word] = (
            word_frequency.get(word, 0) + 1
        )

    repeated_words = {
        word: count
        for word, count in word_frequency.items()
        if count >= 4
    }

    if not words_list:
        return None, {}

    # -----------------------------------------------------
    # Repetition score
    # -----------------------------------------------------

    score = 100.0

    for word, count in repeated_words.items():

        excess = count - 3

        score -= min(
            excess * 2.5,
            12
        )

    score -= min(
        len(repeated_words) * 2,
        15
    )

    return (
        round(max(0, min(100, score))),
        repeated_words
    )


# =========================================================
# TRANSCRIPT INTELLIGENCE
# =========================================================

def analyze_transcript(
    text,
    analysis_type="General Speech"
):

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
            "speech_quality": None,
            "repetition_score": None,
            "repeated_words": {},
        }

    words = count_words(text)

    fillers = find_fillers(text)

    filler_count = sum(
        fillers.values()
    )

    sentences = get_sentences(text)

    opening = (
        sentences[0]
        if sentences
        else ""
    )

    conclusion = (
        sentences[-1]
        if sentences
        else ""
    )

    # -----------------------------------------------------
    # Repetition
    # -----------------------------------------------------

    repetition_score, repeated_words = (
        calculate_repetition(text)
    )

    # -----------------------------------------------------
    # Structure
    # -----------------------------------------------------

    structure_score = calculate_structure(
        text,
        sentences
    )

    # -----------------------------------------------------
    # Clarity
    # -----------------------------------------------------

    clarity_score = calculate_clarity(
        text,
        words,
        sentences,
        filler_count,
        repeated_words
    )

    # -----------------------------------------------------
    # SPEECH QUALITY
    #
    # No longer simply equal to clarity.
    #
    # It combines:
    # - clarity
    # - structure
    # - repetition
    # - filler control
    # -----------------------------------------------------

    quality_components = []

    if clarity_score is not None:
        quality_components.append(
            (clarity_score, 0.40)
        )

    if structure_score is not None:
        quality_components.append(
            (structure_score, 0.30)
        )

    if repetition_score is not None:
        quality_components.append(
            (repetition_score, 0.20)
        )

    # Filler control
    if words > 0:

        filler_control = max(
            0,
            min(
                100,
                100 - (
                    (filler_count / words)
                    * 100
                    * 4
                )
            )
        )

        quality_components.append(
            (filler_control, 0.10)
        )

    if quality_components:

        total_weight = sum(
            weight
            for _, weight
            in quality_components
        )

        speech_quality = round(
            sum(
                value * weight
                for value, weight
                in quality_components
            )
            / total_weight
        )

    else:
        speech_quality = None

    return {

        "word_count": words,

        "filler_count": filler_count,

        "fillers": fillers,

        "opening": opening,

        "conclusion": conclusion,

        "structure_score": structure_score,

        "clarity_score": clarity_score,

        "speech_quality": speech_quality,

        "repetition_score": repetition_score,

        "repeated_words": repeated_words,
    }


# =========================================================
# AI FEEDBACK
# =========================================================

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

    analysis = analyze_transcript(
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

    voice_energy = result.get(
        "voice_energy"
    )

    structure = analysis.get(
        "structure_score"
    )

    clarity = analysis.get(
        "clarity_score"
    )

    repetition = analysis.get(
        "repetition_score"
    )

    fillers = analysis.get(
        "fillers",
        {}
    )

    filler_count = analysis.get(
        "filler_count",
        0
    )

    # =====================================================
    # CONFIDENCE
    # =====================================================

    if confidence is not None:

        if confidence >= 80:

            strengths.append(
                "Your delivery shows a strong confidence foundation based on the available voice and speech signals."
            )

        elif confidence >= 60:

            strengths.append(
                "Your delivery demonstrates a developing level of confidence."
            )

        else:

            improvements.append(
                "Your delivery could communicate confidence more consistently."
            )

            suggestions.append(
                "Use a deliberate opening, controlled pauses and stronger emphasis on your main message."
            )

    # =====================================================
    # LEADERSHIP
    # =====================================================

    if leadership is not None:

        if leadership >= 80:

            strengths.append(
                "Your communication shows strong leadership-oriented delivery."
            )

        elif leadership < 60:

            improvements.append(
                "Your delivery could project stronger leadership and authority."
            )

            suggestions.append(
                "State your main point clearly and support it with a concise reason or example."
            )

    # =====================================================
    # STRUCTURE
    # =====================================================

    if structure is not None:

        if structure >= 80:

            strengths.append(
                "Your speech shows a clear progression of ideas."
            )

        elif structure < 60:

            improvements.append(
                "The movement between ideas could be more clearly signposted for the listener."
            )

            suggestions.append(
                "Use short transition phrases such as 'first', 'next', 'however' or 'finally'."
            )

    # =====================================================
    # CLARITY
    # =====================================================

    if clarity is not None:

        if clarity >= 80:

            strengths.append(
                "Your language is generally clear and understandable."
            )

        elif clarity < 60:

            improvements.append(
                "Some parts of the speech may be harder to follow because of fillers, repetition or sentence complexity."
            )

            suggestions.append(
                "Use shorter sentences and pause briefly between major ideas."
            )

    # =====================================================
    # FILLERS
    # =====================================================

    if filler_count == 0:

        strengths.append(
            "No significant filler-word usage was detected in the transcript."
        )

    elif filler_count <= 3:

        strengths.append(
            "Your filler-word usage is relatively controlled."
        )

    else:

        improvements.append(
            f"{filler_count} filler-word occurrences were detected."
        )

        suggestions.append(
            "Replace filler words with a short pause when you need time to think."
        )

    # =====================================================
    # REPETITION
    # =====================================================

    if repetition is not None:

        repeated_words = analysis.get(
            "repeated_words",
            {}
        )

        if repeated_words:

            words_text = ", ".join(
                sorted(
                    repeated_words,
                    key=repeated_words.get,
                    reverse=True
                )[:5]
            )

            improvements.append(
                f"Some ideas or words appear repeatedly: {words_text}."
            )

            suggestions.append(
                "After making your main point once, develop it with an example, explanation or consequence instead of repeating it."
            )

        elif repetition >= 85:

            strengths.append(
                "The transcript does not show significant repetition of content words."
            )

    # =====================================================
    # SPEAKING RATE
    # =====================================================

    speech_rate = result.get(
        "speech"
    )

    if speech_rate:

        if 110 <= speech_rate <= 150:

            strengths.append(
                f"Your speaking pace of approximately {round(speech_rate)} words per minute is within a comfortable range for clear communication."
            )

        elif speech_rate > 150:

            improvements.append(
                "Your speaking pace is relatively fast."
            )

            suggestions.append(
                "Slow slightly at important points and use pauses to give the audience time to process your message."
            )

        elif speech_rate < 100:

            improvements.append(
                "Your speaking pace is relatively slow."
            )

            suggestions.append(
                "Maintain forward momentum while keeping deliberate pauses around your key points."
            )

    # =====================================================
    # OPENING
    # =====================================================

    opening = analysis.get(
        "opening",
        ""
    )

    if opening:

        strengths.append(
            f'Your opening begins with: "{opening[:180]}". This gives us a concrete starting point for improving how you establish the speech.'
        )

    # =====================================================
    # CONCLUSION
    # =====================================================

    conclusion = analysis.get(
        "conclusion",
        ""
    )

    if conclusion:

        lower_conclusion = conclusion.lower()

        if lower_conclusion in {
            "thank you",
            "thanks",
            "thank you very much",
        }:

            suggestions.append(
                'Your final sentence is a simple closing. Consider ending future recordings with a clear takeaway or memorable final message.'
            )

        elif lower_conclusion:

            strengths.append(
                "Your speech contains a defined closing statement."
            )

    # =====================================================
    # FALLBACK
    # =====================================================

    if not strengths:

        strengths.append(
            "The available speech measurements have been processed successfully."
        )

    if not improvements:

        improvements.append(
            "No major weakness was identified from the measurements currently available."
        )

    if not suggestions:

        suggestions.append(
            "Continue practising and compare your next recording against this baseline."
        )

    return {

        "strengths": strengths,

        "improvements": improvements,

        "suggestions": suggestions,
    }