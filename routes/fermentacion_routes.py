from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, TextAreaField, SelectField, FloatField # Importamos FloatField para PH y Densidades
from wtforms.validators import DataRequired, Optional # Optional si algunos campos pueden ser nulos


from models.fermentacion import Fermentacion
from models.recepcion import RecepcionUva 
from extensions import db #  Aseguramos que use la misma instancia de DB


# Definir el formulario dentro de este archivo
class FermentacionForm(FlaskForm):
    recepcion_id = SelectField('Recepción', coerce=str, validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()]) # Puede ser nulo
    temperatura = FloatField('Temperatura (°C)', validators=[DataRequired()]) # Cambiado a FloatField
    levadura_utilizada = TextAreaField('Levadura Utilizada', validators=[Optional()]) # Campo Levadura
    ph_inicial = FloatField('pH Inicial', validators=[DataRequired()]) # Cambiado a FloatField
    ph_final = FloatField('pH Final', validators=[Optional()]) # Cambiado a FloatField
    densidad_inicial = FloatField('Densidad Inicial', validators=[DataRequired()]) # Cambiado a FloatField
    densidad_final = FloatField('Densidad Final', validators=[Optional()]) # Cambiado a FloatField
    notas = TextAreaField('Notas', validators=[Optional()]) # Asegúrate que tu modelo Fermentacion tenga este campo si lo usas


# Blueprint para las rutas de Fermentación
fermentacion_bp = Blueprint('fermentacion_bp', __name__, url_prefix='/fermentacion')

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
        try:
            nueva = Fermentacion(
                recepcion_id=form.recepcion_id.data,
                fecha_inicio=form.fecha_inicio.data,
                fecha_fin=form.fecha_fin.data,
                temperatura=form.temperatura.data,
                levadura_utilizada=form.levadura_utilizada.data, # Agregado
                ph_inicial=form.ph_inicial.data, # CORREGIDO: ahora mapea a ph_inicial
                ph_final=form.ph_final.data, # Agregado
                densidad_inicial=form.densidad_inicial.data, # Agregado
                densidad_final=form.densidad_final.data, # Agregado
                notas=form.notas.data # Agregado
            )
            db.session.add(nueva)
            db.session.commit()
            flash("Fermentación guardada correctamente", "success")
            return redirect(url_for('fermentacion_bp.lista_fermentaciones'))
        except Exception as e:
            db.session.rollback() # En caso de error, deshacer cambios
            flash(f"Error al guardar fermentación: {e}", "danger")
            print(f"Error al guardar fermentación: {e}") # Imprimir el error en consola para depuración

    return render_template('fermentacion/form.html', form=form, titulo="Nueva Fermentación")

# Ruta para editar una fermentación existente
@fermentacion_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_fermentacion(id):
    fermentacion = Fermentacion.query.get_or_404(id)
    form = FermentacionForm(obj=fermentacion)

    # Cargar dinámicamente las opciones del select de recepciones
    form.recepcion_id.choices = [(r.id, f"{r.fecha} - {r.cantidad_kg} kg") for r in RecepcionUva.query.all()]

    if form.validate_on_submit():
        try:
            fermentacion.recepcion_id = form.recepcion_id.data
            fermentacion.fecha_inicio = form.fecha_inicio.data
            fermentacion.fecha_fin = form.fecha_fin.data
            fermentacion.temperatura = form.temperatura.data
            fermentacion.levadura_utilizada = form.levadura_utilizada.data # Agregado
            fermentacion.ph_inicial = form.ph_inicial.data # CORREGIDO
            fermentacion.ph_final = form.ph_final.data # Agregado
            fermentacion.densidad_inicial = form.densidad_inicial.data # Agregado
            fermentacion.densidad_final = form.densidad_final.data # Agregado
            fermentacion.notas = form.notas.data # Agregado
            db.session.commit()
            flash("Fermentación actualizada correctamente", "success")
            return redirect(url_for('fermentacion_bp.lista_fermentaciones'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar fermentación: {e}", "danger")
            print(f"Error al actualizar fermentación: {e}")

    return render_template('fermentacion/form.html', form=form, titulo="Editar Fermentación")

# Ruta para eliminar una fermentación(opcional)
@fermentacion_bp.route('/eliminar/<string:id>', methods=['POST'])
def eliminar_fermentacion(id):
    fermentacion = Fermentacion.query.get_or_404(id)
    try:
        db.session.delete(fermentacion)
        db.session.commit()
        flash("Fermentación eliminada correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar fermentación: {e}", "danger")
        print(f"Error al eliminar fermentación: {e}")
    return redirect(url_for('fermentacion_bp.lista_fermentaciones'))