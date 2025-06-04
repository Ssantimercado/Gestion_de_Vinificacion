from flask import Flask, render_template, redirect, url_for
import os
from extensions import db  # <--- Importa 'db' desde extensions.py
from flask_migrate import Migrate  # <--- Importa Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '451433203SANGERPA'
app.config['UPLOAD_FOLDER'] = 'uploads/fotos_variedades'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Leoncio0@127.0.0.1:3306/flask_db'

# Configurar la ruta estática para la carpeta de subidas
app.add_url_rule('/uploads/<filename>', endpoint='uploaded_file', build_only=True)
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Importar y registrar el blueprint DESPUÉS de inicializar 'app'
from routes.variedad import variedad_bp
app.register_blueprint(variedad_bp)

# Inicializar la extensión SQLAlchemy con la aplicación
db.init_app(app)

# Inicializar Flask-Migrate con la aplicación y la instancia db
migrate = Migrate(app, db)  # <--- Asegúrate de que esté AQUÍ

if __name__ == '__main__':
    app.run(debug=True)