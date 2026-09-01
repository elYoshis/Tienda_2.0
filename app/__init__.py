from flask import Flask
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar las extensiones con la app
    db.init_app(app)

    # Registrar Blueprints (Módulos)
    from app.main import main_bp
    app.register_blueprint(main_bp)
    
    # Nota: Aquí iremos registrando catalog_bp, admin_bp, cart_bp más adelante.

    return app