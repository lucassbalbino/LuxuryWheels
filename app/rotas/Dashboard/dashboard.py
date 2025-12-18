from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard_bp.route('/dashboards')
@login_required
def home():
   return render_template('dashboards.html')