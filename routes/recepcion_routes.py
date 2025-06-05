from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired
from models.recepcion import RecepcionUva
from models.variedad import VariedadUva
from models.db import db



# Formulario WTForms
class RecepcionUvaForm(FlaskForm):
    variedad_id = SelectField('Variedad', coerce=str, validators=[DataRequired()])  # UUID como string
    cantidad_kg = IntegerField('Cantidad (kg)', validators=[DataRequired()])
    fecha = DateField('Fecha de Recepción', validators=[DataRequired()])
    notas = TextAreaField('Notas')

# Blueprint
recepcion_bp = Blueprint('recepcion_bp', __name__, url_prefix='/recepciones')

# Listar recepciones
@recepcion_bp.route('/')
def lista_recepciones():
    recepciones = RecepcionUva.query.all()
    return render_template('recepcion/list.html', recepciones=recepciones)

# Crear nueva recepción
@recepcion_bp.route('/nueva', methods=['GET', 'POST'])
def nueva_recepcion():
    form = RecepcionUvaForm()
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

# Editar recepción
@recepcion_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_recepcion(id):
    recepcion = RecepcionUva.query.get_or_404(id)
    form = RecepcionUvaForm(obj=recepcion)
    form.variedad_id.choices = [(v.id, v.nombre) for v in VariedadUva.query.all()]

    if form.validate_on_submit():
        recepcion.fecha = form.fecha.data
        recepcion.variedad_id = form.variedad_id.data
        recepcion.cantidad_kg = form.cantidad_kg.data
        recepcion.notas = form.notas.data

        db.session.commit()
        flash("Recepción actualizada correctamente", "success")
        return redirect(url_for('recepcion_bp.lista_recepciones'))

    return render_template('recepcion/form.html', form=form, titulo="Editar Recepción")

