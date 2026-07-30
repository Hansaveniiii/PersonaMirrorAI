import os
import time
from unittest import result
import streamlit as st

from modules.analyzer import analyze_video
from modules.analysis_manager import save_results
from modules.ai_coach import generate_ai_feedback
from modules.ai_engine import (
    calculate_confidence,
    calculate_leadership,
    calculate_interview_score,
    calculate_presentation_score,
    calculate_executive_presence,
)
from modules.voice_analysis import analyze_voice
from modules.emotion_analysis import analyze_emotion
from modules.speech_to_text import transcribe_video
from modules.speech import analyze_speech

UPLOAD_FOLDER = "uploads"


def show():

    st.title("🎥 Upload Video")

    st.markdown("""
Upload your **self-introduction, interview, presentation, debate, or speech**.

PersonaMirror AI will analyze your communication performance using Artificial Intelligence.
""")

    uploaded_file = st.file_uploader(
        "Choose a video",
        type=["mp4", "mov", "avi", "mkv"]
    )

    if uploaded_file:

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        file_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ Video uploaded successfully")

        st.video(file_path)

        size = uploaded_file.size / (1024 * 1024)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("📁 File Name", uploaded_file.name)

        with col2:
            st.metric("💾 Size", f"{size:.2f} MB")

        if st.button("🚀 Analyze Video", use_container_width=True):

            status = st.empty()
            progress = st.progress(0)

            # Step 1
            status.info("🎥 Loading video...")
            time.sleep(0.5)
            progress.progress(10)

            # Step 2
            status.info("😀 Detecting faces...")
            result = analyze_video(file_path)
            time.sleep(0.5)
            progress.progress(30)

            # Step 3
            status.info("🗣️ Analyzing speech...")
            speech = analyze_speech(file_path)
            result.update(speech)
            time.sleep(0.5)
            progress.progress(45)

            # Step 4
            status.info("🎤 Transcribing speech...")
            transcript = transcribe_video(file_path)
            result.update(transcript)
            time.sleep(0.5)
            progress.progress(60)

            # Step 5
            status.info("🔊 Analyzing voice...")
            voice = analyze_voice(file_path)
            result.update(voice)
            time.sleep(0.5)
            progress.progress(75)

            # Step 6
            status.info("😊 Detecting emotion...")
            result["emotion"] = analyze_emotion(file_path)
            time.sleep(0.5)
            progress.progress(85)

            # Step 7
            status.info("🧠 Calculating AI Scores...")
            result["confidence"] = calculate_confidence(result)

            result["leadership"] = calculate_leadership(result)

            result["interview_score"] = calculate_interview_score(result)

            result["presentation_score"] = calculate_presentation_score(result)

            result["executive_presence"] = calculate_executive_presence(result)
            time.sleep(0.5)
            progress.progress(92)

            # Step 8
            status.info("🤖 Generating AI Feedback...")
            feedback = generate_ai_feedback(result)
            result["feedback"] = feedback
            time.sleep(0.5)

            save_results(result)

            progress.progress(100)
            status.success("✅ Analysis Complete!")

            time.sleep(1)

            progress.empty()
            status.empty()

            st.success("🎉 Analysis Completed Successfully!")

            st.balloons()

            st.subheader("📊 Quick Preview")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("⭐ Confidence", f"{result['confidence']}%")

            with c2:
                st.metric("👑 Leadership", f"{result['leadership']}%")

            with c3:
                st.metric("👀 Eye Contact", f"{result['eye_contact']}%")

            st.info("Open Dashboard to view complete communication analysis.")