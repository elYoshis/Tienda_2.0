from app.catalog import catalog_bp
from flask import render_template
from app.models import Category, Product
from flask import request, jsonify # Asegúrate de importar request y jsonify en la parte superior

@catalog_bp.route('/catalogo')
def index():
    # Obtenemos todas las categorías y productos de la base de datos
    categories = Category.query.all()
    products = Product.query.all()
    
    return render_template('catalog/index.html', categories=categories, products=products)

@catalog_bp.route('/api/productos')
def api_productos():
    # Empezamos con todos los productos
    query = Product.query
    
    # 1. Filtro por texto (Nombre del juguete)
    search = request.args.get('q', '')
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
        
    # 2. Filtro por tipo de juguete
    toy_type = request.args.get('type', '')
    if toy_type:
        query = query.filter(Product.toy_type == toy_type)
        
    # 3. Filtro por tamaño
    size = request.args.get('size', '')
    if size:
        query = query.filter(Product.size == size)
        
    # 4. Filtro por precio máximo
    max_price = request.args.get('max_price', type=float)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
        
    # Ejecutar la consulta
    products = query.all()
    
    # Convertir los resultados a diccionarios para enviarlos como JSON
    result = []
    for p in products:
        result.append({
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'main_image': p.main_image
        })
        
    return jsonify(result)

@catalog_bp.route('/categorias')
def categories_list():
    categories = Category.query.all()
    return render_template('catalog/categories.html', categories=categories)

@catalog_bp.route('/ofertas')
def offers():
    # Filtramos solo los productos que tienen un 'discount_price' configurado
    products = Product.query.filter(Product.discount_price.isnot(None)).all()
    return render_template('catalog/offers.html', products=products)

@catalog_bp.route('/novedades')
def new_arrivals():
    # Obtenemos los últimos 12 productos agregados a la base de datos
    products = Product.query.order_by(Product.id.desc()).limit(12).all()
    return render_template('catalog/new_arrivals.html', products=products)