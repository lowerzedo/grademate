from app.models.admin import Admin
from sqlalchemy import select
from flask import jsonify, request, abort
from app import db

def get_admin(**kwargs):
    # Get all admins from admin table in db
    admins = db.session.execute(select(Admin)).scalars().all()

    if not admins:
        return jsonify([]), 200
    
    serialized_admin = [admin.serialize() for admin in admins]

    return jsonify(serialized_admin)
    

def add_admin(**kwargs):
    # checks if the json body is sent from frontend
    if not request.json:
        abort(400, "Request must be JSON")
    
    # assign internal variables to values sent from frontend in json
    _admin_id = request.json.get('admin_id')
    _full_name = request.json.get('full_name')
    _email = request.json.get('email')

    # check if the admin is already created || you do it by fetching admin where admin_id is equal to one frontend sent
    admin_exists = db.session.execute(select(Admin).where(Admin.admin_id == _admin_id)).scalars().first()

    # if it fetches anything (not empty) return an error || The endpoint will stop here
    if admin_exists:
        abort(400, "Admin already exists")

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
        abort(400, "Request must be JSON")
    
    # assign internal variables to values sent from frontend in json
    # .get() is used to set the value of the variable to None if frontend didnt pass item
        # ie: so if email was not passed from frontend, then _email will be set to None | _email=None
    _admin_id = request.json.get("admin_id")
    _full_name = request.json.get("full_name")
    _email = request.json.get("email")

    # check if the admin is already created || you do it by fetching admin where admin_id is equal to one frontend sent
    admin_exists = db.session.execute(select(Admin).where(Admin.admin_id==_admin_id)).scalars().first()

    if not admin_exists:
        abort(404, "Admin does not exist")

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
        abort(404, "Admin not found")
    
    db.session.delete(admin_exists)
    db.session.commit()

    return jsonify({"message":"Admin record was deleted!"})


