import os
import streamlit as st

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def upload_video():

    st.markdown(
        """
        <h1 style='text-align:center;'>
        🎥 Upload Your Communication Video
        </h1>

        <p style='text-align:center;font-size:18px;color:gray;'>
        Upload your Interview, Presentation, Debate,
        Public Speaking or Self-Introduction video.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.info(
        """
💡 **Tips for Best AI Analysis**

• Face the camera directly

• Keep good lighting

• Speak clearly

• Maintain eye contact

• Keep your full upper body visible
"""
    )

    uploaded_file = st.file_uploader(
        "Choose your video",
        type=["mp4", "mov", "avi", "mkv"],
        help="Supported formats: MP4, MOV, AVI, MKV"
    )

    if uploaded_file is not None:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ Video uploaded successfully!")

        st.video(file_path)

        st.divider()

        st.subheader("📁 Video Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Filename",
                uploaded_file.name
            )

        with col2:
            st.metric(
                "Size",
                f"{uploaded_file.size / (1024*1024):.2f} MB"
            )

        with col3:
            st.metric(
                "Format",
                uploaded_file.type
            )

        st.divider()

        st.subheader("🤖 AI Analysis Modules")

        c1, c2 = st.columns(2)

        with c1:

            st.success("😀 Emotion Detection")

            st.success("👁 Eye Contact")

            st.success("🎤 Voice Analysis")

            st.success("😊 Smile Detection")

        with c2:

            st.success("🧍 Posture Analysis")

            st.success("✋ Gesture Detection")

            st.success("🗣 Speech Analysis")

            st.success("📄 AI Report Generation")

        st.divider()

        st.warning(
            "Click **🚀 Analyze Video** from the Upload page to start the complete AI analysis."
        )