from app import db

class Program(db.Model):
    __tablename__ = "program"
    program_id = db.Column(
            db.Integer,
            unique = True,
            primary_key = True
        )
    program_name = db.Column(
            db.String(200)
        )
    
    def serialize(self):
        return {
            "program_id": self.program_id,
            "program_name": self.program_name
        }
        