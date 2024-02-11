from app.models.student import Student
from sqlalchemy import select
from flask import jsonify, request, abort
from app import db

def get_students(**kwargs):
    students = db.session.execute(select(Student)).scalars().all()

    if not students:
        return jsonify([]), 200
    
    return jsonify(students)
    

    