import os
from flask import Flask, render_template
from sqlalchemy.sql import text
from dotenv import load_dotenv
from extensions import db
from models.user import User
from flask_login import LoginManager

login_manager = LoginManager()

load_dotenv()

# print(os.environ.get("AZURE_DATABASE_URL"))

app = Flask(__name__, static_folder="static")


connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string


app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")

db.init_app(app)

login_manager.init_app(app)

try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        # db.drop_all()
        # db.create_all()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)


from routes.policies_bp import policies_bp

app.register_blueprint(policies_bp)


from routes.customers_bp import customers_bp

app.register_blueprint(customers_bp)


from routes.claims_bp import claims_bp

app.register_blueprint(claims_bp)

from routes.users_bp import users_bp

app.register_blueprint(users_bp)

from routes.home_bp import home_bp

app.register_blueprint(home_bp)


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/", methods=["POST", "GET"])
def landing_page():
    return render_template("landing_page.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
