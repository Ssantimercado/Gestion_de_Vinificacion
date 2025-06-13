# models/crianza_models.py
import uuid
from extensions import db
import datetime

class Crianza(db.Model):
    __tablename__ = 'crianzas'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fermentacion_id = db.Column(db.String(36), db.ForeignKey('fermentaciones.id'), unique=True, nullable=False) # Unique si una fermentación solo tiene una crianza
    tipo_barrica = db.Column(db.String(100), nullable=False)
    tiempo_crianza_meses = db.Column(db.Numeric(5, 2), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False, default=datetime.date.today)
    fecha_fin = db.Column(db.Date, nullable=True)
    temperatura_crianza = db.Column(db.Numeric(5, 2), nullable=True)
    notas = db.Column(db.Text, nullable=True)

    # Relación con Fermentacion
    fermentacion = db.relationship('Fermentacion', back_populates='crianza')

    # Relación con Embotellado
    embotellado = db.relationship('Embotellado', back_populates='crianza', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Crianza {self.id} - Tipo: {self.tipo_barrica} - Inicio: {self.fecha_inicio}>"