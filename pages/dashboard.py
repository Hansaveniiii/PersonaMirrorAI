import streamlit as st
from modules.analysis_manager import load_results


def show():

    result = load_results()

    st.title("📊 PersonaMirror AI Dashboard")
    st.caption("AI-Powered Communication Performance Dashboard")

    # ---------------- Overall Score ----------------

    overall_score = int(
        (
            result["confidence"]
            + result["leadership"]
            + result["eye_contact"]
            + min(result["speech"], 100)
        ) / 4
    )

    st.metric("🏆 Overall AI Score", f"{overall_score}/100")

    st.divider()

    # ---------------- Top Metrics ----------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("⭐ Confidence", f"{result['confidence']}%")

    with col2:
        st.metric("👑 Leadership", f"{result['leadership']}%")

    with col3:
        st.metric("😊 Emotion", result["emotion"])

    st.divider()

    # ---------------- Communication Scores ----------------

    st.subheader("📈 Communication Scores")

    st.write("⭐ Confidence")
    st.progress(result["confidence"] / 100)

    st.write(f"{result['confidence']}%")

    st.write("👀 Eye Contact")
    st.progress(result["eye_contact"] / 100)

    st.write(f"{result['eye_contact']}%")

    speech_score = min(result["speech"], 100)

    st.write("🎤 Speech")

    st.progress(speech_score / 100)

    st.write(f"{result['speech']} WPM")

    st.write("👑 Leadership")

    st.progress(result["leadership"] / 100)

    st.write(f"{result['leadership']}%")

    st.write("👁 Face Visibility")

    st.progress(result["visibility"] / 100)

    st.write(f"{result['visibility']}%")

    st.divider()

    # ---------------- Video Statistics ----------------

    st.subheader("🎥 Video Statistics")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Frames", result["frames"])

    with c2:
        st.metric("Maximum Faces", result["faces"])

    with c3:
        st.metric("Average Faces", result["average_faces"])

    st.divider()

    # ---------------- Communication Summary ----------------

    st.subheader("🧠 AI Communication Summary")

    if overall_score >= 85:
        st.success("Outstanding communication performance.")
    elif overall_score >= 70:
        st.info("Good communication with room for improvement.")
    else:
        st.warning("Practice is recommended to improve communication skills.")

    st.divider()

    # ---------------- Personalized Suggestions ----------------

    st.subheader("💡 Personalized Suggestions")

    if result["confidence"] < 80:
        st.warning("Increase confidence by practicing mock presentations.")

    if result["eye_contact"] < 70:
        st.warning("Maintain eye contact with the camera while speaking.")

    if result["speech"] > 170:
        st.warning("Your speaking speed is too fast. Slow down slightly.")

    elif result["speech"] < 110:
        st.warning("Speak a little faster to improve engagement.")

    else:
        st.success("Your speaking speed is well balanced.")

    if result["visibility"] < 90:
        st.warning("Keep your face centered and visible throughout the recording.")

    if result["leadership"] >= 80:
        st.success("Excellent leadership presence detected.")

    st.divider()

    st.success("🚀 More advanced AI analytics and charts are coming soon.")