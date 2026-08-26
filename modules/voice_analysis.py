import os
import subprocess
import tempfile

import librosa
import numpy as np


def extract_audio(video_path, audio_path):
    """
    Extract mono 16 kHz PCM audio from the uploaded video.
    """

    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-acodec",
        "pcm_s16le",
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
            "FFmpeg audio extraction failed: "
            + result.stderr[-1000:]
        )


def _unavailable_result(message):
    """
    Return None for unavailable measurements.

    IMPORTANT:
    None means the metric could not be measured.
    It must NOT become 0, because 0 means genuinely
    extremely poor performance.
    """

    return {
        "voice_energy": None,
        "pause_score": None,
        "voice_confidence": None,
        "duration": None,
        "speech_rate": None,
        "pace_feedback": message,
        "voice_analysis_available": False,
    }


def analyze_voice(video_path):

    audio_file = None

    try:

        # -------------------------------------------------
        # Validate input
        # -------------------------------------------------

        if not video_path or not os.path.exists(video_path):
            return _unavailable_result(
                "Voice analysis unavailable: video file not found."
            )

        # -------------------------------------------------
        # Temporary WAV
        # -------------------------------------------------

        temp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        )

        audio_file = temp.name
        temp.close()

        # -------------------------------------------------
        # Extract audio
        # -------------------------------------------------

        extract_audio(
            video_path,
            audio_file,
        )

        if not os.path.exists(audio_file):
            raise RuntimeError(
                "FFmpeg did not create the audio file."
            )

        # -------------------------------------------------
        # Load audio
        # -------------------------------------------------

        y, sr = librosa.load(
            audio_file,
            sr=16000,
            mono=True,
        )

        if y is None or len(y) == 0:
            return _unavailable_result(
                "No usable audio was detected."
            )

        y = np.asarray(y, dtype=np.float32)

        # Remove NaN / infinity safely
        y = np.nan_to_num(
            y,
            nan=0.0,
            posinf=0.0,
            neginf=0.0,
        )

        duration = len(y) / float(sr)

        if duration <= 0:
            return _unavailable_result(
                "Audio duration could not be measured."
            )

        # -------------------------------------------------
        # Remove DC offset
        # -------------------------------------------------

        y = y - np.mean(y)

        # -------------------------------------------------
        # RMS ENERGY
        # -------------------------------------------------

        rms = librosa.feature.rms(
            y=y,
            frame_length=2048,
            hop_length=512,
        )[0]

        rms = np.nan_to_num(
            rms,
            nan=0.0,
            posinf=0.0,
            neginf=0.0,
        )

        # Only non-silent frames should influence
        # vocal-energy estimation.

        non_silent_rms = rms[rms > 0.003]

        if len(non_silent_rms) == 0:
            return _unavailable_result(
                "No clear spoken audio was detected."
            )

        median_rms = float(
            np.median(non_silent_rms)
        )

        # -------------------------------------------------
        # ROBUST VOICE ENERGY NORMALIZATION
        #
        # RMS is typically much smaller than 1.
        # Convert to a dB-like scale instead of using
        # energy * 1800, which is highly recording-dependent.
        # -------------------------------------------------

        db = 20.0 * np.log10(
            max(median_rms, 1e-6)
        )

        # Typical speech recordings roughly occupy
        # this practical range.
        #
        # -45 dB -> 0
        # -15 dB -> 100

        voice_energy = (
            (db + 45.0)
            / 30.0
        ) * 100.0

        voice_energy = int(
            np.clip(
                voice_energy,
                0,
                100,
            )
        )

        # -------------------------------------------------
        # SPEECH / SILENCE DETECTION
        # -------------------------------------------------

        intervals = librosa.effects.split(
            y,
            top_db=30,
        )

        active_duration = 0.0

        for start, end in intervals:

            active_duration += (
                end - start
            ) / float(sr)

        active_duration = float(
            np.clip(
                active_duration,
                0,
                duration,
            )
        )

        pause_ratio = (
            duration - active_duration
        ) / duration

        pause_ratio = float(
            np.clip(
                pause_ratio,
                0,
                1,
            )
        )

        # -------------------------------------------------
        # PAUSE SCORE
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
                100,
            )
        )

        # -------------------------------------------------
        # SPEECH RATE
        #
        # Actual WPM comes from transcription.
        # Do not invent it here.
        # -------------------------------------------------

        speech_rate = None

        pace_feedback = (
            "Your vocal pacing is evaluated using "
            "transcription timing."
        )

        return {
            "voice_energy": voice_energy,
            "pause_score": pause_score,
            "voice_confidence": voice_confidence,
            "duration": round(duration, 1),
            "speech_rate": speech_rate,
            "pace_feedback": pace_feedback,
            "voice_analysis_available": True,
        }

    except Exception as e:

        print(
            "VOICE ANALYSIS ERROR:",
            repr(e),
        )

        return _unavailable_result(
            "Voice analysis unavailable."
        )

    finally:

        if (
            audio_file
            and os.path.exists(audio_file)
        ):

            try:
                os.remove(audio_file)
            except Exception:
                pass