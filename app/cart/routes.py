from flask import render_template, request, redirect, url_for, session, flash
from app.cart import cart_bp
from app.models import Product
import urllib.parse

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

@cart_bp.route('/checkout')
def checkout_whatsapp():
    # Obtener el carrito actual
    cart = session.get('cart', {})
    
    # Si el carrito está vacío, lo devolvemos a la página del carrito
    if not cart:
        return redirect(url_for('cart.index'))
        
    total = sum(item['price'] * item['quantity'] for item in cart.values())
    
    # 1. Armar el mensaje de texto
    mensaje = "👋 ¡Hola Cajita de Tesoros! Me gustaría realizar el siguiente pedido:\n\n"
    
    for item in cart.values():
        subtotal = item['price'] * item['quantity']
        mensaje += f"▪️ {item['quantity']}x {item['name']} - Bs. {subtotal}\n"
        
    mensaje += f"\n💰 *Total a pagar: Bs. {total}*\n\n"
    mensaje += "Por favor, indíquenme los métodos de pago (QR/Transferencia) y cómo coordinamos el envío a mi dirección."
    
    # 2. Codificar el mensaje para que sea válido en una URL
    mensaje_codificado = urllib.parse.quote(mensaje)
    
    # 3. Tu número de teléfono (Asegúrate de incluir el código de país, ej: 591 para Bolivia)
    # Reemplaza '59170000000' con el número real de atención al cliente de la juguetería
    numero_tienda = "59165434972" 
    
    # 4. Generar el enlace de la API
    whatsapp_url = f"https://wa.me/{numero_tienda}?text={mensaje_codificado}"
    
    # 5. Vaciar el carrito porque el pedido ya pasó a WhatsApp
    session.pop('cart', None)
    session.modified = True
    
    # 6. Redirigir al usuario
    return redirect(whatsapp_url)