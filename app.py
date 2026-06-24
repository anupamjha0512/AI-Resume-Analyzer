from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

skills_db = [
    "python",
    "java",
    "c++",
    "c",
    "sql",
    "html",
    "css",
    "javascript",
    "flask",
    "react",
    "git",
    "github",
    "machine learning",
    "data structures",
    "oop",
    "dbms"
]

required_skills = [
    "python",
    "sql",
    "git",
    "dbms",
    "oop"
]


def extract_text(pdf_path):
    text = ""

    try:
        reader = PdfReader(pdf_path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text.lower()

    except Exception as e:
        print(e)

    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]

    if file.filename == "":
        return "No file selected"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    resume_text = extract_text(filepath)

    found_skills = []

    for skill in skills_db:
        if skill in resume_text:
            found_skills.append(skill)

    score = 50 + (len(found_skills) * 5)

    if score > 95:
        score = 95

    missing_skills = []

    for skill in required_skills:
        if skill not in found_skills:
            missing_skills.append(skill)

    recommendations = []

    if len(missing_skills) == 0:

        recommendations.append(
            "Great technical skill coverage."
        )

        recommendations.append(
            "Add more projects and achievements to strengthen your resume."
        )

    else:

        for skill in missing_skills:

            if skill == "python":
                recommendations.append(
                    "Add Python projects to strengthen your profile."
                )

            elif skill == "sql":
                recommendations.append(
                    "Learn SQL and include database projects."
                )

            elif skill == "git":
                recommendations.append(
                    "Add GitHub repositories to showcase your work."
                )

            elif skill == "dbms":
                recommendations.append(
                    "Mention DBMS coursework or database projects."
                )

            elif skill == "oop":
                recommendations.append(
                    "Highlight OOP concepts and projects."
                )

    return render_template(
        "result.html",
        filename=file.filename,
        score=score,
        skills=found_skills,
        missing_skills=missing_skills,
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)