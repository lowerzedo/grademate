from app import db
from app.models.assessment import Assessment
from app.models.grade import Grade
from app.models.subject import Subject
from app.models.student import Student
from app.models.semester import Semester
from app.models.program import Program
from flask import jsonify, request
from sqlalchemy import select


def get_all_subjects(**kwargs):
    
    subjects = db.session.execute(select(Subject)).scalars().all()

    if not subjects:
        return jsonify([])

    subjects_serialize = [subject.serialize() for subject in subjects]

    return jsonify(subjects_serialize), 200

def student_class_code(**kwargs):

    student_id = request.args.get("student_id")

    student_exist = db.session.execute(select(Student).where(Student.student_id == student_id)).scalars().first()

    if not student_exist:
        return jsonify({"message":"Student doesn't exist"}), 404

    stmt = (
        select(Subject)
        .join(Semester, Subject.semester_id == Semester.semester_id)
        .join(Student, Semester.semester_id == Student.current_semester)
        .join(Program, Semester.program_id == Program.program_id)
        .where(Program.program_id == student_exist.program_id)
        .distinct()
    )

    student_class_codes = db.session.execute(stmt).scalars().all()


    if not student_class_codes:
        return jsonify([]), 200


    student_class_codes_serialized = [class_code.serialize() for class_code in student_class_codes]

    
    return jsonify(student_class_codes_serialized), 200




