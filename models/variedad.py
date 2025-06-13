# models/variedad.py

from sqlalchemy import Column, String
from extensions import db #  Importamos 'db' desde extensions.py
import uuid

class VariedadUva(db.Model):
    __tablename__ = 'variedades'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4())) # UUID como clave primaria
    nombre = db.Column(db.String(100), nullable=False)
    origen = Column(String(100))
    foto = Column(String(255))

    def __repr__(self):
        return f"<VariedadUva(nombre='{self.nombre}', origen='{self.origen}')>"