import streamlit as st
import plotly.graph_objects as go

from modules.analysis_manager import load_results


def safe_score(value):
    if value is None:
        return None

    try:
        value = float(value)

        if 0 <= value <= 100:
            return value

    except (TypeError, ValueError):
        pass

    return None


def display_score(value):
    value = safe_score(value)

    if value is None:
        return "Not measured"

    return f"{value:g}%"


def calculate_speech_stats(result):
    """
    Recover duration/WPM from transcript segments when the
    speech-rate field is missing or incorrect.
    """

    words = result.get("transcript_word_count")

    if words is None:
        words = result.get("word_count")

    try:
        words = int(words or 0)
    except (TypeError, ValueError):
        words = 0

    duration = result.get("duration")

    try:
        duration = float(duration or 0)
    except (TypeError, ValueError):
        duration = 0.0

    segments = result.get("segments") or []

    # Recover duration from actual transcription timestamps.
    if duration <= 0 and segments:

        ends = []

        for segment in segments:

            try:
                end = float(segment.get("end", 0))

                if end > 0:
                    ends.append(end)

            except (TypeError, ValueError):
                pass

        if ends:
            duration = max(ends)

    # Recover word count if necessary.
    if words <= 0 and segments:

        text = " ".join(
            str(segment.get("text", ""))
            for segment in segments
        )

        words = len(text.split())

    # Calculate WPM from real duration.
    if words > 0 and duration > 0:

        wpm = round(
            words / (duration / 60)
        )

    else:

        wpm = None

    return words, duration, wpm


def make_gauge(title, value):

    value = safe_score(value)

    if value is None:
        return None

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%"},
            title={"text": title},
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "bar": {
                    "color": "#7C3AED"
                },
                "steps": [
                    {
                        "range": [0, 40],
                        "color": "#252035"
                    },
                    {
                        "range": [40, 70],
                        "color": "#33294A"
                    },
                    {
                        "range": [70, 100],
                        "color": "#463568"
                    },
                ],
            },
        )
    )

    fig.update_layout(
        height=280,
        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10,
        ),
    )

    return fig


def show():

    st.title("📊 PersonaMirror AI Dashboard")
    st.caption(
        "Your communication performance at a glance"
    )

    # =========================================================
    # LOAD PERSISTED ANALYSIS
    # =========================================================

    result = load_results()

    if not isinstance(result, dict):

        st.warning(
            "🎥 Upload and analyze a video first."
        )

        return

    if not result.get(
        "analysis_ready",
        False
    ):

        st.warning(
            "🎥 Upload and analyze a video first."
        )

        return

    # =========================================================
    # READ REAL STORED SCORES
    # =========================================================

    confidence = safe_score(
        result.get("confidence")
    )

    leadership = safe_score(
        result.get("leadership")
    )

    voice_confidence = safe_score(
        result.get("voice_confidence")
    )

    presentation = safe_score(
        result.get("presentation_score")
    )

    executive = safe_score(
        result.get("executive_presence")
    )

    speech_quality = safe_score(
        result.get("speech_quality")
    )

    structure = safe_score(
        result.get("structure_score")
    )

    clarity = safe_score(
        result.get("clarity")
    )

    repetition = safe_score(
        result.get("repetition_score")
    )

    overall = safe_score(
        result.get("overall_score")
    )

    # =========================================================
    # SPEECH STATS
    # =========================================================

    words, duration, wpm = calculate_speech_stats(
        result
    )

    # =========================================================
    # HERO
    # =========================================================

    st.success(
        "✅ Analysis loaded successfully"
    )

    if overall is not None:

        st.metric(
            "🏆 Overall PersonaMirror Score",
            f"{overall:g}/100"
        )

    else:

        st.metric(
            "🏆 Overall PersonaMirror Score",
            "Not measured"
        )

    # =========================================================
    # CORE PERFORMANCE
    # =========================================================

    st.subheader(
        "🎯 Core Performance"
    )

    cols = st.columns(4)

    cards = [
        (
            "⭐ Confidence",
            confidence
        ),
        (
            "👑 Leadership",
            leadership
        ),
        (
            "🎤 Voice Confidence",
            voice_confidence
        ),
        (
            "🎥 Presentation",
            presentation
        ),
    ]

    for col, (title, value) in zip(
        cols,
        cards
    ):

        with col:

            st.metric(
                title,
                display_score(value)
            )

    # =========================================================
    # SECONDARY PERFORMANCE
    # =========================================================

    cols = st.columns(4)

    cards = [
        (
            "💼 Executive Presence",
            executive
        ),
        (
            "🗣 Speech Quality",
            speech_quality
        ),
        (
            "🧠 Structure",
            structure
        ),
        (
            "✨ Clarity",
            clarity
        ),
    ]

    for col, (title, value) in zip(
        cols,
        cards
    ):

        with col:

            st.metric(
                title,
                display_score(value)
            )

    # =========================================================
    # PERFORMANCE SIGNALS
    # =========================================================

    st.divider()

    st.subheader(
        "📈 Performance Signals"
    )

    gauge_data = [
        (
            "Confidence",
            confidence
        ),
        (
            "Leadership",
            leadership
        ),
        (
            "Voice Confidence",
            voice_confidence
        ),
    ]

    gauge_cols = st.columns(3)

    for col, (title, value) in zip(
        gauge_cols,
        gauge_data
    ):

        with col:

            fig = make_gauge(
                title,
                value
            )

            if fig is not None:

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.info(
                    f"{title}: Not measured"
                )

    # =========================================================
    # COMMUNICATION PROFILE
    # =========================================================

    st.divider()

    st.subheader(
        "🧠 Communication Profile"
    )

    radar_data = [
        (
            "Confidence",
            confidence
        ),
        (
            "Leadership",
            leadership
        ),
        (
            "Voice",
            voice_confidence
        ),
        (
            "Presentation",
            presentation
        ),
        (
            "Structure",
            structure
        ),
        (
            "Clarity",
            clarity
        ),
    ]

    valid = [
        item
        for item in radar_data
        if item[1] is not None
    ]

    if len(valid) >= 3:

        names = [
            item[0]
            for item in valid
        ]

        values = [
            item[1]
            for item in valid
        ]

        radar = go.Figure()

        radar.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=names + [names[0]],
                fill="toself",
                line=dict(
                    color="#7C3AED"
                ),
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
            use_container_width=True
        )

    else:

        st.info(
            "Not enough measured signals for the communication profile."
        )

    # =========================================================
    # SPEECH INTELLIGENCE
    # =========================================================

    st.divider()

    st.subheader(
        "🗣 Speech Intelligence"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if wpm is not None:

            st.metric(
                "Speaking Rate",
                f"{wpm} WPM"
            )

        else:

            st.metric(
                "Speaking Rate",
                "Not measured"
            )

    with c2:

        if duration > 0:

            minutes = int(duration // 60)
            seconds = int(duration % 60)

            st.metric(
                "⏱ Duration",
                f"{minutes}:{seconds:02d}"
            )

        else:

            st.metric(
                "⏱ Duration",
                "Not measured"
            )

    with c3:

        st.metric(
            "📝 Words",
            words if words > 0 else "Not measured"
        )

    with c4:

        filler_count = result.get(
            "filler_count"
        )

        if filler_count is not None:

            st.metric(
                "🚫 Fillers",
                filler_count
            )

        else:

            st.metric(
                "🚫 Fillers",
                "Not measured"
            )

    # =========================================================
    # REPETITION
    # =========================================================

    st.divider()

    st.subheader(
        "🔁 Repetition Intelligence"
    )

    repeated_words = result.get(
        "repeated_words",
        {}
    )

    if repeated_words:

        sorted_words = sorted(
            repeated_words.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for word, count in sorted_words[:5]:

            st.write(
                f"**{word}** — {count} times"
            )

    else:

        st.info(
            "No significant repeated words detected."
        )

    # =========================================================
    # AI FEEDBACK
    # =========================================================

    st.divider()

    st.subheader(
        "🤖 PersonaMirror AI Feedback"
    )

    feedback = result.get(
        "feedback",
        {}
    )

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

    # ---------------------------------------------------------
    # Strengths
    # ---------------------------------------------------------

    st.markdown(
        "### 💪 Strengths"
    )

    if strengths:

        for item in strengths:

            st.write(
                f"✓ {item}"
            )

    else:

        st.info(
            "No strengths recorded."
        )

    # ---------------------------------------------------------
    # Improvements
    # ---------------------------------------------------------

    st.markdown(
        "### ⚠️ Improvement Areas"
    )

    if improvements:

        for item in improvements:

            st.write(
                f"→ {item}"
            )

    else:

        st.info(
            "No major weakness was identified from the measured signals."
        )

    # ---------------------------------------------------------
    # Suggestions
    # ---------------------------------------------------------

    st.markdown(
        "### 🎯 Personalized Recommendations"
    )

    if suggestions:

        for index, item in enumerate(
            suggestions,
            start=1
        ):

            st.write(
                f"**{index}.** {item}"
            )

    else:

        st.info(
            "No additional recommendations available."
        )

    # =========================================================
    # TRANSCRIPT
    # =========================================================

    st.divider()

    st.subheader(
        "📝 Speech Transcript"
    )

    transcript = result.get(
        "transcript",
        ""
    )

    if transcript:

        with st.expander(
            "View full transcript"
        ):

            st.write(
                transcript
            )

    else:

        st.info(
            "Transcript not available."
        )

    # =========================================================
    # GROWTH LOOP
    # =========================================================

    st.divider()

    st.subheader(
        "🌱 PersonaMirror Growth Loop"
    )

    st.markdown(
        """
        **Analyze → Understand → Practice → Re-analyze → Improve**

        Your current analysis is a baseline.
        The goal is not simply to get a high score —
        it is to become a stronger communicator over time.
        """
    )
