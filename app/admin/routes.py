import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_required
from app.admin import admin_bp
from app.extensions import db
from app.models import Product, Category

# Extensiones de imagen permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/')
@login_required
def dashboard():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('admin/dashboard.html', products=products)

@admin_bp.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        
        # Capturamos el precio de descuento
        discount_price_raw = request.form.get('discount_price')
        discount_price = float(discount_price_raw) if discount_price_raw else None
        
        stock = int(request.form.get('stock'))
        category_id = int(request.form.get('category_id'))
        
        # Manejo de la imagen
        file = request.files.get('image')
        filename = None
        
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        # Guardamos en la base de datos
        new_product = Product(
            name=name,
            price=price,
            discount_price=discount_price,
            stock_quantity=stock,
            category_id=category_id,
            main_image=filename
        )
        
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

# app/admin/routes.py (Añadir al final del archivo)

@admin_bp.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    # Buscamos el producto por su ID
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        # Actualizamos los datos
        product.name = request.form.get('name')
        product.price = float(request.form.get('price'))
        
        discount_price_raw = request.form.get('discount_price')
        product.discount_price = float(discount_price_raw) if discount_price_raw else None
        
        product.stock_quantity = int(request.form.get('stock'))
        product.category_id = int(request.form.get('category_id'))
        
        # Manejo de imagen (solo actualiza si el usuario sube una nueva)
        file = request.files.get('image')
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            product.main_image = filename # Reemplazamos la imagen vieja
            
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    
    # Si es GET, cargamos las categorías y enviamos el producto actual a la vista
    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@admin_bp.route('/producto/eliminar/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))