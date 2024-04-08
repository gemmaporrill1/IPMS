import uuid
from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    # JSON - Keys
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }
