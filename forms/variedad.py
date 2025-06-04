from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class VariedadUvaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    origen = StringField('Origen')
    foto = FileField('Foto', validators=[FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Solo se permiten imágenes')])
    submit = SubmitField('Guardar')