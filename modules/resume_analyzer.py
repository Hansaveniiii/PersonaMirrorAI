import re

COMMON_SKILLS = [
    "Python",
    "Java",
    "C++",
    "C",
    "SQL",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node",
    "Git",
    "GitHub",
    "Machine Learning",
    "AI",
    "Data Analysis",
    "Excel",
    "Power BI",
    "Communication",
    "Leadership",
    "Teamwork",
    "Problem Solving",
    "AWS",
    "Docker"
]


def analyze_resume(text):

    text_lower = text.lower()

    detected = []

    for skill in COMMON_SKILLS:
        if skill.lower() in text_lower:
            detected.append(skill)

    ats = 40

    ats += min(len(detected) * 3, 30)

    if "education" in text_lower:
        ats += 5

    if "experience" in text_lower:
        ats += 10

    if "project" in text_lower:
        ats += 10

    if "achievement" in text_lower:
        ats += 5

    ats = min(ats, 100)

    missing = [
        s for s in COMMON_SKILLS
        if s not in detected
    ][:10]

    strengths = []

    if len(detected) > 8:
        strengths.append("Strong technical skillset")

    if "project" in text_lower:
        strengths.append("Projects included")

    if "experience" in text_lower:
        strengths.append("Work experience present")

    if "achievement" in text_lower:
        strengths.append("Achievements mentioned")

    improvements = []

    if "summary" not in text_lower:
        improvements.append("Add Professional Summary")

    if "github" not in text_lower:
        improvements.append("Add GitHub profile")

    if "linkedin" not in text_lower:
        improvements.append("Add LinkedIn profile")

    if len(detected) < 8:
        improvements.append("Add more technical skills")

    recruiter = (
        "This resume has good potential but can become stronger by "
        "adding measurable achievements, action verbs, projects and "
        "industry keywords."
    )

    return {

        "ats": ats,

        "skills": detected,

        "missing": missing,

        "strengths": strengths,

        "improvements": improvements,

        "recruiter": recruiter
    }