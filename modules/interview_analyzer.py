import re


def analyze_answer(question, text):

    question = question.lower().strip()
    text = text.strip()

    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)

    if word_count == 0:
        return {
            "score": 0,
            "confidence": 0,
            "fluency": 0,
            "professionalism": 0,
            "communication": 0,
            "word_count": 0,
            "relevance_score": 0,
            "relevant": False,
            "answer_status": "No answer detected",
            "suggestions": [
                "No speech was detected.",
                "Please record your answer again."
            ]
        }

    # -------------------------------------------------
    # QUESTION TYPE
    # -------------------------------------------------

    question_type = "general"

    if (
        "tell me about yourself" in question
        or "introduce yourself" in question
    ):
        question_type = "about_you"

    elif (
        "object-oriented programming" in question
        or "object oriented programming" in question
        or "explain oop" in question
        or "what is oop" in question
    ):
        question_type = "oop"

    elif (
        "technical project" in question
        or "project you built" in question
        or "project you developed" in question
        or "project you created" in question
        or "project have you built" in question
    ):
        question_type = "technical_project"

    elif (
        "why do you want" in question
        or "why do you want to become" in question
        or "why should we hire" in question
    ):
        question_type = "motivation"

    elif (
        "strength" in question
        or "greatest strength" in question
    ):
        question_type = "strength"

    elif (
        "weakness" in question
        or "greatest weakness" in question
    ):
        question_type = "weakness"

    # -------------------------------------------------
    # RELEVANCE ANALYSIS
    # -------------------------------------------------

    relevance_score = 0
    matched_concepts = 0
    strong_evidence = 0

    # -------------------------------------------------
    # TELL ME ABOUT YOURSELF
    # -------------------------------------------------

    if question_type == "about_you":

        personal_concepts = [
            "my name",
            "i am",
            "i'm",
            "currently",
            "i study",
            "i'm studying",
            "student",
            "education",
            "degree",
            "college",
            "university",
            "experience",
            "skills",
            "career",
            "goal",
            "interest",
            "passionate",
            "background"
        ]

        matched_concepts = sum(
            1
            for concept in personal_concepts
            if concept in text_lower
        )

        if "my name" in text_lower:
            strong_evidence += 1

        if "currently" in text_lower:
            strong_evidence += 1

        if "studying" in text_lower or "student" in text_lower:
            strong_evidence += 1

        if "experience" in text_lower:
            strong_evidence += 1

        if "skills" in text_lower:
            strong_evidence += 1

        if "goal" in text_lower or "career" in text_lower:
            strong_evidence += 1

        relevance_score = min(
            100,
            matched_concepts * 8
            + strong_evidence * 8
        )

    # -------------------------------------------------
    # OBJECT ORIENTED PROGRAMMING
    # -------------------------------------------------

    elif question_type == "oop":

        core_concepts = [
            "class",
            "object",
            "encapsulation",
            "inheritance",
            "polymorphism",
            "abstraction",
            "method",
            "attribute",
            "constructor",
            "instance"
        ]

        explanation_concepts = [
            "blueprint",
            "real world",
            "data",
            "behavior",
            "reuse",
            "security",
            "hide",
            "parent",
            "child",
            "overriding",
            "overloading"
        ]

        core_hits = sum(
            1
            for concept in core_concepts
            if re.search(
                r"\b" + re.escape(concept) + r"\b",
                text_lower
            )
        )

        explanation_hits = sum(
            1
            for concept in explanation_concepts
            if concept in text_lower
        )

        matched_concepts = core_hits + explanation_hits

        if core_hits >= 1:
            strong_evidence += 1

        if core_hits >= 2:
            strong_evidence += 1

        if core_hits >= 3:
            strong_evidence += 1

        if explanation_hits >= 1:
            strong_evidence += 1

        relevance_score = min(
            100,
            core_hits * 18
            + explanation_hits * 8
        )

    # -------------------------------------------------
    # TECHNICAL PROJECT
    # -------------------------------------------------

    elif question_type == "technical_project":

        project_actions = [
            "i built",
            "i developed",
            "i created",
            "i designed",
            "i implemented",
            "i programmed",
            "i made",
            "i worked on",
            "my project",
            "my application",
            "my app",
            "my website",
            "i developed a",
            "i built a",
            "i created a"
        ]

        technologies = [
            "python",
            "java",
            "c++",
            "c programming",
            "javascript",
            "html",
            "css",
            "react",
            "streamlit",
            "opencv",
            "tensorflow",
            "pytorch",
            "sql",
            "database",
            "api",
            "machine learning",
            "artificial intelligence",
            "ai"
        ]

        project_components = [
            "application",
            "app",
            "website",
            "software",
            "system",
            "platform",
            "tool",
            "model",
            "program",
            "project"
        ]

        problem_solving = [
            "problem",
            "challenge",
            "solved",
            "solution",
            "implemented",
            "feature",
            "functionality",
            "algorithm"
        ]

        results = [
            "result",
            "improved",
            "increased",
            "reduced",
            "saved",
            "achieved",
            "users",
            "completed",
            "successfully",
            "worked",
            "performance"
        ]

        action_hits = sum(
            1
            for phrase in project_actions
            if phrase in text_lower
        )

        technology_hits = sum(
            1
            for tech in technologies
            if tech in text_lower
        )

        component_hits = sum(
            1
            for component in project_components
            if re.search(
                r"\b" + re.escape(component) + r"\b",
                text_lower
            )
        )

        problem_hits = sum(
            1
            for item in problem_solving
            if item in text_lower
        )

        result_hits = sum(
            1
            for item in results
            if item in text_lower
        )

        # A project answer needs PERSONAL ACTION.
        if action_hits >= 1:
            strong_evidence += 2

        if technology_hits >= 1:
            strong_evidence += 1

        if component_hits >= 1:
            strong_evidence += 1

        if problem_hits >= 1:
            strong_evidence += 1

        if result_hits >= 1:
            strong_evidence += 1

        relevance_score = (
            min(action_hits * 25, 40)
            + min(technology_hits * 10, 20)
            + min(component_hits * 5, 15)
            + min(problem_hits * 5, 10)
            + min(result_hits * 5, 15)
        )

        # Merely saying "I have projects" is not enough.
        if action_hits == 0:
            relevance_score = min(
                relevance_score,
                20
            )

    # -------------------------------------------------
    # MOTIVATION
    # -------------------------------------------------

    elif question_type == "motivation":

        motivation_concepts = [
            "because",
            "passionate",
            "interested",
            "love",
            "enjoy",
            "goal",
            "career",
            "technology",
            "software",
            "engineering",
            "learning",
            "problem solving",
            "solving problems",
            "future",
            "contribute",
            "grow"
        ]

        matched_concepts = sum(
            1
            for concept in motivation_concepts
            if concept in text_lower
        )

        relevance_score = min(
            100,
            matched_concepts * 10
        )

    # -------------------------------------------------
    # STRENGTH
    # -------------------------------------------------

    elif question_type == "strength":

        strength_concepts = [
            "strength",
            "good at",
            "strong at",
            "communication",
            "leadership",
            "problem solving",
            "teamwork",
            "discipline",
            "creative",
            "logical",
            "adapt",
            "learn",
            "organized",
            "responsible"
        ]

        matched_concepts = sum(
            1
            for concept in strength_concepts
            if concept in text_lower
        )

        relevance_score = min(
            100,
            matched_concepts * 12
        )

    # -------------------------------------------------
    # WEAKNESS
    # -------------------------------------------------

    elif question_type == "weakness":

        weakness_concepts = [
            "weakness",
            "improve",
            "improving",
            "challenge",
            "difficulty",
            "struggle",
            "learning",
            "working on",
            "better",
            "development"
        ]

        matched_concepts = sum(
            1
            for concept in weakness_concepts
            if concept in text_lower
        )

        relevance_score = min(
            100,
            matched_concepts * 12
        )

    # -------------------------------------------------
    # GENERAL QUESTION
    # -------------------------------------------------

    else:

        question_words = set(
            re.findall(
                r"\b[a-z]{4,}\b",
                question
            )
        )

        answer_words = set(
            re.findall(
                r"\b[a-z]{4,}\b",
                text_lower
            )
        )

        ignored_words = {
            "what",
            "tell",
            "about",
            "explain",
            "describe",
            "your",
            "does",
            "this",
            "that",
            "with",
            "from",
            "have",
            "would",
            "could",
            "should",
            "please"
        }

        question_words -= ignored_words

        matches = question_words.intersection(
            answer_words
        )

        if len(question_words) > 0:

            keyword_ratio = (
                len(matches)
                / len(question_words)
            )

            relevance_score = int(
                keyword_ratio * 100
            )

        else:
            relevance_score = 50

    # -------------------------------------------------
    # FINAL RELEVANCE LIMITS
    # -------------------------------------------------

    relevance_score = min(
        100,
        max(
            0,
            relevance_score
        )
    )

    # -------------------------------------------------
    # IMPORTANT ANTI-FALSE-POSITIVE RULES
    # -------------------------------------------------

    if question_type == "technical_project":

        if strong_evidence < 2:
            relevance_score = min(
                relevance_score,
                35
            )

        if (
            "tell me about yourself" not in question
            and action_hits == 0
        ):
            relevance_score = min(
                relevance_score,
                25
            )

    if question_type == "oop":

        if strong_evidence == 0:
            relevance_score = min(
                relevance_score,
                15
            )

    # -------------------------------------------------
    # ANSWER STATUS
    # -------------------------------------------------

    if relevance_score < 25:

        relevant = False
        answer_status = "❌ Irrelevant Answer"

    elif relevance_score < 50:

        relevant = False
        answer_status = "⚠️ Partially Relevant"

    elif relevance_score < 70:

        relevant = True
        answer_status = "✅ Relevant Answer"

    else:

        relevant = True
        answer_status = "✅ Strongly Relevant Answer"

    # -------------------------------------------------
    # FLUENCY
    # -------------------------------------------------

    if word_count >= 120:
        fluency = 95

    elif word_count >= 80:
        fluency = 88

    elif word_count >= 50:
        fluency = 78

    elif word_count >= 30:
        fluency = 65

    else:
        fluency = 50

    # -------------------------------------------------
    # CONFIDENCE
    # -------------------------------------------------

    confidence_words = [
        "achieved",
        "led",
        "managed",
        "developed",
        "created",
        "improved",
        "designed",
        "built",
        "implemented",
        "successfully",
        "solved",
        "completed"
    ]

    confidence_hits = sum(
        1
        for word in confidence_words
        if re.search(
            r"\b" + re.escape(word) + r"\b",
            text_lower
        )
    )

    confidence = min(
        100,
        60 + confidence_hits * 5
    )

    # -------------------------------------------------
    # PROFESSIONALISM
    # -------------------------------------------------

    professionalism = 60

    professional_words = [
        "experience",
        "project",
        "team",
        "technology",
        "developed",
        "created",
        "problem",
        "solution",
        "learning",
        "career",
        "education"
    ]

    professional_hits = sum(
        1
        for word in professional_words
        if word in text_lower
    )

    professionalism += professional_hits * 4

    professionalism = min(
        100,
        professionalism
    )

    # -------------------------------------------------
    # COMMUNICATION
    # -------------------------------------------------

    sentences = re.split(
        r"[.!?]+",
        text
    )

    sentences = [
        sentence
        for sentence in sentences
        if sentence.strip()
    ]

    sentence_count = max(
        1,
        len(sentences)
    )

    average_sentence = (
        word_count / sentence_count
    )

    if average_sentence < 10:
        communication = 70

    elif average_sentence < 22:
        communication = 90

    else:
        communication = 75

    # -------------------------------------------------
    # QUESTION-SPECIFIC SUGGESTIONS
    # -------------------------------------------------

    suggestions = []

    if not relevant:

        suggestions.append(
            "Your answer does not directly answer the question asked."
        )

        suggestions.append(
            "Do not reuse a memorized answer from another interview question."
        )

    if question_type == "technical_project":

        if action_hits == 0:

            suggestions.append(
                "Explain what YOU personally built, developed or implemented."
            )

        if technology_hits == 0:

            suggestions.append(
                "Mention the programming languages, frameworks or tools you used."
            )

        if problem_hits == 0:

            suggestions.append(
                "Explain the problem or challenge your project solved."
            )

        if result_hits == 0:

            suggestions.append(
                "Explain the result, outcome or impact of your project."
            )

    elif question_type == "oop":

        if matched_concepts == 0:

            suggestions.append(
                "Your answer should explain OOP concepts such as classes, objects, inheritance, encapsulation or polymorphism."
            )

        elif matched_concepts < 2:

            suggestions.append(
                "Add a simple real-world example to explain Object-Oriented Programming."
            )

    elif question_type == "about_you":

        if "studying" not in text_lower and "student" not in text_lower:

            suggestions.append(
                "Mention your current education or academic background."
            )

        if "skills" not in text_lower:

            suggestions.append(
                "Mention 2 or 3 skills that are relevant to the role."
            )

        if "goal" not in text_lower and "career" not in text_lower:

            suggestions.append(
                "End with your career goal or what you want to contribute."
            )

    if word_count < 40:

        suggestions.append(
            "Add specific details instead of giving a very short answer."
        )

    if confidence_hits < 2:

        suggestions.append(
            "Use specific action words such as built, created, solved, led or implemented."
        )

    # -------------------------------------------------
    # OVERALL SCORE
    # -------------------------------------------------

    if not relevant:

        overall = int(
            relevance_score * 0.70
            + fluency * 0.10
            + professionalism * 0.10
            + communication * 0.10
        )

    else:

        overall = int(
            relevance_score * 0.45
            + fluency * 0.15
            + confidence * 0.15
            + professionalism * 0.10
            + communication * 0.15
        )

    # -------------------------------------------------
    # RETURN
    # -------------------------------------------------

    return {
        "score": overall,
        "confidence": confidence,
        "fluency": fluency,
        "professionalism": professionalism,
        "communication": communication,
        "word_count": word_count,
        "relevance_score": relevance_score,
        "relevant": relevant,
        "answer_status": answer_status,
        "suggestions": suggestions
    }