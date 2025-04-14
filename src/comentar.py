import sys
import os

# Agregar la raíz del proyecto al sys.path para importar 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import random
import tweepy
from dotenv import load_dotenv
from backend.database import SessionLocal
from backend.crud import get_vacantes

# Cargar variables de entorno
load_dotenv()
tweet_id = os.getenv("TWEET_ID_HILO")

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Verificación
if not tweet_id:
    print("❌ No se encontró TWEET_ID_HILO en .env")
    exit()

# Función para construir el tweet a partir de una vacante
def crear_tweet(v):
    tweet = (
        f"🚀 {v.titulo} en {v.empresa}!\n\n"
        f"📍 Ubicación: {v.ubicacion}, {v.pais}\n"
        f"💼 Experiencia: {v.experiencia}\n"
        f"💰 Salario: {v.salario}\n"
        f"🎯 Rol: {v.role}\n"
        f"👉 Contacto: {v.contacto_nombre} ({v.contacto})\n\n"
        f"link: https://www.magneto365.com/es \n"
        "#Empleo #Vacantes #Trabajo"
    )
    return tweet[:280].strip()

# Obtener una vacante aleatoria
def obtener_vacante():
    db = SessionLocal()
    vacantes = get_vacantes(db)
    db.close()

    if not vacantes:
        print("⚠️ No hay vacantes disponibles.")
        return None

    return random.choice(vacantes)

# Autocomentar en el tweet original
def comentar_vacante():
    vacante = obtener_vacante()
    if not vacante:
        return

    texto = crear_tweet(vacante)

    # Conexión a la API de X
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    try:
        respuesta = api.update_status(
            status=texto,
            in_reply_to_status_id=tweet_id,
            auto_populate_reply_metadata=True
        )
        print("✅ Comentario publicado exitosamente.")
    except Exception as e:
        print(f"❌ Error publicando el comentario: {e}")

if __name__ == "__main__":
    comentar_vacante()
