from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user
from app.database import db, bcrypt, admin_login_manager, client_login_manager
from app.models import LoginFormClient, LoginFormAdmin, Client, Admin


login_bp = Blueprint('login', __name__, template_folder='templates')

@client_login_manager.user_loader
def load_user(user_id):
   return Client.query.get(int(user_id))

@admin_login_manager.user_loader
def load_admin(admin_id):
   return Admin.query.get(int(admin_id))

@login_bp.route('/', methods=['GET', 'POST'])
def login_choice():
   return render_template('login_choice.html')

@login_bp.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
   form = LoginFormAdmin()
   if form.validate_on_submit():
       user = Admin.query.filter_by(company_name=form.company_name.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user)
           return redirect('dashboards')

   return render_template('login_admin.html', form=form)


@login_bp.route('/login_cliente', methods=['GET', 'POST'])
def login_cliente():
   form = LoginFormClient()
   if form.validate_on_submit():
       user = Client.query.filter_by(username=form.username.data).first()
       if user and bcrypt.check_password_hash(user.password, form.password.data):
           login_user(user)
           return redirect('dashboards')

   return render_template('login_cliente.html', form=form)


@login_bp.route('/logout', methods=['GET', 'POST'])
def logout():
   logout_user()
   return redirect(url_for('register.register_choice'))
