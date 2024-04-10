from app import db

class Grade(db.Model):
    __tablename__ = "grade"
    grade_id = db.Column(
            db.Integer,
            unique = True,
            primary_key = True
        )
    assessment_id = db.Column(
            db.Integer,
            db.ForeignKey("assessment.assessment_id")
        )
    student_id = db.Column(
            db.String(32),
            db.ForeignKey("student.student_id")
        )
    achieved_grade = db.Column(
            db.Float
        )
    
    # Relationship to the Assessment model. The backref creates a virtual column in the Assessment model.
    assessment = db.relationship("Assessment", back_populates="grades")

    # Relationship to the Student model. The backref creates a virtual column in the Student model.
    student = db.relationship("Student", back_populates="grades")
    
    def serialize(self):
        return {
            "grade_id": self.grade_id,
            "assessment_id": self.assessment_id,
            "student_id": self.student_id,
            "achieved_grade": self.achieved_grade
        }
        