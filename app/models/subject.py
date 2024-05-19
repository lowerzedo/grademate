from app import db

class Subject(db.Model):
    __tablename__ = "subject"
    subject_id = db.Column(
            db.Integer,
            unique = True,
            primary_key = True
        )
    name = db.Column(
            db.String(200)
        )
    code = db.Column(
            db.String(200)
        )
    description = db.Column(
            db.String(2000)
        )
    topics = db.Column(
            db.String(2000)
    )
    semester_id = db.Column(
            db.Integer,
            db.ForeignKey("semester.semester_id")
        )
    
    semester = db.relationship("Semester")
    assessments = db.relationship('Assessment', back_populates='subject')
    
    def serialize(self):
        return {
            "subject_id": self.subject_id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "topics": self.topics,
            "semester_id": self.semester_id
        }
        