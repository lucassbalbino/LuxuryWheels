from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from app.models import Veiculos
from app.database import db
from app.models import add_Veiculo_Form, client_required, admin_required, edit_Veiculo_Form


veiculos_bp = Blueprint('veiculos', __name__, template_folder='templates')

@veiculos_bp.route('/display_veiculos')
def display_veiculos():
    veiculo = Veiculos.query.filter_by(alugado=False, em_manutençao=False).all()
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
            diaria=form.diaria.data,
            categoria=form.categoria.data,
            ultima_inspeçao=form.ultima_inspeçao.data,
            proxima_inspeçao=form.proxima_inspeçao.data,
            em_manutençao=form.em_manutençao.data,
            legalizaçao=form.legalizaçao.data,
            valor_legalizaçao=form.valor_legalizaçao.data,
        )
        db.session.add(new_veiculo)
        db.session.commit()
        return redirect(url_for('veiculos.display_veiculos'))
    return render_template('add_veiculo.html', form=form)



@veiculos_bp.route('/del_veiculo', methods=['POST'])
def del_veiculo():
    # Lógica para deletar um veículo
    pass


@veiculos_bp.route('/editar_veiculo/<int:id>', methods=['GET', 'POST'])
def editar_veiculo(id):
   veiculo = Veiculos.query.get_or_404(id)
   form = edit_Veiculo_Form(obj=veiculo)

   if form.validate_on_submit():
       veiculo.tipo = form.tipo.data
       veiculo.marca = form.marca.data
       veiculo.modelo = form.modelo.data
       veiculo.ano = form.ano.data
       veiculo.diaria = form.diaria.data
       veiculo.categoria = form.categoria.data
       veiculo.ultima_inspeçao = form.ultima_inspeçao.data
       veiculo.proxima_inspeçao = form.proxima_inspeçao.data
       veiculo.em_manutençao = form.em_manutençao.data
       veiculo.legalizaçao = form.legalizaçao.data
       veiculo.valor_legalizaçao = form.valor_legalizaçao.data
       veiculo.alugado = form.alugado.data
       db.session.commit()
       return redirect(url_for('veiculos.display_veiculos'))
   return render_template('editar_veiculo.html', form=form, veiculo=veiculo)