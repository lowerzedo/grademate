from app import db
from app.models.program import Program
from sqlalchemy import select
from flask import jsonify, request



def get_all_programs(**kwargs):
    
    programs = db.session.execute(select(Program)).scalars().all()

    if not programs:
        return jsonify([])

    programs_serialize = [program.serialize() for program in programs]

    return jsonify(programs_serialize), 200