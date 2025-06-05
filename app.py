from flask import Flask, render_template, redirect, url_for, send_from_directory
import os
from extensions import db  # <--- Importa 'db' desde extensions.py

app = Flask(__name__)
app.config['SECRET_KEY'] = '451433203SANGERPA'
app.config['UPLOAD_FOLDER'] = 'uploads/fotos_variedades'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Leoncio0@127.0.0.1:3306/flask_db'

# Crear la carpeta de uploads si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Ruta para acceder a los archivos subidos
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Importar y registrar los blueprints de las rutas después de inicializar la app
from routes.variedad import variedad_bp
from routes.recepcion_routes import recepcion_bp
from routes.fermentacion_routes import fermentacion_bp
from routes.crianza_routes import crianza_bp
from routes.embotellado_routes import embotellado_bp

# Registrar los blueprints
app.register_blueprint(variedad_bp)
app.register_blueprint(recepcion_bp)
app.register_blueprint(fermentacion_bp)
app.register_blueprint(crianza_bp)
app.register_blueprint(embotellado_bp)

# Inicializar la extensión SQLAlchemy con la aplicación
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
