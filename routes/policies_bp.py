from flask import Blueprint, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models.policy import Policy

policies_bp = Blueprint("policies", __name__)


@policies_bp.route("/policy", methods=["GET", "POST"])
def policy_page():
    policies = Policy.query.all()
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        premium = request.form.get("premium")
        length = request.form.get("length")
        payout = request.form.get("payout")
        policies_data = Policy(
            name=name,
            description=description,
            premium=premium,
            length=length,
            payout=payout,
        )
        db.session.add(policies_data)
        db.session.commit()
    return render_template("policy.html", policies=policies)


@policies_bp.route("/add_policy", methods=["GET"])
def add_policy_page():
    return render_template("add_policy.html")
