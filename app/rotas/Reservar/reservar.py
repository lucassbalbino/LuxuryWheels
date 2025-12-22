from app.models import client_required, admin_required, Reservas, Veiculos, nova_reserva
from flask_login import current_user

from flask import Blueprint, render_template


reservar_bp = Blueprint('reservar', __name__, template_folder='templates')

@reservar_bp.route('/reservar_veiculo/<int:veiculo_id>', methods=['GET', 'POST'])
@client_required
def reservar_veiculo(veiculo_id):
    veiculos = Veiculos.query.filter_by(alugado=False, em_manuntenção=False).all()
    client = current_user
    form = nova_reserva()
    nova_reserva = Reservas(
         client_id=client.id, 
         veiculo_id=veiculo_id,
         nome=client.nome,
         data_inicio=None,  
         data_fim=None,    
         total=0.0,         
         metodo_pagamento='' )
    return render_template('reservar_veiculo.html', veiculos=veiculos)