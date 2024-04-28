from app import db
from app.models.grade import Grade
from app.models.student import Student
from app.models.assessment import Assessment
from sqlalchemy import select
from flask import jsonify, request


def save_grades(**kwargs):
    if not request.json:
        return jsonify({"message":"Request must be JSON"}), 400

    _student_id = request.json.get("studentId")
    _assessment_id = request.json.get("selectedAssessment")
    _achieved_grade = request.json.get("newGrade")

    assessment_exists = db.session.execute(select(Assessment).where(Assessment.assessment_id== _assessment_id)).scalars().first()

    if not assessment_exists:
        return jsonify({"error": "Assessment not found"}), 404

    assessment_grade = db.session.execute(select(Grade).where(Grade.student_id == _student_id, Grade.assessment_id == _assessment_id)).scalars().first()

    if assessment_grade:
        update_grade = assessment_grade(
            achieved_grade = _achieved_grade
        )

        db.session.commit()

    new_grade = Grade(
        assessment_id = _assessment_id,
        student_id = _student_id,
        achieved_grade = _achieved_grade
    )

    db.session.add(new_grade)
    db.session.commit()

    return jsonify(new_grade.serialize()), 200


