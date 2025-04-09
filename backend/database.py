from sqlalchemy import create_engine #Conecta la base de datos usando URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker #Sesiones para interactuar con la base de datos.
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) #conexion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
