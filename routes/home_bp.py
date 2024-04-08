from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user
from extensions import db
from models.user import User
from models.customer import Customer
from models.claim import Claim

home_bp = Blueprint("home", __name__)


@home_bp.route("/home", methods=["POST", "GET"])
@login_required
def home_page():
    # username
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()

    # claims count
    claims = Claim.query.all()
    claim_count = len(claims)

    # customer count
    customers = Customer.query.all()
    customer_count = len(customers)

    return render_template(
        "home.html",
        user=user,
        claim_count=claim_count,
        customer_count=customer_count,
    )
