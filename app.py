# app.py

import os
from flask import Flask, render_template, redirect, url_for, send_from_directory
from dotenv import load_dotenv
from extensions import db #Importamos 'db' desde extensions.py

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# --- Instancia de la Aplicación Flask ---
app = Flask(__name__)

# --- Configuración de la Aplicación ---
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'una_clave_secreta_por_defecto_para_desarrollo')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Configuración de la Carpeta de Subidas de Fotos ---
UPLOAD_FOLDER_VARIEDADES_RELATIVE = 'static/fotos_variedades'
app.config['UPLOAD_FOLDER_VARIEDADES'] = os.path.join(app.root_path, UPLOAD_FOLDER_VARIEDADES_RELATIVE)
os.makedirs(app.config['UPLOAD_FOLDER_VARIEDADES'], exist_ok=True)

# --- Inicialización de Extensiones ---
db.init_app(app)

#Importar Modelos para que SQLAlchemy los registre
# Importa solo los módulos (archivos) de modelos aquí, no las clases individuales.
# Esto asegura que el código de definición de cada clase se ejecute y SQLAlchemy las conozca.
import models.variedad          # Asume que tu modelo de VariedadUva está en models/variedad.py
import models.embotellado_models # Asume que tu modelo de Embotellado está en models/embotellado_models.py
import models.crianza_models     # Asume que tu modelo de Crianza está en models/crianza_models.py
import models.fermentacion      # Asume que tu modelo de Fermentacion está en models/fermentacion.py
import models.recepcion         # Asume que tu modelo de RecepcionUva está en models/recepcion.py

# --- Importar y Registrar Blueprints ---
from routes.variedad import variedad_bp
from routes.embotellado_routes import embotellado_bp
from routes.crianza_routes import crianza_bp
from routes.fermentacion_routes import fermentacion_bp
from routes.recepcion_routes import recepcion_bp

app.register_blueprint(variedad_bp)
app.register_blueprint(embotellado_bp)
app.register_blueprint(crianza_bp)
app.register_blueprint(fermentacion_bp)
app.register_blueprint(recepcion_bp)


# --- Rutas Principales de la Aplicación ---
@app.route('/')
def index():
    return redirect(url_for('variedad.listar_variedades'))

# --- Ruta para servir archivos estáticos (fotos de variedades) ---
@app.route(f'/{UPLOAD_FOLDER_VARIEDADES_RELATIVE}/<path:filename>')
def serve_variedad_photo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_VARIEDADES'], filename)


# --- Ejecución de la Aplicación ---
if __name__ == '__main__':
    with app.app_context():
        # db.create_all() debe ejecutarse DENTRO del contexto de la aplicación,
        # y DESPUÉS de que todas las clases de modelo hayan sido importadas
        # (para que SQLAlchemy sepa de su existencia).
        db.create_all()

    app.run(debug=os.getenv('FLASK_DEBUG') == 'True')