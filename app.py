from flask import Flask, render_template, redirect, url_for, send_from_directory
import os
from extensions import db
from flask_migrate import Migrate

# Configuración inicial
app = Flask(__name__)
app.config['SECRET_KEY'] = '451433203SANGERPA'
app.config['UPLOAD_FOLDER'] = 'uploads/fotos_variedades'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Leoncio0@127.0.0.1:3306/bodega'

# Ruta para servir imágenes subidas
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Inicializar la base de datos
db.init_app(app)
migrate = Migrate(app, db)

# Registrar Blueprints
from routes.variedad import variedad_bp
from routes.crianza_routes import crianza_bp
from routes.embotellado_routes import embotellado_bp

app.register_blueprint(variedad_bp)
app.register_blueprint(crianza_bp)
app.register_blueprint(embotellado_bp)

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
