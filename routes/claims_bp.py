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
        # years = datetime.now().year - chosen_customer.startDate.year
        # Calculate the total contributions made by the customer over the months
        # months_contributed = (datetime.now().year - chosen_customer.startDate.year) * 12
        years = datetime.now().year - chosen_customer.startDate.year

        # Calculate the difference in months
        months = datetime.now().month - chosen_customer.startDate.month

        # Adjust months if the current month is less than the start month
        if months < 0:
            years -= 1  # Adjust years
            months += 12  # Add 12 months to get the correct difference

        # Calculate the total months contributed
        months_contributed = years * 12 + months
        total_contributions = chosen_policy.premium * months_contributed

        pay_total = total_contributions + chosen_policy.payout

        new_claim = Claim(
            reportedDate=datetime.now(),
            claimDescription=description,
            customerID=chosen_customer.customerID,
            policyID=chosen_policy.policyID,
            claim_amount=pay_total,
            approval_status=None,
        )

        db.session.add(new_claim)
        db.session.commit()

        return render_template(
            "claim_result.html",
            claim_amount=pay_total,
            policy=chosen_policy,
            customer=chosen_customer,
            claim=new_claim,
            months=months_contributed,
        )
    else:
        return "Invalid policy or customer ID. Please check your input."


@claims_bp.route("/claim_approval/<claimsID>", methods=["GET", "POST"])
@login_required
def claim_approval(claimsID):
    claim = Claim.query.get(claimsID)

    if request.method == "POST":
        approval_status = request.form.get("approval_status")
        claim.approval_status = approval_status == "True"
        db.session.commit()

    return render_template("status.html", claim=claim, claimsID=claimsID)
