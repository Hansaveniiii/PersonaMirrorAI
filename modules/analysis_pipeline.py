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

        if visual_result:
            result.update(visual_result)

    except Exception as e:

        print(
            "Visual analysis error:",
            e
        )

    # =========================================================
    # 2. SPEECH TRANSCRIPTION
    # =========================================================

    print("STEP 2: Speech transcription")

    try:

        transcript_result = transcribe_video(
            video_path
        )

        if transcript_result:
            result.update(
                transcript_result
            )

    except Exception as e:

        print(
            "Speech transcription error:",
            e
        )

        result["transcript"] = ""
        result["word_count"] = 0
        result["speech"] = 0
        result["duration"] = 0
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

        transcript_result = process_transcript(
            original_transcript,
            analysis_type
        )

        result["original_transcript"] = (
            transcript_result.get(
                "original_transcript",
                original_transcript
            )
        )

        result["transcript"] = (
            transcript_result.get(
                "transcript",
                original_transcript
            )
        )

        result["hallucination_flags"] = (
            transcript_result.get(
                "hallucination_flags",
                []
            )
        )

        result["transcript_quality"] = (
            transcript_result.get(
                "transcript_quality"
            )
        )

        result["transcript_cleaned"] = (
            transcript_result.get(
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

        result.update({

            "transcript_word_count":
                transcript_analysis.get(
                    "word_count"
                ),

            "filler_count":
                transcript_analysis.get(
                    "filler_count"
                ),

            "fillers":
                transcript_analysis.get(
                    "fillers",
                    {}
                ),

            "opening":
                transcript_analysis.get(
                    "opening",
                    ""
                ),

            "conclusion":
                transcript_analysis.get(
                    "conclusion",
                    ""
                ),

            "structure_score":
                transcript_analysis.get(
                    "structure_score"
                ),

            "clarity":
                transcript_analysis.get(
                    "clarity_score"
                ),

            "speech_quality":
                transcript_analysis.get(
                    "clarity_score"
                ),

            "repetition_score":
                transcript_analysis.get(
                    "repetition_score"
                ),

            "repeated_words":
                transcript_analysis.get(
                    "repeated_words",
                    {}
                ),
        })

    except Exception as e:

        print(
            "Transcript analysis error:",
            e
        )

        result["structure_score"] = None
        result["clarity"] = None
        result["speech_quality"] = None
        result["repetition_score"] = None

    # =========================================================
    # 5. VOICE ANALYSIS
    # =========================================================

    print("STEP 5: Voice analysis")

    try:

        voice_result = analyze_voice(
            video_path
        )

        if voice_result:

            result.update(
                voice_result
            )

    except Exception as e:

        print(
            "Voice analysis error:",
            e
        )

        result["voice_confidence"] = None
        result["voice_energy"] = None
        result["pause_score"] = None

    # =========================================================
    # 6. EMOTION ANALYSIS
    # =========================================================

    print("STEP 6: Emotion analysis")

    try:

        result["emotion"] = analyze_emotion(
            video_path
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
    # 8. AI SCORING
    # =========================================================

    print("STEP 7: AI scoring")

    result["confidence"] = (
        calculate_confidence(result)
    )

    result["leadership"] = (
        calculate_leadership(result)
    )

    result["interview_score"] = (
        calculate_interview_score(result)
    )

    result["presentation_score"] = (
        calculate_presentation_score(result)
    )

    result["executive_presence"] = (
        calculate_executive_presence(result)
    )

    result["overall_score"] = (
        calculate_overall_score(result)
    )

    # =========================================================
    # 9. PERSONALIZED COACHING
    # =========================================================

    print(
        "STEP 8: Personalized coaching"
    )

    try:

        result["feedback"] = (
            generate_ai_feedback(
                result,
                analysis_type
            )
        )

    except Exception as e:

        print(
            "AI feedback error:",
            e
        )

        result["feedback"] = {

            "strengths": [],

            "improvements": [],

            "suggestions": [],
        }

    # =========================================================
    # 10. COMPLETE
    # =========================================================

    print(
        "STEP 9: Analysis completed"
    )

    return result