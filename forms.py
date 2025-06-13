# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, TextAreaField, SelectField, SubmitField, HiddenField, FileField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
import datetime
from extensions import db

# ASEGÚRATE DE QUE ESTAS IMPORTACIONES SEAN CORRECTAS SEGÚN TU ESTRUCTURA DE ARCHIVOS
# Basado en tus capturas de pantalla, estos son los nombres correctos de los módulos.
from models.variedad import VariedadUva
from models.recepcion import RecepcionUva
from models.fermentacion import Fermentacion
from models.crianza_models import Crianza           # Importación corregida
from models.embotellado_models import Embotellado   # Importación corregida


# --- Formularios de Modelos ---

class VariedadUvaForm(FlaskForm):
    id = HiddenField('ID') # Añadido para edición
    nombre = StringField('Nombre de la Variedad', validators=[DataRequired(), Length(min=2, max=100)])
    origen = StringField('Origen', validators=[DataRequired(), Length(min=2, max=100)])
    foto = FileField('Subir Foto', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Solo imágenes (jpg, png, gif)'), Optional()])
    submit = SubmitField('Guardar Variedad')

class RecepcionUvaForm(FlaskForm):
    id = HiddenField('ID') # Añadido para edición
    # Para SelectField, las choices se cargan dinámicamente en la ruta
    variedad_id = SelectField('Variedad de Uva', validators=[DataRequired()], coerce=str)
    cantidad_kg = DecimalField('Cantidad (kg)', validators=[DataRequired(), NumberRange(min=0.01)])
    fecha = DateField('Fecha de Recepción', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    notas = TextAreaField('Notas', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Guardar Recepción')

    def __init__(self, *args, **kwargs):
        super(RecepcionUvaForm, self).__init__(*args, **kwargs)
        # Cargar opciones de variedades al inicializar el formulario
        self.variedad_id.choices = [(v.id, v.nombre) for v in VariedadUva.query.order_by(VariedadUva.nombre).all()]
        # Añadir una opción vacía si no hay ninguna seleccionada
        if not self.variedad_id.choices:
            self.variedad_id.choices = [('', '--- No hay variedades disponibles ---')]
        else:
            self.variedad_id.choices.insert(0, ('', '--- Seleccione una Variedad ---'))


class FermentacionForm(FlaskForm):
    id = HiddenField('ID') # Añadido para edición
    # La lista de recepciones se carga dinámicamente
    recepcion_id = SelectField('Recepción de Uva', validators=[DataRequired()], coerce=str)
    fecha_inicio = DateField('Fecha de Inicio', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin', format='%Y-%m-%d', validators=[Optional()]) # Puede ser opcional al inicio
    temperatura_max = DecimalField('Temperatura Máxima (°C)', validators=[DataRequired(), NumberRange(min=0)])
    levadura_utilizada = StringField('Levadura Utilizada', validators=[Optional(), Length(max=100)])
    ph_inicial = DecimalField('pH Inicial', validators=[Optional(), NumberRange(min=0, max=14)])
    ph_final = DecimalField('pH Final', validators=[Optional(), NumberRange(min=0, max=14)])
    densidad_inicial = DecimalField('Densidad Inicial', validators=[Optional(), NumberRange(min=0)])
    densidad_final = DecimalField('Densidad Final', validators=[Optional(), NumberRange(min=0)])
    notas = TextAreaField('Notas', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Guardar Fermentación')

    def __init__(self, *args, **kwargs):
        super(FermentacionForm, self).__init__(*args, **kwargs)
        # Cargar opciones de recepciones para el SelectField
        # Solo mostrar recepciones que tienen una variedad asociada
        recepciones_disponibles = RecepcionUva.query.join(VariedadUva).order_by(RecepcionUva.fecha.desc()).all()
        self.recepcion_id.choices = [
            (r.id, f"{r.fecha.strftime('%Y-%m-%d')} - {r.variedad.nombre} ({r.cantidad_kg} kg)")
            for r in recepciones_disponibles if r.variedad
        ]
        if not self.recepcion_id.choices:
            self.recepcion_id.choices = [('', '--- No hay recepciones disponibles ---')]
        else:
            self.recepcion_id.choices.insert(0, ('', '--- Seleccione una Recepción ---'))


class CrianzaForm(FlaskForm):
    id = HiddenField('ID') # Añadido para edición
    fermentacion_id = SelectField('Fermentación Asociada', validators=[DataRequired()], coerce=str)
    tipo_barrica = StringField('Tipo de Barrica', validators=[DataRequired(), Length(min=2, max=100)])
    tiempo_crianza_meses = DecimalField('Tiempo de Crianza (meses)', validators=[DataRequired(), NumberRange(min=0)])
    fecha_inicio = DateField('Fecha de Inicio', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    fecha_fin = DateField('Fecha de Fin', format='%Y-%m-%d', validators=[Optional()])
    temperatura_crianza = DecimalField('Temperatura de Crianza (°C)', validators=[Optional(), NumberRange(min=0)])
    notas = TextAreaField('Notas', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Guardar Crianza')

    def __init__(self, *args, **kwargs):
        super(CrianzaForm, self).__init__(*args, **kwargs)
        # Cargar opciones de fermentaciones
        fermentaciones_disponibles = Fermentacion.query.join(RecepcionUva).join(VariedadUva).order_by(Fermentacion.fecha_inicio.desc()).all()
        self.fermentacion_id.choices = [(f.id, f"ID: {f.id[:8]}... - Inicio: {f.fecha_inicio.strftime('%Y-%m-%d')} - Variedad: {f.recepcion.variedad.nombre if f.recepcion and f.recepcion.variedad else 'N/A'}")
                                         for f in fermentaciones_disponibles if f.recepcion and f.recepcion.variedad]
        if not self.fermentacion_id.choices:
            self.fermentacion_id.choices = [('', '--- No hay fermentaciones disponibles ---')]
        else:
            self.fermentacion_id.choices.insert(0, ('', '--- Seleccione una Fermentación ---'))


class EmbotelladoForm(FlaskForm):
    id = HiddenField('ID') # Añadido para edición
    crianza_id = SelectField('Crianza Asociada', validators=[DataRequired()], coerce=str)
    fecha_embotellado = DateField('Fecha de Embotellado', format='%Y-%m-%d', default=datetime.date.today, validators=[DataRequired()])
    cantidad_botellas = DecimalField('Cantidad de Botellas', validators=[DataRequired(), NumberRange(min=1)])
    tipo_botella = StringField('Tipo de Botella', validators=[DataRequired(), Length(min=2, max=100)])
    notas = TextAreaField('Notas', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Guardar Embotellado')

    def __init__(self, *args, **kwargs):
        super(EmbotelladoForm, self).__init__(*args, **kwargs)
        # Cargar opciones de crianzas
        crianzas_disponibles = Crianza.query.order_by(Crianza.fecha_inicio.desc()).all()
        self.crianza_id.choices = [(c.id, f"ID: {c.id[:8]}... - Tipo Barrica: {c.tipo_barrica} - Inicio: {c.fecha_inicio.strftime('%Y-%m-%d')}")
                                   for c in crianzas_disponibles]
        if not self.crianza_id.choices:
            self.crianza_id.choices = [('', '--- No hay crianzas disponibles ---')]
        else:
            self.crianza_id.choices.insert(0, ('', '--- Seleccione una Crianza ---'))