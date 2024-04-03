from flask import Blueprint, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models.customer import Customer
from models.policy import Policy
from datetime import datetime

customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/customer", methods=["GET", "POST"])
def customer_management():
    customers = Customer.query.all()
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        policy_id = request.form.get("policyID")
        start_date = request.form.get("startDate")
        customers_data = Customer(
            name=name,
            email=email,
            policyID=policy_id,
            startDate=start_date,
        )
        db.session.add(customers_data)
        db.session.commit()

    for customer in customers:
        customer.years_difference = policy_length(customer.startDate)

    return render_template("customer.html", customers=customers)


@customers_bp.route("/add_customer", methods=["GET"])
def add_customer_page():
    policies = Policy.query.all()
    return render_template("add_customer.html", policies=policies)


# fix this part
@customers_bp.route("/customer/<id>/delete")
def delete_customer(id):
    selected_customer = Policy.query.get(id)
    if selected_customer:
        db.session.delete(selected_customer)
        db.session.commit()

    return render_template("/customer")


# date calculation
def policy_length(start_date):
    current_date = datetime.now()
    years_difference = current_date.year - start_date.year
    if current_date.month < start_date.month or (
        current_date.month == start_date.month and current_date.day < start_date.day
    ):
        years_difference -= 1

    return years_difference
