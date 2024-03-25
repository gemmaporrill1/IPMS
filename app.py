from flask import Flask, jsonify, request, render_template

from datetime import datetime

app = Flask(__name__, static_folder="static")

policies = [
    {
        "policyID": 1,
        "name": "Vehicle",
        "description": "Vehicle insurance provides you financial protection against damages, theft, or liability related to operating a vehicle. Costs vary based on factors like coverage type, vehicle value, driver history, and location.",
        "premium": 99,
        "length": 2,
        "payOut": 50000,
    },
    {
        "policyID": 2,
        "name": "Property",
        "description": "Property insurance safeguards real estate against damages from various perils like fire, theft, and natural disasters, including liability coverage. Costs vary based on property value, location, coverage type, and deductible, ranging from hundreds to thousands annually.",
        "premium": 300,
        "length": 10,
        "payOut": 800000,
    },
    {
        "policyID": 3,
        "name": "Life Insurance",
        "description": "Life insurance provides a lump-sum payment to beneficiaries upon the policyholder's death. Costs depend on factors like age, health, coverage amount, and policy type, varying from low monthly payments to higher premiums.",
        "premium": 159,
        "length": 50,
        "payOut": 2000000,
    },
]

customers = [
    {
        "id": 1,
        "name": "John Smith",
        "email": "johnsmith@email.com",
        "policy": "Health",
        "startDate": "2020-01-01",
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "email": "janesmith@email.com",
        "policy": "Vehicle",
        "startDate": "2021-04-01",
    },
    {
        "id": 3,
        "name": "Doug Brown",
        "email": "dougbrown@email.com",
        "policy": "Health",
        "startDate": "2018-12-01",
    },
    {
        "id": 4,
        "name": "Henry Pants",
        "email": "hp12@email.com",
        "policy": "Life",
        "startDate": "2023-01-01",
    },
]


@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/home", methods=["POST", "GET"])
def home_page():
    return render_template("home.html")


@app.route("/customer", methods=["GET", "POST"])
def customer_management():
    def policy_length(start_date):
        current_date = datetime.now()
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        years_difference = current_date.year - start_date.year
        if current_date.month < start_date.month or (
            current_date.month == start_date.month and current_date.day < start_date.day
        ):
            years_difference -= 1

        return years_difference

    if request.method == "POST":
        max_id = max([int(customer["id"]) for customer in customers])
        new_id = str(max_id + 1)
        name = request.form.get("name")
        email = request.form.get("email")
        policy = request.form.get("policy")
        start_date = request.form.get("startDate")
        form_data = {
            "id": new_id,
            "name": name,
            "email": email,
            "policy": policy,
            "startDate": start_date,
        }
        customers.append(form_data)

    for customer in customers:
        customer["years_difference"] = policy_length(customer["startDate"])

    return render_template("customer.html", customers=customers)


@app.route("/policy", methods=["GET"])
def policy_page():
    return render_template("policy.html", policies=policies)


@app.route("/claims", methods=["GET"])
def claims_page():
    return render_template("claims.html", customers=customers)


@app.route("/add_customer", methods=["GET"])
def add_customer_page():
    return render_template("add_customer.html", policies=policies)


@app.route("/customer/<id>/delete")
def delete_customer(id):
    selected_customer = next(
        (customer for customer in customers if customer["id"] == id), None
    )
    if selected_customer:
        customers.remove(selected_customer)
    return render_template("customer.html", customers=customers)
