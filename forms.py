from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Length(min=6, max=255)])
    password = PasswordField("password")
    remember_me = BooleanField("remember me")
    submit = SubmitField("submit")