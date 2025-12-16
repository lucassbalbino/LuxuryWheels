from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
app.config['SECRET_KEY'] = 'LuxuryWheelsSecretKey'
db = SQLAlchemy(app)
class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), nullable=False, unique=True)
   password = db.Column(db.String(50), nullable=False)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def  register():
    return render_template('register.html')

@app.route('/dashboards')
def home():
    return render_template('dashboards.html')


if __name__ == '__main__':
    app.run(debug=True)
