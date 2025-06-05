import uuid
from models.db import db

class Fermentacion(db.Model):
    __tablename__ = 'fermentaciones'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    temperatura = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=False)
    recepcion_id = db.Column(db.String(36), db.ForeignKey('recepciones_uva.id'), nullable=False)

    recepcion = db.relationship("RecepcionUva", back_populates="fermentaciones")

    def __init__(self, fecha_inicio, fecha_fin, temperatura, ph, recepcion_id):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.temperatura = temperatura
        self.ph = ph
        self.recepcion_id = recepcion_id

    def serialize(self):
        return {
            'id': self.id,
            'fecha_inicio': str(self.fecha_inicio),
            'fecha_fin': str(self.fecha_fin),
            'temperatura': self.temperatura,
            'ph': self.ph,
            'recepcion_id': self.recepcion_id
        }
