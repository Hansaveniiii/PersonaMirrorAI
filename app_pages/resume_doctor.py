import streamlit as st
import PyPDF2
import docx

from modules.resume_analyzer import analyze_resume


def extract_pdf(file):

    reader = PyPDF2.PdfReader(file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def extract_docx(file):

    document = docx.Document(file)

    text = ""

    for para in document.paragraphs:
        text += para.text + "\n"

    return text


def show():

    st.title("📄 AI Resume Doctor")

    st.write(
        "Upload your resume and receive an AI-powered ATS analysis."
    )

    uploaded = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    if uploaded is None:
        return

    st.success("✅ Resume uploaded successfully.")

    if uploaded.name.endswith(".pdf"):
        resume_text = extract_pdf(uploaded)
    else:
        resume_text = extract_docx(uploaded)

    if st.button("🚀 Analyze Resume"):

        report = analyze_resume(resume_text)

        st.subheader("🎯 ATS Score")

        st.progress(report["ats"] / 100)

        st.metric("ATS Score", f'{report["ats"]}/100')

        st.divider()

        st.subheader("✅ Skills Detected")

        if report["skills"]:
            st.write(", ".join(report["skills"]))
        else:
            st.warning("No major skills detected.")

        st.divider()

        st.subheader("❌ Missing Skills")

        st.write(", ".join(report["missing"]))

        st.divider()

        st.subheader("💪 Strengths")

        for item in report["strengths"]:
            st.success(item)

        st.divider()

        st.subheader("🚀 Improvements")

        for item in report["improvements"]:
            st.warning(item)

        st.divider()

        st.subheader("👨‍💼 Recruiter Feedback")

        st.info(report["recruiter"])