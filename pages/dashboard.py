import streamlit as st
import plotly.graph_objects as go

from modules.analysis_manager import load_results


def gauge(title, value, color):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,

        title={"text": title},

        gauge={
            "axis": {"range": [0, 100]},

            "bar": {"color": color},

            "steps": [
                {"range": [0, 40], "color": "#2E2E2E"},
                {"range": [40, 70], "color": "#444444"},
                {"range": [70, 100], "color": "#666666"},
            ]
        }
    ))

    fig.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=60, b=10)
    )

    return fig


def show():

    st.title("📊 AI Communication Dashboard")

    result = load_results()

    if result["confidence"] == 0:
        st.warning("Please analyze a video first.")
        return

    c1, c2, c3 = st.columns(3)

    with c1:
        st.plotly_chart(
            gauge("Confidence", result["confidence"], "#7C3AED"),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            gauge("Leadership", result["leadership"], "#06B6D4"),
            use_container_width=True
        )

    with c3:
        st.plotly_chart(
            gauge("Eye Contact", result["eye_contact"], "#22C55E"),
            use_container_width=True
        )

    st.divider()

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=[
            result["confidence"],
            result["leadership"],
            result["eye_contact"],
            result["voice_confidence"],
            result["gesture_score"],
            result["posture"],
        ],

        theta=[
            "Confidence",
            "Leadership",
            "Eye Contact",
            "Voice",
            "Gestures",
            "Posture",
        ],

        fill="toself"
    ))

    radar.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100])),
        showlegend=False,
        height=500
    )

    st.subheader("🕸 Personality Radar")

    st.plotly_chart(
        radar,
        use_container_width=True
    )

    st.divider()

    a, b, c = st.columns(3)

    a.metric("😊 Emotion", result["emotion"])
    b.metric("🗣 Speech", f'{result["speech"]} WPM')
    c.metric("👥 Face Visibility", f'{result["visibility"]}%')

    st.divider()

    st.subheader("🤖 AI Summary")

    st.success(result["feedback"]["strengths"])

    st.warning(result["feedback"]["improvements"])

    st.info(result["feedback"]["suggestions"])