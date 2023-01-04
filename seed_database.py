import os
from datetime import datetime
from flask import Flask
from model import db, connect_to_db, User, Dog, Message, Post, Connect

app = Flask(__name__)

connect_to_db(app)

# Drop the existing database
try:
    os.system("dropdb -U postgres dog-app")
    os.system("createdb -U postgres dog-app")

# Recreate the dog-app database
except:
    os.system("createdb dog-app")

# Creates our tables
db.create_all()

# Dummy users

# Dog owners
user1 = User("Hank", "Hill", "propaneaccessories@gmail.com", "pass")
user2 = User("Peter", "Griffin", "whatgrindsmygears@email.com", "pass")
user3 = User("Bart", "Simpson", "eatmyshorts@email.com", "pass")
user4 = User("Austin", "Holmes", "aholmes@test.com", "pass")
user5 = User("Bennett", "Crowley", "bennett@email.com", "pass")

# Dog trainers
trainer1 = User("Caesar", "Milan", "dogwhipserer@email.com", "pass", is_trainer=True)
trainer2 = User("Zak", "George", "imalwaysnice@email.com", "pass", is_trainer=True)
trainer3 = User("American", "Standard", "imalwaysmean@email.com", "pass", is_trainer=True)
trainer4 = User("Heather", "White", "heathersk9community@email.com", "pass", is_trainer=True)

# Add dog owners and trainers
db.session.add_all([
    user1,
    user2,
    user3,
    user4,
    user5,
    trainer1,
    trainer2,
    trainer3,
    trainer4
])
db.session.commit()


# Dummy dogs
dog1 = Dog(1, "Lady Bird", "Golden Retriever", "Gold", datetime(1982, 6, 1), "No steaks cooked with charcoal.")
dog2 = Dog(2, "Brian", "Liberal Dog", "White", datetime(1995, 9, 1), "Vegan")
dog3 = Dog(3, "Santas Little Helper", "Greyhound", "Brown", datetime(1989, 12, 24), "eats food")
dog4 = Dog(4, "Kaya", "Border Collie", "White & Black", datetime(2020, 10, 24), "Only dog food.")
dog5 = Dog(5, "Charlie", "Great Dane / Weireimmer", "Brown & White", datetime(2021, 6, 1), "Kibble & Bits")

# Commit dogs to database
db.session.add_all([dog1, dog2, dog3, dog4, dog5])
db.session.commit()