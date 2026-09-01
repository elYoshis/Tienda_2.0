from flask import render_template, request, redirect, url_for
from app.admin import admin_bp
from app.extensions import db
from app.models import Product, Category

@admin_bp.route('/')
def dashboard():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin/dashboard.html', products=products)

@admin_bp.route('/producto/nuevo', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Capturamos los datos del formulario HTML
        name = request.form.get('name')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        category_id = int(request.form.get('category_id'))
        
        # Creamos la instancia del nuevo producto
        new_product = Product(
            name=name,
            price=price,
            stock_quantity=stock,
            category_id=category_id
        )
        
        # Guardamos en la base de datos
        db.session.add(new_product)
        db.session.commit()
        
        return redirect(url_for('admin.dashboard'))
    
    # Si es GET, mostramos el formulario cargando las categorías disponibles
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)