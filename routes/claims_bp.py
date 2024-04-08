from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models.policy import Policy
from models.customer import Customer
from models.claim import Claim
from datetime import datetime

claims_bp = Blueprint("claims", __name__)


@claims_bp.route("/claims", methods=["GET"])
@login_required
def claims_page():
    policies = Policy.query.all()
    customers = Customer.query.all()

    return render_template("claims.html", customers=customers, policies=policies)


@claims_bp.route("/calculate_claim", methods=["GET", "POST"])
@login_required
def calculate_claim():
    policyID = request.form["policyID"]
    customerID = request.form["customerID"]
    description = request.form["description"]

    chosen_policy = Policy.query.get(policyID)
    chosen_customer = Customer.query.get(customerID)

    if chosen_policy and chosen_customer:
        # Calculate the total contributions made by the customer over the months
        months_contributed = (datetime.now().year - chosen_customer.startDate.year) * 12
        total_contributions = chosen_policy.premium * months_contributed

        pay_total = total_contributions + chosen_policy.payout

        new_claim = Claim(
            reportedDate=datetime.now(),
            claimDescription=description,
            customerID=chosen_customer.customerID,
            policyID=chosen_policy.policyID,
        )

        db.session.add(new_claim)
        db.session.commit()

        return render_template(
            "claim_result.html",
            claim_amount=pay_total,
            policy=chosen_policy,
            customer=chosen_customer,
            claim=new_claim,
        )
    else:
        return "Invalid policy or customer ID. Please check your input."
