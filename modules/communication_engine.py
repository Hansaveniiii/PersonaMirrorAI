from modules.interview_ai import transcribe
from modules.interview_voice import analyze_interview_voice
from modules.interview_vision import analyze_interview_video
from modules.interview_analyzer import analyze_answer


def analyze_communication(video_path):

    # Speech → Text
    transcript = transcribe(video_path)

    # Voice Analysis
    voice = analyze_interview_voice(
        video_path,
        transcript
    )

    # Video Analysis
    vision = analyze_interview_video(
        video_path
    )

    # Speech Quality
    analysis = analyze_answer(
        transcript
    )

    return {

        "transcript": transcript,

        "voice": voice,

        "vision": vision,

        "analysis": analysis

    }