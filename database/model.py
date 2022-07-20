from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import *
from ..settings import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class Users(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(1638), nullable=True)
    role = db.Column(db.Integer)

    def __init__(self, name, email, password="", role=0):
        self.name = name
        self.password = password
        self.email = email
        self.role = role

    def serialize(self):
        return{

            "name": self.name,
            "email": self.email,
            "role": self.role
        }

class BlacklistedTokens(db.Model):
    token = db.Column(db.String(1638), primary_key=True, nullable=False)

    def __init__(self, token):
        self.token = token

def create():
    db.drop_all()
    db.create_all()
