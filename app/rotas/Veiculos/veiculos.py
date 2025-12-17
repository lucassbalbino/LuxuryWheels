from flask import Blueprint, render_template, redirect, url_for
from app import db, Veiculos
veiculos_bp = Blueprint('veiculos', __name__)
veiculos_bp.route('/display_veiculos')

def display_veiculos():
    veiculo = Veiculos.query.all()
    return render_template('display_veiculos.html', veiculo=veiculo)


def add_veiculo():
    # Lógica para adicionar um novo veículo
    pass

def del_veiculo():
    # Lógica para deletar um veículo
    pass

def update_veiculo():
      # Lógica para atualizar um veículo
      pass