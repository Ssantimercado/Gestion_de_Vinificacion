from flask import Blueprint, render_template, redirect, url_for, request, flash
from models.fermentacion import Fermentacion
from models.recepcion import RecepcionUva
from forms.fermentacion import FermentacionForm
from models.db import db

fermentacion_bp = Blueprint('fermentacion_bp', __name__, url_prefix='/fermentaciones')


@fermentacion_bp.route('/')
def lista_fermentaciones():
    fermentaciones = Fermentacion.query.all()
    return render_template('fermentacion/list.html', fermentaciones=fermentaciones)


@fermentacion_bp.route('/nueva', methods=['GET', 'POST'])
def nueva_fermentacion():
    form = FermentacionForm()

    # Cargar dinámicamente las recepciones disponibles
    form.recepcion_id.choices = [
        (r.id, f"{r.fecha} - {r.cantidad_kg} kg") for r in RecepcionUva.query.all()
    ]

    if form.validate_on_submit():
        nueva = Fermentacion(
            fecha_inicio=form.fecha_inicio.data,
            fecha_fin=form.fecha_fin.data,
            temperatura=form.temperatura.data,
            ph=form.ph.data,
            recepcion_id=form.recepcion_id.data
        )
        db.session.add(nueva)
        db.session.commit()
        flash("Fermentación guardada correctamente", "success")
        return redirect(url_for('fermentacion_bp.lista_fermentaciones'))

    return render_template('fermentacion/form.html', form=form, titulo="Nueva Fermentación")


@fermentacion_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_fermentacion(id):
    fermentacion = Fermentacion.query.get_or_404(id)
    form = FermentacionForm(obj=fermentacion)

    form.recepcion_id.choices = [
        (r.id, f"{r.fecha} - {r.cantidad_kg} kg") for r in RecepcionUva.query.all()
    ]

    if form.validate_on_submit():
        fermentacion.fecha_inicio = form.fecha_inicio.data
        fermentacion.fecha_fin = form.fecha_fin.data
        fermentacion.temperatura = form.temperatura.data
        fermentacion.ph = form.ph.data
        fermentacion.recepcion_id = form.recepcion_id.data
        db.session.commit()
        flash("Fermentación actualizada correctamente", "success")
        return redirect(url_for('fermentacion_bp.lista_fermentaciones'))

    return render_template('fermentacion/form.html', form=form, titulo="Editar Fermentación")
