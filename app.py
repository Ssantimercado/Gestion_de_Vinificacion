# app.py

import os
from flask import Flask, render_template, redirect, url_for, send_from_directory
from extensions import db             # Importa 'db' desde extensions.py
from dotenv import load_dotenv        # Importa para cargar .env

# Carga las variables de entorno desde el archivo .env
# ¡Esta línea es clave para que el .env "haga algo"!
load_dotenv()

# --- Instancia de la Aplicación Flask ---
app = Flask(__name__)

# --- Configuración de la Aplicación ---
# Ahora obtenemos la configuración de la base de datos y la SECRET_KEY del archivo .env
# Si no se encuentra la variable de entorno, se usa un valor por defecto (fallback)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'una_clave_secreta_por_defecto_para_desarrollo')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') # No hay fallback si no está en .env, ya que siempre esperas MySQL

# Asegúrate de que Flask no emita advertencias sobre el seguimiento de modificaciones de objetos SQLAlchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Configuración de la Carpeta de Subidas de Fotos ---
# Esta ruta DEBE COINCIDIR con la UPLOAD_FOLDER en routes/variedad.py
# La ruta es relativa a la raíz del proyecto.
UPLOAD_FOLDER_VARIEDADES_RELATIVE = 'static/fotos_variedades'
app.config['UPLOAD_FOLDER_VARIEDADES'] = os.path.join(app.root_path, UPLOAD_FOLDER_VARIEDADES_RELATIVE)

# Asegura que la carpeta de subidas exista al inicio de la aplicación
# (Esto crea las carpetas 'static' y 'fotos_variedades' si no existen)
os.makedirs(app.config['UPLOAD_FOLDER_VARIEDADES'], exist_ok=True)

# --- Inicialización de Extensiones ---
db.init_app(app)       # Inicializa SQLAlchemy con la aplicación

# --- Importar y Registrar Blueprints ---
# La importación y el registro deben hacerse DESPUÉS de crear la instancia 'app'
from routes.variedad import variedad_bp
app.register_blueprint(variedad_bp)

# --- Rutas Principales de la Aplicación ---
@app.route('/')
def index():
    return render_template('index.html') # Asumiendo que tienes un index.html en tu carpeta templates

# --- Ejecución de la Aplicación ---
if __name__ == '__main__':
    # en tu base de datos MySQL al iniciar la aplicación por primera vez.
    # Asegúrate de que tu MySQL esté corriendo y que la base de datos 'bodega' exista.
    with app.app_context():
        db.create_all()

    # El modo debug se controla a través de la variable de entorno FLASK_DEBUG
    # En tu .env: FLASK_DEBUG=True para desarrollo, FLASK_DEBUG=False para producción
    app.run(debug=os.getenv('FLASK_DEBUG') == 'True')