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


def analyze_complete_video(video_path, analysis_type="General Speech"):

    result = {}

    # =========================================================
    # 1. VISUAL ANALYSIS
    # =========================================================

    print("STEP 1: Visual analysis")

    try:
        visual_result = analyze_video(video_path, analysis_type)

        if isinstance(visual_result, dict):
            result.update(visual_result)

    except Exception as e:
        print("Visual analysis error:", e)

    # =========================================================
    # 2. SPEECH TRANSCRIPTION
    # =========================================================

    print("STEP 2: Speech transcription")

    try:
        transcript_result = transcribe_video(video_path)

        if isinstance(transcript_result, dict):
            result.update(transcript_result)

    except Exception as e:

        print("Speech transcription error:", e)

        result["transcript"] = ""
        result["word_count"] = 0
        result["speech"] = None
        result["duration"] = None
        result["transcription_available"] = False

    # =========================================================
    # 3. TRANSCRIPT CLEANING
    # =========================================================

    print("STEP 3: Transcript cleaning")

    original_transcript = result.get("transcript", "")

    try:

        cleaned = process_transcript(
            original_transcript,
            analysis_type
        )

        if isinstance(cleaned, dict):

            result["original_transcript"] = cleaned.get(
                "original_transcript",
                original_transcript
            )

            result["transcript"] = cleaned.get(
                "transcript",
                original_transcript
            )

            result["hallucination_flags"] = cleaned.get(
                "hallucination_flags",
                []
            )

            result["transcript_quality"] = cleaned.get(
                "transcript_quality"
            )

            result["transcript_cleaned"] = cleaned.get(
                "cleaned",
                False
            )

    except Exception as e:

        print("Transcript cleaning error:", e)

        result["original_transcript"] = original_transcript
        result["transcript"] = original_transcript
        result["hallucination_flags"] = []
        result["transcript_quality"] = None
        result["transcript_cleaned"] = False

    # =========================================================
    # 4. TRANSCRIPT INTELLIGENCE
    # =========================================================

    print("STEP 4: Transcript intelligence")

    try:

        transcript_analysis = analyze_transcript(
            result.get("transcript", ""),
            analysis_type
        )

        if isinstance(transcript_analysis, dict):

            result.update({
                "transcript_word_count":
                    transcript_analysis.get("word_count"),

                "filler_count":
                    transcript_analysis.get("filler_count"),

                "fillers":
                    transcript_analysis.get("fillers", {}),

                "opening":
                    transcript_analysis.get("opening", ""),

                "conclusion":
                    transcript_analysis.get("conclusion", ""),

                "structure_score":
                    transcript_analysis.get("structure_score"),

                "clarity":
                    transcript_analysis.get("clarity_score"),

                "speech_quality":
                    transcript_analysis.get("clarity_score"),

                "repetition_score":
                    transcript_analysis.get("repetition_score"),

                "repeated_words":
                    transcript_analysis.get("repeated_words", {}),
            })

    except Exception as e:

        print("Transcript analysis error:", e)

        result["structure_score"] = None
        result["clarity"] = None
        result["speech_quality"] = None
        result["repetition_score"] = None

    # =========================================================
    # 5. VOICE ANALYSIS
    # =========================================================

    print("STEP 5: Voice analysis")

    try:

        voice_result = analyze_voice(video_path)

        if isinstance(voice_result, dict):
            result.update(voice_result)

    except Exception as e:

        print("Voice analysis error:", e)

        result["voice_confidence"] = None
        result["voice_energy"] = None
        result["pause_score"] = None

    # =========================================================
    # 6. EMOTION ANALYSIS
    # =========================================================

    print("STEP 6: Emotion analysis")

    try:

        result["emotion"] = analyze_emotion(video_path)

    except Exception as e:

        print("Emotion analysis error:", e)
        result["emotion"] = "Unknown"

    # =========================================================
    # 7. ANALYSIS TYPE
    # =========================================================

    result["analysis_type"] = analysis_type

    # =========================================================
    # 8. AI SCORING
    # =========================================================

    print("STEP 7: AI scoring")

    try:
        result["confidence"] = calculate_confidence(result)
    except Exception as e:
        print("Confidence scoring error:", e)
        result["confidence"] = None

    try:
        result["leadership"] = calculate_leadership(result)
    except Exception as e:
        print("Leadership scoring error:", e)
        result["leadership"] = None

    try:
        result["interview_score"] = calculate_interview_score(result)
    except Exception as e:
        print("Interview scoring error:", e)
        result["interview_score"] = None

    try:
        result["presentation_score"] = calculate_presentation_score(result)
    except Exception as e:
        print("Presentation scoring error:", e)
        result["presentation_score"] = None

    try:
        result["executive_presence"] = calculate_executive_presence(result)
    except Exception as e:
        print("Executive scoring error:", e)
        result["executive_presence"] = None

    try:
        result["overall_score"] = calculate_overall_score(result)
    except Exception as e:
        print("Overall scoring error:", e)
        result["overall_score"] = None

    # =========================================================
    # 9. AI FEEDBACK
    # =========================================================

    print("STEP 8: AI feedback")

    try:

        feedback = generate_ai_feedback(
            result,
            analysis_type
        )

        if isinstance(feedback, dict):
            result["feedback"] = feedback
        else:
            result["feedback"] = {
                "strengths": [],
                "improvements": [],
                "suggestions": []
            }

    except Exception as e:

        print("AI feedback error:", e)

        result["feedback"] = {
            "strengths": [],
            "improvements": [],
            "suggestions": []
        }

    # =========================================================
    # 10. FINAL NORMALIZATION
    # =========================================================

    # Use transcript word count when available.
    if not result.get("word_count"):
        result["word_count"] = result.get(
            "transcript_word_count",
            0
        )

    # Calculate WPM from actual duration when possible.
    duration = result.get("duration")
    words = result.get("word_count", 0)

    try:
        duration = float(duration)
        words = int(words)

        if duration > 0 and words > 0:
            result["speech"] = round(
                words / (duration / 60),
                1
            )
    except (TypeError, ValueError, ZeroDivisionError):
        pass

    # Never turn unavailable measurements into fake zeroes.
    for key in (
        "voice_confidence",
        "voice_energy",
        "pause_score",
        "eye_contact",
        "posture",
        "gesture_score",
        "smile",
        "engagement",
    ):
        if result.get(key) == 0 and not result.get(
            f"{key}_available",
            True
        ):
            result[key] = None

    result["analysis_ready"] = True

    print("=================================================")
    print("ANALYSIS COMPLETE")
    print("Overall:", result.get("overall_score"))
    print("Confidence:", result.get("confidence"))
    print("Leadership:", result.get("leadership"))
    print("Presentation:", result.get("presentation_score"))
    print("Executive:", result.get("executive_presence"))
    print("Speech Quality:", result.get("speech_quality"))
    print("Structure:", result.get("structure_score"))
    print("Clarity:", result.get("clarity"))
    print("Voice Confidence:", result.get("voice_confidence"))
    print("Words:", result.get("word_count"))
    print("Duration:", result.get("duration"))
    print("=================================================")

    return result
