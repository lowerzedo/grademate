from app import db

class Assessment(db.Model):
    __tablename__ = "assessment"
    assessment_id = db.Column(
            db.Integer,
            unique = True,
            primary_key = True
        )
    type = db.Column(
            db.String(255)
        )
    max_grade = db.Column(
            db.Float
        )
    subject_id = db.Column(
            db.Integer,
            db.ForeignKey("subject.subject_id")
        )
    
    subject = db.relationship("Subject", back_populates="assessments")
    grades = db.relationship("Grade", back_populates="assessment")

    
    def serialize(self):
        return {
            "assessment_id": self.assessment_id,
            "type": self.type,
            "max_grade": self.max_grade,
            "subject_id": self.subject_id
        }
        