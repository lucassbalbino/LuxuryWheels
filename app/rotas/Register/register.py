from app.database import db, bcrypt, login_manager
from app.models import RegisterFormAdmin, RegisterFormClient, Client, Admin
from flask import Blueprint, render_template, redirect, url_for, request

register_bp = Blueprint('register', __name__, template_folder='templates')



@register_bp.route('/', methods=['GET', 'POST'])
def register_choice():
   return render_template('register_choice.html')


@register_bp.route('/register_cliente', methods=['GET', 'POST'])
def  register():
   form = RegisterFormClient()

   if request.method == 'POST': 
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         new_user = Client(username=form.username.data, password=hashed_password)
         db.session.add(new_user)
         db.session.commit()
         return redirect(url_for('login'))

   return render_template('register.html', form=form)



@register_bp.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
   form = RegisterFormAdmin()

   if request.method == 'POST': 
         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
         new_admin = Admin(company_name=form.company_name.data, NIPC=form.nipc.data, password=hashed_password)
         db.session.add(new_admin)
         db.session.commit()
         return redirect(url_for('login'))

   return render_template('register_admin.html', form=form)
