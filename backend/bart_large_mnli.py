import os
import time
import tweepy
import pandas as pd
import torch
import json
from transformers import pipeline
from dotenv import load_dotenv
from backend.database import SessionLocal
from backend.crud import get_vacantes


# Cargar credenciales de API
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
tweet_id_hilo = os.getenv("TWEET_ID_HILO")

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
query = "(busco trabajo OR busco empleo OR #buscoEmpleo OR #buscotrabajo) -is:retweet lang:es"
tweet_fields = ["id", "text", "created_at", "author_id","possibly_sensitive"]
user_fields = ["username"]
expansions = ["author_id"]
max_results = 10

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
    "trabajacolombia", "empleoactual", "PortalEmpleo", "VacantesHOY", "TrabajoEnZamora", "TrabajoEnAstur", "Trabajo en Asturias"
]

def buscar_tweets():
    """Busca tweets recientes y los almacena en un CSV antes de analizarlos."""
    print("🔍 Buscando tweets en X...")

    #Busqueda de tweet mas reciente y manejo de errores
    try:
        response = client.search_recent_tweets(
            query=query,
            tweet_fields=tweet_fields,
            expansions=expansions,
            user_fields=user_fields,
            max_results=max_results #importante para no pasarse de tokens
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

            # Filtrar tweets con enlaces (probablemente reclutadores)
            #if "http" in tweet_text or "https" in tweet_text:
            #   continue
            
            if getattr(tweet, "possibly_sensitive", False):
                print(f"Filtrado por contenido sensible: {tweet.text}")
                continue
            # Omitir tweets de usuarios en lista negra (reclutadores conocidos)
            if username in usuarios_excluidos:
                print(f"Filtrado por usuario bloqueado: {username}")
                continue

            # Omitir tweets que contengan palabras clave de reclutadores
            if any(palabra.lower() in tweet_text.lower() for palabra in palabras_excluidas):
                print(f"Filtrado por palabra clave: {tweet_text}")
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

def cargar_vacantes_desde_db():
    print("🗃️ Cargando vacantes desde la base de datos...")
    try:
        db = SessionLocal()
        vacantes = get_vacantes(db)
        db.close()
        return [
            {
                "Job Title": v.titulo,
                "Job Description": v.descripcion,
                "skills": v.skills,
                "Company": v.empresa
            }
            for v in vacantes
        ]
    except Exception as e:
        print(f"❌ Error cargando vacantes desde la DB: {e}")
        return []

def analizar_tweets_con_ia(tweets, vacantes):
    """Usa Hugging Face para analizar tweets y recomendar vacantes."""
    print("🤖 Analizando tweets con IA...")

    # Cargar modelo de clasificación
    model_name = "facebook/bart-large-mnli" #Se ejecuta local con pykle desde la cache
    device = 0 if torch.cuda.is_available() else -1 #cargar GPU
    classifier = pipeline("zero-shot-classification", model=model_name, device=device)

    texts = [tweet[2] for tweet in tweets]
    usernames = [tweet[1] for tweet in tweets]
    candidate_labels = list(set(v["Job Title"] for v in vacantes if v["Job Title"].strip()))

    results = classifier(texts, candidate_labels, multi_label=True)
    recomendaciones = []

    for i, result in enumerate(results):
        best_match = result["labels"][0]
        empresa = next((v["Company"] for v in vacantes if v["Job Title"] == best_match), "Desconocida")
        recomendaciones.append({
            "usuario": usernames[i],
            "tweet": texts[i],
            "vacante": best_match,
            "empresa": empresa
        })


    print("✅ Análisis completado.")
    return recomendaciones

def comentar_en_tweet_ancla(recomendaciones):
    for rec in recomendaciones:
        texto = (
            f"@{rec['usuario']}\n"
            f"📝 {rec['tweet']}\n\n"
            f"Recomendación:\n{rec['vacante']}\nen\n{rec['empresa']}"
        )
        try:
            client.create_tweet(
                text=texto[:280],
                in_reply_to_tweet_id=tweet_id_hilo
            )
            print("✅ Comentario publicado")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Error comentando: {e}")

#Analisis local
def analizar_tweets_csv(csv_path, vacantes):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error leyendo el archivo CSV: {e}")
        return []

    try:
        classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    except Exception as e:
        print(f"❌ Error cargando el modelo: {e}")
        return []

    textos = df["Texto"].tolist()
    usernames = df["Username"].tolist()
    candidate_labels = [v["Job Title"] for v in vacantes]

    try:
        results = classifier(textos, candidate_labels, multi_label=True)
    except Exception as e:
        print(f"❌ Error al procesar el batch: {e}")
        return []

    recomendaciones = []

    for i, result in enumerate(results):
        mejor = result["labels"][0]
        empresa = next((v["Company"] for v in vacantes if v["Job Title"] == mejor), "Desconocida")
        recomendaciones.append({
            "usuario": usernames[i],
            "tweet": textos[i],
            "vacante": mejor,
            "empresa": empresa
        })

    print("✅ Análisis local completado.")
    return recomendaciones

# Ejecutar el flujo completo
if __name__ == "__main__":
    tweets = buscar_tweets()
    if not tweets:
        print("⚠️ No hay tweets para analizar.")
        exit()

    vacantes = cargar_vacantes_desde_db()
    if not vacantes:
        print("⚠️ No hay vacantes para recomendar.")
        exit()

    recomendaciones = analizar_tweets_con_ia(tweets, vacantes)
    print(recomendaciones)
    comentar_en_tweet_ancla(recomendaciones)
