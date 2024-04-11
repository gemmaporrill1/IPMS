from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models.policy import Policy
from sqlalchemy.exc import IntegrityError

policies_bp = Blueprint("policies", __name__)


@policies_bp.route("/policy", methods=["GET", "POST"])
@login_required
def policy_page():
    policies = Policy.query.all()
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        premium = request.form.get("premium")
        length = request.form.get("length")
        payout = request.form.get("payout")
        image = request.form.get("image")
        policies_data = Policy(
            name=name,
            description=description,
            premium=premium,
            length=length,
            payout=payout,
            image=image,
        )
        db.session.add(policies_data)
        db.session.commit()
    return render_template("policy.html", policies=policies)


@policies_bp.route("/add_policy", methods=["GET"])
@login_required
def add_policy_page():
    return render_template("add_policy.html")

@policies_bp.route("/policy/<policyID>/delete", methods=["GET", "POST"])
@login_required
def delete_policy(policyID):
    try:
        selected_policy = Policy.query.get(policyID)
        if selected_policy:
            db.session.delete(selected_policy)
            db.session.commit()
        return redirect(url_for("policies.policy_page"))
    except IntegrityError:
        error_message = (
            "Cannot delete this policy because it is being actively used by customers."
        )
        return render_template("error.html", error_message=error_message)