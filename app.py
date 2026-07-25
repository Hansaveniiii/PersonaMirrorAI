import streamlit as st
from streamlit_option_menu import option_menu
import os

from pages.home import show as home_page
from pages.upload import show as upload_page
from pages.dashboard import show as dashboard_page
# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="PersonaMirror AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
            "Report",
            "Founder"
        ],

        icons=[
            "house",
            "camera-video",
            "cpu",
            "bar-chart",
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
    st.info("🚧 AI Analysis feature coming soon.")

elif selected == "Dashboard":
    dashboard_page()
elif selected == "Report":

    st.title("📄 Report")
    st.info("🚧 AI Report feature coming soon.")

elif selected == "Founder":

    st.title("👩‍💻 Founder")

    # Automatically load whichever image exists
    if os.path.exists("assets/images/founder.jpg"):
        st.image("assets/images/founder.jpg", width=250)

    elif os.path.exists("assets/images/founder.png"):
        st.image("assets/images/founder.png", width=250)

    elif os.path.exists("assets/images/founder.png..jpg"):
        st.image("assets/images/founder.png..jpg", width=250)

    else:
        st.warning("Founder image not found.")

    st.markdown("""
# Hansaveni Bhardwaj

## 🚀 Founder & Developer

Welcome to **PersonaMirror AI**.

PersonaMirror AI is an AI-powered communication and personality analysis platform designed to help students, professionals, and aspiring leaders improve their communication skills through intelligent AI feedback.

---

## 🌟 Vision

To build an AI mentor that empowers individuals to become confident speakers, effective communicators, and inspiring leaders.

---

## 🎯 Mission

To make AI-powered communication coaching accessible to everyone.

---

## 💡 Current Features

- 🎥 Video Upload
- 🖥 Modern Dashboard
- 📁 Secure Video Storage

---

## 🔮 Upcoming AI Features

- 😊 Emotion Detection
- 👀 Eye Contact Analysis
- 🎤 Speech-to-Text
- 🗣 Voice & Tone Analysis
- 🧠 Personality Analysis
- 📊 Confidence Score
- ⭐ Leadership Score
- 📄 AI Performance Report
- 📈 Progress Tracking

---

## 🛠 Technologies Used

- Python
- Streamlit
- OpenCV
- Artificial Intelligence
- Machine Learning
- Computer Vision

---

## ❤️ Motto

### "See Yourself. Improve Yourself."

---

### Designed & Developed By

# Hansaveni Bhardwaj

© 2026 PersonaMirror AI
All Rights Reserved.
""")