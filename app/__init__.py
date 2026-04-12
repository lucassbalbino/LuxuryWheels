from flask import Flask
from config import Config
from app.extensions import db, bcrypt, migrate, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from flask import session
        from app.models import Client, Admin
        user_type = session.get('user_type', 'client')
        if user_type == 'admin':
            return Admin.query.get(int(user_id))
        return Client.query.get(int(user_id))

    # Register blueprints
    from app.blueprints import login_bp, register_bp, dashboard_bp, home_bp, veiculos_bp, reservar_bp
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(reservar_bp)

    return app

