from app.models.student import Student
from sqlalchemy import select
from sqlalchemy.orm import Session
from flask import jsonify, request
from app import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token



def register_student(**kwargs):
    if not request.json:
        return jsonify({"message":"Request must be JSON"}), 400

    _email = request.json.get("email")
    _password = request.json.get("password")
    _student_id = request.json.get("student_id")
    _full_name = request.json.get("full_name")
    _advisor_id = request.json.get("advisor_id")
    _program_id = request.json.get("program_id")

    student_exist = db.session.execute(select(Student).where(Student.email == _email)).scalars().first()

    if student_exist:
        return jsonify({"message":"Student already exists"}), 400

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


def register_student_in_bulk():
    # Retrieve student data from the request
    students = request.json.get("students")

    # Check if any student data is provided
    if not students:
        return jsonify({"message": "No student details were passed"}), 400

    not_existing_students = []

    # Create a new database session
    with Session(db.engine) as session:
        for student_data in students:
            # Check if the student already exists in the database
            student_exists = session.execute(
                select(Student).where(Student.email == student_data['email'])
            ).scalars().first()

            if not student_exists:
                # If the student does not exist, prepare to add them
                new_student = Student(
                    student_id=student_data['student_id'],
                    email=student_data['email'],
                    full_name=student_data['full_name'],
                    advisor_id=student_data['advisor_id'],
                    program_id=student_data['program_id'],
                    status=1 
                )
                new_student.set_password(student_data['password'])  # Encrypt the password
                not_existing_students.append(new_student)

        # Bulk insert new students
        if not_existing_students:
            session.add_all(not_existing_students)
            session.commit()  # Commit the session to insert new records

            return jsonify({"message": f"Added {len(not_existing_students)} students"}), 201
        else:
            return jsonify({"message": "All students already exist"}), 200



def login_student(**kwargs):
    if not request.json:
        return jsonify({"message":"Request must be JSON"}), 400

    _email = request.json.get("email")
    _password = request.json.get("password")

    student_exist = db.session.execute(select(Student).where(Student.email == _email)).scalars().first()

    if not student_exist:
        return jsonify({"message":"Student does not exist"}), 404

    if student_exist and student_exist.check_password_hash(password=_password):
        additional_claims = {"email": _email, "name": student_exist.full_name, "student_id": student_exist.student_id, "role": "student"}  
        access_token = create_access_token(identity=_email, additional_claims=additional_claims)
        return jsonify(
            {
                "student": student_exist.serialize(),
                "token": access_token
            }
        )
    else:
        return jsonify({"message":"Incorrect email or password"}), 400


def get_student(**kwargs):
    student_id = kwargs.get("student_id")

    student = db.session.execute(select(Student).where(Student.student_id == student_id)).scalars().first()

    if not student:
        return jsonify({"message":"Student not found"}), 404

    program_name = student.program.program_name 

    return jsonify({
        "student": student.serialize(),
        "program_name": program_name,
        "semester": student.semester.name
    }), 200

def get_students(**kwargs):
    students = db.session.execute(select(Student)).scalars().all()

    if not students:
        return jsonify([]), 200

    students_serialized = [student.serialize() for student in students]
    
    return jsonify(students_serialized), 200
    


def drop_students():
    student_ids = request.json.get("ids")

    if not student_ids:
        return jsonify({"error": "No student ids were sent"}), 401

    try:
        # Fetch students to be updated
        students_to_update = Student.query.filter(Student.student_id.in_(student_ids)).all()

        if not students_to_update:
            return jsonify({"error": "No students found with the provided ids"}), 404

        # Update the status of students
        for student in students_to_update:
            student.status = 0 
        
        db.session.commit()

        return jsonify({"message": f"Successfully updated {len(students_to_update)} students to inactive status."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500