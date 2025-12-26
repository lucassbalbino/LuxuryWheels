from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from app.models import Veiculos
from app.database import db
from app.models import add_Veiculo_Form, client_required, admin_required, edit_Veiculo_Form

alugar_bp = Blueprint('alugar', __name__, template_folder='templates')

@alugar_bp.route('/alugar_veiculo/<int:id>', methods=['GET', 'POST'])
@client_required
def alugar_veiculo(id):
   return render_template('alugar_veiculo.html', veiculo_id=id)