import os

import pandas as pd
import plotly.express as px
import streamlit as st

from modules.interview_report import generate_interview_report
from modules.question_engine import get_questions
from modules.recruiter_ai import recruiter_decision
from modules.recruiter_notes import generate_recruiter_notes

from modules.math_engine import (
    weighted_score,
    interview_readiness,
    confidence_label,
    recommendation,
)


def show():

    st.title("🎤 AI Mock Interview")

    st.markdown(
        """
        Answer the interview questions naturally.

        PersonaMirror AI will evaluate:
        - 🎯 Whether your answer matches the question
        - 🧠 Answer quality
        - 🎤 Voice
        - 👀 Visual presentation
        - 📊 Overall interview performance
        """
    )

    # -------------------------------------------------
    # SESSION STATE
    # -------------------------------------------------

    if "question" not in st.session_state:
        st.session_state.question = 0

    if "history" not in st.session_state:
        st.session_state.history = []

    if "questions" not in st.session_state:

        role = st.session_state.get(
            "selected_role",
            "HR Interview"
        )

        st.session_state.questions = get_questions(role)

    # -------------------------------------------------
    # CHECK QUESTIONS
    # -------------------------------------------------

    if not st.session_state.questions:

        st.error(
            "No interview questions were found."
        )

        return

    # -------------------------------------------------
    # INTERVIEW COMPLETED
    # -------------------------------------------------

    if st.session_state.question >= len(
        st.session_state.questions
    ):

        st.success(
            "✅ Interview Completed"
        )

        st.balloons()

        st.markdown(
            """
            ## 🎉 Congratulations!

            Your interview has been completed.

            PersonaMirror AI has analysed your interview
            performance, answer relevance, communication,
            confidence and presentation.
            """
        )

        if st.session_state.history:

            st.subheader(
                "📊 Interview Summary"
            )

            history_df = pd.DataFrame(
                st.session_state.history
            )

            if "score" in history_df.columns:

                average_score = int(
                    history_df["score"].mean()
                )

                st.metric(
                    "Average Interview Score",
                    f"{average_score}/100"
                )

            if "relevance_score" in history_df.columns:

                average_relevance = int(
                    history_df["relevance_score"].mean()
                )

                st.metric(
                    "Average Answer Relevance",
                    f"{average_relevance}%"
                )

        st.divider()

        if st.button(
            "🏠 Back to Interview Selection",
            use_container_width=True
        ):

            st.session_state.start_interview = False
            st.session_state.question = 0

            if "questions" in st.session_state:
                del st.session_state["questions"]

            if "history" in st.session_state:
                del st.session_state["history"]

            st.rerun()

        return

    # -------------------------------------------------
    # CURRENT QUESTION
    # -------------------------------------------------

    current_question = st.session_state.questions[
        st.session_state.question
    ]

    question_number = (
        st.session_state.question + 1
    )

    total_questions = len(
        st.session_state.questions
    )

    st.progress(
        question_number / total_questions
    )

    st.subheader(
        f"Question {question_number} of {total_questions}"
    )

    st.info(
        current_question
    )

    # -------------------------------------------------
    # RECORD / UPLOAD
    # -------------------------------------------------

    st.markdown(
        "### 📹 Record Your Answer"
    )

    st.write(
        """
        Record your answer using your phone or laptop
        camera and upload the video below.
        """
    )

    st.info(
        """
        Supported formats:

        • MP4
        • MOV
        • AVI
        """
    )

    uploaded_video = st.file_uploader(
        "Upload Your Recorded Interview",
        type=[
            "mp4",
            "mov",
            "avi"
        ]
    )

    if uploaded_video is None:

        st.info(
            "Upload your answer video to begin AI analysis."
        )

        return

    # -------------------------------------------------
    # SAVE VIDEO
    # -------------------------------------------------

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    video_path = os.path.join(
        "uploads",
        uploaded_video.name
    )

    with open(
        video_path,
        "wb"
    ) as file:

        file.write(
            uploaded_video.getbuffer()
        )

    st.success(
        "✅ Video Uploaded Successfully"
    )

    st.video(
        video_path
    )

    # -------------------------------------------------
    # ANALYSIS
    # -------------------------------------------------

    with st.spinner(
        "🤖 PersonaMirror AI is analysing your answer..."
    ):

        try:

            report = generate_interview_report(
                current_question,
                video_path
            )

        except Exception as e:

            st.error(
                "Interview analysis failed."
            )

            st.exception(e)

            return

    # -------------------------------------------------
    # GET REPORT DATA
    # -------------------------------------------------

    transcript = report.get(
        "transcript",
        ""
    )

    voice = report.get(
        "voice",
        {}
    )

    vision = report.get(
        "vision",
        {}
    )

    analysis = report.get(
        "analysis",
        {}
    )

    feedback = report.get(
        "feedback",
        ""
    )

    # -------------------------------------------------
    # IMPORTANT:
    # QUESTION RELEVANCE
    # -------------------------------------------------

    relevance_score = analysis.get(
        "relevance_score",
        0
    )

    answer_status = analysis.get(
        "answer_status",
        "Not Available"
    )

    relevant = analysis.get(
        "relevant",
        False
    )

    # -------------------------------------------------
    # DISPLAY ANSWER STATUS FIRST
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "🎯 Does Your Answer Match the Question?"
    )

    if relevance_score < 25:

        st.error(
            "❌ IRRELEVANT ANSWER"
        )

        st.metric(
            "Question Relevance",
            f"{relevance_score}%"
        )

        st.warning(
            """
            Your answer does not directly answer
            the question asked.

            The AI detected that the content appears
            to belong to a different interview question.
            """
        )

    elif relevance_score < 50:

        st.warning(
            "⚠️ PARTIALLY RELEVANT ANSWER"
        )

        st.metric(
            "Question Relevance",
            f"{relevance_score}%"
        )

        st.warning(
            """
            Your answer contains some related information,
            but it does not fully answer the question.
            """
        )

    elif relevance_score < 70:

        st.info(
            "🟡 RELEVANT BUT COULD BE STRONGER"
        )

        st.metric(
            "Question Relevance",
            f"{relevance_score}%"
        )

    else:

        st.success(
            "✅ STRONGLY RELEVANT ANSWER"
        )

        st.metric(
            "Question Relevance",
            f"{relevance_score}%"
        )

    st.caption(
        f"AI classification: {answer_status}"
    )

    # -------------------------------------------------
    # QUESTION VS ANSWER
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "🔎 Question vs Your Answer"
    )

    st.markdown(
        "**Interview Question:**"
    )

    st.info(
        current_question
    )

    st.markdown(
        "**Your Transcribed Answer:**"
    )

    if transcript:

        st.write(
            transcript
        )

    else:

        st.warning(
            "No transcript available."
        )

    # -------------------------------------------------
    # STOP GENERIC FEEDBACK FROM HIDING BAD ANSWERS
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "🧠 Answer Review"
    )

    if not relevant:

        st.error(
            """
            This answer should not be considered a
            successful response to the interview question.

            Improve the answer by directly addressing
            the question instead of using a generic
            or memorized response.
            """
        )

    else:

        st.success(
            "Your answer is relevant to the question."
        )

    # -------------------------------------------------
    # ANALYZER SUGGESTIONS
    # -------------------------------------------------

    suggestions = analysis.get(
        "suggestions",
        []
    )

    if suggestions:

        st.subheader(
            "💡 Question-Specific Suggestions"
        )

        for suggestion in suggestions:

            st.warning(
                suggestion
            )

    # -------------------------------------------------
    # COACH FEEDBACK
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "🤖 PersonaMirror AI Coach"
    )

    if feedback:

        st.markdown(
            feedback
        )

    else:

        st.info(
            "AI coaching feedback is unavailable."
        )

    # -------------------------------------------------
    # MATHEMATICAL EVALUATION
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "🧮 Mathematical Evaluation"
    )

    confidence_score = analysis.get(
        "confidence",
        0
    )

    leadership_score = analysis.get(
        "professionalism",
        0
    )

    eye_contact_score = vision.get(
        "eye_contact",
        0
    )

    voice_energy = voice.get(
        "voice_energy",
        0
    )

    body_language = vision.get(
        "engagement",
        0
    )

    fluency_score = analysis.get(
        "fluency",
        0
    )

    math_score = weighted_score(
        {
            "relevance": relevance_score,
            "answer_quality": analysis.get("score", 0),
            "confidence": confidence_score,
            "eye_contact": eye_contact_score,
            "voice": voice_energy,
            "body_language": body_language,
            "professionalism": analysis.get(
                "professionalism",
                 0
            )
        }
    )

    # If answer is irrelevant,
    # prevent the mathematical score
    # from looking artificially positive.

    if relevance_score < 25:

        math_score = min(
            math_score,
            35
        )

    elif relevance_score < 50:

        math_score = min(
            math_score,
            55
        )

    confidence = confidence_label(
        math_score
    )

    hiring = recommendation(
        math_score
    )

    readiness = interview_readiness(
        confidence_score,
        eye_contact_score,
        leadership_score
    )

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Weighted AI Score",
            f"{math_score}/100"
        )

    with m2:

        st.metric(
            "Answer Relevance",
            f"{relevance_score}%"
        )

    with m3:

        st.metric(
            "Confidence Level",
            confidence
        )

    with m4:

        st.metric(
            "Interview Readiness",
            readiness
        )

    st.metric(
        "Recruiter Recommendation",
        hiring
    )

    # -------------------------------------------------
    # VOICE ANALYSIS
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "🎤 Voice Analysis"
    )

    v1, v2, v3 = st.columns(3)

    with v1:

        st.metric(
            "Duration",
            f"{voice.get('duration', 'N/A')} sec"
        )

    with v2:

        st.metric(
            "Speech Rate",
            f"{voice.get('speech_rate', 'N/A')} WPM"
        )

    with v3:

        st.metric(
            "Voice Energy",
            f"{voice.get('voice_energy', 'N/A')}%"
        )

    st.info(
        voice.get(
            "pace_feedback",
            "Voice analysis completed."
        )
    )

    # -------------------------------------------------
    # VISION ANALYSIS
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "👀 Vision Analysis"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Eye Contact",
            f"{vision.get('eye_contact', 0)}%"
        )

    with c2:

        st.metric(
            "Face Visibility",
            f"{vision.get('face_visibility', 0)}%"
        )

    with c3:

        st.metric(
            "Engagement",
            f"{vision.get('engagement', 0)}%"
        )

    c4, c5 = st.columns(2)

    with c4:

        st.metric(
            "Face Centering",
            f"{vision.get('face_centering', 0)}%"
        )

    with c5:

        st.metric(
            "Head Stability",
            f"{vision.get('head_stability', 0)}%"
        )

    # -------------------------------------------------
    # AI SCORES
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "📊 AI Interview Scores"
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.metric(
            "Interview Score",
            f"{analysis.get('score', 0)}%"
        )

    with s2:

        st.metric(
            "Fluency",
            f"{fluency_score}%"
        )

    with s3:

        st.metric(
            "Professionalism",
            f"{analysis.get('professionalism', 0)}%"
        )

    with s4:

        st.metric(
            "Communication",
            f"{analysis.get('communication', 0)}%"
        )

    # -------------------------------------------------
    # RECRUITER DECISION
    # -------------------------------------------------

    try:

        decision = recruiter_decision(
            report
        )

    except Exception:

        decision = {
            "decision": hiring,
            "strengths": [],
            "concerns": []
        }

    try:

        notes = generate_recruiter_notes(
            report
        )

    except Exception:

        notes = []

    st.divider()

    st.subheader(
        "👔 AI Recruiter Decision"
    )

    if not relevant:

        st.error(
            "⚠️ Recruiter Warning: Answer does not match the question."
        )

    st.info(
        decision.get(
            "decision",
            hiring
        )
    )

    # -------------------------------------------------
    # RECRUITER NOTES
    # -------------------------------------------------

    st.subheader(
        "📝 Recruiter's Private Notes"
    )

    with st.expander(
        "View Internal Recruiter Notes"
    ):

        if notes:

            for note in notes:

                st.write(
                    "•",
                    note
                )

        else:

            st.write(
                "No recruiter notes available."
            )

    # -------------------------------------------------
    # STRENGTHS
    # -------------------------------------------------

    strengths = decision.get(
        "strengths",
        []
    )

    if strengths:

        st.subheader(
            "✅ Strengths"
        )

        for item in strengths:

            st.success(
                item
            )

    # -------------------------------------------------
    # CONCERNS
    # -------------------------------------------------

    concerns = decision.get(
        "concerns",
        []
    )

    if concerns:

        st.subheader(
            "⚠️ Areas to Improve"
        )

        for item in concerns:

            st.warning(
                item
            )

    # -------------------------------------------------
    # SAVE HISTORY
    # -------------------------------------------------

    current_history = {
        "question": current_question,
        "score": math_score,
        "relevance_score": relevance_score,
        "fluency": fluency_score,
        "professionalism": analysis.get(
            "professionalism",
            0
        ),
        "eye_contact": eye_contact_score
    }

    # Avoid duplicate history entries caused
    # by Streamlit reruns.

    existing_questions = [
        item.get("question")
        for item in st.session_state.history
    ]

    if current_question not in existing_questions:

        st.session_state.history.append(
            current_history
        )

    # -------------------------------------------------
    # PROGRESS GRAPH
    # -------------------------------------------------

    st.divider()

    st.subheader(
        "📈 Interview Progress"
    )

    if len(st.session_state.history) > 0:

        df = pd.DataFrame(
            st.session_state.history
        )

        if len(df) > 1:

            fig = px.line(
                df,
                x="question",
                y="score",
                markers=True,
                title="Interview Score Progress"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Complete another question to see your progress graph."
            )

    # -------------------------------------------------
    # NAVIGATION
    # -------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "➡️ Next Question",
            use_container_width=True
        ):

            st.session_state.question += 1

            st.rerun()

    with col2:

        if st.button(
            "🏠 End Interview",
            use_container_width=True
        ):

            st.session_state.start_interview = False
            st.session_state.question = 0

            if "questions" in st.session_state:
                del st.session_state["questions"]

            if "history" in st.session_state:
                del st.session_state["history"]

            st.rerun()