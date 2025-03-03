import os
import time
from dotenv import load_dotenv
import tweepy
import pandas as pd

# Cargar las credenciales de la API desde el archivo .env
load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Comprobar que las credenciales se cargaron correctamente
if not all([api_key, api_secret, bearer_token, access_token, access_token_secret]):
    print("Error: Faltan credenciales en el archivo .env")
    exit()

try:
    # Crear cliente de la API v2
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

    # Probar la conexión a la API
    try:
        user = client.get_me()
        print(f"✅ Conexión con la API exitosa. Usuario autenticado: {user.data.username}")
    except tweepy.TweepyException as e:
        print(f"Error de conexión: {e}")
        exit()

    # Cargar el archivo CSV de vacantes
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../jobs/vacantes.csv')

    if not os.path.exists(csv_path):
        print(f"Archivo no encontrado: {csv_path}")
        exit()

    df = pd.read_csv(csv_path)

    # Función para crear un tweet a partir de una fila del DataFrame con formato
    def crear_tweet(row):
        tweet_text = (
            f"🚀 {row['Job Title']} en {row['Company']}!\n\n"
            f"📍 Ubicación: {row['location']}, {row['Country']}\n"
            f"💼 Experiencia: {row['Experience']}\n"
            f"💰 Salario: {row['Salary Range']}\n"
            f"🎯 Rol: {row['Role']}\n"
            f"👉 Contacto: {row['Contact Person']} ({row['Contact']})\n\n"
            "#Empleo #Vacantes #Trabajo"
        )
        
        # Limitar el tweet a 280 caracteres
        if len(tweet_text) > 280:
            tweet_text = tweet_text[:277] + "..."
        
        return tweet_text.strip()


    # Opción 1: Publicar una vacante específica por ID
    def publicar_por_id(vacante_id):
        row = df[df['Job Id'] == vacante_id]
        
        if not row.empty:
            tweet_text = crear_tweet(row.iloc[0])
            try:
                response = client.create_tweet(text=tweet_text)
                if response and response.data:
                    tweet_id = response.data.get("id")
                    print(f"Tweet publicado con éxito: https://twitter.com/user/status/{tweet_id}")
                else:
                    print("Error: No se recibió respuesta de la API.")
            except tweepy.TweepyException as e:
                print(f"Error al publicar el tweet: {e}")
        else:
            print(f"La vacante con ID {vacante_id} no existe.")

    # Opción 2: Publicar varias vacantes por una lista de IDs
    def publicar_varias_ids(lista_ids, delay=10):
        for vacante_id in lista_ids:
            publicar_por_id(vacante_id)
            try:
                time.sleep(delay)
            except KeyboardInterrupt:
                print("Proceso interrumpido manualmente.")
                break

    # Ejemplos de uso:
    # Publicar una sola vacante por ID
    publicar_por_id(5)

    # Publicar múltiples vacantes por una lista de IDs
    # publicar_varias_ids([1, 2, 3], delay=5)

except Exception as e:
    print(f"Error general: {e}")
