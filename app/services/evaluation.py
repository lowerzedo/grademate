from app.models.student import Student
from flask import jsonify, request
from app.services.StudentEvaluation import StudentEvaluator

from app.services.delete_this_later import grades, subjects
from app.models.subject_grade import SubjectGrade
from app.models.subject import Subject
from app.models.student import Student
from app import db
from sqlalchemy import select

# defining the evaluation object
studentEvaluate = StudentEvaluator()

def evaluate_student(**kwargs):
    if not request.json:
        return jsonify({"message": "Request must be JSON"}), 400

    student_id = request.json.get("student_id")
    if not student_id:
        student_id = "A121031"

    # Fetching subject grades for the student
    subject_grades_query = (
        select(SubjectGrade.achieved_grade, Subject.name, Subject.code)
        .join(Subject, SubjectGrade.subject_id == Subject.subject_id)
        .where(SubjectGrade.student_id == student_id)
    )
    subject_grades_result = db.session.execute(subject_grades_query).fetchall()

    grades = {}
    for grade in subject_grades_result:
        grades[grade.name] = {
            "code": grade.code,
            "grade": grade.achieved_grade,
        }

    # Fetching subjects with details
    subjects_result = db.session.execute(select(Subject)).scalars().all()


    subjects = {}
    for subject in subjects_result:
        subjects[subject.name] = {
            "code": subject.code,
            "description": subject.description,
            "topics": subject.topics.split(", ") if subject.topics else []
        }

    # Call the StudentEvaluator to get the evaluation (assuming it needs grades and subjects as input)
    output = studentEvaluate.evaluate_student(grades=grades, subjects=subjects)

    return jsonify(output)

