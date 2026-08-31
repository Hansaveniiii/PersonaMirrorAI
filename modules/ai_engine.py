# =========================================================
# PERSONAMIRROR AI
# REAL COMMUNICATION SCORE ENGINE
# =========================================================
#
# PRINCIPLE:
#
# VIDEO
#   ↓
# PRIMARY MEASUREMENTS
#   ↓
# INDIVIDUAL DIMENSION SCORES
#   ↓
# OVERALL SCORE
#
# IMPORTANT:
# No dimension score is calculated from another dimension score.
#
# Missing measurements are NOT replaced by artificial values.
# =========================================================

import math


# =========================================================
# BASIC UTILITIES
# =========================================================

def clamp(value, default=None):

    if value is None:
        return default

    try:
        value = float(value)

        if not math.isfinite(value):
            return default

        return max(
            0,
            min(
                100,
                round(value)
            )
        )

    except (TypeError, ValueError):
        return default


def get_value(result, key):

    if not isinstance(result, dict):
        return None

    value = result.get(key)

    if value is None:
        return None

    try:

        value = float(value)

        if not math.isfinite(value):
            return None

        if value < 0 or value > 100:
            return None

        return value

    except (TypeError, ValueError):

        return None


# =========================================================
# WEIGHTED AVERAGE
# =========================================================
#
# Missing measurements are excluded.
#
# This means:
#
# measured values → contribute
# unavailable values → do NOT contribute
#
# No artificial zeroes.
# No artificial 100s.
# =========================================================

def weighted_average(values):

    valid = []

    for value, weight in values:

        if value is None:
            continue

        try:

            value = float(value)
            weight = float(weight)

        except (TypeError, ValueError):

            continue

        if not math.isfinite(value):
            continue

        if not math.isfinite(weight):
            continue

        if weight <= 0:
            continue

        valid.append(
            (value, weight)
        )

    if not valid:
        return None

    total_weight = sum(
        weight
        for _, weight in valid
    )

    if total_weight <= 0:
        return None

    total = sum(
        value * weight
        for value, weight in valid
    )

    return clamp(
        total / total_weight
    )


# =========================================================
# PACE SCORE
# =========================================================
#
# WPM is a PRIMARY measurement.
#
# The score rewards a comfortable speaking range,
# rather than assuming faster is better.
# =========================================================

def calculate_pace_score(result):

    wpm = result.get("speech")

    try:

        wpm = float(wpm)

    except (TypeError, ValueError):

        return None

    if not math.isfinite(wpm):
        return None

    if wpm <= 0:
        return None

    if wpm < 80:
        return 45

    if wpm < 95:
        return 65

    if wpm < 105:
        return 78

    if wpm <= 145:
        return 95

    if wpm <= 160:
        return 85

    if wpm <= 180:
        return 68

    return 50


# =========================================================
# REPETITION QUALITY
# =========================================================
#
# PRIMARY SOURCE:
#
# repeated_words
#
# Frequency matters.
#
# Example:
#
# India ×10
# merely ×6
# freedom ×5
# courage ×4
#
# is significantly more repetitive than:
#
# India ×2
# =========================================================

def calculate_repetition_quality(result):

    repeated = result.get(
        "repeated_words",
        {}
    )

    if not isinstance(
        repeated,
        dict
    ):

        return None

    if not repeated:

        return 98

    repeated_types = 0
    total_repetitions = 0
    maximum_frequency = 0

    for frequency in repeated.values():

        try:

            frequency = int(
                frequency
            )

        except (
            TypeError,
            ValueError
        ):

            continue

        if frequency < 2:
            continue

        repeated_types += 1

        total_repetitions += (
            frequency - 1
        )

        maximum_frequency = max(
            maximum_frequency,
            frequency
        )

    if repeated_types == 0:

        return 98

    # -----------------------------------------------------
    # Penalty for number of repeated word types.
    # -----------------------------------------------------

    penalty = (
        repeated_types * 4
    )

    # -----------------------------------------------------
    # Penalty for total repeated occurrences.
    # -----------------------------------------------------

    penalty += (
        total_repetitions * 2
    )

    # -----------------------------------------------------
    # Strong penalty for excessive repetition.
    # -----------------------------------------------------

    if maximum_frequency >= 10:

        penalty += 15

    elif maximum_frequency >= 7:

        penalty += 10

    elif maximum_frequency >= 5:

        penalty += 5

    return clamp(
        100 - penalty
    )


# =========================================================
# FILLER CONTROL
# =========================================================
#
# Uses actual filler count / actual word count.
# =========================================================

def calculate_filler_quality(result):

    words = result.get(
        "word_count"
    )

    fillers = result.get(
        "filler_count"
    )

    try:

        words = float(words)
        fillers = float(fillers)

    except (
        TypeError,
        ValueError
    ):

        return None

    if not math.isfinite(words):
        return None

    if not math.isfinite(fillers):
        return None

    if words <= 0:
        return None

    if fillers < 0:
        return None

    ratio = (
        fillers / words
    ) * 100

    if ratio == 0:
        return 100

    if ratio <= 1:
        return 95

    if ratio <= 2:
        return 88

    if ratio <= 4:
        return 78

    if ratio <= 6:
        return 65

    return 50


# =========================================================
# CONFIDENCE
# =========================================================
#
# PRIMARY MEASUREMENTS ONLY.
#
# voice_confidence is used ONLY when actually measured.
#
# No leadership.
# No presentation.
# No executive presence.
# =========================================================

def calculate_confidence(result):

    values = []

    voice_confidence = get_value(
        result,
        "voice_confidence"
    )

    if voice_confidence is not None:

        values.append(
            (voice_confidence, 0.35)
        )

    voice_energy = get_value(
        result,
        "voice_energy"
    )

    if voice_energy is not None:

        values.append(
            (voice_energy, 0.20)
        )

    pause_score = get_value(
        result,
        "pause_score"
    )

    if pause_score is not None:

        values.append(
            (pause_score, 0.15)
        )

    clarity = get_value(
        result,
        "clarity"
    )

    if clarity is not None:

        values.append(
            (clarity, 0.10)
        )

    pace = calculate_pace_score(
        result
    )

    if pace is not None:

        values.append(
            (pace, 0.10)
        )

    filler = calculate_filler_quality(
        result
    )

    if filler is not None:

        values.append(
            (filler, 0.10)
        )

    return weighted_average(
        values
    )


# =========================================================
# LEADERSHIP
# =========================================================

def calculate_leadership(result):

    values = []

    structure = get_value(
        result,
        "structure_score"
    )

    if structure is not None:

        values.append(
            (structure, 0.30)
        )

    clarity = get_value(
        result,
        "clarity"
    )

    if clarity is not None:

        values.append(
            (clarity, 0.20)
        )

    voice = get_value(
        result,
        "voice_confidence"
    )

    if voice is not None:

        values.append(
            (voice, 0.15)
        )

    energy = get_value(
        result,
        "voice_energy"
    )

    if energy is not None:

        values.append(
            (energy, 0.10)
        )

    repetition = calculate_repetition_quality(
        result
    )

    if repetition is not None:

        values.append(
            (repetition, 0.10)
        )

    pace = calculate_pace_score(
        result
    )

    if pace is not None:

        values.append(
            (pace, 0.15)
        )

    return weighted_average(
        values
    )


# =========================================================
# INTERVIEW
# =========================================================

def calculate_interview_score(result):

    values = []

    clarity = get_value(
        result,
        "clarity"
    )

    if clarity is not None:

        values.append(
            (clarity, 0.25)
        )

    structure = get_value(
        result,
        "structure_score"
    )

    if structure is not None:

        values.append(
            (structure, 0.20)
        )

    voice = get_value(
        result,
        "voice_confidence"
    )

    if voice is not None:

        values.append(
            (voice, 0.15)
        )

    pace = calculate_pace_score(
        result
    )

    if pace is not None:

        values.append(
            (pace, 0.15)
        )

    filler = calculate_filler_quality(
        result
    )

    if filler is not None:

        values.append(
            (filler, 0.15)
        )

    repetition = calculate_repetition_quality(
        result
    )

    if repetition is not None:

        values.append(
            (repetition, 0.10)
        )

    return weighted_average(
        values
    )


# =========================================================
# PRESENTATION
# =========================================================

def calculate_presentation_score(result):

    values = []

    structure = get_value(
        result,
        "structure_score"
    )

    if structure is not None:

        values.append(
            (structure, 0.25)
        )

    clarity = get_value(
        result,
        "clarity"
    )

    if clarity is not None:

        values.append(
            (clarity, 0.20)
        )

    voice = get_value(
        result,
        "voice_confidence"
    )

    if voice is not None:

        values.append(
            (voice, 0.15)
        )

    energy = get_value(
        result,
        "voice_energy"
    )

    if energy is not None:

        values.append(
            (energy, 0.10)
        )

    gesture = get_value(
        result,
        "gesture_score"
    )

    if gesture is not None:

        values.append(
            (gesture, 0.10)
        )

    posture = get_value(
        result,
        "posture"
    )

    if posture is not None:

        values.append(
            (posture, 0.10)
        )

    pace = calculate_pace_score(
        result
    )

    if pace is not None:

        values.append(
            (pace, 0.10)
        )

    return weighted_average(
        values
    )


# =========================================================
# EXECUTIVE PRESENCE
# =========================================================

def calculate_executive_presence(result):

    values = []

    structure = get_value(
        result,
        "structure_score"
    )

    if structure is not None:

        values.append(
            (structure, 0.25)
        )

    clarity = get_value(
        result,
        "clarity"
    )

    if clarity is not None:

        values.append(
            (clarity, 0.20)
        )

    voice = get_value(
        result,
        "voice_confidence"
    )

    if voice is not None:

        values.append(
            (voice, 0.15)
        )

    energy = get_value(
        result,
        "voice_energy"
    )

    if energy is not None:

        values.append(
            (energy, 0.10)
        )

    posture = get_value(
        result,
        "posture"
    )

    if posture is not None:

        values.append(
            (posture, 0.10)
        )

    gesture = get_value(
        result,
        "gesture_score"
    )

    if gesture is not None:

        values.append(
            (gesture, 0.10)
        )

    repetition = calculate_repetition_quality(
        result
    )

    if repetition is not None:

        values.append(
            (repetition, 0.10)
        )

    return weighted_average(
        values
    )


# =========================================================
# OVERALL SCORE
# =========================================================
#
# PRIMARY MEASUREMENTS ONLY.
#
# NEVER USE:
#
# confidence
# leadership
# interview_score
# presentation_score
# executive_presence
#
# =========================================================

def calculate_overall_score(result):

    values = []

    # -----------------------------------------------------
    # Speech quality
    # -----------------------------------------------------

    speech_quality = get_value(
        result,
        "speech_quality"
    )

    if speech_quality is not None:

        values.append(
            (speech_quality, 0.18)
        )

    # -----------------------------------------------------
    # Clarity
    # -----------------------------------------------------

    clarity = get_value(
        result,
        "clarity"
    )

    if clarity is not None:

        values.append(
            (clarity, 0.15)
        )

    # -----------------------------------------------------
    # Structure
    # -----------------------------------------------------

    structure = get_value(
        result,
        "structure_score"
    )

    if structure is not None:

        values.append(
            (structure, 0.15)
        )

    # -----------------------------------------------------
    # Voice confidence
    #
    # Only contributes when actually measured.
    # -----------------------------------------------------

    voice_confidence = get_value(
        result,
        "voice_confidence"
    )

    if voice_confidence is not None:

        values.append(
            (voice_confidence, 0.12)
        )

    # -----------------------------------------------------
    # Voice energy
    # -----------------------------------------------------

    voice_energy = get_value(
        result,
        "voice_energy"
    )

    if voice_energy is not None:

        values.append(
            (voice_energy, 0.10)
        )

    # -----------------------------------------------------
    # Pace
    # -----------------------------------------------------

    pace = calculate_pace_score(
        result
    )

    if pace is not None:

        values.append(
            (pace, 0.10)
        )

    # -----------------------------------------------------
    # Repetition
    # -----------------------------------------------------

    repetition = calculate_repetition_quality(
        result
    )

    if repetition is not None:

        values.append(
            (repetition, 0.10)
        )

    # -----------------------------------------------------
    # Filler control
    # -----------------------------------------------------

    filler = calculate_filler_quality(
        result
    )

    if filler is not None:

        values.append(
            (filler, 0.05)
        )

    # -----------------------------------------------------
    # Posture
    # -----------------------------------------------------

    posture = get_value(
        result,
        "posture"
    )

    if posture is not None:

        values.append(
            (posture, 0.025)
        )

    # -----------------------------------------------------
    # Gesture
    # -----------------------------------------------------

    gesture = get_value(
        result,
        "gesture_score"
    )

    if gesture is not None:

        values.append(
            (gesture, 0.025)
        )

    return weighted_average(
        values
    )