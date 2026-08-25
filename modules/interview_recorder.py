import streamlit as st
from streamlit_webrtc import (
    webrtc_streamer,
    WebRtcMode,
    VideoProcessorBase,
)
import av
import tempfile
import os


class VideoProcessor(VideoProcessorBase):

    def __init__(self):
        self.frames = []


    def recv(self, frame):

        img = frame.to_ndarray(
            format="bgr24"
        )

        self.frames.append(img)

        return frame



def record_interview():

    st.subheader("🎥 Record Your Answer")


    ctx = webrtc_streamer(
        key="interview-recording",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=VideoProcessor,
        media_stream_constraints={
            "video": True,
            "audio": True,
        },
    )


    if ctx.state.playing:

        st.success(
            "🔴 Recording in progress..."
        )


    if ctx.video_processor:

        st.write(
            "Frames captured:",
            len(ctx.video_processor.frames)
        )


    if st.button(
        "⏹ Finish Recording"
    ):

        if ctx.video_processor is None:

            st.error(
                "Processor not initialized. Refresh page and allow camera."
            )

            return None


        frames = ctx.video_processor.frames


        if len(frames) == 0:

            st.error(
                "Camera opened but no frames captured."
            )

            return None



        save_path = os.path.join(
            tempfile.gettempdir(),
            "interview_answer.mp4"
        )


        height, width, _ = frames[0].shape


        container = av.open(
            save_path,
            "w"
        )


        stream = container.add_stream(
            "libx264",
            rate=20
        )


        stream.width = width
        stream.height = height
        stream.pix_fmt = "yuv420p"


        for img in frames:

            frame = av.VideoFrame.from_ndarray(
                img,
                format="bgr24"
            )

            for packet in stream.encode(frame):

                container.mux(packet)


        for packet in stream.encode():

            container.mux(packet)


        container.close()


        st.success(
            "✅ Saved: " + save_path
        )


        st.video(save_path)


        return save_path


    return None