from app import db

class Admin(db.Model):
    __tablename___ = "admin"
    admin_id = db.Column(
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
            "admin_id": self.admin_id,
            "full_name": self.full_name,
            "email": self.email
        }
        