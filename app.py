from flask import Flask, render_template, request
from utils.ai import generate_questions, evaluate_interview

import json
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/interview", methods=["POST"])
def interview():

    candidate_name = request.form["candidate_name"]
    role = request.form["role"]

    questions = generate_questions(role)

    return render_template(
        "interview.html",
        candidate_name=candidate_name,
        role=role,
        questions=questions
    )

@app.route("/evaluate", methods=["POST"])
def evaluate():

    candidate_name = request.form["candidate_name"]
    role = request.form["role"]

    questions = []
    answers = []

    # Read all 5 questions and answers

    i = 0

    while f"question{i}" in request.form:
        questions.append(request.form[f"question{i}"])
        answers.append(request.form[f"answer{i}"])
        i += 1
    

    # Get AI evaluation
    report = evaluate_interview(
        candidate_name,
        role,
        questions,
        answers
    )

    record = {
    "candidate": candidate_name,
    "role": role,
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "report": report
    }


    os.makedirs("data", exist_ok=True)
    file_path = "data/interviews.json"

    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                interviews = json.load(f)
        except json.JSONDecodeError:
            interviews = []
    else:
        interviews = []

    interviews.append(record)

    with open(file_path, "w") as f:
        json.dump(interviews, f, indent=4)

    return render_template(
        "result.html",
        candidate_name=candidate_name,
        role=role,
        report=report
    )

if __name__ == "__main__":
    app.run(debug=True)