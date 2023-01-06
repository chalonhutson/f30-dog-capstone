from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Length(min=6, max=255)])
    password = PasswordField("password")
    remember_me = BooleanField("remember me")
    submit = SubmitField("submit")

class RegisterForm(FlaskForm):
    first_name = StringField("first name", validators=[DataRequired(), Length(max=255)])
    last_name = StringField("last name", validators=[DataRequired(), Length(max=255)])
    email = StringField("email", validators=[DataRequired(), Length(min=6, max=255)])
    password = PasswordField("password")
    confirm_password = PasswordField("confirm password", validators=[ EqualTo("password", message="Passwords must match")])
    is_trainer = BooleanField("are you a dog trainer?")
    submit = SubmitField("submit")