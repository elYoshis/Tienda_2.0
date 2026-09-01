from app.extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True) # Ej: Peluches, De madera
    slug = db.Column(db.String(100), nullable=False, unique=True) # Para URLs limpias (ej: /categoria/de-madera)
    icon_url = db.Column(db.String(200), nullable=True) # Para los iconos de la interfaz
    
    # Relación uno a muchos con Product
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Precios pensados para manejarse en bolivianos (Bs.)
    price = db.Column(db.Float, nullable=False) 
    discount_price = db.Column(db.Float, nullable=True) # Llenar solo si hay ofertas/rebajas
    
    stock_quantity = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True) # Para ocultar juguetes sin borrarlos de la BD
    
    # Filtros y clasificaciones (según tu diseño)
    toy_type = db.Column(db.String(100), nullable=True) # "Tipo de juguete" en el buscador
    size = db.Column(db.String(50), nullable=True) # "Tamaño" en el buscador
    season = db.Column(db.String(100), nullable=True) # "Temporadas" (Ej: Navidad, Día del niño)
    
    main_image = db.Column(db.String(255), nullable=True)
    
    # Auditoría básica
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Llave foránea hacia categorías
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f"<Product {self.name} - Bs. {self.price}>"