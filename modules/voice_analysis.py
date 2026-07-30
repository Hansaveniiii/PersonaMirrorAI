import os
import librosa
import numpy as np
from moviepy.editor import VideoFileClip


def analyze_voice(video_path):

    try:

        audio_path = "temp_audio.wav"

        # Remove old audio file if it exists
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # Extract audio from video
        video = VideoFileClip(video_path)

        if video.audio is None:
            return {
                "voice_energy": 0,
                "pause_score": 0,
                "voice_confidence": 0
            }

        video.audio.write_audiofile(
            audio_path,
            fps=16000,
            codec="pcm_s16le",
            logger=None
        )

        # Load audio
        y, sr = librosa.load(audio_path, sr=None)

        if len(y) == 0:
            return {
                "voice_energy": 0,
                "pause_score": 0,
                "voice_confidence": 0
            }

        # ---------------- Voice Energy ----------------

        rms = librosa.feature.rms(y=y)[0]
        energy = float(np.mean(rms))

        energy_score = int(np.clip(energy * 1200, 0, 100))

        # ---------------- Pause Detection ----------------

        intervals = librosa.effects.split(y, top_db=25)

        duration = librosa.get_duration(y=y, sr=sr)

        active_time = sum(
            end - start
            for start, end in intervals
        ) / sr

        pause_ratio = max(
            0,
            (duration - active_time) / duration
        )

        pause_score = int(np.clip((1 - pause_ratio) * 100, 0, 100))

        # ---------------- Voice Confidence ----------------

        confidence = int(
            (energy_score + pause_score) / 2
        )

        # Clean up
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return {
            "voice_energy": energy_score,
            "pause_score": pause_score,
            "voice_confidence": confidence
        }

    except Exception as e:

        print("Voice Analysis Error:", e)

        return {
            "voice_energy": 0,
            "pause_score": 0,
            "voice_confidence": 0
        }