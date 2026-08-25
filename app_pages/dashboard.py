import streamlit as st
import plotly.graph_objects as go

from modules.analysis_manager import load_results


def safe_score(value):
    """Return a valid numeric score or None."""
    if value is None:
        return None

    try:
        value = float(value)
        if 0 <= value <= 100:
            return value
    except (TypeError, ValueError):
        pass

    return None


def gauge(title, value):
    value = safe_score(value)

    if value is None:
        return None

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#7C3AED"},
                "steps": [
                    {"range": [0, 40], "color": "#2E2E2E"},
                    {"range": [40, 70], "color": "#444444"},
                    {"range": [70, 100], "color": "#666666"},
                ],
            },
        )
    )

    fig.update_layout(
        height=250,
        margin=dict(l=10, r=10, t=55, b=10),
    )

    return fig


def metric_display(value, suffix="%"):
    value = safe_score(value)

    if value is None:
        return "Not measured"

    if suffix:
        return f"{value:g}{suffix}"

    return f"{value:g}"


def show():

    st.title("📊 PersonaMirror AI Dashboard")
    st.caption("Your communication performance at a glance")

    # =========================================================
    # LOAD PERSISTED ANALYSIS
    # IMPORTANT:
    # Do NOT depend on Streamlit session_state.
    # =========================================================

    result = load_results()

    if not isinstance(result, dict):
        st.warning("🎥 Upload and analyze a video first.")
        return

    if not result.get("analysis_ready", False):
        st.warning("🎥 Upload and analyze a video first.")
        return

    # =========================================================
    # CORE SCORES
    # =========================================================

    confidence = safe_score(result.get("confidence"))
    leadership = safe_score(result.get("leadership"))
    voice_confidence = safe_score(result.get("voice_confidence"))
    presentation = safe_score(result.get("presentation_score"))
    executive = safe_score(result.get("executive_presence"))
    speech_quality = safe_score(result.get("speech_quality"))
    structure = safe_score(result.get("structure_score"))
    clarity = safe_score(result.get("clarity"))
    repetition = safe_score(result.get("repetition_score"))
    overall = safe_score(result.get("overall_score"))

    # =========================================================
    # HERO SCORE
    # =========================================================

    if overall is not None:
        st.metric(
            "🏆 Overall PersonaMirror Score",
            f"{overall:g}/100",
        )

    st.success("✅ Analysis loaded successfully")

    # =========================================================
    # PRIMARY PERFORMANCE
    # =========================================================

    st.subheader("🎯 Core Performance")

    cols = st.columns(4)

    cards = [
        ("⭐ Confidence", confidence),
        ("👑 Leadership", leadership),
        ("🎤 Voice Confidence", voice_confidence),
        ("🎥 Presentation", presentation),
    ]

    for col, (title, value) in zip(cols, cards):
        with col:
            if value is not None:
                st.metric(title, f"{value:g}%")
            else:
                st.metric(title, "Not measured")

    # =========================================================
    # EXECUTIVE PRESENCE
    # =========================================================

    cols = st.columns(4)

    cards = [
        ("💼 Executive Presence", executive),
        ("🗣 Speech Quality", speech_quality),
        ("🧠 Structure", structure),
        ("✨ Clarity", clarity),
    ]

    for col, (title, value) in zip(cols, cards):
        with col:
            if value is not None:
                st.metric(title, f"{value:g}%")
            else:
                st.metric(title, "Not measured")

    st.divider()

    # =========================================================
    # GAUGES
    # =========================================================

    st.subheader("📈 Performance Signals")

    gauge_data = [
        ("Confidence", confidence),
        ("Leadership", leadership),
        ("Voice Confidence", voice_confidence),
    ]

    gauge_cols = st.columns(3)

    for col, (title, value) in zip(gauge_cols, gauge_data):
        with col:
            fig = gauge(title, value)

            if fig is not None:
                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )
            else:
                st.info(f"{title}: Not measured")

    # =========================================================
    # COMMUNICATION PROFILE
    # =========================================================

    st.divider()

    st.subheader("🧠 Communication Profile")

    radar_names = [
        "Confidence",
        "Leadership",
        "Voice",
        "Presentation",
        "Structure",
        "Clarity",
    ]

    radar_values = [
        confidence,
        leadership,
        voice_confidence,
        presentation,
        structure,
        clarity,
    ]

    valid_radar = [
        (name, value)
        for name, value in zip(radar_names, radar_values)
        if value is not None
    ]

    if len(valid_radar) >= 3:

        names = [x[0] for x in valid_radar]
        values = [x[1] for x in valid_radar]

        names_closed = names + [names[0]]
        values_closed = values + [values[0]]

        radar = go.Figure()

        radar.add_trace(
            go.Scatterpolar(
                r=values_closed,
                theta=names_closed,
                fill="toself",
                line=dict(color="#7C3AED"),
                name="Performance",
            )
        )

        radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                )
            ),
            showlegend=False,
            height=450,
        )

        st.plotly_chart(
            radar,
            use_container_width=True,
        )

    else:
        st.info("Not enough measured signals for the communication profile.")

    # =========================================================
    # SPEECH DETAILS
    # =========================================================

    st.divider()

    st.subheader("🗣 Speech Intelligence")

    speech = result.get("speech")
    duration = result.get("duration")
    word_count = result.get("word_count")
    filler_count = result.get("filler_count")

    cols = st.columns(4)

    with cols[0]:
        st.metric(
            "Speaking Rate",
            f"{speech:g} WPM" if isinstance(speech, (int, float)) else "Not measured",
        )

    with cols[1]:
        st.metric(
            "⏱ Duration",
            f"{float(duration):.1f}s"
            if isinstance(duration, (int, float))
            else "Not measured",
        )

    with cols[2]:
        st.metric(
            "📝 Words",
            str(word_count)
            if word_count is not None
            else "Not measured",
        )

    with cols[3]:
        st.metric(
            "🚫 Fillers",
            str(filler_count)
            if filler_count is not None
            else "Not measured",
        )

    # =========================================================
    # REPEATED WORDS
    # =========================================================

    repeated_words = result.get("repeated_words", {})

    if repeated_words:

        st.subheader("🔁 Repetition Intelligence")

        for word, count in sorted(
            repeated_words.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:5]:

            st.write(
                f"**{word}** — {count} times"
            )

    # =========================================================
    # AI FEEDBACK
    # =========================================================

    st.divider()

    st.subheader("🤖 PersonaMirror AI Feedback")

    feedback = result.get("feedback", {})

    if isinstance(feedback, dict):

        strengths = feedback.get("strengths", [])
        improvements = feedback.get("improvements", [])
        suggestions = feedback.get("suggestions", [])

        if strengths:
            st.markdown("### 💪 Strengths")

            for item in strengths:
                st.success(f"✓ {item}")

        if improvements:
            st.markdown("### ⚠️ Improvement Areas")

            for item in improvements:
                st.warning(f"→ {item}")

        if suggestions:
            st.markdown("### 🎯 Personalized Recommendations")

            for index, item in enumerate(
                suggestions,
                start=1,
            ):
                st.info(f"**{index}.** {item}")

    # =========================================================
    # TRANSCRIPT
    # =========================================================

    transcript = result.get("transcript", "")

    if transcript:

        st.divider()

        st.subheader("📝 Speech Transcript")

        with st.expander("View full transcript"):
            st.write(transcript)

    # =========================================================
    # GROWTH LOOP
    # =========================================================

    st.divider()

    st.markdown(
        """
        ### 🌱 PersonaMirror Growth Loop

        **Analyze → Understand → Practice → Re-analyze → Improve**

        Your current analysis is a baseline.  
        The goal is not simply to get a high score — it is to become a stronger communicator over time.
        """
    )
