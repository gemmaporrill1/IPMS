from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/profile")
def profile_page():
    return render_template("profile.html")


@app.route("/policy")
def policy_page():
    return render_template("policy.html")


@app.route("/claims")
def claims_page():
    return render_template("claims.html")
