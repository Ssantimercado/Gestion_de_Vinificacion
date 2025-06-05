from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, DateField
from wtforms.validators import DataRequired
from models.recepcion import RecepcionUva
from models.variedad import VariedadUva
from models.db import db

# Definir el formulario dentro de este archivo
class RecepcionUvaForm(FlaskForm):
    variedad_id = IntegerField('Variedad', validators=[DataRequired()])
    cantidad_kg = IntegerField('Cantidad (kg)', validators=[DataRequired()])
    fecha = DateField('Fecha de Recepción', validators=[DataRequired()])
    notas = TextAreaField('Notas')

# Blueprint para las rutas de Recepción
recepcion_bp = Blueprint('recepcion_bp', __name__, url_prefix='/recepciones')

# Ruta para listar todas las recepciones
@recepcion_bp.route('/')
def lista_recepciones():
    recepciones = RecepcionUva.query.all()
    return render_template('recepcion/list.html', recepciones=recepciones)

# Ruta para agregar una nueva recepción
@recepcion_bp.route('/nueva', methods=['GET', 'POST'])
def nueva_recepcion():
    form = RecepcionUvaForm()

    # Cargar dinámicamente las opciones del select de variedad
    form.variedad_id.choices = [(v.id, v.nombre) for v in VariedadUva.query.all()]

    if form.validate_on_submit():
        nueva = RecepcionUva(
            fecha=form.fecha.data,
            variedad_id=form.variedad_id.data,
            cantidad_kg=form.cantidad_kg.data,
            notas=form.notas.data
        )
        db.session.add(nueva)
        db.session.commit()
        flash("Recepción guardada correctamente", "success")
        return redirect(url_for('recepcion_bp.lista_recepciones'))

    return render_template('recepcion/form.html', form=form, titulo="Nueva Recepción")

# Ruta para editar una recepción existente
@recepcion_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_recepcion(id):
    # Buscar la recepción usando el UUID
    recepcion = RecepcionUva.query.get_or_404(id)  # Aquí 'id' ahora es un UUID (String)
    
    form = RecepcionUvaForm(obj=recepcion)

    # Cargar dinámicamente las opciones del select de variedad
    form.variedad_id.choices = [(v.id, v.nombre) for v in VariedadUva.query.all()]

    if form.validate_on_submit():
        # Actualizar los campos de la recepción
        recepcion.fecha = form.fecha.data
        recepcion.variedad_id = form.variedad_id.data
        recepcion.cantidad_kg = form.cantidad_kg.data
        recepcion.notas = form.notas.data
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        flash("Recepción actualizada correctamente", "success")
        return redirect(url_for('recepcion_bp.lista_recepciones'))

    return render_template('recepcion/form.html', form=form, titulo="Editar Recepción")


    
