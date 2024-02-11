from flask import Blueprint
from app.controllers.controllers import *
from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

bp = Blueprint("views", __name__)


bp.route("/student", method=["GET"])(get_students_main)