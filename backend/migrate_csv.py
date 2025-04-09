import os
import pandas as pd
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from backend import models, database
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear tabla si no existe
# Se asegura que esté creada
models.Base.metadata.create_all(bind=database.engine)

# Leer el archivo CSV
csv_path = Path("jobs/vacantes.csv")
df = pd.read_csv(csv_path)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database.engine)
session = SessionLocal()

# Contadores
insertados = 0
actualizados = 0

# Iterar por cada fila del CSV
for _, row in df.iterrows():
    # Extraer campos del CSV
    job_id = int(row["Job Id"])
    titulo = row["Job Title"]
    empresa = row["Company"]
    descripcion = row.get("Job Description", "")# usar cadena vacía si no hay descripcion
    salario = row.get("Salary Range", "")
    ubicacion = row.get("location", "")
    pais = row.get("Country", "")
    experiencia = row.get("Experience", "")
    tipo_trabajo = row.get("Work Type", "")
    skills = row.get("skills", "")
    contacto = row.get("Contact", "")
    contacto_nombre = row.get("Contact Person", "")
    beneficios = row.get("Benefits", "")
    portal = row.get("Job Portal", "")
    role = row.get("Role", "")
    fecha_publicacion = row.get("Job Posting Date", "")
    qualifications = row.get("Qualifications", "")
    tamano_empresa = row.get("Company Size", "")

    # Consultar si ya existe una vacante con este job_id en la base de datos
    vacante_existente = session.query(models.Vacante).filter_by(job_id=job_id).first()

    if vacante_existente:
        # Si la vacante ya existe, verificar si algunos campos clave han cambiado
        cambios = False
        # Actualizar descripción,salario y skils
        if vacante_existente.descripcion != descripcion:
            vacante_existente.descripcion = descripcion 
            cambios = True
        if vacante_existente.salario != salario:
            vacante_existente.salario = salario
            cambios = True
        if vacante_existente.skills != skills:
            vacante_existente.skills = skills
            cambios = True

        if cambios:
            actualizados += 1
    else:
        # Si la vacante no existe en BD, crear una nueva instancia del modelo Vacante con todos los campos
        nueva = models.Vacante(
            job_id=job_id,
            titulo=titulo,
            empresa=empresa,
            descripcion=descripcion,
            salario=salario,
            ubicacion=ubicacion,
            pais=pais,
            experiencia=experiencia,
            tipo_trabajo=tipo_trabajo,
            skills=skills,
            contacto=contacto,
            contacto_nombre=contacto_nombre,
            beneficios=beneficios,
            portal=portal,
            role=role,
            fecha_publicacion=fecha_publicacion,
            qualifications=qualifications,
            tamano_empresa=tamano_empresa
        )
        session.add(nueva)
        insertados += 1

# Guardar cambios
session.commit()
session.close() # Cerrar la sesión para liberar la conexión

print(f"✅ {insertados} vacantes insertadas.")
print(f"🔄 {actualizados} vacantes actualizadas si cambiaron.")
