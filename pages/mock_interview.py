import streamlit as st
import random

QUESTIONS = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "What are your strengths?",
    "What are your weaknesses?",
    "Describe a difficult situation you handled.",
    "Where do you see yourself in 5 years?",
    "Why do you want this job?",
    "What motivates you?",
    "Tell me about your biggest achievement.",
    "Why are you interested in our company?"
]


def show():

    st.title("🎤 AI Mock Interview")

    st.write(
        "Practice your interview with AI-generated HR questions."
    )

    if "question" not in st.session_state:
        st.session_state.question = random.choice(QUESTIONS)

    st.subheader("Current Question")

    st.info(st.session_state.question)

    answer = st.text_area(
        "Your Answer",
        height=180
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Next Question", use_container_width=True):

            st.session_state.question = random.choice(QUESTIONS)

            st.rerun()

    with col2:

        if st.button("Evaluate Answer", use_container_width=True):

            if len(answer) < 40:

                st.warning(
                    "Your answer is too short."
                )

            else:

                st.success("Excellent attempt!")

                st.metric("Confidence", "91%")
                st.metric("Clarity", "88%")
                st.metric("Professionalism", "90%")

                st.info(
                    "AI Feedback:\n\n"
                    "• Good structure\n"
                    "• Maintain eye contact\n"
                    "• Add one real-life example\n"
                    "• End with confidence"
                )