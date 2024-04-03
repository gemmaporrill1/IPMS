from flask import Blueprint, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models.policy import Policy
from models.customer import Customer
from models.claim import Claim
from datetime import datetime

claims_bp = Blueprint("claims", __name__)


@claims_bp.route("/claims", methods=["GET"])
def claims_page():
    policies = Policy.query.all()
    customers = Customer.query.all()

    return render_template("claims.html", customers=customers, policies=policies)


@claims_bp.route("/calulate_claim", methods=["POST"])
def calculate_claim():
    policyID = request.form["policyID"]
    customerID = request.form["customerID"]

    policy = Policy.query.get(policyID)
    customer = Customer.query.get(customerID)

    claim_amount = claims_calculation(policy, customer)
    return render_template("claim_result.html", claim_amount=claim_amount)


def claims_calculation(policy, customer):
    payout_amount = policy.payout
    contributions = policy.premium
    length_contributed = customer.startDate

    length_contributed = (datetime.now() - customer.startDate).days / 365

    length_contributed = max(length_contributed, 1)

    pay_estimate = contributions * length_contributed

    pay_estimate = min(pay_estimate, payout_amount)

    pay_total = payout_amount - pay_estimate

    pay_total = max(pay_total, 0)

    return pay_total
