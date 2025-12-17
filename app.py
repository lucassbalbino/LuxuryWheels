
from flask import Flask, render_template, url_for, redirect, request
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from rotas.veiculos import veiculos_bp

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'database.db')}"
app.config['SECRET_KEY'] = 'LuxuryWheelsSecretKey'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.register_blueprint(veiculos_bp)


@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))


class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), nullable=False, unique=True)
   password = db.Column(db.String(50), nullable=False)


class RegisterForm(FlaskForm):
   username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': ''})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': ''})
   submit = SubmitField('Register')

   def validate_username(self, username):
       existing_username = User.query.filter_by(username=username.data).first()
       if existing_username:
           raise ValidationError("That username already exists. Please choose a different one.")




class LoginForm(FlaskForm):
   username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
   submit = SubmitField('Login')



class Veiculos(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   marca = db.Column(db.String(50), nullable=False)
   modelo = db.Column(db.String(50), nullable=False)
   ano = db.Column(db.Integer, nullable=False)
   preco = db.Column(db.Float, nullable=False)


@app.route('/', methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       user = User.query.filter_by(username=form.username.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user)
           return redirect('dashboards')

   return render_template('login.html', form=form)





@app.route('/register', methods=['GET', 'POST'])
def  register():
   form = RegisterForm()
    


   if request.method == 'POST': 
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         new_user = User(username=form.username.data, password=hashed_password)
         db.session.add(new_user)
         db.session.commit()
         return redirect(url_for('login'))

   return render_template('register.html', form=form)



@app.route('/dashboards')
@login_required
def home():
   return render_template('dashboards.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
   logout_user()
   return redirect(url_for('login'))



if __name__ == '__main__':
   app.run(debug=True)
