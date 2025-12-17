from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user
from app import app, db, Veiculos
from app.models.models import RegisterForm, LoginForm, User, bcrypt

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/', methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       user = User.query.filter_by(username=form.username.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user)
           return redirect('dashboards')

   return render_template('login.html', form=form)



@login_bp.route('/register', methods=['GET', 'POST'])
def  register():
   form = RegisterForm()
    


   if request.method == 'POST': 
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         new_user = User(username=form.username.data, password=hashed_password)
         db.session.add(new_user)
         db.session.commit()
         return redirect(url_for('login'))

   return render_template('register.html', form=form)
