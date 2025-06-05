# routes/variedad.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
import os 
from models.db import db
from models.variedad import VariedadUva
from forms.variedad import VariedadUvaForm 
from werkzeug.utils import secure_filename
import uuid

# --- CONFIGURACIÓN DE SUBIDA DE ARCHIVOS ---
UPLOAD_FOLDER = 'static/fotos_variedades'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Verifica si la extensión del archivo es permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def guardar_foto(file):
    """Guarda la foto si es válida y devuelve el nombre del archivo."""
    if file and allowed_file(file.filename):
        filename_original = secure_filename(file.filename)
        ext = filename_original.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return filename
    return None

# --- DEFINICIÓN DEL BLUEPRINT ---
variedad_bp = Blueprint('variedad', __name__, url_prefix='/variedades')

# --- RUTAS ---

@variedad_bp.route('/')
def listar_variedades():
    """Muestra la lista de todas las variedades de uva."""
    variedades = VariedadUva.query.all()
    return render_template('variedad/list.html', variedades=variedades)

@variedad_bp.route('/agregar', methods=['GET', 'POST'])
def agregar_variedad():
    """Permite agregar una nueva variedad de uva."""
    form = VariedadUvaForm()
    if form.validate_on_submit():
        # Validación de unicidad
        if VariedadUva.query.filter_by(nombre=form.nombre.data).first():
            flash('Ya existe una variedad con ese nombre. Por favor, elige otro.', 'danger')
            return render_template('variedad/form.html', form=form, title='Agregar Variedad')

        nueva_variedad = VariedadUva(
            nombre=form.nombre.data,
            origen=form.origen.data
        )

        # Guardar foto si fue cargada
        if form.foto.data:
            filename = guardar_foto(form.foto.data)
            if filename:
                nueva_variedad.foto = filename
            else:
                flash(f'Tipo de archivo no permitido. Permitidos: {", ".join(ALLOWED_EXTENSIONS)}', 'danger')
                return render_template('variedad/form.html', form=form, title='Agregar Variedad')

        db.session.add(nueva_variedad)
        db.session.commit()
        flash('Variedad agregada exitosamente', 'success')
        return redirect(url_for('variedad.listar_variedades'))

    return render_template('variedad/form.html', form=form, title='Agregar Variedad')

@variedad_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_variedad(id):
    """Permite editar una variedad de uva existente."""
    variedad = VariedadUva.query.get_or_404(id)
    form = VariedadUvaForm(obj=variedad)

    if form.validate_on_submit():
        # Validar nombre único si fue modificado
        if form.nombre.data != variedad.nombre and VariedadUva.query.filter_by(nombre=form.nombre.data).first():
            flash('Ya existe una variedad con ese nombre. Por favor, elige otro.', 'danger')
            return render_template('variedad/form.html', form=form, title='Editar Variedad', variedad=variedad)

        # Actualizar campos
        variedad.nombre = form.nombre.data
        variedad.origen = form.origen.data

        # Manejo de foto nueva
        if form.foto.data and getattr(form.foto.data, 'filename', ''):
            # Eliminar la anterior
            if variedad.foto:
                ruta_anterior = os.path.join(UPLOAD_FOLDER, variedad.foto)
                if os.path.exists(ruta_anterior):
                    os.remove(ruta_anterior)

            filename = guardar_foto(form.foto.data)
            if filename:
                variedad.foto = filename
            else:
                flash(f'Tipo de archivo no permitido. Permitidos: {", ".join(ALLOWED_EXTENSIONS)}', 'danger')
                return render_template('variedad/form.html', form=form, title='Editar Variedad', variedad=variedad)

        db.session.commit()
        flash('Variedad actualizada exitosamente', 'success')
        return redirect(url_for('variedad.listar_variedades'))

    return render_template('variedad/form.html', form=form, title='Editar Variedad', variedad=variedad)

@variedad_bp.route('/eliminar/<id>', methods=['POST'])
def eliminar_variedad(id):
    """Permite eliminar una variedad de uva y su foto asociada."""
    variedad = VariedadUva.query.get_or_404(id)

    # Eliminar foto asociada
    if variedad.foto:
        file_path = os.path.join(UPLOAD_FOLDER, variedad.foto)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.session.delete(variedad)
    db.session.commit()
    flash('Variedad eliminada exitosamente', 'success')
    return redirect(url_for('variedad.listar_variedades'))
