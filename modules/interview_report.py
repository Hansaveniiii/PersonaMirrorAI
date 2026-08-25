from modules.speech_to_text import transcribe_video
from modules.interview_analyzer import analyze_answer
from modules.interview_coach import generate_interview_feedback
from modules.video_analyzer import analyze_video


def generate_interview_report(question, video_path):

    # Speech-to-Text
    speech_result = transcribe_video(video_path)

    transcript = speech_result.get("transcript", "")

    if not transcript:
        transcript = "No speech detected."

    # Voice Information
    voice = {
        "speech_rate": speech_result.get("speech", 0),
        "duration": speech_result.get("duration", 0),
        "voice_energy": 0,
        "voice_confidence": 0,
        "pause_score": 0,
        "pace_feedback": "Voice transcription completed."
    }

    # Vision Analysis
    try:
        vision = analyze_video(video_path)

    except Exception as e:
        print("Vision analysis error:", e)

        vision = {
            "eye_contact": 0,
            "face_visibility": 0,
            "face_centering": 0,
            "head_stability": 0,
            "engagement": 0
        }

    # Language Analysis
    analysis = analyze_answer(
        question,
        transcript
    )
    # AI Interview Feedback
    feedback = generate_interview_feedback(
        question,
        transcript,
        voice,
        analysis
    )

    # Final Report
    return {
        "transcript": transcript,
        "voice": voice,
        "vision": vision,
        "analysis": analysis,
        "feedback": feedback
    }