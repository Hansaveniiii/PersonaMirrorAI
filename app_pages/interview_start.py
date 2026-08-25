import streamlit as st


INTERVIEWERS = {

    "Tripti Bhardwaj": {
        "role": "Senior HR Recruiter",
        "company": "Google",
        "experience": "12 Years",
        "avatar": "👩"
    },

    "Albus Brian": {
        "role": "Technical Interviewer",
        "company": "Microsoft",
        "experience": "10 Years",
        "avatar": "👨‍💻"
    },

    "Ted Mark": {
        "role": "Leadership Coach",
        "company": "McKinsey",
        "experience": "15 Years",
        "avatar": "👩‍💼"
    }

}


ROLES = [
    "Software Engineer",
    "Data Analyst",
    "AI Engineer",
    "Product Manager",
    "HR Interview",
    "MBA Admission",
    "Public Speaking"
]


def show():

    st.title("🎯 PersonaMirror AI Interview")

    st.markdown(
        "Prepare for a realistic AI-powered interview."
    )

    interviewer = st.selectbox(
        "Choose AI Interviewer",
        list(INTERVIEWERS.keys())
    )

    role = st.selectbox(
        "Interview Role",
        ROLES
    )

    difficulty = st.select_slider(
        "Difficulty",
        options=["Easy", "Medium", "Hard"]
    )

    info = INTERVIEWERS[interviewer]

    st.divider()

    st.markdown(f"""
## {info['avatar']} {interviewer}

**Role:** {info['role']}

**Company:** {info['company']}

**Experience:** {info['experience']}
""")

    st.info(
        f"""
Today's Interview

• Position: {role}

• Difficulty: {difficulty}

• Questions: 5

• Estimated Time: 10–15 minutes
"""
    )

    st.success(
        "The AI interviewer will evaluate your communication, confidence, speaking style and interview performance."
    )

    if st.button(
        "🚀 Start Interview",
        use_container_width=True
    ):

        st.session_state.selected_role = role
        st.session_state.selected_interviewer = interviewer
        st.session_state.difficulty = difficulty
        st.session_state.start_interview = True
        st.session_state.question = 0
        st.rerun()