from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models.customer import Customer
from models.policy import Policy
from datetime import datetime
from sqlalchemy.exc import IntegrityError


customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/customer", methods=["GET", "POST"])
@login_required
def customer_management():
    customers = Customer.query.all()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        policy_id = request.form.get("policyID")
        startDate = request.form.get("startDate")
        customers_data = Customer(
            name=name,
            email=email,
            policyID=policy_id,
            startDate=startDate,
        )
        db.session.add(customers_data)
        db.session.commit()

    for customer in customers:
        customer.years_difference = policy_length(customer.startDate)

    return render_template("customer.html", customers=customers)


def policy_length(startDate):
    if startDate is None:
        return None

    current_date = datetime.now()
    years_difference = current_date.year - startDate.year

    if current_date.month < startDate.month or (
        current_date.month == startDate.month and current_date.day < startDate.day
    ):
        years_difference -= 1

    return years_difference


@customers_bp.route("/add_customer", methods=["GET"])
@login_required
def add_customer_page():
    policies = Policy.query.all()
    return render_template("add_customer.html", policies=policies)


# update
@customers_bp.route("/update_customer/<customerID>", methods=["GET", "POST"])
@login_required
def update_customer_page(customerID):
    policies = Policy.query.all()
    selected_customer = Customer.query.get(customerID)

    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_email = request.form.get("email")
        updated_policy = request.form.get("policyID")
        updated_startDate = request.form.get("startDate")

        selected_customer.name = updated_name
        selected_customer.email = updated_email
        selected_customer.policyID = updated_policy
        selected_customer.startDate = updated_startDate

        db.session.commit()

    return render_template(
        "update_customer.html", policies=policies, selected_customer=selected_customer
    )


# delete
@customers_bp.route("/customer/<customerID>/delete", methods=["GET", "POST"])
@login_required
def delete_customer(customerID):
    try:
        selected_customer = Customer.query.get(customerID)
        if selected_customer:
            db.session.delete(selected_customer)
            db.session.commit()
        return redirect(url_for("customers.customer_management"))
    except IntegrityError:
        error_message = (
            "Cannot delete the customer because they have previously made a claim."
        )
        return render_template("error.html", error_message=error_message)
