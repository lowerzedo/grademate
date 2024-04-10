from app import db
from app.models.assessment import Assessment
from app.models.grade import Grade
from app.models.subject import Subject
from app.models.student import Student
from app.models.semester import Semester
from app.models.program import Program
from flask import jsonify, request, abort
from sqlalchemy import select

def student_class_code(**kwargs):

    student_id = request.json.get("student_id")

    student_exist = db.session.execute(select(Student).where(Student.student_id == student_id)).scalars().first()

    if not student_exist:
        abort(404, "Student doesn't exist")

    stmt = (
        select(Subject)
        .join(Semester, Subject.semester_id == Semester.semester_id)
        .join(Program, Semester.program_id == Program.program_id)
        .where(Program.program_id == student_exist.program_id)
        .distinct()
    )

    student_class_codes = db.session.execute(stmt).scalars().all()


    if not student_class_codes:
        return jsonify([]), 200


    student_class_codes_serialized = [class_code.serialize() for class_code in student_class_codes]

    
    return jsonify(student_class_codes_serialized), 200




