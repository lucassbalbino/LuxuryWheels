from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), nullable=False)
   password = db.Column(db.String(50), nullable=False)
   

