## routes/variedad.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
import os 
from extensions import db
from models.variedad import VariedadUva
from forms.variedad import VariedadUvaForm 
from werkzeug.utils import secure_filename
import uuid

# CONFIGURACIÓN DE SUBIDA DE ARCHIVOS 
# La carpeta donde se guardarán las fotos dentro de 'static'
UPLOAD_FOLDER = 'static/fotos_variedades'
# Extensiones de archivo permitidas para las fotos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Función para verificar si la extensión del archivo es permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# DEFINICIÓN DEL BLUEPRINT 
# ¡
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
        # --
        # Verifica si ya existe una variedad con el nombre ingresado
        if VariedadUva.query.filter_by(nombre=form.nombre.data).first():
            flash('Ya existe una variedad con ese nombre. Por favor, elige otro.', 'danger')
            return render_template('variedad/form.html', form=form, title='Agregar Variedad')
        #  FIN VALIDACIÓN 

        nueva_variedad = VariedadUva(
            nombre=form.nombre.data,
            origen=form.origen.data
        )

        # Manejo de la subida de la foto
        if form.foto.data:
            file = form.foto.data
            # Verifica si se seleccionó un archivo y si su extensión es permitida
            if file and allowed_file(file.filename):
                # Genera un nombre de archivo único para evitar colisiones
                filename_original = secure_filename(file.filename)
                file_extension = filename_original.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

                # Asegura que la carpeta de subida exista
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                # Guarda el archivo en el sistema de archivos
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)

                # Guarda solo el nombre único del archivo en la base de datos
                nueva_variedad.foto = unique_filename
            else:
                flash('Tipo de archivo no permitido para la foto.', 'danger')
                return render_template('variedad/form.html', form=form, title='Agregar Variedad')
        
        # Agrega la nueva variedad a la sesión de la base de datos y guarda
        db.session.add(nueva_variedad)
        db.session.commit()
        
        flash('Variedad agregada exitosamente', 'success')
        return redirect(url_for('variedad.listar_variedades'))
    
    return render_template('variedad/form.html', form=form, title='Agregar Variedad')

@variedad_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_variedad(id):
    """Permite editar una variedad de uva existente."""
    variedad = VariedadUva.query.get_or_404(id) # Obtiene la variedad por su ID o muestra 404
    form = VariedadUvaForm(obj=variedad) # Pre-rellena el formulario con los datos de la variedad

    if form.validate_on_submit():
        # --- VALIDACIÓN PARA EL CAMPO 'nombre' (UNIQUE) al editar ---
        # Solo verifica unicidad si el nombre ha cambiado Y ya existe otra variedad con ese nombre
        if form.nombre.data != variedad.nombre and VariedadUva.query.filter_by(nombre=form.nombre.data).first():
            flash('Ya existe una variedad con ese nombre. Por favor, elige otro.', 'danger')
            return render_template('variedad/form.html', form=form, title='Editar Variedad', variedad=variedad)
        # --- FIN VALIDACIÓN ---
        
        # Actualiza los campos de texto
        variedad.nombre = form.nombre.data
        variedad.origen = form.origen.data

        # Manejo de la nueva foto (si se sube una)
        # Verifica si hay datos en el campo de foto Y si form.foto.data tiene el atributo 'filename'
        # Esto evita el AttributeError cuando form.foto.data es una cadena vacía ('')
        if form.foto.data and hasattr(form.foto.data, 'filename') and form.foto.data.filename != '':
            file = form.foto.data
            
            if file and allowed_file(file.filename):
                # Elimina la foto antigua si existe (para evitar dejar archivos "huérfanos")
                if variedad.foto and os.path.exists(os.path.join(UPLOAD_FOLDER, variedad.foto)):
                    os.remove(os.path.join(UPLOAD_FOLDER, variedad.foto))

                filename_original = secure_filename(file.filename)
                file_extension = filename_original.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{file_extension}"

                os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Asegura que la carpeta exista
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                
                variedad.foto = unique_filename # Actualiza el nombre de la foto en la DB
            else:
                flash('Tipo de archivo no permitido para la foto.', 'danger')
                return render_template('variedad/form.html', form=form, title='Editar Variedad', variedad=variedad)
        
        # Guarda los cambios en la base de datos
        db.session.commit()
        
        flash('Variedad actualizada exitosamente', 'success')
        return redirect(url_for('variedad.listar_variedades'))
    
    return render_template('variedad/form.html', form=form, title='Editar Variedad', variedad=variedad)

@variedad_bp.route('/eliminar/<id>', methods=['POST'])
def eliminar_variedad(id):
    """Permite eliminar una variedad de uva y su foto asociada."""
    variedad = VariedadUva.query.get_or_404(id) # Busca la variedad por ID o muestra 404

    # Opcional: Eliminar la foto asociada del sistema de archivos
    if variedad.foto:
        file_path = os.path.join(UPLOAD_FOLDER, variedad.foto)
        if os.path.exists(file_path):
            os.remove(file_path) # Elimina el archivo físico

    # Elimina la variedad de la base de datos
    db.session.delete(variedad)
    db.session.commit()

    flash('Variedad eliminada exitosamente', 'success')
    return redirect(url_for('variedad.listar_variedades'))