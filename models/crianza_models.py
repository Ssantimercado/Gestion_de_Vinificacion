import uuid
from models.db import db

class Crianza(db.Model):
    __tablename__ = 'crianzas'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # Corregido para generar un UUID por defecto
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    tipo_recipient = db.Column(db.String(100), nullable=False)
    observaciones = db.Column(db.Text)
    fermentacion_id = db.Column(db.String(36), db.ForeignKey('fermentaciones.id'), nullable=False)

    # Relación con Fermentación
    fermentacion = db.relationship("Fermentacion", back_populates="crianza")
    # Relación con Embotellado
    embotellados = db.relationship("Embotellado", back_populates="crianza", cascade="all, delete-orphan")

    def __init__(self, fecha_inicio, tipo_recipient, fermentacion_id, fecha_fin=None, observaciones=None):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo_recipient = tipo_recipient
        self.observaciones = observaciones
        self.fermentacion_id = fermentacion_id

    def serialize(self):
        return {
            'id': self.id,
            'fecha_inicio': str(self.fecha_inicio),
            'fecha_fin': str(self.fecha_fin) if self.fecha_fin else None,
            'tipo_recipient': self.tipo_recipient,
            'observaciones': self.observaciones,
            'fermentacion_id': self.fermentacion_id
        }
