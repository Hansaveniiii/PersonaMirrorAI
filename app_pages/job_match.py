import streamlit as st
import PyPDF2
import docx

from modules.job_match import job_match


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

    st.title("🎯 AI Job Match Analyzer")

    resume = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    jd = st.text_area(
        "Paste Job Description"
    )

    if resume is None:
        return

    if resume.name.endswith(".pdf"):
        resume_text = extract_pdf(resume)
    else:
        resume_text = extract_docx(resume)

    if st.button("Analyze Match"):

        report = job_match(
            resume_text,
            jd
        )

        st.metric(
            "Job Match Score",
            f'{report["score"]}%'
        )

        st.progress(
            report["score"] / 100
        )

        st.subheader("✅ Matching Skills")

        st.write(report["matched"])

        st.subheader("❌ Missing Skills")

        st.write(report["missing"])