from flask import Blueprint, render_template, redirect, url_for
from app import db, Veiculos
veiculos_bp = Blueprint('veiculos', __name__, template_folder='../templates')

veiculos_bp.route('/display_veiculos')

def display_veiculos():
    veiculo = Veiculos.query.all()
    return render_template('display_veiculos.html', veiculo=veiculo)