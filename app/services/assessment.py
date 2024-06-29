from app import db
from flask import jsonify, request
from werkzeug.utils import secure_filename
import os
import openai
from dotenv import load_dotenv
from tika import parser
from app.models.assessment import Assessment
from app.models.subject import Subject
from app.models.grade import Grade
from app.models.student import Student
from sqlalchemy import select, func
from config import Config

load_dotenv()

def get_subject_assessments(**kwargs):
    subject_id = request.args.get("subject_id")
    existing_subject = db.session.execute(select(Subject).where(Subject.subject_id == subject_id)).scalars().first()
    if not existing_subject:
        return jsonify({"message":"Subject not found"}), 404

    stmt = select(Assessment).where(Assessment.subject_id == subject_id)

    subject_assessments = db.session.execute(stmt).scalars().all()

    if not subject_assessments:
        return jsonify([]), 200

    serialized_subject_assessments = [subject_assessment.serialize() for subject_assessment in subject_assessments]

    return jsonify(serialized_subject_assessments),200


def get_student_assessment_grades(**kwargs):
    subject_id = request.args.get("subject_id")
    existing_subject = db.session.execute(select(Subject).where(Subject.subject_id == subject_id)).scalars().first()
    if not existing_subject:
        return jsonify({"message": "Subject not found"}), 404

    student_id = request.args.get("student_id")
    student_exists = db.session.execute(select(Student).where(Student.student_id == student_id)).scalars().first()
    if not student_exists:
        return jsonify({"message": "Student doesn't exist"}), 404

    stmt = (
        select(
            Assessment.assessment_id,
            Assessment.type,
            Assessment.max_grade,
            Grade.achieved_grade
        )
        .join(Grade, Assessment.assessment_id == Grade.assessment_id, isouter=True)
        .where(
            (Assessment.subject_id == subject_id) & 
            (Grade.student_id == student_id)
        )
    )

    subject_assessments = db.session.execute(stmt).all()

    if not subject_assessments:
        return jsonify([])

    serialized_subject_assessments = [{
        'assessment_id': assessment.assessment_id,
        'type': assessment.type,
        'max_grade': assessment.max_grade,
        'achieved_grade': assessment.achieved_grade or 0  # Ensure None is replaced with 0
    } for assessment in subject_assessments]

    # Calculate the total grade achieved by the student
    total_grade = sum(
        ((assessment['achieved_grade'] / 100) * assessment['max_grade']) 
        for assessment in serialized_subject_assessments
    )

    # Calculate the percentage of the total possible score (which should sum to 100)
    total_max_grade = sum(assessment['max_grade'] for assessment in serialized_subject_assessments)
    # Calculate the percentage of the grade percentage
    if total_max_grade > 0:
        grade_percentage = (total_grade / total_max_grade) * 100
        grade_percentage = round(grade_percentage, 1)  # Round to one decimal place
    else:
        grade_percentage = 0

    return jsonify({"grade_percentage": grade_percentage, "assessments": serialized_subject_assessments}), 200


def add_new_assessment(**kwargs):
    _subject_id = request.json.get("subject_id")
    _assessment_type = request.json.get("type")
    _max_grade = request.json.get("max_grade")

    # existing_assessment = db.session.execute(select(Assessment).where(Assessment.type == _assessment_type))

    subject_exists = db.session.execute(select(Subject).where(Subject.subject_id == _subject_id)).scalars().first()

    if not subject_exists:
        return jsonify({"message":"Subject doesn't exists"}), 404

    new_assessment = Assessment(
        type = _assessment_type,
        max_grade = _max_grade,
        subject_id = _subject_id
    )

    db.session.add(new_assessment)
    db.session.commit()

    return jsonify(new_assessment.serialize()), 200


def course_outline_manual(**kwargs):
    subject_id = request.json.get("subject_id")

    subject_exists = db.session.execute(select(Subject).where(Subject.subject_id == subject_id)).scalars().first()

    if not subject_exists:
        return jsonify({"message":"Subject doesn't exists"}), 404
    
    assessments = request.json.get("assessments")

    for key, value in assessments[0].items():
        new_assessment = Assessment(
            type = key,
            max_grade = value,
            subject_id = subject_id
        )

        db.session.add(new_assessment)
        db.session.commit()

    new_assessments = db.session.execute(select(Assessment).where(Assessment.subject_id == subject_id)).scalars().all()

    new_assessments_serialized = [new_assessment.serialize() for new_assessment in new_assessments]

    return jsonify(new_assessments_serialized), 200


def course_outline(**kwargs):
    pdf_file = request.files.get('pdf_file')

    filename = secure_filename(pdf_file.filename)

    temp_path = os.path.join('/tmp', filename)
    pdf_file.save(temp_path)

    raw = parser.from_file(temp_path)

    raw_text = raw['content']

    openai.api_key = os.environ.get('OPENAI_KEY')

    def extract_information(raw_text):
        response = openai.Completion.create(
            engine="babbage-002",
            prompt=f"Extract table assessments and percentage numbers only where column names are 'Assessment' and 'Percentage' from the following text:\n\n{raw_text}.",
            max_tokens=1024,
            temperature=0.3,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n\n"]
        )
        return response.choices[0].text.strip()

    extracted_info = extract_information(raw_text)

    os.remove(temp_path)

    return jsonify({"course_syllabus": extracted_info})


