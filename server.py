from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return "welcome to the login page"
    else:
        return "you are trying to login"

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return "this is the register page"
    else:
        return "trying to register"

@app.route("/home")
def home():
    return "this is the home page"

@app.route("/messages")
def messages():
    return "here are all your messages"


@app.route("/profile/<trainer_id>")
def profile(trainer_id):
    return f"this is the profile of trainer {trainer_id}"


if __name__ == "__main__":
    app.run(debug=True)