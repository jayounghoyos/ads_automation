from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import crud, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/vacantes/", response_model=list[schemas.Vacante])
def read_vacantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vacantes(db, skip=skip, limit=limit)
