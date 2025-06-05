from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.recepcion import RecepcionUva
from models.variedad import VariedadUva
from forms.recepcion import RecepcionUvaForm
from models.db import db

recepcion_bp = Blueprint('recepcion_bp', __name__, url_prefix='/recepciones')


@recepcion_bp.route('/')
def lista_recepciones():
    recepciones = RecepcionUva.query.all()
    return render_template('recepcion/list.html', recepciones=recepciones)


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
