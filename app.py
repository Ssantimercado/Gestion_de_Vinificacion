import os
from flask import Flask, redirect, url_for, send_from_directory
from extensions import db
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Crear la aplicación
app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave_secreta_default')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///vinificacion.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Carpeta de subida para fotos de variedades
app.config['UPLOAD_FOLDER'] = 'uploads/fotos_variedades'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar la base de datos
db.init_app(app)

# Ruta para servir imágenes
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Registrar blueprints
from routes.variedad import variedad_bp
from routes.crianza_routes import crianza_bp
from routes.embotellado_routes import embotellado_bp

app.register_blueprint(variedad_bp)
app.register_blueprint(crianza_bp)
app.register_blueprint(embotellado_bp)

# Redirigir al inicio
@app.route('/')
def index():
    return redirect(url_for('variedad.listar_variedades'))

# Ejecutar la app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=os.getenv('FLASK_DEBUG') == 'True')
