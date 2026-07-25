import streamlit as st

def show():

    st.markdown("""
    <style>

    .hero{
        text-align:center;
        padding:40px;
        border-radius:20px;
        background:linear-gradient(135deg,#071A2F,#0B4F8C,#3B82F6);
        color:white;
        box-shadow:0px 0px 30px rgba(0,170,255,0.3);
    }

    .hero h1{
        font-size:60px;
        margin-bottom:10px;
    }

    .hero h3{
        color:#d6e8ff;
    }

    .feature{
        background:#111827;
        padding:25px;
        border-radius:20px;
        color:white;
        text-align:center;
        border:1px solid #2d4f7c;
        height:220px;
    }

    .stats{
        background:#0F172A;
        color:white;
        text-align:center;
        padding:20px;
        border-radius:18px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">

    <h1>🧠 PersonaMirror AI</h1>

    <h3>See Yourself. Improve Yourself.</h3>

    <p style="font-size:20px;">
    AI Powered Communication & Personality Coach
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1,col2=st.columns(2)

    with col1:

        if st.button("🚀 Start Analysis",use_container_width=True):
            st.success("Go to Upload page from the sidebar.")

    with col2:

        if st.button("📖 Learn More",use_container_width=True):
            st.info("Visit the Founder page to learn more.")

    st.write("")
    st.write("")

    st.subheader("✨ AI Features")

    c1,c2,c3=st.columns(3)

    with c1:

        st.markdown("""
        <div class="feature">

        <h2>😊</h2>

        <h3>Emotion Detection</h3>

        <p>
        Detect facial emotions using Artificial Intelligence.
        </p>

        </div>
        """,unsafe_allow_html=True)

    with c2:

        st.markdown("""
        <div class="feature">

        <h2>👀</h2>

        <h3>Eye Contact</h3>

        <p>
        Analyze eye contact and engagement during presentations.
        </p>

        </div>
        """,unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="feature">

        <h2>🎤</h2>

        <h3>Speech Analysis</h3>

        <p>
        Evaluate speaking style, clarity and confidence.
        </p>

        </div>
        """,unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.subheader("📊 Platform")

    a,b,c,d=st.columns(4)

    with a:
        st.metric("Videos", "0")

    with b:
        st.metric("Reports", "0")

    with c:
        st.metric("AI Models", "6")

    with d:
        st.metric("Version", "1.0")

    st.divider()

    st.markdown("""
    <center>

    <h3>Designed & Developed by</h3>

    <h2>Hansaveni Bhardwaj</h2>

    <p>© 2026 PersonaMirror AI</p>

    </center>
    """,unsafe_allow_html=True)