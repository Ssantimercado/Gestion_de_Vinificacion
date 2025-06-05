from flask import Flask, render_template, redirect, url_for, send_from_directory
import os
from extensions import db

app = Flask(__name__)
app.config['SECRET_KEY'] = '451433203SANGERPA'
app.config['UPLOAD_FOLDER'] = 'uploads/fotos_variedades'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Leoncio0@127.0.0.1:3306/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Blueprints
from routes.variedad import variedad_bp
from routes.recepcion import recepcion_bp
from routes.fermentacion import fermentacion_bp
from routes.crianza import crianza_bp
from routes.embotellado import embotellado_bp

app.register_blueprint(variedad_bp)
app.register_blueprint(recepcion_bp)
app.register_blueprint(fermentacion_bp)
app.register_blueprint(crianza_bp)
app.register_blueprint(embotellado_bp)

db.init_app(app)

with app.app_context():
    from models.variedad import VariedadUva
    from models.recepcion import RecepcionUva
    from models.fermentacion import Fermentacion
    from models.crianza import Crianza
    from models.embotellado import Embotellado

    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
