# models/recepcion.py
import uuid
from extensions import db
import datetime

class RecepcionUva(db.Model):
    __tablename__ = 'recepciones'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    variedad_id = db.Column(db.String(36), db.ForeignKey('variedades.id'), nullable=False)
    cantidad_kg = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.date.today)
    notas = db.Column(db.Text, nullable=True)

    # Relación con VariedadUva
    variedad = db.relationship('VariedadUva', backref=db.backref('recepciones', lazy=True))

    # Relación inversa con Fermentacion
    # 'Fermentacion' es el nombre de la CLASE del modelo Fermentacion
    # back_populates='recepcion' debe coincidir con el nombre de la relación en el modelo Fermentacion
    fermentaciones = db.relationship('Fermentacion', back_populates='recepcion', lazy=True, cascade="all, delete-orphan")


    def __repr__(self):
        return f"<RecepcionUva {self.id} - {self.cantidad_kg}kg de {self.variedad.nombre if self.variedad else 'N/A'}>"