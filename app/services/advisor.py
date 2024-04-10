from flask import jsonify, request, abort
from app.models.advisor import Advisor
from app import db
from sqlalchemy import select
from flask_jwt_extended import JWTManager, jwt_required, create_access_token



def register_advisor(**kwargs):
    if not request.json:
        abort(400, "Request must be JSON")

    _email = request.json.get("email")
    _password = request.json.get("password")
    _advisor_id = request.json.get("advisor_id")
    _full_name = request.json.get("full_name")

    advisor_exist = db.session.execute(select(Advisor).where(Advisor.email == _email)).scalars().first()

    if advisor_exist:
        abort(400, "Advisor already exists")

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
        abort(400, "Request must be JSON")

    _email = request.json.get("email")
    _password = request.json.get("password")

    advisor_exist = db.session.execute(select(Advisor).where(Advisor.email == _email)).scalars().first()

    if not advisor_exist:
        abort(404,"Advisor doesn't exist")

    if advisor_exist and advisor_exist.check_password_hash(password=_password):
        access_token = create_access_token(identity=_email)
        return jsonify(
            {
                "advisor": advisor_exist.serialize(),
                "token": access_token
            }
        )
    else:
        abort(400, "Incorrect email or password")



    