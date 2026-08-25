import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import tempfile
import cv2


class VideoProcessor:

    def __init__(self):

        self.frames = []


    def recv(self, frame):

        img = frame.to_ndarray(
            format="bgr24"
        )

        self.frames.append(img)

        return frame



def record_video():

    st.write(
        "📷 Camera Interview Recording"
    )


    ctx = webrtc_streamer(
        key="interview_camera",
        video_processor_factory=VideoProcessor,
        media_stream_constraints={
            "video": True,
            "audio": True
        }
    )


    if ctx.video_processor:

        return ctx.video_processor.frames


    return None