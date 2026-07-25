import os
import streamlit as st

UPLOAD_FOLDER = "uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def upload_video():
    st.header("🎥 Upload Your Self-Introduction Video")

    uploaded_file = st.file_uploader(
        "Choose a video",
        type=["mp4", "mov", "avi"]
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

        st.subheader("Video Details")

        st.write(f"**File Name:** {uploaded_file.name}")

        st.write(f"**File Size:** {round(uploaded_file.size/1024,2)} KB")

        st.write(f"**File Type:** {uploaded_file.type}")