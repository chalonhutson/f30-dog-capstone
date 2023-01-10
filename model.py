import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(199), nullable=False, unique=True)
    password = db.Column(db.String(299), nullable=False)
    is_trainer = db.Column(db.Boolean, default=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now())

    dogs = db.relationship("Dog", backref="user", lazy=True)

    def get_received_messages(self):
        return Message.query.filter_by(to_user_id=self.id).all()

    def get_sent_messages(self):
        return Message.query.filter_by(from_user_id=self.id).all()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, first_name, last_name, email, password, is_trainer=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_trainer = is_trainer

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"

class Dog(db.Model):
    __tablename__ = "dogs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    breed = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.DateTime, nullable=True)
    dietary_info = db.Column(db.String(999), nullable=True)
    datetime_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_id, name, breed, color, birthday, dietary_info):
        self.user_id = user_id
        self.name = name
        self.breed = breed
        self.color = color
        self.birthday = birthday
        self.dietary_info = dietary_info

    def __repr__(self):
        return f"<Dog {self.name}>"


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dog_id = db.Column(db.Integer, db.ForeignKey("dogs.id"), nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now())

    # dog = db.relationship("Dog", backref="messages")

    def get_message_sender(self):
        return User.query.get(self.from_user_id)


    def __init__(self, dog_id, from_user_id, to_user_id, content):
        self.dog_id = dog_id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.content = content

    def __repr__(self):
        return f"<Message {self.content}>"

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content

    def __repr__(self):
        return f"<Post {self.content}>"

class Connect(db.Model):
    __tablename__ = "connection"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    connecter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    connectee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    datetime_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, connecter_id, connectee_id):
        self.connecter_id = connecter_id
        self.connectee_id = connectee_id


def connect_to_db(app, db_uri=os.environ["DATABASE_URI"]):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.app = app
    db.init_app(app)
    print("You are connected to the doggo app bruh!!!!")


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)