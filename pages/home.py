import streamlit as st

def show():

    st.markdown(
        """
        <style>
        .hero{
            padding:50px;
            border-radius:25px;
            background:linear-gradient(135deg,#7C3AED,#2563EB);
            color:white;
            text-align:center;
            margin-bottom:30px;
        }

        .hero h1{
            font-size:52px;
            font-weight:800;
            margin-bottom:10px;
        }

        .hero p{
            font-size:22px;
            opacity:.95;
        }

        .card{
            background:#1E293B;
            padding:25px;
            border-radius:20px;
            border:1px solid #334155;
            margin-top:20px;
            transition:.3s;
        }

        .card:hover{
            transform:translateY(-5px);
            box-shadow:0 12px 30px rgba(0,0,0,.35);
        }

        .feature{
            font-size:20px;
            font-weight:600;
            margin-bottom:10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='hero'>
        <h1>🧠 PersonaMirror AI</h1>
        <p>Your Personal AI Communication Coach</p>
        <p>Analyze speeches, interviews, presentations and become a confident leader.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card'>
            <div class='feature'>🎥 Video Analysis</div>
            Upload any speech or interview and receive instant AI feedback.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card'>
            <div class='feature'>😊 Personality Insights</div>
            Confidence, leadership, communication, voice and body language analysis.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='card'>
            <div class='feature'>📈 AI Improvement Plan</div>
            Get personalized suggestions to improve every presentation.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("✨ What PersonaMirror AI Can Analyze")

    c1, c2 = st.columns(2)

    with c1:
        st.success("✅ Confidence Score")
        st.success("✅ Leadership Score")
        st.success("✅ Speech Analysis")
        st.success("✅ Voice Energy")
        st.success("✅ Facial Emotion")

    with c2:
        st.success("✅ Presentation Skills")
        st.success("✅ Interview Readiness")
        st.success("✅ Executive Presence")
        st.success("✅ Communication Report")
        st.success("✅ AI Suggestions")

    st.divider()

    st.info("👈 Start by opening the Upload page from the sidebar.")