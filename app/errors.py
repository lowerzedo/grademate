# 400 - Bad Request
# 401 - Unauthorized
# 403 - Forbidden
# 404 - Not Found
# 409 - Conflict
# 500 - Internal Server Error

from flask import Blueprint, jsonify

blueprint = Blueprint('errors', __name__)


@blueprint.app_errorhandler(400)
def bad_request(error):
    return jsonify(
        {
            "error": {
                "reason": "Bad Request",
                "message": error.description,
                "status": 400
            }
        }
    ), 400


@blueprint.app_errorhandler(401)
def unauthorized_access(error):
    return jsonify(
        {
            "error": {
                "reason": "Unauthorized Access",
                "message": error.description,
                "status": 401
            }
        }
    ), 401


@blueprint.app_errorhandler(403)
def forbidden_request(error):
    return jsonify(
        {
            "error": {
                "reason": "Forbidden Request",
                "message": error.description,
                "status": 403
            }
        }
    ), 403


@blueprint.app_errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "error": {
                "reason": "Not Found",
                "message": error.description,
                "status": 404
            }
        }
    ), 404


@blueprint.app_errorhandler(409)
def conflict(error):
    return jsonify(
        {
            "error": {
                "reason": "Conflict",
                "message": error.description,
                "status": 409
            }
        }
    ), 409


@blueprint.app_errorhandler(500)
def internal_server_error(error):
    return jsonify(
        {
            "error": {
                "reason": "Internal Server Error",
                "message": error.description,
                "status": 500
            }
        }
    ), 500

