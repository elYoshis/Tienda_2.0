from app.main import main_bp
from flask import render_template

@main_bp.route('/')
def index():
    # Más adelante cambiaremos esto por render_template('index.html')
    return "<h1>¡Bienvenido a Cajita de Tesoros!</h1><p>El backend funciona correctamente.</p>"