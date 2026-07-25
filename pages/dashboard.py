import streamlit as st
from modules.analysis_manager import load_results


def show():

    result = load_results()

    st.title("📊 PersonaMirror AI Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("😀 Faces", result["faces"])
    col2.metric("🎥 Frames", result["frames"])
    col3.metric("⭐ Confidence", f'{result["confidence"]}%')

    st.divider()

    st.subheader("AI Communication Scores")

    st.write("Confidence")
    st.progress(result["confidence"])

    st.write("Eye Contact")
    st.progress(result["eye_contact"])

    st.write("Speech")
    st.progress(result["speech"])

    st.write("Leadership")
    st.progress(result["leadership"])

    st.divider()

    st.success(f'😊 Dominant Emotion: {result["emotion"]}')

    st.subheader("AI Suggestions")

    if result["confidence"] >= 80:
        st.success("Excellent confidence level.")
    else:
        st.warning("Practice speaking with more confidence.")

    if result["eye_contact"] >= 80:
        st.success("Eye contact is good.")
    else:
        st.warning("Try maintaining eye contact with the audience.")

    if result["speech"] >= 80:
        st.success("Speech clarity is good.")
    else:
        st.warning("Speak more clearly and slightly slower.")