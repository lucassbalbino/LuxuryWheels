from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.models import Client, Admin
from app.database import db
from flask_migrate import Migrate
import os



BASE_DIR = os.path.abspath(os.path.dirname(__file__))

bcrypt = Bcrypt()
client_login_manager = LoginManager()
admin_login_manager = LoginManager()

@client_login_manager.user_loader
def load_client(client_id):
   return Client.query.get(int(client_id))

@admin_login_manager.user_loader
def load_admin(admin_id):
   return Admin.query.get(int(admin_id))

def create_app():
   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'database.db')}"
   app.config['SECRET_KEY'] = 'LuxuryWheelsSecretKey'

   migrate = Migrate(app, db)

   client_login_manager.init_app(app)
   admin_login_manager.init_app(app)

   from app.rotas.Veiculos.veiculos import veiculos_bp
   from app.rotas.Login.login import login_bp
   from app.rotas.Dashboard.dashboard import dashboard_bp
   from app.rotas.Register.register import register_bp  
   from app.rotas.Alugar.alugar import alugar_bp 

   app.register_blueprint(register_bp)
   app.register_blueprint(veiculos_bp)
   app.register_blueprint(login_bp)
   app.register_blueprint(dashboard_bp)
   app.register_blueprint(alugar_bp)
   db.init_app(app)
   return app

