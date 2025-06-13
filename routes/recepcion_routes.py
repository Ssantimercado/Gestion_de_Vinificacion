# routes/recepcion_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.recepcion import RecepcionUva
from models.variedad import VariedadUva
from forms import RecepcionUvaForm # Asegúrate de que tu formulario esté importado
import datetime
import uuid # Para generar IDs únicos si tu modelo lo requiere y no lo hace la base de datos automáticamente

recepcion_bp = Blueprint('recepcion_bp', __name__, url_prefix='/recepcion')

@recepcion_bp.route('/')
def lista_recepciones():
    recepciones = RecepcionUva.query.all()
    return render_template('recepcion/lista.html', recepciones=recepciones)

@recepcion_bp.route('/nueva', methods=['GET', 'POST'])
def nueva_recepcion():
    form = RecepcionUvaForm()

    if form.validate_on_submit():
        # *** AÑADIDO: Generar un UUID para el ID explícitamente ***
        new_id = str(uuid.uuid4())

        nueva_recepcion_obj = RecepcionUva(
            # *** ASIGNAR EL ID GENERADO AQUÍ ***
            id=new_id,
            variedad_id=form.variedad_id.data,
            cantidad_kg=form.cantidad_kg.data,
            fecha=form.fecha.data,
            notas=form.notas.data
        )
        db.session.add(nueva_recepcion_obj)
        try:
            db.session.commit()
            flash('Recepción de uva creada exitosamente!', 'success')
            return redirect(url_for('recepcion_bp.lista_recepciones'))
        except Exception as e:
            db.session.rollback() # En caso de error, deshaz la transacción
            flash(f'Error al crear la recepción: {e}', 'danger')
            # Puedes imprimir 'e' en la consola para depuración
            print(f"Error al guardar nueva recepción: {e}")
            return render_template('recepcion/form.html', form=form, titulo="Nueva Recepción")


    # Para el método GET, o si el formulario no valida
    return render_template('recepcion/form.html', form=form, titulo="Nueva Recepción")

@recepcion_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_recepcion(id):
    recepcion = RecepcionUva.query.get_or_404(id)
    form = RecepcionUvaForm(obj=recepcion) # Pre-popular el formulario con los datos existentes

    if form.validate_on_submit():
        form.populate_obj(recepcion) # Actualiza el objeto recepcion con los datos del formulario
        try:
            db.session.commit()
            flash('Recepción de uva actualizada exitosamente!', 'success')
            return redirect(url_for('recepcion_bp.lista_recepciones'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la recepción: {e}', 'danger')
            print(f"Error al actualizar recepción: {e}")
            return render_template('recepcion/form.html', form=form, titulo="Editar Recepción")


    return render_template('recepcion/form.html', form=form, titulo="Editar Recepción")

@recepcion_bp.route('/eliminar/<string:id>', methods=['POST'])
def eliminar_recepcion(id):
    recepcion = RecepcionUva.query.get_or_404(id)
    try:
        db.session.delete(recepcion)
        db.session.commit()
        flash('Recepción de uva eliminada exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la recepción: {e}', 'danger')
        print(f"Error al eliminar recepción: {e}")

    return redirect(url_for('recepcion_bp.lista_recepciones'))