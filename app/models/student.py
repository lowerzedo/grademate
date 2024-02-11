from app import db


class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(
                db.String(32),
                unique = True,
                primary_key = True
            )
    full_name = db.Column(
                db.String(250),
                nullable = False
                )
    email = db.Column(
                db.String(250),
                nullable = False
            )       
    status = db.Column(
                db.Boolean,
                nullable = False
            )
    cgpa = db.Column(
                db.Float,
                nullable = True
            )
    gpa = db.Column(
                db.Float,
                nullable = True
            )
    advisor_id = db.Column(
                db.Integer,
                db.ForeignKey("advisor.id"),
                nullable = False
            )
    program_id = db.Column(
                db.Integer,
                db.ForeignKey("program.id")
            )
    
    advisor = db.relationship("Advisor")
    program = db.relationship("Program")

    def serialize(self):
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "email": self.email,
            "status": self.status,
            "cgpa": self.cgpa,
            "gpa": self.gpa,
            "advisor_id": self.advisor_id,
            "program_id": self.program_id
        }

