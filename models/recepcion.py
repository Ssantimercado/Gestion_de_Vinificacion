import uuid
from datetime import datetime
from models.db import db

class RecepcionUva(db.Model):
    __tablename__ = 'recepciones'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4))  # Cambié el tipo de campo a String(36) y agregué UUID
    fecha = db.Column(db.Date, nullable=False)
    cantidad_kg = db.Column(db.Integer, nullable=False)
    notas = db.Column(db.Text)
    
    # Relación con VariedadUva
    variedad_id = db.Column(db.Integer, db.ForeignKey('variedades.id'), nullable=False)
    variedad = db.relationship('VariedadUva', backref=db.backref('recepciones', lazy=True))

    def __init__(self, fecha, cantidad_kg, notas, variedad_id):
        self.fecha = fecha
        self.cantidad_kg = cantidad_kg
        self.notas = notas
        self.variedad_id = variedad_id

    def __repr__(self):
        return f'<RecepcionUva {self.id} - {self.fecha} - {self.variedad.nombre}>'
