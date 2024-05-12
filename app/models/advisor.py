from app import db
from werkzeug.security import generate_password_hash, check_password_hash


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
    password = db.Column(
            db.String(250)
        )
    status = db.Column(
            db.Boolean,
            nullable = False
        )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password_hash(self,password):
        return check_password_hash(self.password, password)
    
    def serialize(self):
        return {
            "advisor_id": self.advisor_id,
            "full_name": self.full_name,
            "email": self.email,
            "status": self.status
        }
        