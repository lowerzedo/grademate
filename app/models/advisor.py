from app import db

class Advisor(db.Model):
    __tablename__ = "advisor"
    advisor_id = db.Column(
            db.String(32),
            unique = True,
            primary_key = True
        )
    full_name = db.Column(
            db.String(120)
        )
    email = db.Column(
            db.String(120)
        )
    
    def serialize(self):
        return {
            "advisor_id": self.advisor_id,
            "full_name": self.full_name,
            "email": self.email
        }
        