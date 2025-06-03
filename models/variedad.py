from sqlalchemy import Column, String, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class VariedadUva(Base):
    __tablename__ = 'variedades_uva'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False, unique=True)
    origen = Column(String(100))
    foto = Column(String(255))  # Almacenará la ruta al archivo de la imagen

    def __repr__(self):
        return f"<VariedadUva(nombre='{self.nombre}', origen='{self.origen}')>"