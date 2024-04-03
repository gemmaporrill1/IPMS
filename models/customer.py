import uuid
from extensions import db
from sqlalchemy.orm import relationship


class Customer(db.Model):
    __tablename__ = "customers"
    customerID = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    startDate = db.Column(db.DateTime)
    policyID = db.Column(db.String(50), db.ForeignKey("policies.policyID"))

    def to_dict(self):
        return {
            "customerID": self.customerID,
            "name": self.name,
            "email": self.email,
            "startDate": self.startDate,
            "policyID": self.policyID,
        }
