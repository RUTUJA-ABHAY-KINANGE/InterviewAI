import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=api_key)


def ask_ai(prompt):
    """Send a prompt to Groq and return the response."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

def generate_questions(role):
    """
    Generate 5 interview questions for the selected role.
    """

    with open("prompts/question_prompt.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Generate interview questions for {role}"
            }
        ],
        temperature=0.7
    )

    questions = response.choices[0].message.content

    question_list = []

    for line in questions.split("\n"):
        line = line.strip()

        if line and line[0].isdigit():
            question = line.split(".", 1)[1].strip()
            question_list.append(question)

    return question_list[:5]

if __name__ == "__main__":
    print(generate_questions("Python Developer"))

def evaluate_interview(candidate_name, role, questions, answers):

    with open("prompts/evaluation_prompt.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()

    interview_text = f"""
Candidate Name: {candidate_name}

Role: {role}

"""

    for i in range(len(questions)):
        interview_text += f"""
Question {i+1}:
{questions[i]}

Answer:
{answers[i]}

"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": interview_text
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content