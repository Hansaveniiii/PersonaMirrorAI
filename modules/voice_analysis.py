import os
import subprocess
import tempfile

import librosa
import numpy as np


def extract_audio(video_path, audio_path):
    """
    Extract audio from video using FFmpeg.
    This replaces MoviePy and is considerably more reliable.
    """

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-acodec", "pcm_s16le",
        audio_path,
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "FFmpeg audio extraction failed."
        )


def analyze_voice(video_path):

    audio_file = None

    try:

        # -------------------------------------------------
        # Create temporary audio file
        # -------------------------------------------------

        temp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        audio_file = temp.name
        temp.close()

        # -------------------------------------------------
        # Extract audio using FFmpeg
        # -------------------------------------------------

        extract_audio(
            video_path,
            audio_file
        )

        # -------------------------------------------------
        # Load audio
        # -------------------------------------------------

        y, sr = librosa.load(
            audio_file,
            sr=16000,
            mono=True
        )

        if y is None or len(y) == 0:

            return {
                "voice_energy": 0,
                "pause_score": 0,
                "voice_confidence": 0,
                "duration": 0,
                "speech_rate": 0,
                "pace_feedback": "No audio detected."
            }

        # -------------------------------------------------
        # Duration
        # -------------------------------------------------

        duration = len(y) / sr

        if duration <= 0:
            duration = 1

        # -------------------------------------------------
        # VOICE ENERGY
        # -------------------------------------------------

        rms = librosa.feature.rms(
            y=y,
            frame_length=2048,
            hop_length=512
        )[0]

        energy = float(
            np.mean(rms)
        )

        # Normalize energy more gently.
        voice_energy = int(
            np.clip(
                energy * 1800,
                0,
                100
            )
        )

        # -------------------------------------------------
        # SPEECH / SILENCE DETECTION
        # -------------------------------------------------

        intervals = librosa.effects.split(
            y,
            top_db=30
        )

        active_duration = 0

        for start, end in intervals:

            active_duration += (
                end - start
            ) / sr

        active_duration = min(
            active_duration,
            duration
        )

        pause_ratio = (
            duration - active_duration
        ) / duration

        pause_ratio = float(
            np.clip(
                pause_ratio,
                0,
                1
            )
        )

        # -------------------------------------------------
        # PAUSE SCORE
        #
        # A speech should NOT be punished for
        # having natural pauses.
        # -------------------------------------------------

        if 0.08 <= pause_ratio <= 0.35:

            pause_score = 90

        elif pause_ratio < 0.08:

            pause_score = 75

        elif pause_ratio <= 0.50:

            pause_score = 70

        else:

            pause_score = 50

        # -------------------------------------------------
        # VOICE CONFIDENCE
        # -------------------------------------------------

        voice_confidence = int(
            np.clip(
                (
                    voice_energy * 0.55
                    +
                    pause_score * 0.45
                ),
                0,
                100
            )
        )

        # -------------------------------------------------
        # IMPORTANT
        #
        # We do NOT pretend that audio duration itself
        # tells us speaking speed.
        #
        # Actual WPM should come from Whisper.
        # -------------------------------------------------

        speech_rate = 0

        # -------------------------------------------------
        # PACE FEEDBACK
        # -------------------------------------------------

        pace = (
            "Your vocal pacing can be evaluated "
            "from the transcription and timing analysis."
        )

        return {

            "voice_energy": voice_energy,

            "pause_score": pause_score,

            "voice_confidence": voice_confidence,

            "duration": round(
                duration,
                1
            ),

            "speech_rate": speech_rate,

            "pace_feedback": pace

        }

    except Exception as e:

        print(
            "Voice analysis error:",
            e
        )

        return {

            "voice_energy": 0,

            "pause_score": 0,

            "voice_confidence": 0,

            "duration": 0,

            "speech_rate": 0,

            "pace_feedback":
                "Voice analysis unavailable."

        }

    finally:

        if (
            audio_file
            and
            os.path.exists(audio_file)
        ):

            try:
                os.remove(audio_file)
            except Exception:
                pass