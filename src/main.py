import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

# Acceder a las credenciales de la API desde el archivo .env
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
    client = tweepy.Client(bearer_token, api_key, api_secret, access_token,access_token_secret)
    
    #Publicar tweet
    response = client.create_tweet(text="¡HELLO WORLD!")
    
    if response and response.data:
        tweet_id = response.data.get("id")
        print(f"Tweet publicado con éxito: https://twitter.com/user/status/{tweet_id}")
    else:
        print("Error: No se recibió respuesta de la API.")

except Exception as e:
    print(f"Error al publicar el tweet: {e}")