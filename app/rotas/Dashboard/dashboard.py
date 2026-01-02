from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required
from app.models import Admin, Veiculos, admin_required, edit_Admin_Form, db

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboards')
@admin_required
def dashboards():

   total_veiculos = Veiculos.query.count()
   
   return render_template('dashboards.html')


@dashboard_bp.route('/admin_edit/<int:admin_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(admin_id):
   admin = Admin.query.get_or_404(admin_id)
   form = edit_Admin_Form(obj=admin)
   if form.validate_on_submit():
      admin.NIPC = form.NIPC.data
      admin.company_name = form.company_name.data
      db.session.commit()
      return redirect(url_for('dashboard.dashboards'))
   else:
      flash('Erro ao atualizar os dados. Por favor, tente novamente.', 'danger')
   return render_template('admin_edit.html', form=form, admin=admin)

@dashboard_bp.route('/admin_edit/<int:admin_id>')
@admin_required
def admin_view(admin_id):
   admin = Admin.query.get_or_404(admin_id)
   return render_template('admin_view.html', admin=admin)


@dashboard_bp.route('/admin_reservas/<int:admin_id>')
@admin_required
def admin_reservas(admin_id):
   admin = Admin.query.get_or_404(admin_id)
   reservas = admin.reservas_admin



@dashboard_bp.route('/logout')
@admin_required
def logout():
   from flask_login import logout_user
   logout_user()
   return redirect(url_for('login.login_admin'))
