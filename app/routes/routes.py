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