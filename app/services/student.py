from app.models.student import Student
from sqlalchemy import select
from flask import jsonify, request, abort
from app import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token



def register_student(**kwargs):
    if not request.json:
        abort(400, "Request must be JSON")

    _email = request.json.get("email")
    _password = request.json.get("password")
    _student_id = request.json.get("student_id")
    _full_name = request.json.get("full_name")
    _advisor_id = request.json.get("advisor_id")
    _program_id = request.json.get("program_id")

    student_exist = db.session.execute(select(Student).where(Student.email == _email)).scalars().first()

    if student_exist:
        abort(400, "Student already exists")

    new_student = Student(
        student_id = _student_id,
        email = _email,
        full_name = _full_name,
        advisor_id = _advisor_id,
        program_id = _program_id,
        status = 1
    )

    new_student.set_password(password=_password)

    db.session.add(new_student)
    db.session.commit()

    return jsonify(new_student.serialize())    

def login_student(**kwargs):
    if not request.json:
        abort(400, "Request must be JSON")

    _email = request.json.get("email")
    _password = request.json.get("password")

    student_exist = db.session.execute(select(Student).where(Student.email == _email)).scalars().first()

    if not student_exist:
        abort(404,"Student doesn't exist")

    if student_exist and student_exist.check_password_hash(password=_password):
        access_token = create_access_token(identity=_email)
        return jsonify(
            {
                "student": student_exist.serialize(),
                "token": access_token
            }
        )
    else:
        abort(400, "Incorrect email or password")


def get_students(**kwargs):
    students = db.session.execute(select(Student)).scalars().all()

    if not students:
        return jsonify([]), 200
    
    return jsonify(students)
    

    