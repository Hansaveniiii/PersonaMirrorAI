import re


# =========================================================
# PERSONAMIRROR AI
# TRANSCRIPT QUALITY ENGINE
# =========================================================


def normalize_text(text):
    """
    Normalize text for comparison only.

    This does NOT modify the transcript displayed to the user.
    """

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^\w\s']",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# REPEATED PHRASES
# =========================================================

def remove_repeated_phrases(text):
    """
    Remove only exact consecutive repetitions.

    Example:

        hello everyone hello everyone

    becomes:

        hello everyone

    No semantic rewriting is performed.
    """

    if not text:
        return ""

    words = text.split()

    if len(words) < 6:
        return text

    cleaned = []

    i = 0

    while i < len(words):

        removed = False

        max_size = min(
            12,
            len(words) // 2
        )

        for size in range(
            max_size,
            1,
            -1
        ):

            end_first = i + size
            end_second = i + (size * 2)

            if end_second > len(words):
                continue

            first = words[
                i:end_first
            ]

            second = words[
                end_first:end_second
            ]

            if (
                first == second
                and len(first) >= 2
            ):

                cleaned.extend(first)

                i = end_second

                removed = True

                break

        if not removed:

            cleaned.append(
                words[i]
            )

            i += 1

    return " ".join(cleaned)


# =========================================================
# REPEATED SENTENCES
# =========================================================

def find_repeated_sentences(text):

    if not text:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    normalized_sentences = []

    for sentence in sentences:

        value = normalize_text(
            sentence
        )

        if value:
            normalized_sentences.append(
                (sentence.strip(), value)
            )

    repeated = []

    seen = set()

    for sentence, normalized in normalized_sentences:

        if normalized in seen:

            repeated.append(
                sentence
            )

        else:

            seen.add(
                normalized
            )

    return repeated


# =========================================================
# SUSPICIOUS SEGMENTS
# =========================================================

def find_suspicious_segments(text):

    if not text:
        return []

    suspicious = []

    # -----------------------------------------------------
    # Repeated complete sentences
    # -----------------------------------------------------

    repeated = find_repeated_sentences(
        text
    )

    for sentence in repeated:

        if sentence not in suspicious:

            suspicious.append(
                sentence
            )

    # -----------------------------------------------------
    # Suspicious isolated fragments
    #
    # Do NOT flag normal short speech such as:
    #
    # "Thank you."
    # "Jai Hind!"
    # "Good morning."
    # -----------------------------------------------------

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    safe_short_phrases = {
        "jai hind",
        "jai bharat",
        "thank you",
        "good morning",
        "good afternoon",
        "good evening",
        "welcome everyone",
        "dear friends",
        "my dear friends",
    }

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        normalized = normalize_text(
            sentence
        )

        words = normalized.split()

        if (
            len(words) <= 2
            and normalized not in safe_short_phrases
            and len(words) == 1
        ):

            # Only flag isolated one-word fragments.
            suspicious.append(
                sentence
            )

    return suspicious


# =========================================================
# SAFE NORMALIZATION
# =========================================================

def conservative_cleanup(
    text,
    analysis_type="General Speech"
):

    if not text:
        return ""

    cleaned = str(text).strip()

    # -----------------------------------------------------
    # Whitespace
    # -----------------------------------------------------

    cleaned = re.sub(
        r"\s+",
        " ",
        cleaned
    )

    # -----------------------------------------------------
    # Spaces before punctuation
    # -----------------------------------------------------

    cleaned = re.sub(
        r"\s+([,.!?;:])",
        r"\1",
        cleaned
    )

    # -----------------------------------------------------
    # Safe capitalization
    # -----------------------------------------------------

    cleaned = re.sub(
        r"\bjai hind\b",
        "Jai Hind",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\bjai bharat\b",
        "Jai Bharat",
        cleaned,
        flags=re.IGNORECASE
    )

    # -----------------------------------------------------
    # Tricolour
    #
    # IMPORTANT:
    #
    # Never replace "triangle".
    # Never replace unrelated words.
    # -----------------------------------------------------

    cleaned = re.sub(
        r"\btricolor\b",
        "Tricolour",
        cleaned,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\btricolour\b",
        "Tricolour",
        cleaned,
        flags=re.IGNORECASE
    )

    # -----------------------------------------------------
    # Final whitespace cleanup
    # -----------------------------------------------------

    cleaned = re.sub(
        r"\s{2,}",
        " ",
        cleaned
    )

    return cleaned.strip()


# =========================================================
# QUALITY SCORE
# =========================================================

def calculate_transcript_quality(
    original,
    cleaned,
    suspicious_segments=None
):

    if not original:
        return None

    original_words = original.split()

    cleaned_words = cleaned.split()

    if not original_words:
        return None

    # -----------------------------------------------------
    # Measure how much automatic processing changed.
    # -----------------------------------------------------

    change_ratio = abs(
        len(cleaned_words)
        -
        len(original_words)
    ) / max(
        len(original_words),
        1
    )

    score = 100

    if change_ratio > 0.20:

        score -= 20

    elif change_ratio > 0.10:

        score -= 10

    elif change_ratio > 0.05:

        score -= 5

    # -----------------------------------------------------
    # Suspicious material
    # -----------------------------------------------------

    suspicious_count = len(
        suspicious_segments or []
    )

    score -= min(
        suspicious_count * 3,
        15
    )

    return max(
        0,
        min(
            100,
            round(score)
        )
    )


# =========================================================
# FINAL TRANSCRIPT PROCESSOR
# =========================================================

def process_transcript(
    text,
    analysis_type="General Speech"
):

    if not text:

        return {
            "transcript": "",
            "original_transcript": "",
            "hallucination_flags": [],
            "transcript_quality": None,
            "cleaned": False
        }

    original = str(text).strip()

    # -----------------------------------------------------
    # STEP 1
    # Remove exact consecutive repetitions only.
    # -----------------------------------------------------

    cleaned = remove_repeated_phrases(
        original
    )

    # -----------------------------------------------------
    # STEP 2
    # Apply safe formatting/capitalization.
    # -----------------------------------------------------

    cleaned = conservative_cleanup(
        cleaned,
        analysis_type
    )

    # -----------------------------------------------------
    # STEP 3
    # Detect suspicious material.
    # -----------------------------------------------------

    suspicious = find_suspicious_segments(
        cleaned
    )

    # -----------------------------------------------------
    # STEP 4
    # Calculate transcript quality.
    # -----------------------------------------------------

    quality = calculate_transcript_quality(
        original,
        cleaned,
        suspicious
    )

    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    return {

        "transcript": cleaned,

        "original_transcript": original,

        "hallucination_flags": suspicious,

        "transcript_quality": quality,

        "cleaned": (
            cleaned != original
        )
    }