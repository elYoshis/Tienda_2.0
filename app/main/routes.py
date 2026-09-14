from flask import render_template
from app.main import main_bp
from app.models import Category, Product

@main_bp.route('/')
def index():
    # Obtenemos todas las categorías para mostrarlas en los botones circulares
    categories = Category.query.all()
    
    # Obtenemos los 4 últimos productos agregados para la sección de "Novedades"
    latest_products = Product.query.filter_by(is_active=True).order_by(Product.id.desc()).limit(4).all()
    
    return render_template('main/index.html', categories=categories, products=latest_products)

@main_bp.route('/contacto')
def contact():
    return render_template('main/contact.html')