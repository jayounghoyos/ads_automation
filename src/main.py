# Nuevo main.py optimizado para solo buscar vacantes por ID directamente en la base de datos
import os
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
import tweepy
from backend.database import SessionLocal
from backend.models import Vacante  # Acceso directo al modelo

# UTF-8 para consola
sys.stdout.reconfigure(encoding='utf-8')

# Cargar credenciales desde .env
load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

if not all([api_key, api_secret, bearer_token, access_token, access_token_secret]):
    print("Error: Faltan credenciales en el archivo .env")
    exit()

try:
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

    try:
        user = client.get_me()
        print(f"✅ Conexión con la API exitosa. Usuario autenticado: {user.data.username}")
    except tweepy.TweepyException as e:
        print(f"Error de conexión: {e}")
        exit()

    def crear_tweet(v):
        tweet = (
            f"🚀 {v.titulo} en {v.empresa}!\n\n"
            f"📍 Ubicación: {v.ubicacion}, {v.pais}\n"
            f"💼 Experiencia: {v.experiencia}\n"
            f"💰 Salario: {v.salario}\n"
            f"🎯 Rol: {v.role}\n"
            f"👉 Contacto: {v.contacto_nombre} ({v.contacto})\n\n"
            "#Empleo #Vacantes #Trabajo"
        )
        return tweet[:280].strip()

    def publicar_por_id(vacante_id):
        db = SessionLocal()
        vacante = db.query(Vacante).filter(Vacante.job_id == int(vacante_id)).first()
        db.close()

        if vacante:
            tweet_text = crear_tweet(vacante)
            try:
                response = client.create_tweet(text=tweet_text)
                tweet_id = response.data.get("id") if response and response.data else None
                if tweet_id:
                    print(f"✅ Tweet publicado con éxito: https://twitter.com/user/status/{tweet_id}")
                else:
                    print("⚠️ No se recibió respuesta válida de la API.")
            except tweepy.TweepyException as e:
                print(f"❌ Error al publicar el tweet: {e}")
        else:
            print(f"⚠️ La vacante con ID {vacante_id} no existe.")

    def publicar_varias_ids(lista_ids, delay=10):
        for vacante_id in lista_ids:
            publicar_por_id(vacante_id)
            try:
                time.sleep(delay)
            except KeyboardInterrupt:
                print("Proceso interrumpido manualmente.")
                break

    if len(sys.argv) > 1:
        ids = sys.argv[1:]
        print(f"📤 Publicando vacantes con IDs: {ids}")
        publicar_varias_ids(ids, delay=5)
    else:
        print("⚠️ No se proporcionaron IDs de vacantes para publicar.")

except Exception as e:
    print(f"❌ Error general: {e}")
