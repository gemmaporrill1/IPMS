import uuid
from extensions import db
from sqlalchemy.orm import relationship


class Policy(db.Model):
    __tablename__ = "policies"
    policyID = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    premium = db.Column(db.Float)
    length = db.Column(db.Integer)
    payout = db.Column(db.Integer)

    customers = relationship("Customer", backref="policy")

    # JSON = keys
    def to_dict(self):
        return {
            "policyID": self.policyID,
            "name": self.name,
            "description": self.description,
            "premium": self.premium,
            "length": self.length,
            "payout": self.payout,
        }
