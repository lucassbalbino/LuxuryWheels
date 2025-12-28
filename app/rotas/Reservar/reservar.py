from app.models import client_required, admin_required, Reservas, Veiculos, nova_reserva, db
from flask_login import current_user
import stripe
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime as dt


reservar_bp = Blueprint('reservar', __name__, template_folder='templates')

@reservar_bp.route('/reservar_veiculo/<int:veiculo_id>', methods=['GET'])
@client_required
def reservar_veiculo(veiculo_id):
   veiculo = Veiculos.query.get_or_404(veiculo_id)
   data_inicio = request.args.get('data_inicio')
   data_fim = request.args.get('data_fim')

   try: 
      dt_inicio = dt.strptime(data_inicio, '%Y-%m-%d').date()
      dt_fim = dt.strptime(data_fim, '%Y-%m-%d').date()
      dias_total = (dt_fim - dt_inicio).days
      if dias_total <= 0:
         flash('Data de fim deve ser após a data de início.', 'danger')
         return redirect(url_for('veiculos.display_veiculos'))
      valor_total = veiculo.diaria * dias_total
   except ValueError:
      flash('Data inválida.', 'danger')
      return redirect(url_for('veiculos.display_veiculos'))

   try:
      checkout_session = stripe.checkout.Session.create(
         payment_method_types=['card', 'mbway'],
         phone_number_collection={
            'enabled': True,
         },
         line_items=[
            {
               'price_data': {
                  'currency': 'eur',
                  'product_data': {
                     'name': f'Reserva de {veiculo.marca} {veiculo.modelo} por {dias_total} dias',
                  },
                  'unit_amount': int(valor_total * 100),
               },
               'quantity': 1,
            },
         ],
         mode='payment',
         metadata={
            'client_id': current_user.id,
            'veiculo_id': veiculo.id,
            'data_inicio': dt_inicio,
            'data_fim': dt_fim,
            'total_valor': valor_total,
         },
         success_url=url_for('dashboard.client_dashboard', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
         cancel_url=url_for('veiculos.display_veiculos', _external=True),
         
      )
   except:
      flash('Erro ao iniciar o pagamento. Por favor, tente novamente.', 'danger')
      return redirect(url_for('veiculos.display_veiculos'))
   return redirect(checkout_session.url, code=303)

@reservar_bp.route('/sucesso_pagamento', methods=['GET'])
@client_required
def sucesso_pagamento():
    session_id = request.args.get('session_id')
    
    if not session_id:
        return redirect(url_for('veiculos.display_veiculos'))

    try:
        # Recuperar a sessão do Stripe para confirmar pagamento e pegar dados
        session = stripe.checkout.Session.retrieve(session_id)
        
        # Verificar se já não foi processado (opcional, mas recomendado)
        
        data = session.metadata
        
        # Criar a reserva no banco de dados
        nova_reserva = Reservas(
            client_id=int(data['client_id']),
            veiculo_id=int(data['veiculo_id']),
            data_inicio=dt.strptime(data['data_inicio'], '%Y-%m-%d').date(),
            data_fim=dt.strptime(data['data_fim'], '%Y-%m-%d').date(),
            total=float(data['total']),
            metodo_pagamento='Stripe'
        )
        
        db.session.add(nova_reserva)
        db.session.commit()
        
        flash('Reserva confirmada com sucesso!', 'success')
        return render_template('sucesso.html')
      
    except:
      flash('Erro ao processar a reserva. Por favor, entre em contato com o suporte.', 'danger')
      return redirect(url_for('veiculos.display_veiculos'))
