import os
import streamlit as st


def show():

    # =========================================================
    # FOUNDER HERO
    # =========================================================

    st.html(
        """
        <section class="founder-hero">

            <div class="founder-badge">
                FOUNDER • PERSONAMIRROR AI
            </div>

            <h1>
                Meet the Mind Behind<br>
                PersonaMirror AI
            </h1>

            <p class="founder-tagline">
                Building intelligent technology at the intersection of
                communication, artificial intelligence and human growth.
            </p>

        </section>
        """,
    )

    st.write("")

    # =========================================================
    # FOUNDER PROFILE
    # =========================================================

    col1, col2 = st.columns([1, 1.6], gap="large")

    with col1:

        image_path = None

        if os.path.exists("assets/images/founder.jpg"):
            image_path = "assets/images/founder.jpg"

        elif os.path.exists("assets/images/founder.png"):
            image_path = "assets/images/founder.png"

        if image_path:

            st.image(
                image_path,
                use_container_width=True
            )

        else:

            st.info("Founder image not found.")

    with col2:

        st.html(
            """
            <div class="founder-profile-card">

                <div class="small-label">
                    FOUNDER & DEVELOPER
                </div>

                <h2>
                    Hansaveni Bhardwaj
                </h2>

                <p>
                    Founder and creator of <strong>PersonaMirror AI</strong>,
                    an emerging communication intelligence platform built
                    around a simple belief: meaningful improvement begins
                    with an honest understanding of how we present ourselves.
                </p>

                <p>
                    My work brings together software development, artificial
                    intelligence, public communication and human-centred
                    design to create technology that does more than measure
                    performance. It should help people understand it.
                </p>

                <div class="founder-quote">
                    “See Yourself. Improve Yourself.”
                </div>

            </div>
            """,
        )

    st.write("")
    st.divider()

    # =========================================================
    # STORY
    # =========================================================

    st.markdown("## ✨ The Story Behind PersonaMirror AI")

    st.html(
        """
        <div class="story-card">

            Communication shapes how ideas are received, how leaders are
            perceived and how confidently people move through the world.

            <br><br>

            Yet communication is surprisingly difficult to evaluate.
            We can listen to ourselves, watch a recording and still miss
            the small patterns that influence our delivery.

            <br><br>

            A pause that changes the rhythm of a sentence.
            A repeated phrase.
            A shift in vocal energy.
            A moment when expression disappears.
            A delivery pattern that the speaker may never notice.

            <br><br>

            <strong>
                PersonaMirror AI is being built to make those patterns
                easier to see and understand.
            </strong>

            <br><br>

            The ambition is not to reduce communication to a single
            number. It is to combine measurable signals with context,
            thoughtful interpretation and useful guidance so that every
            recording can become an opportunity for improvement.

        </div>
        """,
    )

    st.write("")
    st.divider()

    # =========================================================
    # FOUNDER JOURNEY
    # =========================================================

    st.markdown("## 🚀 The Founder Journey")

    journey = [
        (
            "🎤",
            "Public Speaking",
            "A lasting interest in speaking and presenting ideas created the foundation for understanding communication from the speaker's perspective."
        ),
        (
            "🏆",
            "Leadership",
            "Leadership experiences strengthened the conviction that influence is inseparable from clarity, presence and the ability to connect with people."
        ),
        (
            "🗣️",
            "Debate & Expression",
            "Debate and public expression developed an appreciation for argument, structure, persuasion and the precision of language."
        ),
        (
            "💻",
            "Technology",
            "Learning Python, artificial intelligence and software development opened a way to transform those interests into something practical."
        ),
        (
            "🧠",
            "PersonaMirror AI",
            "Communication, technology and curiosity eventually converged into the idea behind PersonaMirror AI."
        ),
    ]

    cols = st.columns(5)

    for col, item in zip(cols, journey):

        icon, title, description = item

        with col:

            st.html(
                f"""
                <div class="journey-card">

                    <div class="journey-icon">
                        {icon}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                </div>
                """,
            )

    st.write("")
    st.divider()

    # =========================================================
    # WHY PERSONAMIRROR
    # =========================================================

    st.markdown("## 🪞 Why PersonaMirror AI?")

    col1, col2 = st.columns(2, gap="large")

    with col1:

        st.html(
            """
            <div class="vision-card">

                <div class="small-label">
                    THE PROBLEM
                </div>

                <h2>
                    Feedback is often too generic.
                </h2>

                <p>
                    Speak more confidently.
                    Improve your eye contact.
                    Use stronger body language.
                </p>

                <p>
                    Advice like this can be useful, but it often stops
                    before answering the question that matters most:
                    <strong>what actually happened in this recording?</strong>
                </p>

                <p>
                    Good coaching should begin with evidence rather than
                    assumptions.
                </p>

            </div>
            """,
        )

    with col2:

        st.html(
            """
            <div class="vision-card highlight">

                <div class="small-label">
                    THE IDEA
                </div>

                <h2>
                    Feedback should reflect the individual.
                </h2>

                <p>
                    PersonaMirror AI is designed to move beyond generic
                    communication advice by examining the actual recording,
                    the selected context and the measurable signals available
                    from that performance.
                </p>

                <p>
                    A ceremonial speech should not be evaluated like a job
                    interview. A presentation should not receive the same
                    coaching as a casual conversation.
                </p>

                <p>
                    <strong>
                        Context changes what good communication looks like.
                    </strong>
                </p>

            </div>
            """,
        )

    st.write("")
    st.divider()

    # =========================================================
    # WHAT WE ARE BUILDING
    # =========================================================

    st.markdown("## 🧠 What We Are Building")

    features = [
        (
            "🎥",
            "Communication Intelligence",
            "Analyse speech delivery, pacing, vocal energy and observable communication patterns."
        ),
        (
            "🎤",
            "Presentation Intelligence",
            "Help speakers understand their delivery and identify patterns that may strengthen their presentations."
        ),
        (
            "💼",
            "Interview Intelligence",
            "Evaluate interview communication with criteria designed specifically for professional conversations."
        ),
        (
            "📄",
            "Career Intelligence",
            "Connect communication insights with resumes, opportunities and professional development."
        ),
        (
            "🤖",
            "Personalised AI Coaching",
            "Transform measured observations into recommendations that reflect the recording and its context."
        ),
        (
            "📊",
            "Progress Tracking",
            "Compare future recordings and make improvement visible over time rather than relying only on memory."
        ),
    ]

    cols = st.columns(3)

    for index, item in enumerate(features):

        icon, title, description = item

        with cols[index % 3]:

            st.html(
                f"""
                <div class="feature-card">

                    <div class="feature-icon">
                        {icon}
                    </div>

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                </div>
                """,
            )

    st.write("")
    st.divider()

    # =========================================================
    # TECHNOLOGY
    # =========================================================

    st.markdown("## ⚙️ The Technology Behind It")

    technologies = [
        (
            "Python",
            "Application logic, data processing and AI integration."
        ),
        (
            "Streamlit",
            "The interactive application layer powering the platform."
        ),
        (
            "OpenCV",
            "Computer vision and visual signal analysis."
        ),
        (
            "Faster-Whisper",
            "Efficient speech transcription and spoken-content analysis."
        ),
        (
            "Librosa",
            "Audio processing and voice-signal analysis."
        ),
        (
            "Machine Learning",
            "Pattern analysis and intelligent interpretation."
        ),
    ]

    cols = st.columns(3)

    for index, item in enumerate(technologies):

        title, description = item

        with cols[index % 3]:

            st.html(
                f"""
                <div class="tech-card">

                    <h3>
                        {title}
                    </h3>

                    <p>
                        {description}
                    </p>

                </div>
                """,
            )

    st.write("")
    st.divider()

    # =========================================================
    # VISION
    # =========================================================

    st.html(
        """
        <div class="vision-hero">

            <div class="small-label">
                THE VISION
            </div>

            <h1>
                Make self-improvement measurable.
            </h1>

            <p>
                Imagine recording yourself speaking and receiving an
                intelligent reflection of your communication: what worked,
                what changed, what deserves attention and what can be
                improved next.
            </p>

            <p>
                Not a generic checklist.
                Not an arbitrary judgement.
                A thoughtful interpretation of your own performance.
            </p>

            <p>
                <strong>
                    That is the direction PersonaMirror AI is being built toward.
                </strong>
            </p>

        </div>
        """,
    )

    st.write("")
    st.divider()

    # =========================================================
    # FOUNDER NOTE
    # =========================================================

    st.markdown("## 💜 A Note From the Founder")

    st.html(
        """
        <div class="founder-note">

            I have always believed that growth begins with awareness.

            <br><br>

            We spend years learning how to speak, present, interview,
            lead and express ideas, yet very little of that learning
            teaches us how to objectively observe ourselves.

            <br><br>

            A recording can reveal something we did not notice in the
            moment. A repeated phrase. A change in pace. A hesitation.
            A strength we had underestimated. A habit that quietly affects
            the way our message is received.

            <br><br>

            That is the idea behind PersonaMirror AI.

            <br><br>

            I do not want to build technology that simply assigns people
            a score and tells them what they did wrong. I want to build
            something that encourages curiosity about one's own
            communication and turns observation into meaningful progress.

            <br><br>

            The long-term ambition is to create a system that becomes
            increasingly thoughtful about context, increasingly precise
            about evidence and increasingly useful in the guidance it gives.

            <br><br>

            Because improvement should never be about becoming someone else.

            <br><br>

            It should be about understanding yourself well enough to
            become a stronger version of who you already are.

            <br><br>

            <strong>
                See Yourself. Improve Yourself.
            </strong>

        </div>
        """,
    )

    st.write("")
    st.divider()

    # =========================================================
    # FINAL CTA
    # =========================================================

    st.html(
        """
        <div class="founder-final">

            <h2>
                PersonaMirror AI
            </h2>

            <p>
                Understand yourself. Communicate with intention.
                Grow with clarity.
            </p>

            <div class="founder-badge">
                BUILT WITH AI • BUILT FOR GROWTH
            </div>

        </div>
        """,
    )