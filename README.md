# Magneto Ads - Automatización de Vacantes

Este proyecto automatiza la publicación, edición y análisis de vacantes laborales mediante una plataforma web moderna que combina FastAPI y Next.js con shadcn/ui. Se conecta a redes sociales como X (Twitter) y Telegram para publicar automáticamente, analizar contenido y mostrar métricas de desempeño.

---

## Funcionalidades principales

* Publicación automática de vacantes en X y Telegram
* Filtros interactivos por ciudad y salario
* Editor lateral estilo email para modificar vacantes
* Análisis de tweets con IA para detectar búsquedas de empleo
* Dashboard de métricas de tweets publicados
* Backend estructurado con SQLAlchemy y PostgreSQL

---

## Estructura del proyecto

```
ads_automation/  
├── backend/           # API en FastAPI + lógica de negocio  
├── frontend/          # Next.js + Tailwind + shadcn/ui  
├── data/              # CSVs para análisis local de tweets  
├── src/               # Scripts para publicar y clasificar  
├── venv/              # Entorno virtual Python  
├── .env               # Variables de entorno (no se sube al repo)  
├── .gitignore         # Archivos y carpetas ignoradas  
├── package.json       # Frontend (Node.js)  
├── requirements.txt   # Dependencias de backend (Python)  
└── README.md  
```

---

## Cómo correr el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/jayounghoyos/ads_automation.git
cd ads_automation
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias del backend

```bash
pip install -r requirements.txt
```

### 4. Crear archivo .env

```
API_KEY=my_api_key
API_SECRET=my_secret
ACCESS_TOKEN=my_token
ACCESS_TOKEN_SECRET=my_token_secret
BEARER_TOKEN=my_bearer
TELEGRAM_TOKEN=my_telegram_token
TELEGRAM_CHAT_ID=my_chat_id
tweet_id_hilo=my_tweet_id_base
DATABASE_URL=postgresql://usuario:clave@localhost/db
```

### 5. Ejecutar el backend

```bash
uvicorn backend.main:app --reload
```

### 6. Ejecutar el frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Análisis de tweets con IA

El script `bart_large_mnli.py` usa un modelo `zero-shot` de Hugging Face para clasificar tweets en función de las vacantes disponibles. Puedes usar:

* `GET /analizar/` para hacer análisis en vivo (consume tokens de API X)
* `GET /tweets/analisis_local/` para análisis local desde CSV en `data/tweets_obtenidos.csv`

Las recomendaciones se comentan en un tweet ancla configurado en el `.env`.

---

## Dashboard de métricas

La vista principal incluye un panel con estadísticas de tweets publicados:

* Total de likes, retweets, respuestas e impresiones
* Gráfica de barras comparativa por tweet

---

## Base de datos (PostgreSQL)

Contiene campos detallados por vacante:

* job\_id, titulo, empresa, descripcion, salario
* ubicacion, pais, experiencia, tipo\_trabajo, skills
* contacto, contacto\_nombre, beneficios, role
* fecha\_publicacion, qualifications, tamano\_empresa

---

## Tecnologías usadas

**Frontend:**

* Next.js
* Tailwind CSS
* shadcn/ui
* recharts

**Backend:**

* FastAPI
* SQLAlchemy + Pydantic
* Tweepy (X API)
* python-telegram-bot
* Hugging Face Transformers
* pandas / torch

---

## Scripts clave

* `src/publicador.py` → Publica una o varias vacantes en X (Twitter)
* `backend/bart_large_mnli.py` → Clasifica tweets y recomienda vacantes
* `src/telegram_publicador.py` → Publica vacantes en Telegram

---

## Estado actual del proyecto

* Cuenta con funcionalidades completas para: publicar, editar, eliminar, analizar y comentar vacantes desde UI
* Optimizado para ejecutar localmente con GPU
* API de X y Telegram integradas, otras plataformas desestimadas por restricciones técnicas o de uso