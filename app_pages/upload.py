import os
from unittest import result
import streamlit as st

from modules.analysis_pipeline import analyze_complete_video
from modules.analysis_manager import (
    save_results,
    clear_results,
)

UPLOAD_FOLDER = "uploads"


def show():

    st.title("🎥 Upload & Analyze")

    st.write(
        "Upload a speech, presentation, interview, debate or communication video "
        "and let PersonaMirror AI understand your performance."
    )

    st.markdown("### 🎯 What are you uploading?")

    analysis_type = st.selectbox(
        "Choose analysis type",
        [
            "🎤 Speech / Presentation",
            "💼 Mock Interview",
            "🗣️ General Communication",
            "🎙️ Debate / Public Speaking"
        ]
    )

    uploaded_file = st.file_uploader(
        "Choose your video",
        type=["mp4", "mov", "avi", "mkv"],
        key="video_uploader"
    )

    # ---------------------------------------------------------
    # NOTHING UPLOADED
    # ---------------------------------------------------------

    if uploaded_file is None:
        return

    # ---------------------------------------------------------
    # IDENTIFY THIS UPLOAD
    # ---------------------------------------------------------

    upload_key = (
        f"{uploaded_file.name}_"
        f"{uploaded_file.size}"
    )

    previous_upload = st.session_state.get(
        "current_upload_key"
    )

    # ---------------------------------------------------------
    # NEW VIDEO = NEW SESSION
    # ---------------------------------------------------------

    if previous_upload != upload_key:

        # Remove previous analysis
        clear_results()

        # Previous analysis is no longer ready
        st.session_state["analysis_ready"] = False

        # Remember this upload
        st.session_state["current_upload_key"] = upload_key

    # ---------------------------------------------------------
    # SAVE VIDEO
    # ---------------------------------------------------------

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    video_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.name
    )

    with open(
        video_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    st.success(
        "✅ Video uploaded successfully"
    )

    st.video(video_path)

    st.markdown(
        f"### Selected Mode: {analysis_type}"
    )

    # ---------------------------------------------------------
    # ANALYZE
    # ---------------------------------------------------------

    if st.button(
        "🚀 Analyze My Performance",
        use_container_width=True
    ):

        progress = st.progress(0)

        status = st.empty()

        status.info(
            "🤖 Preparing PersonaMirror AI..."
        )

        progress.progress(10)

        try:

            # -------------------------------------------------
            # IMPORTANT:
            # Do NOT show the old result.
            # Analyze THIS uploaded video.
            # -------------------------------------------------

            result = analyze_complete_video(
                video_path,
                analysis_type
            )

            # =================================================
            # VERIFIED SPEAKING SPEED
            # =================================================
            # Use measured speech rate when available.
            # Otherwise derive WPM from transcript words and
            # measured duration already produced by the pipeline.
            speech_rate = result.get("speech_rate")

            if speech_rate is None:
                speech_rate = result.get("speech")

            if speech_rate is None:
                try:
                    words = result.get(
                        "transcript_word_count",
                        result.get("word_count")
                    )
                    duration = result.get("duration")

                    if (
                        words is not None
                        and duration is not None
                        and float(words) > 0
                        and float(duration) > 0
                    ):
                        speech_rate = round(
                            float(words) /
                            (float(duration) / 60.0),
                            1
                        )
                except (
                    TypeError,
                    ValueError,
                    ZeroDivisionError
                ):
                    speech_rate = None

            if speech_rate is not None:
                result["speech_rate"] = speech_rate
            st.session_state["current_analysis"] = result

            progress.progress(85)

            # Store analysis mode
            result["analysis_type"] = analysis_type

            # Mark analysis as ready
            result["analysis_ready"] = True

            status.info(
                "🧠 Generating personalized insights..."
            )

            # Save ONLY this latest analysis
            save_results(result)

            # Store THIS latest analysis in the current session
            st.session_state["current_analysis"] = result

            # Store readiness in current browser session
            st.session_state["analysis_ready"] = True

            st.balloons()

            # -------------------------------------------------
            # QUICK SNAPSHOT
            # -------------------------------------------------

            st.markdown(
                "## 📊 Quick Performance Snapshot"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                confidence = result.get(
                    "confidence"
                )

                st.metric(
                    "Confidence",
                    (
                        f"{confidence}%"
                        if confidence is not None
                        else "Not measured"
                    )
                )

            with c2:

                leadership = result.get(
                    "leadership"
                )

                st.metric( 
                    "Leadership",
                    (
                        f"{leadership}%"
                        if leadership is not None
                        else "Not measured"
                    )
                )

            with c3:

                eye_contact = result.get("eye_contact")

                st.metric(
                    "Eye Contact",
                    (
                        f"{eye_contact}%"
                        if eye_contact is not None
                        else "Not measured"
                    )
                )

            # -------------------------------------------------
            # SPEAKING SPEED
            # -------------------------------------------------

            if speech_rate is not None:
                st.metric(
                    "🗣 Speaking Speed",
                    f"{float(speech_rate):.1f} WPM"
                )
            else:
                st.metric(
                    "🗣 Speaking Speed",
                    "Not measured"
                )

            st.success(
                "Your personalized analysis is ready. "
                "Open Analysis, Dashboard or Report."
            )

        except Exception as e:

            progress.empty()

            # Analysis failed = no valid result
            st.session_state["analysis_ready"] = False

            clear_results()

            st.error(
                "❌ Analysis could not be completed."
            )

            st.exception(e)
