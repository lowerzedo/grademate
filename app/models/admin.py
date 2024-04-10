from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(
            db.String(32),
            unique = True,
            primary_key = True
        )
    full_name = db.Column(
            db.String(120),
            nullable = False
        )
    email = db.Column(
            db.String(120),
            nullable = False
        )
    password = db.Column(
            db.String(250)
        )
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password_hash(self,password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            "admin_id": self.admin_id,
            "full_name": self.full_name,
            "email": self.email
        }
        