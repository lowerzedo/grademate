from flask import Blueprint
from app.controllers.controllers import *
from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

name = 'default'
# we need blueprint to define the routes
bp = Blueprint("views", name)

bp.route("/admin", methods=["GET"])(get_admin_main)
bp.route("/admin/register", methods=["POST"])(register_admin_main)
bp.route("/admin/login", methods=["POST"])(login_admin_main)
bp.route("/admin", methods=["PUT"])(update_admin_main)
bp.route("/admin", methods=["DELETE"])(delete_admin_main)

bp.route("/advisor/register", methods=["POST"])(register_advisor_main)
bp.route("/advisor/register/bulk", methods=["POST"])(register_advisor_in_bulk_main)
bp.route("/advisor/login", methods=["POST"])(login_advisor_main)
bp.route("/advisor/students", methods=['GET'])(get_advisor_students_main)
bp.route("/advisor/student/semesters", methods=['GET'])(get_advisor_student_semester_main)
bp.route("/advisor/student/semester/classes", methods=['GET'])(get_advisor_student_semester_class_main)
bp.route("/advisors", methods=['GET'])(get_all_advisors_main)
bp.route("/advisor/drop", methods=['PUT'])(drop_advisors_main)
bp.route("/advisor/fetch_students", methods=['GET'])(fetch_students_main)
bp.route("/advisor/add_advisee", methods=['POST'])(add_advisee_main)
# CSV file upload
bp.route("/advisor/add_advisee/bulk", methods=['POST'])(add_advisee_bulk_main)

bp.route("/student", methods=["GET"])(get_students_main)
bp.route("/student/<student_id>", methods=["GET"])(get_student_main)
bp.route("/student/register", methods=["POST"])(register_student_main)
bp.route("/student/register/bulk", methods=["POST"])(register_student_in_bulk_main)
bp.route("/student/login", methods=["POST"])(login_student_main)
bp.route("/student/class_code", methods=["GET"])(student_class_code_main)
bp.route("/student/assessment_grades", methods=["GET"])(get_student_assessment_grades_main)
bp.route("/student/drop", methods=["PUT"])(drop_students_main)

bp.route("/subject/assessments", methods=["GET"])(get_subject_assessments_main)
bp.route("/subject/assessment", methods=["POST"])(add_new_assessment_main)
bp.route("/subjects", methods=['GET'])(get_all_subjects_main)

bp.route("/course_outline", methods=["POST"])(course_outline_main)
bp.route("/course_outline/manual", methods=["POST"])(course_outline_manual_main)

bp.route("/grade/save_grade", methods=["POST"])(save_grades_main)

bp.route("/programs", methods=["GET"])(get_all_programs_main)

bp.route("/evaluate", methods=["POST"])(get_student_evaluation)