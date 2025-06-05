import uuid
from models.db import db

class Embotellado(db.Model):
    __tablename__ = 'embotellados'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Corregido para generar un UUID por defecto
    fecha = db.Column(db.Date, nullable=False)
    cantidad_botellas = db.Column(db.Integer, nullable=False)
    crianza_id = db.Column(db.String(36), db.ForeignKey('crianzas.id'), nullable=False)

    # Relación con Crianza
    crianza = db.relationship("Crianza", back_populates="embotellados")

    def __init__(self, fecha, cantidad_botellas, crianza_id):
        self.fecha = fecha
        self.cantidad_botellas = cantidad_botellas
        self.crianza_id = crianza_id

    def serialize(self):
        return {
            'id': self.id,
            'fecha': str(self.fecha),
            'cantidad_botellas': self.cantidad_botellas,
            'crianza_id': self.crianza_id
        }
