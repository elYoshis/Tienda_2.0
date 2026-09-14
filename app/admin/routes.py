import os
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, current_app
from app.admin import admin_bp
from app.extensions import db
from app.models import Product, Category
from flask_login import login_required # <--- Nuevo import

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
@login_required # <--- CANDADO
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        category_id = int(request.form.get('category_id'))
        
        # --- NUEVO: Manejo de la imagen ---
        file = request.files.get('image')
        filename = None
        
        if file and file.filename != '' and allowed_file(file.filename):
            # secure_filename limpia el nombre (ej: "mi foto.jpg" -> "mi_foto.jpg")
            filename = secure_filename(file.filename)
            
            # Asegurarse de que la carpeta de destino exista
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Guardar el archivo en el servidor
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        # ----------------------------------
        
        new_product = Product(
            name=name,
            price=price,
            stock_quantity=stock,
            category_id=category_id,
            main_image=filename # Guardamos el nombre del archivo en la base de datos
        )
        
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)