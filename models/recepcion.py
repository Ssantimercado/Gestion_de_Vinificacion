import uuid
from datetime import datetime
from models.db import db
from flask_sqlalchemy import SQLAlchemy
from models.variedad import VariedadUva  # Importa correctamente el modelo

db = SQLAlchemy()

class RecepcionUva(db.Model):
    __tablename__ = 'recepciones'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))  # UUID como clave primaria
    fecha = db.Column(db.Date, nullable=False)
    cantidad_kg = db.Column(db.Integer, nullable=False)
    notas = db.Column(db.Text)

    variedad_id = db.Column(db.String(36), db.ForeignKey('variedades.id'))  # Relación con UUID de VariedadUva
    variedad = db.relationship('VariedadUva', backref='recepciones')  # Relación inversa
    
    fermentaciones = db.relationship('Fermentacion', back_populates='recepcion', cascade="all, delete-orphan")

    def __init__(self, fecha, cantidad_kg, notas, variedad_id):
        self.fecha = fecha
        self.cantidad_kg = cantidad_kg
        self.notas = notas
        self.variedad_id = variedad_id

    def __repr__(self):
        return f'<RecepcionUva {self.id} - {self.fecha} - {self.variedad.nombre}>'
