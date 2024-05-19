from app import db

class SubjectGrade(db.Model):
    __tablename__ = "subjectgrade"
    subject_grade_id = db.Column(
        db.Integer,
        unique = True,
        primary_key = True
    )
    subject_id = db.Column(
            db.Integer,
            db.ForeignKey("subject.subject_id")
        )
    student_id = db.Column(
            db.String(32),
            db.ForeignKey("student.student_id")
        )
    achieved_grade = db.Column(
            db.String(2)
        )
    
    subject = db.relationship("Subject")
    student = db.relationship("Student")
    
    
    def serialize(self):
        return {
            "subject_grade_id": self.subject_grade_id,
            "subject_id": self.subject_id,
            "student_id": self.student_id,
            "achieved_grade": self.achieved_grade
        }
        