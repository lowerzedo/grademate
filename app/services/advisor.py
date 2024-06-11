from flask import jsonify, request
from app.models.advisor import Advisor
from app.models.student import Student
from app.models.semester import Semester
from app.models.program import Program
from app.models.subject import Subject
from app import db
from sqlalchemy import select
from sqlalchemy.orm import Session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import pandas as pd
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def add_advisee():
    student_id = request.json.get("student_id")
    advisor_id = request.json.get("advisor_id")

    student_exist = db.session.execute(select(Student).where(Student.student_id == student_id)).scalars().first()

    if not student_exist:
        return jsonify({"message":"Student not found"}), 404

    advisor_exist = db.session.execute(select(Advisor).where(Advisor.advisor_id == advisor_id)).scalars().first()

    if not advisor_exist:
        return jsonify({"message":"Advisor not found"}), 404

    student_exist.advisor_id = advisor_id
    db.session.commit()

    return jsonify(student_exist.serialize()), 200

def add_advisee_bulk():
    if 'file' not in request.files or 'advisor_id' not in request.form:
        return jsonify({"message": "Invalid request data"}), 400

    file = request.files['file']
    advisor_id = request.form['advisor_id']

    if file.filename == '':
        return jsonify({"message": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Assuming the CSV has a 'Student ID' column
    try:
        df = pd.read_csv(file_path)
        student_ids = df['Student ID'].tolist()

        # Implement the logic to update advisees in the database
        return process_advisees(advisor_id, student_ids)
    except Exception as e:
        return jsonify({"message": "Error processing file", "error": str(e)}), 500

def process_advisees(advisor_id, student_ids):
    not_existing_students = []
    not_existing_advisors = []

    with Session(db.engine) as session:
        for student_id in student_ids:
            student_exist = session.execute(
                select(Student).where(Student.student_id == student_id)
            ).scalars().first()

            advisor_exist = session.execute(
                select(Advisor).where(Advisor.advisor_id == advisor_id)
            ).scalars().first()

            if not student_exist:
                not_existing_students.append(student_id)
            if not advisor_exist:
                not_existing_advisors.append(advisor_id)

            if student_exist and advisor_exist:
                student_exist.advisor_id = advisor_id

        if not_existing_students or not_existing_advisors:
            return jsonify(
                {
                    "message": "Some students or advisors do not exist",
                    "students": not_existing_students,
                    "advisors": not_existing_advisors
                }
            ), 404

        session.commit()

        return jsonify({"message": "Successfully updated students' advisor"}), 200

def register_advisor_in_bulk():
    # Retrieve advisor data from the request
    advisors = request.json.get("advisors")

    # Check if any advisor data is provided
    if not advisors:
        return jsonify({"message": "No advisor details were passed"}), 400

    not_existing_advisors = []

    # Create a new database session
    with Session(db.engine) as session:
        for advisor_data in advisors:
            # Check if the advisor already exists in the database
            advisor_exists = session.execute(
                select(Advisor).where(Advisor.email == advisor_data['email'])
            ).scalars().first()

            if not advisor_exists:
                # If the advisor does not exist, prepare to add them
                new_advisor = Advisor(
                    advisor_id=advisor_data['advisor_id'],
                    email=advisor_data['email'],
                    full_name=advisor_data['full_name'],
                    status=1 
                )
                new_advisor.set_password(advisor_data['password'])  # Encrypt the password
                not_existing_advisors.append(new_advisor)

        # Bulk insert new advisors
        if not_existing_advisors:
            session.add_all(not_existing_advisors)
            session.commit()  # Commit the session to insert new records

            return jsonify({"message": f"Added {len(not_existing_advisors)} advisors"}), 201
        else:
            return jsonify({"message": "All advisors already exist"}), 200



def register_advisor(**kwargs):
    if not request.json:
        return jsonify(400, "Request must be JSON")

    _email = request.json.get("email")
    _password = request.json.get("password")
    _advisor_id = request.json.get("advisor_id")
    _full_name = request.json.get("full_name")

    advisor_exist = db.session.execute(select(Advisor).where(Advisor.email == _email)).scalars().first()

    if advisor_exist:
        return jsonify(400, "Advisor already exists")

    new_advisor = Advisor(
        advisor_id = _advisor_id,
        email = _email,
        full_name = _full_name
    )

    new_advisor.set_password(password=_password)

    db.session.add(new_advisor)
    db.session.commit()

    return jsonify(new_advisor.serialize())



def login_advisor(**kwargs):
    if not request.json:
        return jsonify({"message":"Request must be JSON"}), 400

    _email = request.json.get("email")
    _password = request.json.get("password")

    advisor_exist = db.session.execute(select(Advisor).where(Advisor.email == _email)).scalars().first()

    if not advisor_exist:
        return jsonify({"message":"Advisor doesn't exist"}), 404

    if advisor_exist and advisor_exist.check_password_hash(password=_password):
        additional_claims = {"email": _email, "name": advisor_exist.full_name, "advisor_id": advisor_exist.advisor_id}
        access_token = create_access_token(identity=_email, additional_claims= additional_claims)
        return jsonify(
            {
                "advisor": advisor_exist.serialize(),
                "token": access_token
            }
        )
    else:
        return jsonify({"message":"Incorrect email or password"}), 400



def get_advisor_students(**kwargs):
    advisor_id = request.args.get("advisor_id")

    advisor_exist = db.session.execute(select(Advisor).where(Advisor.advisor_id == advisor_id)).scalars().first()

    if not advisor_exist:
        return jsonify({"message": "Advisor not found"}), 404
    
    advisor_students = db.session.execute(select(Student).where(Student.advisor_id == advisor_id)).scalars().all()

    if not advisor_students:
        return jsonify([])

    
    advisor_students_serialized = [advisor_student.serialize() for advisor_student in advisor_students]

    return jsonify(advisor_students_serialized), 200



def get_advisor_student_semester(**kwargs):
    student_id = request.args.get("student_id")

    student_exist = db.session.execute(select(Student).where(Student.student_id== student_id)).scalars().first()

    if not student_exist:
        return jsonify({"message":"Student not found"}), 404

    student_semesters = db.session.execute(
        select(Semester)
        .join(Program, Semester.program_id == Program.program_id)
        .join(Student, Program.program_id == Student.program_id)
        .where(Student.student_id == student_id)
        ).scalars().all()

    if not student_semesters:
        return jsonify([])

    student_semesters_serialized = [student_semester.serialize() for student_semester in student_semesters]

    return jsonify(student_semesters_serialized), 200


def get_advisor_student_semester_class(**kwargs):
    semester_id = request.args.get("semester_id")

    semester_exist = db.session.execute(select(Semester).where(Semester.semester_id == semester_id)).scalars().first()

    if not semester_exist:
        return jsonify({"message":"Semester not found"}), 404
    
    semester_subjects = db.session.execute(select(Subject).where(Subject.semester_id == semester_id)).scalars().all()

    if not semester_subjects:
        return jsonify([]), 200

    semester_subjects_serialized = [semester_subject.serialize() for semester_subject in semester_subjects]

    return jsonify(semester_subjects_serialized), 200



def get_all_advisors(**kwargs):

    advisors = db.session.execute(select(Advisor)).scalars().all()

    if not advisors:
        return jsonify([]), 200
    
    advisors_serialized = [advisor.serialize() for advisor in advisors]

    return jsonify(advisors_serialized), 200


def drop_advisors():
    advisor_ids = request.json.get("ids")

    if not advisor_ids:
        return jsonify({"error": "No advisor ids were sent"}), 401

    try:
        # Fetch advisors to be updated
        advisors_to_update = Advisor.query.filter(Advisor.advisor_id.in_(advisor_ids)).all()

        if not advisors_to_update:
            return jsonify({"error": "No advisors found with the provided ids"}), 404

        # Update the status of advisors
        for advisor in advisors_to_update:
            advisor.status = 0 
        
        db.session.commit()

        return jsonify({"message": f"Successfully updated {len(advisors_to_update)} advisors to inactive status."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
