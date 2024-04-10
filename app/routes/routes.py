from flask import Blueprint
from app.controllers.controllers import *
from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

bp = Blueprint("views", __name__)

bp.route("/student", methods=["GET"])(get_students_main)
bp.route("/admin", methods=["GET"])(get_admin_main)
bp.route("/admin", methods=["POST"])(add_admin_main)
bp.route("/admin", methods=["PUT"])(update_admin_main)
bp.route("/admin", methods=["DELETE"])(delete_admin_main)
bp.route("/advisor/register", methods=["POST"])(register_advisor_main)
bp.route("/advisor/login", methods=["GET"])(login_advisor_main)
bp.route("/student/register", methods=["POST"])(register_student_main)
bp.route("/student/login", methods=["GET"])(login_student_main)
bp.route("/student/class_code", methods=["GET"])(student_class_code_main)