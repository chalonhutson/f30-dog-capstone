from flask import Flask, render_template, request, redirect, url_for
from flask_login import (LoginManager, 
                        login_required, 
                        login_user, 
                        logout_user, 
                        current_user)

from flask_migrate import Migrate


from src.model import db, connect_to_db, User, Dog
from src.forms import LoginForm, RegisterForm, AddDogForm

app = Flask(__name__)
connect_to_db(app)
migrate = Migrate(app, db)
app.secret_key = "jinja ninja"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=form)
    else:
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(email=email).first()

        if user:
            if user.check_password(password):
                login_user(user)
                return redirect(url_for("home"))
        return "incorrect login info"

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        is_trainer = form.is_trainer.data

        user = User.query.filter_by(email=email).first()

        if user:
            return "Email already exists."

        if password != confirm_password:
            return "You passwords don't match"

        new_user = User(first_name, last_name, email, password, is_trainer=is_trainer)

        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("home"))
        except:
            return "Sorry there was a problem with the registeration"
        return "trying to register"
    else:
        return render_template("register.html", form=form)

@app.route("/home")
@login_required
def home():
    if current_user.is_trainer:
        return render_template("homepage-trainer.html")
    else:
        form = AddDogForm()
        return render_template("homepage-owner.html", form=form)

@app.route("/add-dog", methods=["POST"])
def add_dog():
    form = AddDogForm()
    name = form.name.data 
    breed = form.breed.data 
    color = form.color.data 
    birthday = form.birthday.data 
    dietary_info = form.dietary_info.data

    new_dog = Dog(current_user.id, name, breed, color, birthday, dietary_info)

    print(new_dog)
    try:
        db.session.add(new_dog)
        db.session.commit()
        return redirect(url_for("home"))
    except:
        return "Error adding your dog"

@app.route("/messages")
@login_required
def messages():
    return "here are all your messages"


@app.route("/profile/<trainer_id>")
@login_required
def profile(trainer_id):
    return f"this is the profile of trainer {trainer_id}"


