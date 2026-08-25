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
    "Deep Learning",
    "AI",
    "Data Analysis",
    "Power BI",
    "Excel",
    "AWS",
    "Docker",
    "Linux",
    "TensorFlow",
    "PyTorch",
    "Flask",
    "Django",
    "REST API",
    "Communication",
    "Leadership",
    "Problem Solving"
]


def job_match(resume_text, jd_text):

    resume = resume_text.lower()
    jd = jd_text.lower()

    jd_skills = []

    resume_skills = []

    for skill in COMMON_SKILLS:

        if skill.lower() in jd:
            jd_skills.append(skill)

        if skill.lower() in resume:
            resume_skills.append(skill)

    matched = [
        s for s in jd_skills
        if s in resume_skills
    ]

    missing = [
        s for s in jd_skills
        if s not in resume_skills
    ]

    if len(jd_skills) == 0:
        score = 0
    else:
        score = int(
            len(matched) /
            len(jd_skills) * 100
        )

    return {

        "score": score,

        "matched": matched,

        "missing": missing
    }