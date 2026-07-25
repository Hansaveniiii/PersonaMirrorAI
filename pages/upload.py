import streamlit as st
import os
from modules.face_detection import detect_faces
from modules.analysis_manager import save_results
from modules.ai_engine import calculate_confidence
from modules.emotion import detect_emotion


UPLOAD_FOLDER = "uploads"


def show():

    st.title("🎥 Upload Video")

    st.markdown("""
Upload your **self-introduction, interview, presentation, debate, or speech**.

PersonaMirror AI will analyze your communication skills using Artificial Intelligence.
""")

    uploaded_file = st.file_uploader(
        "Choose a video",
        type=["mp4", "mov", "avi", "mkv"]
    )

    if uploaded_file is not None:

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ Video uploaded successfully!")

        st.video(file_path)

        size = uploaded_file.size / (1024 * 1024)

        st.subheader("📄 Video Details")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Filename", uploaded_file.name)

        with col2:
            st.metric("Size (MB)", f"{size:.2f}")

        if st.button("🚀 Analyze Video", use_container_width=True):

            with st.spinner("🤖 PersonaMirror AI is analyzing your video..."):

                result = detect_faces(file_path)

                
                result["confidence"] = calculate_confidence(result)
                result["emotion"] = detect_emotion(result)
                result["eye_contact"] = 0
                result["speech"] = 80
                result["leadership"] = 85

                save_results(result)

            st.success("✅ Analysis Complete!")

            col3, col4 = st.columns(2)

            with col3:
                st.metric("🎞 Total Frames", result["frames"])

            
            with col4:
                st.metric("👥 Maximum Faces", result["faces"])
                st.metric("📈 Average Faces", result["average_faces"])
                st.metric("👁 Face Visibility", f"{result['visibility']}%")
            st.subheader("📊 AI Communication Analysis")

            col5, col6 = st.columns(2)

            with col5:
                st.metric("👀 Eye Contact", f"{result['eye_contact']}%")

            with col6:
                st.metric("⭐ Confidence", f"{result['confidence']}%")

            col7, col8 = st.columns(2)

            with col7:
                st.metric("🎤 Speech Score", f"{result['speech']}%")

            with col8:
                st.metric("👑 Leadership", f"{result['leadership']}%")

            st.success(f"😊 Detected Emotion: {result['emotion']}")

            st.info(
                "🚀 More AI features like real Emotion Detection, Speech Analysis, Voice Tone and AI Report are coming soon."
            )