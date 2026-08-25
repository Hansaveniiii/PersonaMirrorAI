import streamlit as st

from modules.resume_rewriter import rewrite_resume


def show():

    st.title("✍️ AI Resume Rewriter")


    resume = st.text_area(
        "Paste your resume text"
    )


    jd = st.text_area(
        "Paste target job description"
    )


    if st.button("Rewrite Resume"):

        if resume and jd:

            result = rewrite_resume(
                resume,
                jd
            )


            st.subheader(
                "🚀 AI Improved Resume Suggestions"
            )


            st.write(result)

        else:

            st.warning(
                "Please provide both resume and job description."
            )