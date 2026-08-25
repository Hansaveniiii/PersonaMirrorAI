import sys

from modules import eye_contact
print(sys.executable)

import os
import streamlit as st
from streamlit_option_menu import option_menu

from modules.pdf_report import generate_pdf
from modules.analysis_manager import load_results
import hashlib
from app_pages.home import show as home_page
from app_pages.upload import show as upload_page
from app_pages.dashboard import show as dashboard_page
from app_pages.interview_start import show as interview_start_page
from app_pages.mock_interview import show as interview_page
from app_pages.presentation_coach import show as presentation_page
from app_pages.resume_doctor import show as resume_page
from app_pages.job_match import show as job_match_page
from app_pages.resume_rewriter import show as rewriter_page
from app_pages.founder import show as founder_page
def has_current_analysis():
    return (
        st.session_state.get("analysis_ready", False)
        and st.session_state.get("current_upload_key")
    )


# -------------------------
# Load Custom CSS
# -------------------------

def load_css():
    css_path = "assets/styles/style.css"

    if os.path.exists(css_path):

        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True
        ) 

    else:

        st.error(f"CSS file not found: {os.path.abspath(css_path)}")


# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="PersonaMirror AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)
# =========================================================
# FRESH APP SESSION
# =========================================================

if "analysis_ready" not in st.session_state:
    st.session_state["analysis_ready"] = False

if "current_upload_key" not in st.session_state:
    st.session_state["current_upload_key"] = None
if "current_analysis" not in st.session_state:
    st.session_state["current_analysis"] = None

# Load CSS AFTER page configuration
load_css()


# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    selected = option_menu(
        menu_title="🧠 PersonaMirror AI",

        options=[
            "Home",
            "Upload",
            "Analysis",
            "Dashboard",
            "Mock Interview",
            "Presentation Coach",
            "Resume Doctor",
            "AI Job Match",
            "AI Resume Rewriter",
            "Report",
            "Founder",
        ],
       icons=[
            "house",
            "camera-video",
            "cpu",
            "bar-chart",
            "person-workspace",
            "easel",
            "file-earmark-text",
            "briefcase",
            "pencil-square",
            "file-earmark-pdf",
            "person-circle",
        ],

        default_index=0,
    )

# -------------------------
# Navigation
# -------------------------

if selected == "Home":

    home_page()

elif selected == "Upload":

    upload_page()

elif selected == "Analysis":

    st.title("🤖 AI Analysis")

    # =========================================================
    # ONLY SHOW ANALYSIS FOR CURRENT SESSION
    # =========================================================

    if not has_current_analysis():

        st.info(
            "🎥 No analysis available for this session."
        )

        st.markdown(
            """
            ### Start your PersonaMirror analysis

            1. Go to **Upload**
            2. Upload your video
            3. Choose the analysis type
            4. Click **Analyze My Performance**
            5. Return here to view your results
            """
        )

    else:

        result = st.session_state.get(
            "current_analysis"
        )

        st.success(
            "✅ AI Analysis Loaded Successfully"
        )

        col1, col2 = st.columns(2)

        with col1:

            confidence = result.get("confidence")

            st.metric(
                "⭐ Confidence",
                f"{confidence}%"
                if confidence is not None
                else "Not measured"
            )

            eye_contact = result.get(
                "eye_contact"
            )

            st.metric(
                "👀 Eye Contact",
                f"{eye_contact}%"
                if eye_contact is not None
                else "Not measured"
            )

            st.metric(
                "😊 Emotion",
                result.get(
                    "emotion",
                    "Unknown"
                )
            )

        with col2:

            leadership = result.get(
                "leadership"
            )

            st.metric(
                "👑 Leadership",
                f"{leadership}%"
                if leadership is not None
                else "Not measured"
            )

            speech = result.get(
                "speech"
            )

            st.metric(
                "🗣 Speaking Speed",
                f"{speech} WPM"
                if speech is not None
                else "Not measured"
            )

            visibility = result.get(
                "visibility"
            )

            st.metric(
                "👥 Face Visibility",
                f"{visibility}%"
                if visibility is not None
                else "Not reliably measured"
            )

        st.subheader(
            "📝 Speech Transcript"
        )

        transcript = result.get(
            "transcript",
            ""
        )

        if transcript:

            st.write(transcript)

        else:

            st.info(
                "No transcript available for this recording."
            )

elif selected == "Dashboard":

    dashboard_page()

elif selected == "Mock Interview":

    if st.session_state.get("start_interview", False):
        interview_page()
    else:
        interview_start_page()

elif selected == "Presentation Coach":

        presentation_page()
elif selected == "Resume Doctor":
    resume_page()

elif selected == "AI Job Match":
    job_match_page()

elif selected == "AI Resume Rewriter":
    rewriter_page()
elif selected == "Report":

    st.title("📄 AI Communication Report")

    result = st.session_state.get(
    "current_analysis"
    )

    if not result:
        st.warning("⚠️ Please upload and analyze a video first.")

    else:

        # ---------------------------------------------------------
        # SAFE VALUES
        # ---------------------------------------------------------

        confidence = result.get("confidence")
        leadership = result.get("leadership")
        eye_contact = result.get("eye_contact")
        speech = result.get("speech")
        visibility = result.get("visibility")
        emotion = result.get("emotion", "Unknown")

        # ---------------------------------------------------------
        # DISPLAY UNAVAILABLE METRICS CORRECTLY
        # ---------------------------------------------------------

        if eye_contact is None:
            eye_contact_display = "Not measured"
        else:
            eye_contact_display = f"{eye_contact}%"

        if visibility is None:
            visibility_display = "Not measured"
        else:
            visibility_display = f"{visibility}%"

        if speech is None:
            speech_display = "Not measured"
        else:
            speech_display = f"{speech} WPM"

        # ---------------------------------------------------------
        # OVERALL SCORE
        #
        # Only use measurements that actually exist.
        # Do NOT treat unavailable measurements as zero.
        # ---------------------------------------------------------

        score_values = []

        if confidence is not None:
            score_values.append(float(confidence))

        if leadership is not None:
            score_values.append(float(leadership))

        # Speech-rate quality score
        if speech is not None and speech > 0:

            if 110 <= speech <= 160:
                speech_score = 100

            elif 100 <= speech < 110 or 160 < speech <= 175:
                speech_score = 90

            elif 90 <= speech < 100 or 175 < speech <= 190:
                speech_score = 75

            else:
                speech_score = 60

            score_values.append(float(speech_score))

        if score_values:
            overall_score = round(
                sum(score_values) / len(score_values)
            )
        else:
            overall_score = 0

        # ---------------------------------------------------------
        # PDF
        # ---------------------------------------------------------

        try:

            pdf_path = generate_pdf(result)

            st.success(
                "✅ PersonaMirror AI Report Generated"
            )

        except Exception as e:

            pdf_path = None

            st.warning(
                f"PDF generation unavailable: {e}"
            )

        # ---------------------------------------------------------
        # OVERALL SCORE
        # ---------------------------------------------------------

        st.metric(
            "🏆 Overall AI Score",
            f"{overall_score}/100"
        )

        st.divider()

        # ---------------------------------------------------------
        # CORE METRICS
        # ---------------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "⭐ Confidence",
                f"{confidence}%"
            )

            st.metric(
                "👀 Eye Contact",
                eye_contact_display
            )

            st.metric(
                "😊 Emotion",
                emotion
            )

        with col2:

            st.metric(
                "👑 Leadership",
                f"{leadership}%"
            )

            st.metric(
                "🗣 Speaking Speed",
                speech_display
            )

            st.metric(
                "👁 Face Visibility",
                visibility_display
            )

        st.divider()

        # ---------------------------------------------------------
        # TRANSCRIPT
        # ---------------------------------------------------------

        st.subheader("📝 Speech Transcript")

        transcript = result.get(
            "transcript",
            ""
        )

        if transcript:

            st.write(transcript)

        else:

            st.info(
                "No transcript available for this recording."
            )

        st.divider()

        # ---------------------------------------------------------
        # COMMUNICATION SUMMARY
        # ---------------------------------------------------------

        st.subheader("📊 Communication Summary")

        summary_items = [
            f"⭐ **Confidence:** {confidence}%",
            f"👑 **Leadership:** {leadership}%",
            f"👀 **Eye Contact:** {eye_contact_display}",
            f"🗣 **Speech Speed:** {speech_display}",
            f"👁 **Face Visibility:** {visibility_display}",
            f"😊 **Emotion:** {emotion}",
        ]

        st.markdown(
            "\n".join(
                f"- {item}"
                for item in summary_items
            )
        )

        st.divider()

        # ---------------------------------------------------------
        # AI FEEDBACK
        # ---------------------------------------------------------

        feedback = result.get(
            "feedback",
            {}
        )

        if isinstance(feedback, dict):

            strengths = feedback.get(
                "strengths",
                []
            )

            improvements = feedback.get(
                "improvements",
                []
            )

            suggestions = feedback.get(
                "suggestions",
                []
            )

            if strengths:

                st.subheader(
                    "🌟 What You Are Doing Well"
                )

                for item in strengths:

                    st.success(
                        f"✓ {item}"
                    )

            if improvements:

                st.subheader(
                    "⚠️ What Needs Attention"
                )

                for item in improvements:

                    st.warning(
                        f"→ {item}"
                    )

            if suggestions:

                st.subheader(
                    "🎯 Personalized Recommendations"
                )

                for index, item in enumerate(
                    suggestions,
                    start=1
                ):

                    st.info(
                        f"**{index}.** {item}"
                    )

        # ---------------------------------------------------------
        # DOWNLOAD PDF
        # ---------------------------------------------------------

        if pdf_path and os.path.exists(pdf_path):

            st.divider()

            with open(
                pdf_path,
                "rb"
            ) as pdf_file:

                st.download_button(
                    label="📥 Download AI Report (PDF)",
                    data=pdf_file,
                    file_name="PersonaMirror_AI_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

elif selected == "Founder":

    founder_page()
    