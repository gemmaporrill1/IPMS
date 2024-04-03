import uuid
from extensions import db
from sqlalchemy.orm import relationship


class Claim(db.Model):
    __tablename__ = "claims"
    claimsID = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    reportedDate = db.Column(db.DateTime)
    claimDescription = db.Column(db.String(100))
    customerID = db.Column(db.String(50), db.ForeignKey("customers.customerID"))
    policyID = db.Column(db.String(50), db.ForeignKey("policies.policyID"))

    def to_dict(self):
        return {
            "claimsID": self.claimsID,
            "reportedDate": self.reportedDate,
            "claimDescription": self.claimDescription,
            "customerID": self.customerID,
            "policyID": self.policyID,
        }
