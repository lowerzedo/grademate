from app import db

class Semester(db.Model):
    __tablename__ = "semester"
    semester_id = db.Column(
            db.Integer,
            unique = True,
            primary_key = True
        )
    name = db.Column(
            db.String(200)
        )
    program_id = db.Column(
                db.Integer,
                db.ForeignKey("program.program_id")
            )
    
    program = db.relationship("Program")
    
    def serialize(self):
        return {
            "semester_id": self.semester_id,
            "name": self.name,
            "program_id": self.program_id
        }
        