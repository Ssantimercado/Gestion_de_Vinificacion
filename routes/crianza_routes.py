from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import DateField, TextAreaField, SelectField, FloatField # Importamos FloatField y otros
from wtforms.validators import DataRequired, Optional # Importamos Optional para campos no nulos

from extensions import db
from models.crianza_models import Crianza
from models.fermentacion import Fermentacion 
from models.recepcion import RecepcionUva # Necesario para el join en buscar_crianza
from models.variedad import VariedadUva # Necesario para el join en buscar_crianza

import datetime

# Definir el formulario de Crianza usando FlaskForm
class CrianzaForm(FlaskForm):
    fermentacion_id = SelectField('Fermentación Asociada', coerce=str, validators=[DataRequired()])
    tipo_barrica = SelectField('Tipo de Barrica/Recipiente', validators=[DataRequired()], choices=[
        ('Roble Americano', 'Roble Americano'),
        ('Roble Francés', 'Roble Francés'),
        ('Acero Inoxidable', 'Acero Inoxidable'),
        ('Huevo de Concreto', 'Huevo de Concreto'),
        ('Otro', 'Otro')
    ])
    tiempo_crianza_meses = FloatField('Tiempo de Crianza (meses)', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio de Crianza', validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin de Crianza', validators=[Optional()])
    temperatura_crianza = FloatField('Temperatura de Crianza (°C)', validators=[Optional()])
    notas = TextAreaField('Notas/Observaciones', validators=[Optional()]) # Cambiado de 'observaciones' a 'notas' para coincidir con el modelo

# Definimos el Blueprint
crianza_bp = Blueprint('crianza', __name__, url_prefix='/crianza')

@crianza_bp.route('/nueva', methods=['GET', 'POST'])
def crear_crianza():
    form = CrianzaForm()

    # Cargar dinámicamente las opciones del select de fermentaciones
    # Aca podemos ajustar cómo se muestra cada fermentación
    form.fermentacion_id.choices = [(f.id, f"Fermentación {f.id[:8]} - Inicio: {f.fecha_inicio}") for f in Fermentacion.query.all()]

    if form.validate_on_submit():
        try:
            nueva_crianza = Crianza(
                fermentacion_id=form.fermentacion_id.data,
                tipo_barrica=form.tipo_barrica.data, # CORREGIDO: de tipo_recipient a tipo_barrica
                tiempo_crianza_meses=form.tiempo_crianza_meses.data,
                fecha_inicio=form.fecha_inicio.data,
                fecha_fin=form.fecha_fin.data,
                temperatura_crianza=form.temperatura_crianza.data,
                notas=form.notas.data # CORREGIDO: de observaciones a notas
            )
            db.session.add(nueva_crianza)
            db.session.commit()
            flash('Crianza registrada exitosamente.', 'success')
            return redirect(url_for('crianza.listar_crianza'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar crianza: {e}', 'danger')
            print(f"Error al registrar crianza: {e}") # Para depuración
    
    return render_template('crianza/form.html', form=form, titulo="Registrar Nueva Crianza")

@crianza_bp.route('/')
def listar_crianza():
    crianzas = Crianza.query.all()
    return render_template('crianza/lista.html', crianzas=crianzas)

@crianza_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_crianza(id):
    crianza = Crianza.query.get_or_404(id)
    form = CrianzaForm(obj=crianza) # Precarga el formulario con los datos existentes

    # Cargar dinámicamente las opciones del select de fermentaciones
    form.fermentacion_id.choices = [(f.id, f"Fermentación {f.id[:8]} - Inicio: {f.fecha_inicio}") for f in Fermentacion.query.all()]

    if form.validate_on_submit():
        try:
            crianza.fermentacion_id = form.fermentacion_id.data
            crianza.tipo_barrica = form.tipo_barrica.data # CORREGIDO
            crianza.tiempo_crianza_meses = form.tiempo_crianza_meses.data
            crianza.fecha_inicio = form.fecha_inicio.data
            crianza.fecha_fin = form.fecha_fin.data
            crianza.temperatura_crianza = form.temperatura_crianza.data
            crianza.notas = form.notas.data # CORREGIDO
            db.session.commit()
            flash('Crianza actualizada exitosamente.', 'success')
            return redirect(url_for('crianza.listar_crianza'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar crianza: {e}', 'danger')
            print(f"Error al actualizar crianza: {e}")

    return render_template('crianza/form.html', form=form, titulo="Editar Crianza")


@crianza_bp.route('/eliminar/<string:id>', methods=['POST'])
def eliminar_crianza(id):
    crianza = Crianza.query.get_or_404(id)
    try:
        db.session.delete(crianza)
        db.session.commit()
        flash('Crianza eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar crianza: {e}', 'danger')
        print(f"Error al eliminar crianza: {e}")
    return redirect(url_for('crianza.listar_crianza'))

@crianza_bp.route('/buscar', methods=['GET', 'POST'])
def buscar_crianza():
    resultados = []
    # Usar nombres de variables que no choquen con los nombres de campos del modelo si es posible
    tipo_barrica_busqueda = "" 
    variedad_id_busqueda = ""

    if request.method == 'POST':
        tipo_barrica_busqueda = request.form.get('tipo_barrica', '') # Corregido nombre de campo
        variedad_id_busqueda = request.form.get('variedad_id', '')

        query = Crianza.query.join(Crianza.fermentacion).join(Fermentacion.recepcion).join(RecepcionUva.variedad)

        if tipo_barrica_busqueda:
            query = query.filter(Crianza.tipo_barrica.ilike(f"%{tipo_barrica_busqueda}%")) # Corregido
        if variedad_id_busqueda:
            query = query.filter(RecepcionUva.variedad_id == variedad_id_busqueda)

        resultados = query.all()

    variedades = VariedadUva.query.all()
    return render_template('crianza/buscador.html', resultados=resultados,
                           tipo_barrica_busqueda=tipo_barrica_busqueda, # Pasar el nombre corregido
                           variedad_id_busqueda=variedad_id_busqueda, # Pasar el nombre corregido
                           variedades=variedades)