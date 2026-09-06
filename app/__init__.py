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

    # NUEVO: Registrar el catálogo
    from app.catalog import catalog_bp
    app.register_blueprint(catalog_bp)

    # NUEVO: Registrar el panel de administrador
    from app.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    # NUEVO: Registrar el carrito
    from app.cart import cart_bp
    app.register_blueprint(cart_bp)

    return app