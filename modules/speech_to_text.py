import whisper


def transcribe_video(video_path):
    """
    Transcribes speech from a video using OpenAI Whisper.
    """

    model = whisper.load_model("base")

    result = model.transcribe(video_path)

    transcript = result["text"].strip()

    words = transcript.split()

    word_count = len(words)

    duration = result.get("segments", [{}])[-1].get("end", 1)

    if duration <= 0:
        duration = 1

    wpm = int((word_count / duration) * 60)

    return {
        "transcript": transcript,
        "word_count": word_count,
        "speech": wpm
    }