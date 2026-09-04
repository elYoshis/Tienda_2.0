import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Clave secreta para sesiones y seguridad (cámbiala al desplegar)
    SECRET_KEY = 'super-secret-key-cajita-tesoros'
    
    # Configuración de SQLite (se creará un archivo tienda.db en la raíz)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'tienda.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # NUEVO: Configuración para la subida de imágenes
    # Las imágenes se guardarán en app/static/img/uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app/static/img/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Límite de 16 MB por archivo