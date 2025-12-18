from app.database import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

class Client(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), nullable=False, unique=True)
   password = db.Column(db.String(50), nullable=False)


   
class Admin(db.Model, UserMixin):
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
   company_name = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
   nipc = StringField(validators=[InputRequired(), Length(min=9, max=9)], render_kw={'placeholder': 'NIPC'})
   submit = SubmitField('Register')

   def validate_nipc(self, nipc):
      existing_nipc = Admin.query.filter_by(NIPC=nipc.data).first()
      if existing_nipc:
         raise ValidationError("That NIPC already exists. Please choose a different one.")



class LoginFormAdmin(FlaskForm):
   username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Username'})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
   submit = SubmitField('Login')


class LoginFormClient(FlaskForm):
   nipc = StringField(validators=[InputRequired(), Length(min=9, max=9)], render_kw={'placeholder': 'nipc'})
   password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={'placeholder': 'Password'})
   submit = SubmitField('Login')



class Veiculos(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   marca = db.Column(db.String(50), nullable=False)
   modelo = db.Column(db.String(50), nullable=False)
   ano = db.Column(db.Integer, nullable=False)
   preco = db.Column(db.Float, nullable=False)


class add_Veiculo_Form(FlaskForm):
   marca = StringField('Marca', validators=[InputRequired(message="Marca é obrigatória"), Length(max=50)])
   modelo = StringField('Modelo', validators=[InputRequired(message="Modelo é obrigatório"), Length(max=50)])
   ano = IntegerField('Ano', validators=[InputRequired(message="Ano é obrigatório")])
   preco = FloatField('Preço', validators=[InputRequired(message="Preço é obrigatório")])
   submit = SubmitField('Adicionar Veículo')


class Reservation(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'), nullable=False)
   start_date = db.Column(db.Date, nullable=False)
   end_date = db.Column(db.Date, nullable=False)