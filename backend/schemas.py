from pydantic import BaseModel

class VacanteBase(BaseModel):
    job_id: int
    titulo: str
    empresa: str
    descripcion: str
    salario: str
    ubicacion: str
    pais: str
    experiencia: str
    tipo_trabajo: str
    skills: str
    contacto: str
    contacto_nombre: str
    beneficios: str
    portal: str
    role: str
    fecha_publicacion: str
    qualifications: str
    tamano_empresa: str

class VacanteCreate(VacanteBase):
    pass

class Vacante(VacanteBase):
    id: int

    class Config:
        orm_mode = True
