

from app.models.student import Student
from flask import jsonify, request
from app.services.StudentEvaluation import StudentEvaluator

from app.services.delete_this_later import grades, subjects

# defining the evaluation object
studentEvaluate = StudentEvaluator()

def evaluate_student(**kwargs):
    if not request.json:
        return jsonify({"message":"Request must be JSON"}), 400
    output = studentEvaluate.evaluate_student(grades=grades, subjects=subjects)

    return jsonify(output)