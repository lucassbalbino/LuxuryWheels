from app.models import client_required, admin_required, Reservas, Veiculos, nova_reserva
from flask_login import current_user

from flask import Blueprint, render_template


reservar_bp = Blueprint('reservar', __name__, template_folder='templates')

@reservar_bp.route('/reservar_veiculo/<int:veiculo_id>', methods=['GET', 'POST'])
@client_required
def reservar_veiculo(veiculo_id):
   return render_template('reservar_veiculo.html', veiculo_id=veiculo_id)

