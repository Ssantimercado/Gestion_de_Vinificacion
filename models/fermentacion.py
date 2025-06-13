# models/fermentacion.py
import uuid
from extensions import db
import datetime

class Fermentacion(db.Model):
    __tablename__ = 'fermentaciones'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    recepcion_id = db.Column(db.String(36), db.ForeignKey('recepciones.id'), nullable=False) # Clave foránea

    fecha_inicio = db.Column(db.Date, nullable=False, default=datetime.date.today) # Default si no se especifica
    fecha_fin = db.Column(db.Date, nullable=True) # Puede ser nula al principio
    temperatura = db.Column(db.Float, nullable=False) #Lo modifique por la base de datos
    levadura_utilizada = db.Column(db.String(100), nullable=True)
    ph_inicial = db.Column(db.Numeric(4, 2), nullable=True)
    ph_final = db.Column(db.Numeric(4, 2), nullable=True)
    densidad_inicial = db.Column(db.Numeric(5, 3), nullable=True)
    densidad_final = db.Column(db.Numeric(5, 3), nullable=True)
    notas = db.Column(db.Text, nullable=True)

    # Relación con RecepcionUva
    # back_populates='fermentaciones' debe coincidir con la propiedad en RecepcionUva
    recepcion = db.relationship("RecepcionUva", back_populates="fermentaciones")

    # Relación con Crianza
    # Asegúrate de que 'Crianza' sea el nombre de la CLASE del modelo Crianza
    # Si tu archivo se llama crianza_models.py y la clase es Crianza, esto está bien.
    crianza = db.relationship('Crianza', back_populates='fermentacion', uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Fermentacion {self.id} - Inicio: {self.fecha_inicio} - Recepción ID: {self.recepcion_id}>"