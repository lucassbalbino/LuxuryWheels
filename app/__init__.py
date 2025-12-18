from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.models import User
from app.database import db
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

def create_app():
   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'database.db')}"
   app.config['SECRET_KEY'] = 'LuxuryWheelsSecretKey'



   login_manager.init_app(app)
   login_manager.login_view = 'login'

   from app.rotas.Veiculos.veiculos import veiculos_bp
   from app.rotas.Login.login import login_bp
   from app.rotas.Dashboard.dashboard import dashboard_bp
   app.register_blueprint(veiculos_bp)
   app.register_blueprint(login_bp)
   app.register_blueprint(dashboard_bp)
   db.init_app(app)
   return app

