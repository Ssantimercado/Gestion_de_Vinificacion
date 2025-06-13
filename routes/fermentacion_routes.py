from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from models.fermentacion import Fermentacion
from models.recepcion import RecepcionUva
from extensions import db # ¡IMPORTANTE! Aseguramos que use la misma instancia de DB


# Definir el formulario dentro de este archivo
class FermentacionForm(FlaskForm):
    recepcion_id = SelectField('Recepción', coerce=str, validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin', validators=[DataRequired()])
    temperatura = IntegerField('Temperatura (°C)', validators=[DataRequired()])
    ph = IntegerField('pH', validators=[DataRequired()])
    notas = TextAreaField('Notas') # Asegúrate que tu modelo Fermentacion tenga este campo si lo usas


# Blueprint para las rutas de Fermentación
fermentacion_bp = Blueprint('fermentacion_bp', __name__, url_prefix='/fermentacion') # ¡CAMBIADO el url_prefix!

# Ruta para listar todas las fermentaciones
@fermentacion_bp.route('/')
def lista_fermentaciones():
    fermentaciones = Fermentacion.query.all()
    return render_template('fermentacion/list.html', fermentaciones=fermentaciones)

# Ruta para agregar una nueva fermentación
@fermentacion_bp.route('/nueva', methods=['GET', 'POST'])
def nueva_fermentacion():
    form = FermentacionForm()

    # Cargar dinámicamente las opciones del select de recepciones
    form.recepcion_id.choices = [(r.id, f"{r.fecha} - {r.cantidad_kg} kg") for r in RecepcionUva.query.all()]

    if form.validate_on_submit():
        nueva = Fermentacion(
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            temperatura=form.temperatura.data,
            ph=form.ph.data,
            recepcion_id=form.recepcion_id.data
            # Si tienes 'notas' en tu modelo Fermentacion y en el formulario, añádelo aquí:
            # notas=form.notas.data
        )
        db.session.add(nueva)
        db.session.commit()
        flash("Fermentación guardada correctamente", "success")
        return redirect(url_for('fermentacion_bp.lista_fermentaciones'))

    return render_template('fermentacion/form.html', form=form, titulo="Nueva Fermentación")

# Ruta para editar una fermentación existente
@fermentacion_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_fermentacion(id):
    fermentacion = Fermentacion.query.get_or_404(id)
    form = FermentacionForm(obj=fermentacion)

    # Cargar dinámicamente las opciones del select de recepciones
    form.recepcion_id.choices = [(r.id, f"{r.fecha} - {r.cantidad_kg} kg") for r in RecepcionUva.query.all()]

    if form.validate_on_submit():
        fermentacion.fecha_inicio = form.fecha_inicio.data
        fermentacion.fecha_fin = form.fecha_fin.data
        fermentacion.temperatura = form.temperatura.data
        fermentacion.ph = form.ph.data
        fermentacion.recepcion_id = form.recepcion_id.data
        # Si tienes 'notas' en tu modelo Fermentacion y en el formulario, añádelo aquí:
        # fermentacion.notas = form.notas.data
        db.session.commit()
        flash("Fermentación actualizada correctamente", "success")
        return redirect(url_for('fermentacion_bp.lista_fermentaciones'))

    return render_template('fermentacion/form.html', form=form, titulo="Editar Fermentación")