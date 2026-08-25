def rewrite_resume(resume_text, job_description):

    suggestions = []

    resume = resume_text.lower()
    jd = job_description.lower()


    if "project" not in resume:
        suggestions.append(
            "Add project details with technologies used and results."
        )


    if "achievement" not in resume:
        suggestions.append(
            "Add measurable achievements using numbers."
        )


    if "github" not in resume:
        suggestions.append(
            "Add GitHub profile link."
        )


    if "linkedin" not in resume:
        suggestions.append(
            "Add LinkedIn profile."
        )


    keywords = []

    words = jd.split()

    for word in words:

        word = word.strip(".,()")

        if len(word) > 5 and word not in resume:

            keywords.append(word)


    keywords = list(set(keywords))[:10]


    improved = f"""

PROFESSIONAL RESUME IMPROVEMENTS


SUMMARY:

Experienced candidate with skills aligned towards the target role.
Strong focus on problem solving, technical skills and practical projects.


KEYWORDS TO ADD:

{', '.join(keywords)}


IMPROVEMENT SUGGESTIONS:

"""

    for item in suggestions:

        improved += "\n• " + item


    return improved