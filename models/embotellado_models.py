# models/embotellado_models.py
import uuid
from extensions import db
import datetime

class Embotellado(db.Model):
    __tablename__ = 'embotellados'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    crianza_id = db.Column(db.String(36), db.ForeignKey('crianzas.id'), unique=True, nullable=False) # Unique si una crianza solo tiene un embotellado
    fecha_embotellado = db.Column(db.Date, nullable=False, default=datetime.date.today)
    cantidad_botellas = db.Column(db.Integer, nullable=False)
    tipo_botella = db.Column(db.String(100), nullable=False)
    notas = db.Column(db.Text, nullable=True)

    # Relación con Crianza
    crianza = db.relationship('Crianza', back_populates='embotellado')

    def __repr__(self):
        return f"<Embotellado {self.id} - Fecha: {self.fecha_embotellado} - Botellas: {self.cantidad_botellas}>"