from flask import Flask
from config import Config
from app.extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    
    # --- NUEVA CONFIGURACIÓN DE LOGIN ---
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # A dónde enviar a los intrusos
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    # ------------------------------------

    from app.main import main_bp
    app.register_blueprint(main_bp)
    
    from app.catalog import catalog_bp
    app.register_blueprint(catalog_bp)
    
    from app.cart import cart_bp
    app.register_blueprint(cart_bp)
    
    from app.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from app.auth import auth_bp # <--- Registrar el nuevo Blueprint
    app.register_blueprint(auth_bp)

    return app