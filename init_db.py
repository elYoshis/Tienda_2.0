from app import create_app
from app.extensions import db
# Es vital importar los modelos aquí para que SQLAlchemy sepa qué tablas crear
from app.models import Category, Product

# Instanciamos la aplicación
app = create_app()

with app.app_context():
    # 1. Crear todas las tablas
    db.create_all()
    print("✅ Tablas creadas en la base de datos.")
    
    # 2. Insertar datos de prueba (Seeders) si la tabla está vacía
    if not Category.query.first():
        cat1 = Category(name='Peluches', slug='peluches', icon_url='icon-teddy.png')
        cat2 = Category(name='De madera', slug='de-madera', icon_url='icon-wood.png')
        cat3 = Category(name='Musicales', slug='musicales', icon_url='icon-music.png')
        
        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()
        print("✅ Categorías iniciales insertadas.")
        
    print("¡Base de datos tienda.db lista para usar!")