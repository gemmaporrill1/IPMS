from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user
from extensions import db
from models.user import User
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash


users_bp = Blueprint("users", __name__)

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, field):
        existing_user = User.query.filter_by(username=field.data).first()
        if existing_user:
            raise ValidationError("Username is taken")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Login")

    def validate_username(self, field):
        user_creds = User.query.filter_by(username=field.data).first()
        if user_creds is None:
            raise ValidationError("Wrong credentials")

    def validate_password(self, field):
        user_creds = User.query.filter_by(username=self.username.data).first()

        if user_creds:
            form_password = field.data
            user_data = user_creds.to_dict()

            if not check_password_hash(user_data["password"], form_password):
                raise ValidationError("Invalid credentials")


@users_bp.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegistrationForm()

    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user_data = {"username": form.username.data, "password": password_hash}

        new_user = User(**user_data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Logged in successfully.")

            next = request.args.get("next")

            return redirect(next or url_for("login_page"))
        except Exception as e:
            db.session.rollback()
            return f"<h1>Error happened {str(e)}</h1>", 500
    return render_template("register.html", form=form)


@users_bp.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)

        flash("Logged in successfully.")

        next = request.args.get("next")

        return redirect(next or url_for("home.home_page"))
    return render_template("login.html", form=form)
