from modules.analyzer import analyze_video
from modules.voice_analysis import analyze_voice
from modules.speech_to_text import transcribe_video
from modules.emotion_analysis import analyze_emotion

from modules.transcript_quality import process_transcript

from modules.ai_engine import (
    calculate_confidence,
    calculate_leadership,
    calculate_interview_score,
    calculate_presentation_score,
    calculate_executive_presence,
    calculate_overall_score,
)

from modules.ai_coach import (
    generate_ai_feedback,
    analyze_transcript,
)


def analyze_complete_video(
    video_path,
    analysis_type="General Speech"
):

    result = {}

    # =========================================================
    # 1. VISUAL ANALYSIS
    # =========================================================

    print("STEP 1: Visual analysis")

    try:

        visual_result = analyze_video(
            video_path,
            analysis_type
        )

        if isinstance(visual_result, dict):
            result.update(visual_result)

    except Exception as e:

        print("Visual analysis error:", e)

        result["vision_available"] = False


    # =========================================================
    # 2. SPEECH TRANSCRIPTION
    # =========================================================

    print("STEP 2: Speech transcription")

    try:

        transcript_result = transcribe_video(
            video_path
        )

        if isinstance(transcript_result, dict):

            result.update(
                transcript_result
            )

            result["transcription_available"] = True

    except Exception as e:

        print(
            "Speech transcription error:",
            e
        )

        result["transcript"] = ""
        result["word_count"] = 0
        result["speech"] = None
        result["duration"] = None

        result["transcription_available"] = False


    # =========================================================
    # 3. TRANSCRIPT CLEANING
    # =========================================================

    print("STEP 3: Transcript cleaning")

    original_transcript = result.get(
        "transcript",
        ""
    )

    try:

        cleaned = process_transcript(
            original_transcript,
            analysis_type
        )

        if isinstance(cleaned, dict):

            result["original_transcript"] = (
                cleaned.get(
                    "original_transcript",
                    original_transcript
                )
            )

            result["transcript"] = (
                cleaned.get(
                    "transcript",
                    original_transcript
                )
            )

            result["hallucination_flags"] = (
                cleaned.get(
                    "hallucination_flags",
                    []
                )
            )

            result["transcript_quality"] = (
                cleaned.get(
                    "transcript_quality"
                )
            )

            result["transcript_cleaned"] = (
                cleaned.get(
                    "cleaned",
                    False
                )
            )

    except Exception as e:

        print(
            "Transcript cleaning error:",
            e
        )

        result["original_transcript"] = (
            original_transcript
        )

        result["transcript"] = (
            original_transcript
        )

        result["hallucination_flags"] = []

        result["transcript_quality"] = None

        result["transcript_cleaned"] = False


    # =========================================================
    # 4. TRANSCRIPT INTELLIGENCE
    # =========================================================

    print("STEP 4: Transcript intelligence")

    try:

        transcript_analysis = analyze_transcript(
            result.get(
                "transcript",
                ""
            ),
            analysis_type
        )

        if isinstance(
            transcript_analysis,
            dict
        ):

            result["transcript_word_count"] = (
                transcript_analysis.get(
                    "word_count"
                )
            )

            result["filler_count"] = (
                transcript_analysis.get(
                    "filler_count"
                )
            )

            result["fillers"] = (
                transcript_analysis.get(
                    "fillers",
                    {}
                )
            )

            result["opening"] = (
                transcript_analysis.get(
                    "opening",
                    ""
                )
            )

            result["conclusion"] = (
                transcript_analysis.get(
                    "conclusion",
                    ""
                )
            )

            result["structure_score"] = (
                transcript_analysis.get(
                    "structure_score"
                )
            )

            result["clarity"] = (
                transcript_analysis.get(
                    "clarity_score"
                )
            )

            result["speech_quality"] = (
                transcript_analysis.get(
                    "speech_quality"
                )
            )

            result["repetition_score"] = (
                transcript_analysis.get(
                    "repetition_score"
                )
            )

            result["repeated_words"] = (
                transcript_analysis.get(
                    "repeated_words",
                    {}
                )
            )

    except Exception as e:

        print(
            "Transcript analysis error:",
            e
        )

        result["transcript_word_count"] = None
        result["filler_count"] = None
        result["fillers"] = {}
        result["opening"] = ""
        result["conclusion"] = ""

        result["structure_score"] = None
        result["clarity"] = None
        result["speech_quality"] = None
        result["repetition_score"] = None
        result["repeated_words"] = {}


    # =========================================================
    # 5. VOICE ANALYSIS
    # =========================================================

    print("STEP 5: Voice analysis")

    try:

        voice_result = analyze_voice(
            video_path
        )

        if isinstance(
            voice_result,
            dict
        ):

            result.update(voice_result)

            # Preserve the REAL analyzer availability state.
            # Never mark voice analysis as available merely because
            # the function returned a dictionary.
            result["voice_analysis_available"] = bool(
                voice_result.get("voice_analysis_available", False)
            )

            # =================================================
            # VOICE METRIC AVAILABILITY
            # =================================================

            voice_energy = voice_result.get("voice_energy")
            pause_score = voice_result.get("pause_score")
            voice_confidence = voice_result.get("voice_confidence")

            # If the analyzer produced the underlying voice
            # signals but did not produce the combined score,
            # calculate the combined score from those real signals.
            if voice_confidence is None:
                valid_voice_values = [
                    float(v)
                    for v in (voice_energy, pause_score)
                    if v is not None
                ]

                if valid_voice_values:
                    if (
                        voice_energy is not None
                        and pause_score is not None
                    ):
                        voice_confidence = round(
                            float(voice_energy) * 0.55
                            + float(pause_score) * 0.45
                        )
                    else:
                        voice_confidence = round(
                            sum(valid_voice_values)
                            / len(valid_voice_values)
                        )

                    result["voice_confidence"] = max(
                        0,
                        min(100, int(voice_confidence))
                    )

            result["voice_confidence_available"] = (
                result.get("voice_confidence") is not None
            )

            result["voice_energy_available"] = (
                voice_energy is not None
            )

            result["pause_score_available"] = (
                pause_score is not None
            )

            result["voice_analysis_available"] = (
                result["voice_confidence_available"]
                or result["voice_energy_available"]
                or result["pause_score_available"]
            )

            result["voice_confidence_available"] = (
                voice_result.get("voice_confidence") is not None
            )

            result["voice_energy_available"] = (
                voice_result.get("voice_energy") is not None
            )

            result["pause_score_available"] = (
                voice_result.get("pause_score") is not None
            )

    except Exception as e:

        print(
            "Voice analysis error:",
            e
        )

        result["voice_confidence"] = None
        result["voice_energy"] = None
        result["pause_score"] = None

        result["voice_confidence_available"] = False
        result["voice_energy_available"] = False
        result["pause_score_available"] = False
        result["voice_analysis_available"] = False


    # =========================================================
    # 6. EMOTION ANALYSIS
    # =========================================================

    print("STEP 6: Emotion analysis")

    try:

        result["emotion"] = (
            analyze_emotion(
                video_path
            )
        )

    except Exception as e:

        print(
            "Emotion analysis error:",
            e
        )

        result["emotion"] = "Unknown"


    # =========================================================
    # 7. ANALYSIS TYPE
    # =========================================================

    result["analysis_type"] = (
        analysis_type
    )


    # =========================================================
    # 8. PRIMARY MEASUREMENT NORMALIZATION
    #
    # Nothing is scored until this section is complete.
    # =========================================================

    print(
        "STEP 6.5: Preparing primary measurements"
    )


    # ---------------------------------------------------------
    # WORD COUNT
    # ---------------------------------------------------------

    word_count = result.get(
        "word_count"
    )

    try:

        word_count = int(
            word_count
        )

    except (
        TypeError,
        ValueError
    ):

        word_count = 0


    if word_count <= 0:

        transcript_word_count = (
            result.get(
                "transcript_word_count"
            )
        )

        try:

            word_count = int(
                transcript_word_count
            )

        except (
            TypeError,
            ValueError
        ):

            word_count = 0


    result["word_count"] = (
        word_count
    )


    # ---------------------------------------------------------
    # DURATION
    # ---------------------------------------------------------

    duration = result.get(
        "duration"
    )

    try:

        duration = float(
            duration
        )

        if duration <= 0:

            duration = None

    except (
        TypeError,
        ValueError
    ):

        duration = None


    result["duration"] = (
        duration
    )


    # ---------------------------------------------------------
    # WPM
    #
    # IMPORTANT:
    # This is calculated BEFORE ANY SCORE.
    # ---------------------------------------------------------

    if (
        duration is not None
        and
        duration > 0
        and
        word_count > 0
    ):

        result["speech"] = round(
            word_count /
            (duration / 60),
            1
        )

    else:

        result["speech"] = None


    # ---------------------------------------------------------
    # REPEATED WORDS
    #
    # This remains the source of truth.
    # ---------------------------------------------------------

    repeated_words = result.get(
        "repeated_words",
        {}
    )

    if not isinstance(
        repeated_words,
        dict
    ):

        repeated_words = {}


    result["repeated_words"] = (
        repeated_words
    )


    # ---------------------------------------------------------
    # INVALID ZERO VALUES
    #
    # Zero is accepted ONLY when the measurement
    # was genuinely available.
    # ---------------------------------------------------------

    unavailable_metrics = [

        "voice_confidence",
        "voice_energy",
        "pause_score",

        "eye_contact",
        "posture",
        "gesture_score",
        "smile",
        "engagement",

    ]


    for key in unavailable_metrics:

        value = result.get(
            key
        )

        available = result.get(
            f"{key}_available",
            True
        )

        if (
            value == 0
            and
            available is False
        ):

            result[key] = None


    # =========================================================
    # 9. INDEPENDENT AI SCORING
    #
    # Every dimension reads PRIMARY measurements.
    #
    # NO:
    #
    # confidence -> leadership
    # leadership -> presentation
    # presentation -> executive
    # executive -> overall
    #
    # =========================================================

    print(
        "STEP 7: AI scoring"
    )


    # ---------------------------------------------------------
    # CONFIDENCE
    # ---------------------------------------------------------

    try:

        result["confidence"] = (
            calculate_confidence(
                result
            )
        )

    except Exception as e:

        print(
            "Confidence scoring error:",
            e
        )

        result["confidence"] = None


    # ---------------------------------------------------------
    # LEADERSHIP
    # ---------------------------------------------------------

    try:

        result["leadership"] = (
            calculate_leadership(
                result
            )
        )

    except Exception as e:

        print(
            "Leadership scoring error:",
            e
        )

        result["leadership"] = None


    # ---------------------------------------------------------
    # INTERVIEW
    # ---------------------------------------------------------

    try:

        result["interview_score"] = (
            calculate_interview_score(
                result
            )
        )

    except Exception as e:

        print(
            "Interview scoring error:",
            e
        )

        result["interview_score"] = None


    # ---------------------------------------------------------
    # PRESENTATION
    # ---------------------------------------------------------

    try:

        result["presentation_score"] = (
            calculate_presentation_score(
                result
            )
        )

    except Exception as e:

        print(
            "Presentation scoring error:",
            e
        )

        result["presentation_score"] = None


    # ---------------------------------------------------------
    # EXECUTIVE PRESENCE
    # ---------------------------------------------------------

    try:

        result["executive_presence"] = (
            calculate_executive_presence(
                result
            )
        )

    except Exception as e:

        print(
            "Executive scoring error:",
            e
        )

        result["executive_presence"] = None


    # ---------------------------------------------------------
    # OVERALL
    #
    # ONLY PRIMARY MEASUREMENTS.
    # ---------------------------------------------------------

    try:

        result["overall_score"] = (
            calculate_overall_score(
                result
            )
        )

    except Exception as e:

        print(
            "Overall scoring error:",
            e
        )

        result["overall_score"] = None


    # =========================================================
    # 10. AI FEEDBACK
    # =========================================================

    print(
        "STEP 8: AI feedback"
    )

    try:

        feedback = generate_ai_feedback(
            result,
            analysis_type
        )

        if isinstance(
            feedback,
            dict
        ):

            result["feedback"] = (
                feedback
            )

        else:

            result["feedback"] = {

                "strengths": [],
                "improvements": [],
                "suggestions": []

            }

    except Exception as e:

        print(
            "AI feedback error:",
            e
        )

        result["feedback"] = {

            "strengths": [],
            "improvements": [],
            "suggestions": []

        }


    # =========================================================
    # 11. FINAL STATE
    # =========================================================

    result["analysis_ready"] = True


    # =========================================================
    # DEBUG OUTPUT
    # =========================================================

    print(
        "================================================="
    )

    print(
        "ANALYSIS COMPLETE"
    )

    print(
        "Overall:",
        result.get("overall_score")
    )

    print(
        "Confidence:",
        result.get("confidence")
    )

    print(
        "Leadership:",
        result.get("leadership")
    )

    print(
        "Interview:",
        result.get("interview_score")
    )

    print(
        "Presentation:",
        result.get("presentation_score")
    )

    print(
        "Executive:",
        result.get("executive_presence")
    )

    print(
        "Speech Quality:",
        result.get("speech_quality")
    )

    print(
        "Structure:",
        result.get("structure_score")
    )

    print(
        "Clarity:",
        result.get("clarity")
    )

    print(
        "Repetition Score:",
        result.get("repetition_score")
    )

    print(
        "Repeated Words:",
        result.get("repeated_words")
    )

    print(
        "Voice Confidence:",
        result.get("voice_confidence")
    )

    print(
        "Voice Energy:",
        result.get("voice_energy")
    )

    print(
        "Pause Score:",
        result.get("pause_score")
    )

    print(
        "Words:",
        result.get("word_count")
    )

    print(
        "Duration:",
        result.get("duration")
    )

    print(
        "WPM:",
        result.get("speech")
    )

    print(
        "================================================="
    )


    return result