import whisper


model = whisper.load_model("base")


def analyze_speech(video_path):

    result = model.transcribe(video_path)

    text = result["text"]

    words = len(text.split())

    return {
        "transcript": text,
        "word_count": words
    }