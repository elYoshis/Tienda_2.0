from flask import render_template, request, redirect, url_for, session, flash
from app.cart import cart_bp
from app.models import Product

@cart_bp.route('/')
def index():
    # Obtener el carrito de la sesión (o un diccionario vacío si no existe)
    cart = session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart/index.html', cart=cart, total=total)

@cart_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Si 'cart' no está en la sesión, lo creamos
    if 'cart' not in session:
        session['cart'] = {}
        
    cart = session['cart']
    product_id_str = str(product_id) # Las claves de sesión deben ser strings
    
    # Si el producto ya está, aumentamos la cantidad
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        # Si no está, lo agregamos con sus datos básicos
        cart[product_id_str] = {
            'name': product.name,
            'price': product.price,
            'quantity': 1,
            'image': product.main_image
        }
        
    session.modified = True # Le decimos a Flask que guarde los cambios
    return redirect(url_for('catalog.index'))

@cart_bp.route('/remove/<product_id>')
def remove_item(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        session.modified = True
    return redirect(url_for('cart.index'))