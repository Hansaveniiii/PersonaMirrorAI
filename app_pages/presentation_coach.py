import streamlit as st

def show():

    st.title("🎓 AI Presentation Coach")

    st.markdown(
        """
Practice presentations, seminars, speeches and classroom talks.

Upload a presentation video and receive AI feedback on:

- 🎤 Speaking Confidence
- 👀 Eye Contact
- 😊 Facial Expressions
- 🗣 Voice Clarity
- 📖 Speech Content
- 💡 Professionalism
- 📊 Overall Presentation Score
"""
    )

    st.divider()

    uploaded_video = st.file_uploader(
        "Upload Presentation Video",
        type=["mp4", "mov", "avi"]
    )

    if uploaded_video:

        st.success("✅ Presentation uploaded successfully.")

        st.video(uploaded_video)

        st.info(
            "🚀 AI analysis will be added in the next step."
        )

    else:

        st.warning(
            "Please upload a presentation video."
        )