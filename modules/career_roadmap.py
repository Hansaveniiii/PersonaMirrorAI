def generate_roadmap(goal):

    goal = goal.lower()

    if "software" in goal or "sde" in goal:

        return """
# 🚀 Software Engineer Roadmap

Week 1
• Python
• DSA

Week 2
• OOP
• SQL

Week 3
• Web Development
• Git & GitHub

Week 4
• Projects
• Resume
• Mock Interviews

Final Goal
Become interview ready.
"""

    elif "data" in goal:

        return """
# 📊 Data Scientist Roadmap

Week 1
Python
Statistics

Week 2
Pandas
NumPy

Week 3
Machine Learning

Week 4
Projects
Kaggle
Resume
"""

    elif "ai" in goal:

        return """
# 🤖 AI Engineer Roadmap

Python

Machine Learning

Deep Learning

Computer Vision

NLP

LLMs

Projects

Deployment
"""

    else:

        return """
Choose a career goal.

Examples:

Software Engineer

AI Engineer

Data Scientist

Cyber Security

Cloud Engineer
"""