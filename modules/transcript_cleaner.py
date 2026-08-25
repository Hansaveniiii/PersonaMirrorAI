import re


def clean_transcript(
    text,
    analysis_type="General Speech"
):

    if not text:
        return ""

    cleaned = text.strip()


    # -----------------------------------------------------
    # Only fix extremely obvious recognition errors.
    #
    # DO NOT add sentences.
    # DO NOT change numbers.
    # DO NOT rewrite meaning.
    # -----------------------------------------------------

    corrections = {

        r"\btribal earth\b":
            "Tricolour",

        r"\bthe tribal\b":
            "the Tricolour",

        r"\btricolor\b":
            "Tricolour",

        r"\bJai hind\b":
            "Jai Hind",

        r"\bJai bharat\b":
            "Jai Bharat",
    }


    for pattern, replacement in corrections.items():

        cleaned = re.sub(
            pattern,
            replacement,
            cleaned,
            flags=re.IGNORECASE
        )


    # Fix spaces before punctuation

    cleaned = re.sub(
        r"\s+([,.!?])",
        r"\1",
        cleaned
    )


    # Remove accidental repeated spaces

    cleaned = re.sub(
        r"\s{2,}",
        " ",
        cleaned
    )


    return cleaned.strip()