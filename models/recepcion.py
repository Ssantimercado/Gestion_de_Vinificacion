import uuid
from models.db import db

class RecepcionUva(db.Model):
    __tablename__ = 'recepciones_uva'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha = db.Column(db.Date, nullable=False)
    variedad_id = db.Column(db.String(36), db.ForeignKey('variedades_uva.id'), nullable=False)
    cantidad_kg = db.Column(db.Float, nullable=False)
    notas = db.Column(db.Text)

    variedad = db.relationship("VariedadUva", back_populates="recepciones")
    fermentaciones = db.relationship("Fermentacion", back_populates="recepcion", cascade="all, delete-orphan")

    def __init__(self, fecha, variedad_id, cantidad_kg, notas=None):
        self.fecha = fecha
        self.variedad_id = variedad_id
        self.cantidad_kg = cantidad_kg
        self.notas = notas

    def serialize(self):
        return {
            'id': self.id,
            'fecha': str(self.fecha),
            'variedad_id': self.variedad_id,
            'cantidad_kg': self.cantidad_kg,
            'notas': self.notas
        }
