
import librosa
import numpy as np


def analyze_interview_voice(audio_path, transcript):

    try:

        audio, sr = librosa.load(
            audio_path,
            sr=None
        )


        duration = librosa.get_duration(
            y=audio,
            sr=sr
        )


        words = len(
            transcript.split()
        )


        if duration > 0:

            speaking_speed = int(
                (words / duration) * 60
            )

        else:

            speaking_speed = 0



        # Voice energy

        energy = np.mean(
            librosa.feature.rms(
                y=audio
            )
        )


        energy_score = min(
            int(energy * 1000),
            100
        )



        # Speaking speed feedback

        if speaking_speed < 100:

            pace = "Slow speaking pace"

        elif speaking_speed > 170:

            pace = "Very fast speaking pace"

        else:

            pace = "Good speaking pace"



        return {

            "duration": round(duration,2),

            "speech_rate": speaking_speed,

            "voice_energy": energy_score,

            "pace_feedback": pace

        }


    except Exception as e:

        return {

            "error": str(e)

        }