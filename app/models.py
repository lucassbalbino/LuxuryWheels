from sqlalchemy import Enum
from app.database import db
from flask_login import UserMixin, current_user
from flask import abort
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError
from datetime import datetime as dt



class Client(db.Model, UserMixin):
   __table_args__ = {'extend_existing': True}
   __tablename__ = 'client'
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), nullable=False, unique=True)
   password = db.Column(db.String(50), nullable=False)


   
class Admin(db.Model, UserMixin):
   __table_args__ = {'extend_existing': True}
   __tablename__ = 'admin'
   id = db.Column(db.Integer, primary_key=True)
   NIPC = db.Column(db.String(20), nullable=False, unique=True)
   company_name = db.Column(db.String(50), nullable=False)
   password = db.Column(db.String(50), nullable=False)
   



class RegisterFormClient(FlaskForm):
   username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': ''})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': ''})
   submit = SubmitField('Register')
   def validate_username(self, username):
      existing_username = Client.query.filter_by(username=username.data).first()
      if existing_username:
         raise ValidationError("That username already exists. Please choose a different one.")

class RegisterFormAdmin(FlaskForm):
   company_name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Company Name'})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
   nipc = StringField(validators=[InputRequired(), Length(min=9, max=9)], render_kw={'placeholder': 'NIPC'})

   submit = SubmitField('Register')

   def validate_nipc(self, nipc):
      existing_nipc = Admin.query.filter_by(NIPC=nipc.data).first()
      if existing_nipc:
         raise ValidationError("That NIPC already exists. Please choose a different one.")



class LoginFormClient(FlaskForm):
   username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
   submit = SubmitField('Login')


class LoginFormAdmin(FlaskForm):
   company_name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Company Name'})
   nipc = StringField(validators=[InputRequired(), Length(min=9, max=9)], render_kw={'placeholder': 'Username'})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
   submit = SubmitField('Login')



class Veiculos(db.Model):
   __table_args__ = {'extend_existing': True}
   __tablename__ = 'veiculos'
   id = db.Column(db.Integer, primary_key=True)
   tipo = db.Column(Enum('Gold', 'Silver', 'Econômico', name='tipo_enum_tipo'), nullable=False)
   marca = db.Column(db.String(50), nullable=False)
   modelo = db.Column(db.String(50), nullable=False)
   ano = db.Column(db.Integer, nullable=False)
   diaria = db.Column(db.Float, nullable=False)
   categoria = db.Column(db.String(20), nullable=False)
   ultima_inspeçao = db.Column(db.Date, nullable=False)
   proxima_inspeçao = db.Column(db.Date, nullable=False)
   em_manutençao = db.Column(db.Boolean, nullable=False, default=False)
   alugado = db.Column(db.Boolean, nullable=False, default=False)
   legalizaçao = db.Column(db.Date, nullable=False)
   valor_legalizaçao = db.Column(db.Float, nullable=False)



class Reservas(db.Model):
   __table_args__ = {'extend_existing': True}
   __tablename__ = 'reservas'
   id = db.Column(db.Integer, primary_key=True)
   client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
   veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'), nullable=False)
   data_inicio = db.Column(db.Date, nullable=False)
   data_fim = db.Column(db.Date, nullable=False)
   total = db.Column(db.Float, nullable=False)
   metodo_pagamento = db.Column(db.String(20), nullable=False)

   cliente = db.relationship('Client', backref='clientes', lazy=True)
   veiculo = db.relationship('Veiculos', backref='veiculos_disponiveis', lazy=True)
   reservar_veiculo = db.relationship('Veiculos', backref='todas_reservas', lazy=True)








class add_Veiculo_Form(FlaskForm):
   tipo = SelectField('Tipo', choices=[('Gold', 'Gold'), ('Silver', 'Silver'), ('Econômico', 'Econômico')])
   marca = StringField('Marca', validators=[InputRequired(message="Marca é obrigatória"), Length(max=50)])
   modelo = StringField('Modelo', validators=[InputRequired(message="Modelo é obrigatório"), Length(max=50)])
   ano = IntegerField('Ano', validators=[InputRequired(message="Ano é obrigatório")])
   diaria = FloatField('Diária', validators=[InputRequired(message="Diária é obrigatória")])
   categoria = SelectField('Tipo', choices=[('Moto', 'Moto'), ('Carro', 'Carro')])
   ultima_inspeçao = StringField('Última Inspeção', validators=[InputRequired(message="Última Inspeção é obrigatória")])
   proxima_inspeçao = StringField('Próxima Inspeção', validators=[InputRequired(message="Próxima Inspeção é obrigatória")])
   em_manutençao = BooleanField('Em Manutenção')
   valor_legalizaçao = FloatField('Valor Legalização', validators=[InputRequired(message="Valor Legalização é obrigatório")])

   


   submit = SubmitField('Adicionar Veículo')


class nova_reserva(FlaskForm):

   data_inicio = StringField('Data Início', validators=[InputRequired(message="Data de início é obrigatória")])
   data_fim = StringField('Data Fim', validators=[InputRequired(message="Data de fim é obrigatória")])
   metodo_pagamento = SelectField('Método de Pagamento', choices=[('Cartão de Crédito', 'Cartão de Crédito'), ('PayPal', 'PayPal'), ('Transferência Bancária', 'Transferência Bancária')])
   submit = SubmitField('Reservar Veículo')


def client_required(func):
   def wrapper(*args, **kwargs):
      if not isinstance(current_user, Client):
         abort(403)
      return func(*args, **kwargs)
   wrapper.__name__ = func.__name__
   return wrapper



def admin_required(func):
   def wrapper(*args, **kwargs):
      if not isinstance(current_user, Admin):
         abort(403)
      return  func(*args, **kwargs)
   wrapper.__name__ = func.__name__
   return wrapper
      
def nova_reserva(Form):
   pass