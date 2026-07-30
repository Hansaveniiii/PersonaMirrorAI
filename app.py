import sys
print(sys.executable)

import os
import streamlit as st
from streamlit_option_menu import option_menu

from modules.pdf_report import generate_pdf
from modules.analysis_manager import load_results

from pages.home import show as home_page
from pages.upload import show as upload_page
from pages.dashboard import show as dashboard_page
from pages.mock_interview import show as interview_page


# -------------------------
# Load Custom CSS
# -------------------------

def load_css():
    css_path = "assets/styles/style.css"

    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="PersonaMirror AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
            "Report",
            "Founder"
        ],

        icons=[
            "house",
            "camera-video",
            "cpu",
            "bar-chart",
            "person-workspace",
            "file-earmark-text",
            "person-circle"
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

    result = load_results()

    if result["confidence"] == 0:

        st.warning("⚠️ Please upload and analyze a video first.")

    else:

        st.success("✅ AI Analysis Loaded Successfully")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "⭐ Confidence",
                f"{result['confidence']}%"
            )

            st.metric(
                "👀 Eye Contact",
                f"{result['eye_contact']}%"
            )

            st.metric(
                "😊 Emotion",
                result["emotion"]
            )

        with col2:

            st.metric(
                "👑 Leadership",
                f"{result['leadership']}%"
            )

            st.metric(
                "🗣 Speaking Speed",
                f"{result['speech']} WPM"
            )

            st.metric(
                "👥 Face Visibility",
                f"{result['visibility']}%"
            )

        st.subheader("📝 Speech Transcript")

        st.write(result["transcript"])

elif selected == "Dashboard":

    dashboard_page()

elif selected == "Mock Interview":

    interview_page()

elif selected == "Report":

    st.title("📄 AI Communication Report")

    result = load_results()

    if result["confidence"] == 0:

        st.warning("⚠️ Please analyze a video first.")

    else:

        pdf_path = generate_pdf(result)

        st.success("✅ PersonaMirror AI Report Generated")

        overall_score = int(
            (
                result["confidence"]
                + result["leadership"]
                + result["eye_contact"]
                + min(result["speech"], 100)
            ) / 4
        )

        st.metric(
            "🏆 Overall AI Score",
            f"{overall_score}/100"
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "⭐ Confidence",
                f"{result['confidence']}%"
            )

            st.metric(
                "👀 Eye Contact",
                f"{result['eye_contact']}%"
            )

            st.metric(
                "😊 Emotion",
                result["emotion"]
            )

        with col2:

            st.metric(
                "👑 Leadership",
                f"{result['leadership']}%"
            )

            st.metric(
                "🗣 Speaking Speed",
                f"{result['speech']} WPM"
            )

            st.metric(
                "👁 Face Visibility",
                f"{result['visibility']}%"
            )

        st.divider()

        st.subheader("📝 Speech Transcript")

        st.write(result["transcript"])

        st.divider()

        st.subheader("📊 Communication Summary")

        st.markdown(f"""
- ⭐ **Confidence:** {result['confidence']}%
- 👑 **Leadership:** {result['leadership']}%
- 👀 **Eye Contact:** {result['eye_contact']}%
- 🗣 **Speech Speed:** {result['speech']} WPM
- 👁 **Face Visibility:** {result['visibility']}%
- 😊 **Emotion:** {result['emotion']}
""")

        st.divider()

        with open(pdf_path, "rb") as pdf_file:

            st.download_button(
                label="📥 Download AI Report (PDF)",
                data=pdf_file,
                file_name="PersonaMirror_AI_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

elif selected == "Founder":

    st.title("👩‍💻 Meet the Founder")

    col1, col2 = st.columns([1, 2])

    with col1:

        if os.path.exists("assets/images/founder.jpg"):

            st.image(
                "assets/images/founder.jpg",
                width=260
            )

        elif os.path.exists("assets/images/founder.png"):

            st.image(
                "assets/images/founder.png",
                width=260
            )

        else:

            st.warning("Founder image not found.")

    with col2:

        st.header("Hansaveni Bhardwaj")

        st.markdown("""
### Founder & Developer

Creator of **PersonaMirror AI**

Building Artificial Intelligence that helps people become
better speakers, stronger leaders and more confident communicators.
""")

        st.success(
            "🎯 Mission: AI Communication Coach for Everyone"
        )

    st.divider()

    st.subheader("🚀 About PersonaMirror AI")

    st.write("""
PersonaMirror AI is an intelligent communication coach that analyzes
videos and provides personalized feedback on communication,
confidence, leadership, eye contact, facial expressions,
speech delivery and overall personality.

Instead of generic advice, every user receives customized
suggestions based on their own performance.
""")

    st.divider()

    st.subheader("🌟 Vision")

    st.info("""
To build the world's smartest AI Communication Coach that helps
students, professionals, educators and public speakers improve
through intelligent AI feedback.
""")

    st.divider()

    st.subheader("🏆 Founder Highlights")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
✅ Head Girl

✅ Public Speaker

✅ Inter-School Debate Winner

✅ College Anchor

✅ Event Host

✅ Poetry Performer
""")

    with col2:

        st.markdown("""
✅ Leadership Experience

✅ AI Developer

✅ Python Programmer

✅ Machine Learning Enthusiast

✅ Communication Coach

✅ Startup Builder
""")

    st.divider()

    st.subheader("🧠 Current AI Features")

    st.markdown("""
- 🎥 Video Upload
- 😀 Face Detection
- 📊 Communication Dashboard
- 📈 Confidence Analysis
- 🗣 Speech Analysis
- 🎤 AI Mock Interview
- 🤖 AI Suggestions
""")

    st.divider()

    st.subheader("🚀 Upcoming Features")

    roadmap = {
        "Emotion Detection": "🟡 In Progress",
        "Eye Contact Tracking": "🟡 In Progress",
        "Body Language Analysis": "🔜 Planned",
        "Voice Tone Analysis": "🔜 Planned",
        "Gesture Recognition": "🔜 Planned",
        "AI Communication Coach": "🔜 Planned",
        "Professional PDF Report": "🔜 Planned",
        "Android App": "🔜 Planned",
        "iOS App": "🔜 Planned"
    }

    for feature, status in roadmap.items():

        st.write(f"**{feature}** — {status}")

    st.divider()

    st.subheader("🛠 Technology Stack")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Language", "Python")

    with c2:
        st.metric("Framework", "Streamlit")

    with c3:
        st.metric("AI", "OpenCV + ML")

    st.divider()

    st.subheader("❤️ Motto")

    st.success("See Yourself. Improve Yourself.")

    st.divider()

    st.caption("Designed & Developed by Hansaveni Bhardwaj")
    st.caption("© 2026 PersonaMirror AI • All Rights Reserved")