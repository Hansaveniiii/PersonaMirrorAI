from faster_whisper import WhisperModel
import re


# =========================================================
# PERSONAMIRROR AI
# SPEECH TO TEXT ENGINE
# =========================================================

try:

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )

    print("✅ Faster Whisper small model loaded")

except Exception as e:

    print(
        "❌ Faster Whisper loading error:",
        e
    )

    model = None


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# SEGMENT QUALITY
# =========================================================

def calculate_segment_confidence(segment):

    avg_logprob = getattr(
        segment,
        "avg_logprob",
        None
    )

    compression_ratio = getattr(
        segment,
        "compression_ratio",
        None
    )

    no_speech_probability = getattr(
        segment,
        "no_speech_prob",
        None
    )


    # -----------------------------------------------------
    # Missing probability information
    # -----------------------------------------------------

    if avg_logprob is None:

        return 50


    try:

        avg_logprob = float(
            avg_logprob
        )

    except (
        TypeError,
        ValueError
    ):

        return 50


    # -----------------------------------------------------
    # Log probability
    #
    # More negative = generally less reliable.
    #
    # This is an ESTIMATE, not actual word accuracy.
    # -----------------------------------------------------

    # Typical useful range:
    #
    # -1.5  → poor
    # -1.0  → weak
    # -0.5  → reasonable
    # -0.2  → strong
    #  0.0  → very strong
    #

    confidence = (
        (avg_logprob + 1.5)
        / 1.5
    ) * 100


    confidence = max(
        0,
        min(
            100,
            confidence
        )
    )


    # -----------------------------------------------------
    # Compression ratio
    #
    # Extremely high compression can indicate
    # repetition/hallucination.
    # -----------------------------------------------------

    if compression_ratio is not None:

        try:

            compression_ratio = float(
                compression_ratio
            )

            if compression_ratio > 2.8:

                confidence -= 20

            elif compression_ratio > 2.4:

                confidence -= 10

        except (
            TypeError,
            ValueError
        ):

            pass


    # -----------------------------------------------------
    # NO-SPEECH probability
    #
    # IMPORTANT:
    #
    # We DO NOT directly subtract this from confidence.
    #
    # Whisper's no_speech_prob is not a word-accuracy
    # measurement.
    #
    # It is only used as a secondary signal.
    # -----------------------------------------------------

    if no_speech_probability is not None:

        try:

            no_speech_probability = float(
                no_speech_probability
            )

            # Only flag extremely suspicious
            # combinations.

            if (
                no_speech_probability > 0.90
                and avg_logprob < -0.8
            ):

                confidence -= 15

        except (
            TypeError,
            ValueError
        ):

            pass


    return round(
        max(
            0,
            min(
                100,
                confidence
            )
        ),
        1
    )


# =========================================================
# SEGMENT CLASSIFICATION
# =========================================================

def classify_segment(confidence):

    if confidence >= 75:

        return "high"

    elif confidence >= 55:

        return "review"

    else:

        return "low"


# =========================================================
# TRANSCRIBE VIDEO
# =========================================================

def transcribe_video(video_path):

    if model is None:

        return {

            "transcript": "",

            "word_count": 0,

            "speech": 0,

            "duration": 0,

            "transcription_available": False,

            "transcription_confidence": None,

            "segments": [],

            "high_confidence_segments": 0,

            "review_segments": 0,

            "low_confidence_segments": 0
        }


    try:

        # =================================================
        # WHISPER
        # =================================================

        segments, info = model.transcribe(

            video_path,

            language="en",

            beam_size=5,

            best_of=5,

            temperature=0,

            condition_on_previous_text=False,

            vad_filter=True,

            vad_parameters={

                "min_silence_duration_ms": 500,

                "speech_pad_ms": 200
            },

            word_timestamps=True,

            no_speech_threshold=0.6,

            log_prob_threshold=-1.0,

            compression_ratio_threshold=2.4
        )


        # =================================================
        # PROCESS SEGMENTS
        # =================================================

        transcript_parts = []

        processed_segments = []

        confidence_values = []


        high_count = 0

        review_count = 0

        low_count = 0


        total_duration = 0


        for segment in segments:

            text = clean_text(
                segment.text
            )

            if not text:
                continue


            start = float(
                segment.start
            )

            end = float(
                segment.end
            )

            duration = max(
                0,
                end - start
            )


            total_duration = max(
                total_duration,
                end
            )


            confidence = calculate_segment_confidence(
                segment
            )


            category = classify_segment(
                confidence
            )


            if category == "high":

                high_count += 1

            elif category == "review":

                review_count += 1

            else:

                low_count += 1


            confidence_values.append(
                confidence
            )


            transcript_parts.append(
                text
            )


            processed_segments.append({

                "text": text,

                "start": round(
                    start,
                    2
                ),

                "end": round(
                    end,
                    2
                ),

                "duration": round(
                    duration,
                    2
                ),

                "confidence": confidence,

                "category": category,

                "avg_logprob":
                    getattr(
                        segment,
                        "avg_logprob",
                        None
                    ),

                "no_speech_probability":
                    getattr(
                        segment,
                        "no_speech_prob",
                        None
                    ),

                "compression_ratio":
                    getattr(
                        segment,
                        "compression_ratio",
                        None
                    )
            })


        # =================================================
        # FINAL TRANSCRIPT
        # =================================================

        transcript = clean_text(
            " ".join(
                transcript_parts
            )
        )


        # =================================================
        # EMPTY RESULT
        # =================================================

        if not transcript:

            return {

                "transcript": "",

                "word_count": 0,

                "speech": 0,

                "duration": round(
                    total_duration,
                    2
                ),

                "transcription_available": False,

                "transcription_confidence": None,

                "segments": [],

                "high_confidence_segments": 0,

                "review_segments": 0,

                "low_confidence_segments": 0
            }


        # =================================================
        # WORD COUNT
        # =================================================

        word_count = len(
            transcript.split()
        )


        # =================================================
        # SPEAKING RATE
        # =================================================

        if total_duration > 0:

            speech_rate = round(
                (
                    word_count
                    /
                    total_duration
                )
                * 60
            )

        else:

            speech_rate = 0


        # =================================================
        # OVERALL TRANSCRIPTION CONFIDENCE
        # =================================================

        if confidence_values:

            overall_confidence = round(
                sum(confidence_values)
                /
                len(confidence_values)
            )

        else:

            overall_confidence = None


        # =================================================
        # RETURN RESULT
        # =================================================

        return {

            "transcript": transcript,

            "word_count": word_count,

            "speech": speech_rate,

            "duration": round(
                total_duration,
                2
            ),

            "transcription_available": True,

            "transcription_confidence":
                overall_confidence,

            "segments":
                processed_segments,

            "high_confidence_segments":
                high_count,

            "review_segments":
                review_count,

            "low_confidence_segments":
                low_count
        }


    except Exception as e:

        print(
            "❌ Transcription error:",
            e
        )

        return {

            "transcript": "",

            "word_count": 0,

            "speech": 0,

            "duration": 0,

            "transcription_available": False,

            "transcription_confidence": None,

            "segments": [],

            "high_confidence_segments": 0,

            "review_segments": 0,

            "low_confidence_segments": 0
        }