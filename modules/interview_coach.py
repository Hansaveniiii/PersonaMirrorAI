def generate_interview_feedback(
    question,
    answer,
    voice_data=None,
    analysis=None
):

    if voice_data is None:
        voice_data = {}

    if analysis is None:
        analysis = {}

    question_lower = question.lower()
    answer_lower = answer.lower()

    relevance_score = analysis.get(
        "relevance_score",
        0
    )

    relevant = analysis.get(
        "relevant",
        False
    )

    answer_status = analysis.get(
        "answer_status",
        "Unknown"
    )

    score = analysis.get(
        "score",
        0
    )

    fluency = analysis.get(
        "fluency",
        0
    )

    professionalism = analysis.get(
        "professionalism",
        0
    )

    word_count = analysis.get(
        "word_count",
        0
    )

    suggestions = analysis.get(
        "suggestions",
        []
    )

    # --------------------------------
    # QUESTION-SPECIFIC FEEDBACK
    # --------------------------------

    if not relevant:

        answer_review = f"""
❌ **Your answer does not match the question.**

**Question asked:**
{question}

**Your answer:**
{answer}

**Relevance Score:** {relevance_score}/100

The system detected that your response is talking about a different topic.

Do not try to improve this answer by simply adding more words.

Instead, answer the question that was actually asked.
"""

        if (
            "object-oriented" in question_lower
            or "object oriented" in question_lower
            or "oop" in question_lower
        ):

            answer_review += """
For this question, you should explain concepts such as:

• Classes
• Objects
• Encapsulation
• Inheritance
• Polymorphism
• Abstraction

Use a simple real-world example to explain them.
"""

        elif (
            "technical project" in question_lower
            or "project you built" in question_lower
            or "project you developed" in question_lower
        ):

            answer_review += """
For this question, describe ONE real project you personally built.

Include:

• What you built
• Why you built it
• Technologies you used
• What YOU personally did
• A problem you faced
• How you solved it
• The final result
"""

        elif "tell me about yourself" in question_lower:

            answer_review += """
For this question, focus on yourself.

A good structure is:

• Who you are
• Your education
• Your technical interests
• Your relevant experience or projects
• Your career goal
"""

        else:

            answer_review += """
Read the question carefully and make sure your answer directly addresses its main topic.
"""

    else:

        answer_review = f"""
✅ **Your answer is relevant to the question.**

**Relevance Score:** {relevance_score}/100

Your response addresses the main topic of the question.

Now focus on making the answer more specific and personal.
"""

        if (
            "technical project" in question_lower
            or "project you built" in question_lower
            or "project you developed" in question_lower
        ):

            answer_review += """
For an even stronger project answer, explain:

• What YOU built
• Your exact role
• Technologies used
• Technical challenges
• How you solved them
• The result or impact
"""

        elif (
            "object-oriented" in question_lower
            or "object oriented" in question_lower
            or "oop" in question_lower
        ):

            answer_review += """
A strong explanation should include simple examples of classes and objects and briefly explain the major OOP concepts.
"""

        elif "tell me about yourself" in question_lower:

            answer_review += """
Keep the introduction focused on your education, technical interests, projects, strengths and career direction.
"""

    # --------------------------------
    # COMMUNICATION REVIEW
    # --------------------------------

    if fluency >= 85:

        communication = """
✅ Your answer has good fluency.

Keep your delivery natural and avoid unnecessary repetition.
"""

    elif fluency >= 70:

        communication = """
⚠️ Your fluency is reasonable.

Try to make your sentences smoother and reduce unnecessary pauses.
"""

    else:

        communication = """
⚠️ Your fluency needs improvement.

Speak in complete sentences and maintain a steady pace.
"""

    # --------------------------------
    # VOICE REVIEW
    # --------------------------------

    speech_rate = voice_data.get(
        "speech_rate",
        0
    )

    if speech_rate:

        voice_review = f"""
### 🎤 Voice Analysis

**Speech Rate:** {speech_rate} WPM

Your speech rate was measured from the recorded answer.
"""

        if speech_rate < 110:

            voice_review += """
You are speaking somewhat slowly. Try to maintain a natural conversational pace.
"""

        elif speech_rate > 170:

            voice_review += """
You are speaking quite quickly. Slow down slightly so your points are easier to follow.
"""

        else:

            voice_review += """
Your speaking pace is within a reasonable interview range.
"""

    else:

        voice_review = """
### 🎤 Voice Analysis

Voice information was not available for this recording.
"""

    # --------------------------------
    # SUGGESTIONS
    # --------------------------------

    suggestion_text = ""

    if suggestions:

        suggestion_text = """
### 💡 Specific Improvements

"""

        for suggestion in suggestions:

            suggestion_text += (
                "- "
                + str(suggestion)
                + "\n"
            )

    # --------------------------------
    # FINAL COACH MESSAGE
    # --------------------------------

    if not relevant:

        final_advice = """
### 🚨 Most Important Improvement

Your biggest issue is **question relevance**, not answer length.

Before trying to sound more professional, make sure you are answering the question that was asked.

A polished answer to the wrong question is still a wrong interview answer.
"""

    else:

        final_advice = """
### 🧠 Final AI Coach Advice

Your answer addresses the question.

To make it stronger, add specific examples from your own experience and clearly explain your personal contribution.

Avoid memorized or generic statements.
"""

    # --------------------------------
    # FINAL REPORT
    # --------------------------------

    report = f"""
# 🧠 PersonaMirror AI Interview Coach

## Interview Question

{question}

---

## Your Answer

{answer}

---

# 📊 Answer Relevance

**Status:** {answer_status}

**Relevance Score:** {relevance_score}/100

---

# 📝 Answer Review

{answer_review}

---

# 🗣️ Communication Review

{communication}

---

{voice_review}

---

# 📈 AI Evaluation

**Overall Score:** {score}/100

**Fluency:** {fluency}/100

**Professionalism:** {professionalism}/100

**Word Count:** {word_count}

---

{suggestion_text}

---

{final_advice}
"""

    return report