from flask import Blueprint

main_bp = Blueprint('main', __name__)

# Importamos las rutas al final para evitar dependencias circulares
from app.main import routes