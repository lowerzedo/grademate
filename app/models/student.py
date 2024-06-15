from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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
    password = db.Column(
                db.String(250)
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
                db.String(255),
                db.ForeignKey("advisor.advisor_id"),
                nullable = True
            )
    program_id = db.Column(
                db.Integer,
                db.ForeignKey("program.program_id")
            )
    current_semester = db.Column(
                db.Integer,
                db.ForeignKey("semester.semester_id")
            )
    
    advisor = db.relationship("Advisor")
    program = db.relationship("Program")
    semester = db.relationship("Semester")
    grades = db.relationship("Grade", back_populates="student")

    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password_hash(self,password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "email": self.email,
            "status": self.status,
            "cgpa": self.cgpa,
            "gpa": self.gpa,
            "advisor_id": self.advisor_id,
            "program_id": self.program_id,
            "current_semester": self.current_semester
        }

