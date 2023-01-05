from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user


from model import db, connect_to_db, User
from forms import LoginForm

app = Flask(__name__)

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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return "this is the register page"
    else:
        return "trying to register"

@app.route("/home")
@login_required
def home():
    if current_user.is_trainer:
        return "trainer home page"
    else:
        return "dog owner homepage"

@app.route("/messages")
def messages():
    return "here are all your messages"


@app.route("/profile/<trainer_id>")
def profile(trainer_id):
    return f"this is the profile of trainer {trainer_id}"


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)