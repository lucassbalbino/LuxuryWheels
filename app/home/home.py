from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from app.models import Veiculos, pesquisa_Veiculo_Form, Reservas
from app.database import db
from app.models import add_Veiculo_Form, client_required, admin_required, edit_Veiculo_Form

home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route('/home_page', methods=['GET', 'POST'])
@client_required
def home_page():
   form = pesquisa_Veiculo_Form()
   if form.validate_on_submit():
      return redirect(url_for('veiculos.display_veiculos'))
   return render_template('home_page.html', form=form)


