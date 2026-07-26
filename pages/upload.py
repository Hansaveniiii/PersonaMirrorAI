import streamlit as st
import os

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

        if st.button("📤 Save Video", use_container_width=True):

            st.success("✅ Video saved successfully!")

            st.info("➡️ Open the **Analysis** page from the sidebar to start AI analysis.")