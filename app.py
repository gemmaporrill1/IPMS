import os
import uuid
from flask import Flask, jsonify, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print(os.environ.get("AZURE_DATABASE_URL"))

app = Flask(__name__, static_folder="static")


connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)


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


class Customer(db.Model):
    __tablename__ = "customers"
    customerID = db.Column(
        db.String(50), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    startDate = db.Column(db.DateTime)
    policyID = db.Column(db.String(50), db.ForeignKey("policies.policyID"))

    def to_dict(self):
        return {
            "customerID": self.customerID,
            "name": self.name,
            "email": self.email,
            "startDate": self.startDate,
            "policyID": self.policyID,
        }


@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/home", methods=["POST", "GET"])
def home_page():
    return render_template("home.html")


@app.route("/customer", methods=["GET", "POST"])
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


@app.route("/policy", methods=["GET", "POST"])
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


@app.route("/claims", methods=["GET"])
def claims_page():
    policies = Policy.query.all()
    customers = Customer.query.all()

    return render_template("claims.html", customers=customers, policies=policies)


@app.route("/add_customer", methods=["GET"])
def add_customer_page():
    policies = Policy.query.all()
    return render_template("add_customer.html", policies=policies)


@app.route("/add_policy", methods=["GET"])
def add_policy_page():
    return render_template("add_policy.html")


# fix this part
@app.route("/customer/<id>/delete")
def delete_customer(id):
    selected_customer = Policy.query.get(id)
    if selected_customer:
        db.session.delete(selected_customer)
        db.session.commit()

    return redirect("/customer")


# date calculation
def policy_length(start_date):
    current_date = datetime.now()
    years_difference = current_date.year - start_date.year
    if current_date.month < start_date.month or (
        current_date.month == start_date.month and current_date.day < start_date.day
    ):
        years_difference -= 1

    return years_difference


# claims claculations
# def claims_calculation():
