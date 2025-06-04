from flask import Blueprint, render_template, redirect, url_for, request, current_app
from forms.variedad import VariedadUvaForm
from models.variedad import VariedadUva
import os
from werkzeug.utils import secure_filename
from extensions import db  # <--- Importa 'db' desde extensions.py

variedad_bp = Blueprint('variedad', __name__, url_prefix='/variedades')

UPLOAD_FOLDER = 'uploads/fotos_variedades'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@variedad_bp.route('/')
def listar_variedades():
    variedades = db.session.query(VariedadUva).all()
    return render_template('variedad/list.html', variedades=variedades)

@variedad_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_variedad():
    form = VariedadUvaForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        origen = form.origen.data
        foto_path = None
        if form.foto.data:
            file = form.foto.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                foto_path = filepath

        nueva_variedad = VariedadUva(nombre=nombre, origen=origen, foto=foto_path)
        db.session.add(nueva_variedad)
        db.session.commit()
        return redirect(url_for('variedad.listar_variedades'))
    return render_template('variedad/form.html', form=form, title='Agregar Variedad')

# ... (el resto de tu archivo routes/variedad.py)