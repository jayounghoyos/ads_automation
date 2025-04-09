from sqlalchemy.orm import Session
from . import models, schemas

#Obtener un conjunto de vacantes desde el DB 
def get_vacantes(db: Session, skip: int = 0, limit: int = 100):#obtener con rangos
    return db.query(models.Vacante).offset(skip).limit(limit).all()

#CRUD,Creación de vacante
def create_vacante(db: Session, vacante: schemas.VacanteCreate):
    db_vacante = models.Vacante(**vacante.dict())
    db.add(db_vacante)
    db.commit()
    db.refresh(db_vacante)
    return db_vacante