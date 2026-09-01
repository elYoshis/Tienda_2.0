from app.catalog import catalog_bp
from flask import render_template
from app.models import Category, Product

@catalog_bp.route('/catalogo')
def index():
    # Obtenemos todas las categorías y productos de la base de datos
    categories = Category.query.all()
    products = Product.query.all()
    
    return render_template('catalog/index.html', categories=categories, products=products)