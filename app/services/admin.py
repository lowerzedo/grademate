from app.models.admin import Admin
from sqlalchemy import select
from flask import jsonify, request
from app import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


def get_admin(**kwargs):
    # Get all admins from admin table in db
    admins = db.session.execute(select(Admin)).scalars().all()

    if not admins:
        return jsonify([]), 200
    
    serialized_admin = [admin.serialize() for admin in admins]

    return jsonify(serialized_admin)
    

def register_admin(**kwargs):
    if not request.json:
        return jsonify(400, "Request must be JSON")

    _email = request.json.get("email")
    _password = request.json.get("password")
    _admin_id = request.json.get("admin_id")
    _full_name = request.json.get("full_name")

    admin_exist = db.session.execute(select(Admin).where(Admin.email == _email)).scalars().first()

    if admin_exist:
        return jsonify(400, "Admin already exists")

    new_admin = Admin(
        admin_id = _admin_id,
        email = _email,
        full_name = _full_name
    )

    new_admin.set_password(password=_password)

    db.session.add(new_admin)
    db.session.commit()

    return jsonify(new_admin.serialize())



def login_admin(**kwargs):
    if not request.json:
        return jsonify({"message":"Request must be JSON"}), 400

    _email = request.json.get("email")
    _password = request.json.get("password")

    admin_exist = db.session.execute(select(Admin).where(Admin.email == _email)).scalars().first()

    if not admin_exist:
        return jsonify({"message":"Admin doesn't exist"}), 404

    if admin_exist and admin_exist.check_password_hash(password=_password):
        additional_claims = {"email": _email,"name": admin_exist.full_name }
        access_token = create_access_token(identity=_email, additional_claims=additional_claims)
        return jsonify(
            {
                "admin": admin_exist.serialize(),
                "token": access_token
            }
        )
    else:
        return jsonify({"message":"Incorrect email or password"}), 400




def add_admin(**kwargs):
    # checks if the json body is sent from frontend
    if not request.json:
        return jsonify({"message":"Request must be JSON"}),400
    
    # assign internal variables to values sent from frontend in json
    _admin_id = request.json.get('admin_id')
    _full_name = request.json.get('full_name')
    _email = request.json.get('email')

    # check if the admin is already created || you do it by fetching admin where admin_id is equal to one frontend sent
    admin_exists = db.session.execute(select(Admin).where(Admin.admin_id == _admin_id)).scalars().first()

    # if it fetches anything (not empty) return an error || The endpoint will stop here
    if admin_exists:
        return jsonify({"message":"Admin already exists"}),400

    # if admin details do not exist in db add details to Admin object (model)
    new_admin = Admin(
        admin_id = _admin_id,
        full_name = _full_name,
        email = _email,
    )
    
    # Save that object in to the table
    db.session.add(new_admin)
    db.session.commit()


    # return the new admin object to frontend
    return jsonify(new_admin.serialize())


def update_admin(**kwargs):
    # checks if the json body is sent from frontend
    if not request.json:
        return jsonify({"message":"Request must be JSON"}), 400
    
    # assign internal variables to values sent from frontend in json
    # .get() is used to set the value of the variable to None if frontend didnt pass item
        # ie: so if email was not passed from frontend, then _email will be set to None | _email=None
    _admin_id = request.json.get("admin_id")
    _full_name = request.json.get("full_name")
    _email = request.json.get("email")

    # check if the admin is already created || you do it by fetching admin where admin_id is equal to one frontend sent
    admin_exists = db.session.execute(select(Admin).where(Admin.admin_id==_admin_id)).scalars().first()

    if not admin_exists:
        return jsonify({"message":"Admin does not exist"}), 404

    # Check which fields were passed from frontend and update the record with new values
    if _full_name:
        admin_exists.full_name = _full_name
    if _email:
        admin_exists.email = _email

    db.session.commit()

    return jsonify({"message": "Admin details updated"})


def delete_admin(**kwargs):
    # This time we don't need json since we need only admin_id to delete the admin record
        # if the is request.args meaining the value will be coming from the url params
    _admin_id = request.args.get('admin_id')

    admin_exists = db.session.execute(select(Admin).where(Admin.admin_id==_admin_id)).scalars().first()

    if not admin_exists:
        return jsonify({"message":"Admin not found"}), 404
    
    db.session.delete(admin_exists)
    db.session.commit()

    return jsonify({"message":"Admin record was deleted!"})


