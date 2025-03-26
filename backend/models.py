from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Vacante(Base):
    __tablename__ = "vacantes"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, unique=True, index=True)
    titulo = Column(String)
    empresa = Column(String)
    descripcion = Column(Text)
    salario = Column(String)
    ubicacion = Column(String)
    pais = Column(String)
    experiencia = Column(String)
    tipo_trabajo = Column(String)
    skills = Column(Text)
    contacto = Column(String)
    contacto_nombre = Column(String)
    beneficios = Column(Text)
    portal = Column(String)
    role = Column(String)
    fecha_publicacion = Column(String)
    qualifications = Column(String)
    tamano_empresa = Column(String)
