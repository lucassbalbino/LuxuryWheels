
from flask import Flask, render_template, url_for, redirect, request
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from app.rotas.Veiculos.veiculos import veiculos_bp
from models.models import User, Veiculos
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





@app.route('/', methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       user = User.query.filter_by(username=form.username.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user)
           return redirect('dashboards')

   return render_template('login.html', form=form)






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
