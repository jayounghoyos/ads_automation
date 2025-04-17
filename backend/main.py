import os
import sys
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import subprocess

from .bart_large_mnli import buscar_tweets, cargar_vacantes_desde_db, analizar_tweets_con_ia, analizar_tweets_csv, comentar_en_tweet_ancla

from . import crud, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

# Instancia de la aplicación FastAPI
app = FastAPI(
    title="Vacantes API",
    description="Backend para publicar vacantes en redes sociales",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "🚀 Bienvenido a la API de Vacantes!"}

# Ruta para obtener vacantes con rangos
@app.get("/vacantes/", response_model=list[schemas.Vacante])
def read_vacantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vacantes(db, skip=skip, limit=limit) #devuelve en formato JSON

#obtener vacante por ID
@app.get("/vacantes/{job_id}", response_model=schemas.Vacante)
def get_vacante_by_id(job_id: int, db: Session = Depends(get_db)):
    vacante = db.query(models.Vacante).filter(models.Vacante.job_id == job_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    return vacante

@app.get("/analizar/")
def analizar_y_recomendar():
    tweets = buscar_tweets()
    vacantes = cargar_vacantes_desde_db()
    if not tweets or not vacantes:
        return {"recomendaciones": []}
    
    resultado = analizar_tweets_con_ia(tweets, vacantes)

    try:
        comentar_en_tweet_ancla(resultado)
    except Exception as e:
        print(f"❌ Error comentando automáticamente: {e}")


    return {"recomendaciones": resultado}


@app.get("/tweets/analisis_local/")
def analizar_tweets_local():

    csv_path = "data/tweets_obtenidos.csv"

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=500, detail="El archivo CSV no existe.")

    vacantes = cargar_vacantes_desde_db()

    if not vacantes:
        raise HTTPException(status_code=500, detail="No hay vacantes en la base de datos.")

    try:
        recomendaciones = analizar_tweets_csv(csv_path, vacantes)
        return recomendaciones
    except Exception as e:
        print(f"❌ Error en analizar_tweets_local: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Ruta para publicar vacantes
@app.post("/publicar/")
async def publicar_vacantes(request: Request):
    data = await request.json()
    vacancies = data.get('vacancies', [])
    print("Datos recibidos en publicar_vacantes:", vacancies)

    ids = [str(v['job_id']) for v in vacancies] 

    result = subprocess.run(
        [sys.executable, "src/publicador.py"] + ids,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    print("Resultado del script:", result.stdout)
    print("Errores del script:", result.stderr)

    if result.returncode == 0:
        return JSONResponse(content={"success": True})
    else:
        return JSONResponse(content={"success": False, "error": result.stderr})

@app.post("/vacantes/", response_model=schemas.Vacante)
def create_vacante(vacante: schemas.VacanteCreate, db: Session = Depends(get_db)):
    return crud.create_vacante(db=db, vacante=vacante)

@app.post("/tweets/analizar/")
def analizar_tweets_endpoint():
    tweets = buscar_tweets()
    vacantes = cargar_vacantes_desde_db()
    if not tweets or not vacantes:
        return {"recomendaciones": []}
    resultado = analizar_tweets_con_ia(tweets, vacantes)
    return {"recomendaciones": resultado}

@app.put("/vacantes/{job_id}", response_model=schemas.Vacante)
def update_vacante(job_id: int, vacante_data: schemas.VacanteCreate, db: Session = Depends(get_db)):
    vacante = db.query(models.Vacante).filter(models.Vacante.job_id == job_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    for attr, value in vacante_data.dict().items():
        setattr(vacante, attr, value)
    db.commit()
    db.refresh(vacante)
    return vacante

@app.delete("/vacantes/{job_id}")
def delete_vacante(job_id: int, db: Session = Depends(get_db)):
    vacante = db.query(models.Vacante).filter(models.Vacante.job_id == job_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    db.delete(vacante)
    db.commit()
    return {"message": "Vacante eliminada exitosamente"}
