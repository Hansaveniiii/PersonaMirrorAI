import streamlit as st


def show():

    # =========================================================
    # PAGE BACKGROUND
    # =========================================================

    st.html("""
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(124, 58, 237, 0.30),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(14, 165, 233, 0.25),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(168, 85, 247, 0.22),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #03010a,
                #080318,
                #050817
            );
    }

    .block-container {
        max-width: 1250px;
        padding-top: 35px;
        padding-bottom: 60px;
    }

    /* =====================================================
       HERO
       ===================================================== */

    .pm-hero {
        position: relative;
        overflow: hidden;

        text-align: center;

        padding: 70px 45px 55px 45px;

        border-radius: 34px;

        background:
            radial-gradient(
                circle at 20% 20%,
                rgba(168, 85, 247, 0.18),
                transparent 35%
            ),
            radial-gradient(
                circle at 80% 30%,
                rgba(34, 211, 238, 0.13),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                rgba(32, 12, 65, 0.92),
                rgba(7, 10, 29, 0.96)
            );

        border: 1px solid rgba(192, 132, 252, 0.28);

        box-shadow:
            0 30px 80px rgba(0,0,0,0.55),
            0 0 70px rgba(124,58,237,0.18),
            inset 0 0 50px rgba(124,58,237,0.06);
    }

    .pm-orb {
        position: absolute;
        width: 180px;
        height: 180px;
        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(168,85,247,0.30),
                transparent 70%
            );

        filter: blur(8px);

        animation: floatOrb 7s ease-in-out infinite;
    }

    .pm-orb.one {
        left: -70px;
        top: -60px;
    }

    .pm-orb.two {
        right: -70px;
        bottom: -70px;

        animation-delay: 2s;
    }

    @keyframes floatOrb {

        0%,100% {
            transform: translateY(0px);
        }

        50% {
            transform: translateY(-25px);
        }
    }

    .pm-brain {
        position: relative;
        z-index: 2;

        font-size: 72px;

        animation:
            brainPulse 3s ease-in-out infinite,
            brainFloat 5s ease-in-out infinite;

        filter:
            drop-shadow(0 0 18px rgba(168,85,247,0.75))
            drop-shadow(0 0 35px rgba(56,189,248,0.30));
    }

    @keyframes brainPulse {

        0%,100% {
            transform: scale(1);
        }

        50% {
            transform: scale(1.08);
        }
    }

    @keyframes brainFloat {

        0%,100% {
            margin-top: 0px;
        }

        50% {
            margin-top: -8px;
        }
    }

    .pm-title {
        position: relative;
        z-index: 2;

        margin-top: 15px;

        font-size: 68px;
        font-weight: 950;
        letter-spacing: -3px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #c084fc,
                #67e8f9,
                #a78bfa,
                #ffffff
            );

        background-size: 400% 400%;

        -webkit-background-clip: text;
        background-clip: text;

        -webkit-text-fill-color: transparent;

        animation:
            titleGradient 7s ease infinite,
            titleGlow 3s ease-in-out infinite;
    }

    @keyframes titleGradient {

        0% {
            background-position: 0% 50%;
        }

        50% {
            background-position: 100% 50%;
        }

        100% {
            background-position: 0% 50%;
        }
    }

    @keyframes titleGlow {

        0%,100% {
            filter:
                drop-shadow(0 0 8px rgba(168,85,247,0.35));
        }

        50% {
            filter:
                drop-shadow(0 0 18px rgba(168,85,247,0.75))
                drop-shadow(0 0 35px rgba(34,211,238,0.25));
        }
    }

    .pm-subtitle {
        position: relative;
        z-index: 2;

        margin-top: 12px;

        font-size: 25px;
        font-weight: 750;

        color: #c4b5fd;
    }

    .pm-description {
        position: relative;
        z-index: 2;

        max-width: 850px;

        margin: 25px auto 0 auto;

        color: #cbd5e1;

        font-size: 17px;
        line-height: 1.85;
    }

    .pm-pill {
        position: relative;
        z-index: 2;

        display: inline-block;

        margin-top: 28px;

        padding: 13px 25px;

        border-radius: 50px;

        color: #ede9fe;

        font-size: 12px;
        font-weight: 850;

        letter-spacing: 1.7px;

        background:
            linear-gradient(
                90deg,
                rgba(124,58,237,0.28),
                rgba(14,165,233,0.22),
                rgba(168,85,247,0.28)
            );

        border: 1px solid rgba(192,132,252,0.38);

        box-shadow:
            0 0 25px rgba(124,58,237,0.25);

        animation: pillGlow 4s ease-in-out infinite;
    }

    @keyframes pillGlow {

        0%,100% {
            box-shadow:
                0 0 20px rgba(124,58,237,0.18);
        }

        50% {
            box-shadow:
                0 0 35px rgba(124,58,237,0.40);
        }
    }

    /* =====================================================
       SECTION
       ===================================================== */

    .pm-section {
        margin-top: 55px;

        color: #ffffff;

        font-size: 31px;
        font-weight: 850;
    }

    .pm-muted {
        color: #9690a8;

        font-size: 15px;

        margin-top: 7px;
        margin-bottom: 25px;
    }

    /* =====================================================
       CARDS
       ===================================================== */

    .pm-card {

        min-height: 205px;

        padding: 28px;

        border-radius: 25px;

        background:
            linear-gradient(
                145deg,
                rgba(38,20,70,0.90),
                rgba(8,7,22,0.97)
            );

        border: 1px solid rgba(167,139,250,0.18);

        box-shadow:
            0 18px 45px rgba(0,0,0,0.38),
            inset 0 0 30px rgba(124,58,237,0.035);

        transition:
            transform 0.35s ease,
            border-color 0.35s ease,
            box-shadow 0.35s ease;
    }

    .pm-card:hover {

        transform: translateY(-8px);

        border-color:
            rgba(192,132,252,0.65);

        box-shadow:
            0 25px 55px rgba(0,0,0,0.48),
            0 0 30px rgba(124,58,237,0.18);
    }

    .pm-icon {
        font-size: 42px;

        margin-bottom: 12px;

        filter:
            drop-shadow(
                0 0 10px rgba(168,85,247,0.35)
            );
    }

    .pm-card-title {

        color: #ffffff;

        font-size: 19px;

        font-weight: 850;

        margin-bottom: 10px;
    }

    .pm-card-text {

        color: #aaa4ba;

        font-size: 14px;

        line-height: 1.75;
    }

    /* =====================================================
       FLOW
       ===================================================== */

    .pm-flow {

        margin-top: 25px;

        padding: 35px;

        border-radius: 27px;

        text-align: center;

        background:
            linear-gradient(
                135deg,
                rgba(76,29,149,0.28),
                rgba(8,47,73,0.28)
            );

        border: 1px solid rgba(125,211,252,0.18);

        box-shadow:
            0 0 45px rgba(124,58,237,0.12);
    }

    .pm-flow-text {

        color: #ddd6fe;

        font-size: 16px;

        font-weight: 850;

        letter-spacing: 1.7px;
    }

    /* =====================================================
       FOOTER
       ===================================================== */

    .pm-footer {

        text-align: center;

        color: #716b80;

        margin-top: 60px;

        padding-top: 25px;

        border-top:
            1px solid rgba(255,255,255,0.07);
    }

    </style>
    """)

    # =========================================================
    # HERO
    # =========================================================

    st.html("""
    <div class="pm-hero">

        <div class="pm-orb one"></div>
        <div class="pm-orb two"></div>

        <div class="pm-brain">
            🧠
        </div>

        <div class="pm-title">
            PersonaMirror AI
        </div>

        <div class="pm-subtitle">
            Understand Yourself. Communicate Better. Grow Smarter.
        </div>

        <div class="pm-description">
            An AI-powered personal intelligence platform that
            understands communication, behavior, professional identity,
            interview performance and career readiness.
            PersonaMirror AI combines speech, language, vision and
            mathematical intelligence to create personalized insights.
        </div>

        <div class="pm-pill">
            SPEECH • LANGUAGE • VISION • MATHEMATICS • CAREER AI
        </div>

    </div>
    """)

    # =========================================================
    # DASHBOARD
    # =========================================================

    st.html("""
    <div class="pm-section">
        ✨ Your Personal Intelligence Dashboard
    </div>

    <div class="pm-muted">
        One platform. Multiple dimensions of personal growth.
    </div>
    """)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("AI Intelligence Layers", "5+")

    with c2:
        st.metric("Performance View", "360°")

    with c3:
        st.metric("Personalized", "AI")

    with c4:
        st.metric("Growth Potential", "∞")

    # =========================================================
    # ECOSYSTEM
    # =========================================================

    st.html("""
    <div class="pm-section">
        🌌 The PersonaMirror AI Ecosystem
    </div>

    <div class="pm-muted">
        More than a mock interview application — a complete
        personal intelligence platform.
    </div>
    """)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.html("""
        <div class="pm-card">
            <div class="pm-icon">🎤</div>

            <div class="pm-card-title">
                Communication Intelligence
            </div>

            <div class="pm-card-text">
                Understand speech rate, fluency, clarity,
                vocabulary, pronunciation and communication
                effectiveness.
            </div>
        </div>
        """)

    with c2:
        st.html("""
        <div class="pm-card">
            <div class="pm-icon">👁️</div>

            <div class="pm-card-title">
                Behavior Intelligence
            </div>

            <div class="pm-card-text">
                Analyze eye contact, facial visibility,
                posture, gestures, engagement and
                presentation behavior.
            </div>
        </div>
        """)

    with c3:
        st.html("""
        <div class="pm-card">
            <div class="pm-icon">🧠</div>

            <div class="pm-card-title">
                Language Intelligence
            </div>

            <div class="pm-card-text">
                Evaluate whether your actual answer is
                relevant, structured, professional and
                responsive to the question.
            </div>
        </div>
        """)

    c4, c5, c6 = st.columns(3)

    with c4:
        st.html("""
        <div class="pm-card">
            <div class="pm-icon">🎯</div>

            <div class="pm-card-title">
                Interview Intelligence
            </div>

            <div class="pm-card-text">
                Practice realistic interviews with
                question-specific evaluation and
                personalized feedback.
            </div>
        </div>
        """)

    with c5:
        st.html("""
        <div class="pm-card">
            <div class="pm-icon">🧮</div>

            <div class="pm-card-title">
                Mathematical Intelligence
            </div>

            <div class="pm-card-text">
                Combine multiple performance signals
                using weighted mathematical scoring
                and fuzzy-logic readiness evaluation.
            </div>
        </div>
        """)

    with c6:
        st.html("""
        <div class="pm-card">
            <div class="pm-icon">🚀</div>

            <div class="pm-card-title">
                Career Intelligence
            </div>

            <div class="pm-card-text">
                Turn performance insights into practical
                professional development, skill improvement
                and career-readiness guidance.
            </div>
        </div>
        """)

    # =========================================================
    # HOW IT WORKS
    # =========================================================

    st.html("""
    <div class="pm-section">
        ⚡ How PersonaMirror AI Works
    </div>

    <div class="pm-muted">
        Your performance moves through a complete intelligence pipeline.
    </div>

    <div class="pm-flow">
        <div class="pm-flow-text">
            CAPTURE
            &nbsp; → &nbsp;
            ANALYZE
            &nbsp; → &nbsp;
            MEASURE
            &nbsp; → &nbsp;
            REFLECT
            &nbsp; → &nbsp;
            IMPROVE
            &nbsp; → &nbsp;
            GROW
        </div>
    </div>
    """)

    # =========================================================
    # DIFFERENT
    # =========================================================

    st.html("""
    <div class="pm-section">
        🔮 What Makes PersonaMirror Different?
    </div>

    <div class="pm-muted">
        Designed to analyze the person behind the performance.
    </div>
    """)

    x1, x2 = st.columns(2)

    with x1:
        st.html("""
        <div class="pm-card">

            <div class="pm-icon">💡</div>

            <div class="pm-card-title">
                Personalized, Not Generic
            </div>

            <div class="pm-card-text">
                PersonaMirror evaluates your actual words,
                your actual question, your communication
                signals and your behavioral performance
                instead of repeating identical advice.
            </div>

        </div>
        """)

    with x2:
        st.html("""
        <div class="pm-card">

            <div class="pm-icon">📈</div>

            <div class="pm-card-title">
                Measure Your Growth
            </div>

            <div class="pm-card-text">
                Track your performance and understand
                which areas are improving and which
                areas require focused development.
            </div>

        </div>
        """)

    # =========================================================
    # FINAL
    # =========================================================

    st.html("""
    <div class="pm-flow" style="margin-top:55px;">

        <div style="
            font-size:30px;
            font-weight:850;
            color:#ffffff;
            margin-bottom:15px;
        ">
            Intelligence That Understands the Whole You
        </div>

        <div style="
            max-width:760px;
            margin:auto;
            color:#b9b2ca;
            font-size:16px;
            line-height:1.8;
        ">
            Communication. Behavior. Reasoning. Confidence.
            Professional identity. Career growth.
            PersonaMirror AI brings these dimensions together
            into one intelligent personal growth ecosystem.
        </div>

    </div>
    """)

    # =========================================================
    # FOOTER
    # =========================================================

    st.html("""
    <div class="pm-footer">

        <strong>PersonaMirror AI</strong>

        <br><br>

        Personal Intelligence • Communication • Career Growth

    </div>
    """)