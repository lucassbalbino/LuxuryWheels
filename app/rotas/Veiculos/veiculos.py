from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from app.models import Reservas, Veiculos, pesquisa_Veiculo_Form
from app.database import db
from app.models import add_Veiculo_Form, client_required, admin_required, edit_Veiculo_Form
from datetime import datetime

veiculos_bp = Blueprint('veiculos', __name__, template_folder='templates')

@veiculos_bp.route('/display_veiculos')
@client_required
def display_veiculos():
    form = pesquisa_Veiculo_Form()
    dias = 0
    
    # Captura os parâmetros
    tipo_arg = request.args.get('tipo')
    categoria_arg = request.args.get('categoria')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    # 1. Query Base (Apenas não alugados e sem manutenção)
    query = Veiculos.query.filter_by(alugado=False, em_manutençao=False)

    # 2. Filtros Dinâmicos (Verifica se existe valor na URL antes de filtrar)
    if tipo_arg and tipo_arg.strip() != 'Todos':
        # Filtra pelo tipo (ex: Carro) se foi passado na URL
        query = query.filter(Veiculos.tipo.ilike(tipo_arg.strip()))
    
    if categoria_arg and categoria_arg.strip() != 'Todas':
        # Filtra pela categoria (ex: Gold) se foi passado na URL
        query = query.filter(Veiculos.categoria.ilike(categoria_arg.strip()))

    # 3. Filtro de Datas (Lógica de Disponibilidade)
    if data_inicio and data_fim:
        try:
            dt_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            dt_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            dias = (dt_fim - dt_inicio).days
            if dias <= 0:
                return render_template('display_veiculos.html', veiculos=[], form=form, error="Data de fim deve ser após a data de início.")
        except ValueError:
            return render_template('display_veiculos.html', veiculos=[], form=form, error="Data inválida.")

        # Subquery para encontrar IDs de veículos ocupados nesse período
        veiculos_ocupados = db.session.query(Reservas.veiculo_id).filter(
            (Reservas.data_inicio <= dt_fim) & 
            (Reservas.data_fim >= dt_inicio)
        )
        
        # Adiciona à query principal: EXCLUIR veículos que estão na lista de ocupados
        query = query.filter(~Veiculos.id.in_(veiculos_ocupados))

    # 4. Executa a query final (APENAS UMA VEZ)
    veiculos_disponiveis = query.all()

    return render_template('display_veiculos.html', dias=dias,veiculos=veiculos_disponiveis, form=form)

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




@veiculos_bp.route('/editar_veiculo/<int:id>', methods=['GET', 'POST'])
@admin_required
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
       return redirect(url_for('veiculos.display_veiculos_admin'))
   return render_template('editar_veiculo.html', form=form, veiculo=veiculo)

@veiculos_bp.route('/deletar_veiculo/<int:id>', methods=['POST'])
@admin_required
def deletar_veiculo(id):
   veiculo = Veiculos.query.get_or_404(id)
   db.session.delete(veiculo)
   db.session.commit()
   flash('Veículo deletado com sucesso!', 'success')
   return redirect(url_for('veiculos.display_veiculos_admin'))

@veiculos_bp.route('/display_veiculos_admin')
@admin_required
def display_veiculos_admin():
    veiculo = Veiculos.query.all()
    return render_template('display_veiculos_admin.html', veiculo=veiculo)



@veiculos_bp.route('/manutençao_veiculo/<int:id>', methods=['POST'])
@admin_required
def manutençao_veiculo(id):
    veiculo = Veiculos.query.get_or_404(id)
    veiculo.em_manutençao = True
    db.session.commit()
    flash('Veículo colocado em manutenção com sucesso!', 'success')
    return redirect(url_for('veiculos.display_veiculos_admin'))

@veiculos_bp.route('/concluir_manutençao_veiculo/<int:id>', methods=['POST'])
@admin_required
def concluir_manutençao_veiculo(id):
    veiculo = Veiculos.query.get_or_404(id)
    veiculo.em_manutençao = False
    db.session.commit()
    flash('Manutenção do veículo concluída com sucesso!', 'success')
    return redirect(url_for('veiculos.display_veiculos_admin'))