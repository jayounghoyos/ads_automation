import os
import tweepy
import pandas as pd
import requests
import time
from transformers import pipeline
from dotenv import load_dotenv

# Cargar credenciales de API
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Verificar credenciales
if not all([api_key, api_secret, bearer_token, access_token, access_token_secret]):
    print("❌ Error: Faltan credenciales en el archivo .env")
    exit()

# Configurar API de X (Twitter)
try:
    client = tweepy.Client(
        bearer_token=bearer_token,
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True
    )
    print("✅ Conexión con API de X establecida correctamente.")
except Exception as e:
    print(f"❌ Error al conectar con la API de X: {e}")
    exit()

# Configuración para la búsqueda de tweets
query = "(#buscoEmpleo OR #buscotrabajo) -is:retweet " #OR #Trabajo OR #Vacante lang:es
tweet_fields = ["id", "text", "created_at", "author_id"]
user_fields = ["username"]
expansions = ["author_id"]
max_results = 100  # Aumentamos para capturar más tweets

# Ruta de almacenamiento de datos
data_path = "data"
if not os.path.exists(data_path):
    os.makedirs(data_path)

tweets_csv_path = os.path.join(data_path, "tweets_obtenidos.csv")

# Palabras clave para filtrar tweets de reclutadores
palabras_excluidas = [
    "oferta de trabajo", "envía tu hoja de vida", "envíala al correo",
    "vacante disponible", "ManpowerGroup", "trabaja con nosotros",
    "aplica escaneando", "consulta aquí", "envía tu CV", "inscríbete aquí",
    "postulación", "detalles y postulación", "envía un mensaje"
]

# Lista negra de usuarios de reclutadores conocidos
usuarios_excluidos = [
    "ManpowerGroupCO", "cipemec", "exelacolombia", "Memakker", "serprietom",
    "trabajacolombia", "empleoactual", "PortalEmpleo", "VacantesHOY"
]

def buscar_tweets():
    """Busca tweets recientes y los almacena en un CSV antes de analizarlos."""
    print("🔍 Buscando tweets en X...")

    try:
        response = client.search_recent_tweets(
            query=query,
            tweet_fields=tweet_fields,
            expansions=expansions,
            user_fields=user_fields,
            max_results=max_results
        )

        if not response or not hasattr(response, "data") or response.data is None:
            print("⚠️ No se encontraron tweets con el hashtag.")
            return []

        print(f"📌 Se encontraron {len(response.data)} tweets iniciales antes de filtrar.")

        # Mapeo de author_id a usernames
        users = {user["id"]: user["username"] for user in response.includes.get("users", [])}

        tweets_data = []
        for tweet in response.data:
            tweet_text = tweet.text.replace("\n", " ").strip()  # Limpiar saltos de línea
            username = users.get(tweet.author_id, "Desconocido")

            # 1️⃣ Filtrar tweets con enlaces (probablemente reclutadores)
            if "http" in tweet_text or "https" in tweet_text:
                continue

            # 2️⃣ Omitir tweets de usuarios en lista negra (reclutadores conocidos)
            if username in usuarios_excluidos:
                continue

            # 3️⃣ Omitir tweets que contengan palabras clave de reclutadores
            if any(palabra.lower() in tweet_text.lower() for palabra in palabras_excluidas):
                continue

            # Guardar solo tweets relevantes
            tweets_data.append([tweet.id, username, tweet_text])

        if not tweets_data:
            print("⚠️ No se encontraron tweets relevantes después del filtrado.")
            return []

        # Guardar en CSV
        df = pd.DataFrame(tweets_data, columns=["Tweet ID", "Username", "Texto"])
        df.to_csv(tweets_csv_path, index=False, encoding="utf-8", sep=",")

        print(f"✅ {len(df)} tweets relevantes guardados en {tweets_csv_path}")
        return tweets_data

    except tweepy.TooManyRequests:
        print("❌ Límite de solicitudes alcanzado. Espera antes de intentarlo de nuevo.")
        return []
    except Exception as e:
        print(f"❌ Error buscando tweets: {e}")
        return []

def cargar_vacantes():
    """Carga vacantes desde el archivo vacantes.csv en la carpeta jobs."""
    print("📂 Cargando vacantes...")
    vacantes_path = os.path.join("jobs", "vacantes.csv")

    try:
        if not os.path.exists(vacantes_path):
            print("⚠️ No se encontró vacantes.csv en la carpeta jobs.")
            return []

        df = pd.read_csv(vacantes_path, encoding="utf-8", delimiter=",", on_bad_lines="skip")
        if df.empty:
            print("⚠️ No hay vacantes disponibles en el archivo.")
            return []

        df = df.fillna("No especificado")
        vacantes = df[["Job Title", "Job Description", "skills", "Company"]].dropna()
        print(f"✅ {len(vacantes)} vacantes cargadas correctamente.")
        return vacantes.to_dict(orient="records")

    except Exception as e:
        print(f"❌ Error cargando vacantes: {e}")
        return []

def analizar_tweets_con_ia(tweets, vacantes):
    """Usa Hugging Face para analizar tweets y recomendar vacantes."""
    print("🤖 Analizando tweets con IA...")

    # Cargar modelo de clasificación
    model_name = "facebook/bart-large-mnli"
    classifier = pipeline("zero-shot-classification", model=model_name)

    recomendaciones = []

    for tweet in tweets:
        username = tweet[1]  # Ahora obtenemos el nombre de usuario en vez de solo el ID
        tweet_texto = tweet[2]

        # Construir lista de etiquetas de vacantes
        candidate_labels = [v["Job Title"] for v in vacantes]

        # Clasificación del tweet
        result = classifier(tweet_texto, candidate_labels, multi_label=True)
        best_match = result["labels"][0]  # Tomar la mejor coincidencia

        # Buscar la empresa de la vacante recomendada
        empresa = next((v["Company"] for v in vacantes if v["Job Title"] == best_match), "Desconocida")

        recomendaciones.append(f"📌 @{username} → {best_match} en {empresa}")

        # Agregar un pequeño delay para evitar sobrecarga
        time.sleep(1)

    print("✅ Análisis completado.")
    return "\n🔹 **Recomendaciones Generadas:**\n" + "\n".join(recomendaciones)

# Ejecutar el flujo completo
if __name__ == "__main__":
    tweets = buscar_tweets()
    if not tweets:
        print("⚠️ No hay tweets para analizar.")
        exit()

    vacantes = cargar_vacantes()
    if not vacantes:
        print("⚠️ No hay vacantes para recomendar.")
        exit()

    recomendaciones = analizar_tweets_con_ia(tweets, vacantes)
    print(recomendaciones)
