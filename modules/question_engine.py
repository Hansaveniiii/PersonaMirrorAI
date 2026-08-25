import random


QUESTION_BANK = {

    "Software Engineer": [

        "Tell me about yourself.",

        "What programming languages are you most comfortable with?",

        "Explain Object-Oriented Programming in simple words.",

        "Tell me about one technical project you built.",

        "Describe a bug that took a long time to solve.",

        "Why do you want to become a software engineer?",

        "What is the difference between a process and a thread?",

        "How do you keep yourself updated with technology?"

    ],


    "Data Analyst": [

        "Tell me about yourself.",

        "Explain the difference between Excel and SQL.",

        "Describe a data analysis project.",

        "How would you clean messy data?",

        "Explain data visualization.",

        "What is the importance of statistics?"

    ],


    "AI Engineer": [

        "Tell me about yourself.",

        "What is Machine Learning?",

        "Explain supervised learning.",

        "Describe one AI project.",

        "Difference between CNN and RNN?",

        "How do you evaluate a model?"

    ],


    "HR Interview": [

        "Tell me about yourself.",

        "Why should we hire you?",

        "What are your strengths?",

        "Tell me about your weaknesses.",

        "Describe a challenge you faced.",

        "Where do you see yourself in five years?"

    ],


    "MBA Admission": [

        "Introduce yourself.",

        "Why MBA?",

        "Describe your leadership experience.",

        "Tell me about a failure.",

        "What are your career goals?"

    ],


    "Public Speaking": [

        "Speak about climate change.",

        "Describe your biggest achievement.",

        "Give a motivational speech.",

        "Speak about Artificial Intelligence.",

        "How would you inspire students?"

    ]
}


def get_questions(role, number=5):

    questions = QUESTION_BANK.get(
        role,
        QUESTION_BANK["HR Interview"]
    )

    random.shuffle(questions)

    return questions[:number]