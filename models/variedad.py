# models/variedad.py

from sqlalchemy import Column, String
# Importa 'db' desde extensions.py
from extensions import db 
import uuid

#Base = declarative_base()


class VariedadUva(db.Model): 
    __tablename__ = 'variedades_uva'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(100), nullable=False, unique=True)
    origen = Column(String(100))
    foto = Column(String(255))

    def __repr__(self):
        return f"<VariedadUva(nombre='{self.nombre}', origen='{self.origen}')>"