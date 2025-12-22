from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from app.models import Veiculos
from app.database import db
from app.models import add_Veiculo_Form, client_required, admin_required


veiculos_bp = Blueprint('veiculos', __name__, template_folder='templates')

@veiculos_bp.route('/display_veiculos')
@client_required
def display_veiculos():
    veiculo = Veiculos.query.all()
    return render_template('display_veiculos.html', veiculo=veiculo)

@veiculos_bp.route('/add_veiculo', methods=['GET', 'POST'])
@admin_required
def add_veiculo():
    form = add_Veiculo_Form()
    if form.validate_on_submit():
        new_veiculo = Veiculos(
            tipo=form.tipo.data,
            marca=form.marca.data,
            modelo=form.modelo.data,
            ano=form.ano.data,
            diária=form.diária.data,
            categoria=form.categoria.data,
            ultima_inspeção=form.ultima_inspeção.data,
            proxima_inspeção=form.proxima_inspeção.data,
            manuntenção=form.manutenção.data,
            legalização=form.legalização.data,
            alugado=form.alugado.data
        )
        db.session.add(new_veiculo)
        db.session.commit()
        return redirect(url_for('veiculos.display_veiculos'))
    return render_template('add_veiculo.html', form=form)



@veiculos_bp.route('/del_veiculo', methods=['POST'])
def del_veiculo():
    # Lógica para deletar um veículo
    pass


@veiculos_bp.route('/update_veiculo', methods=['GET', 'POST'])
def update_veiculo():
      # Lógica para atualizar um veículo
      pass