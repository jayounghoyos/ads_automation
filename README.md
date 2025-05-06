# Magneto Ads - Automatización de Vacantes

Este proyecto automatiza la publicación, edición y análisis de vacantes laborales mediante una plataforma web moderna que combina FastAPI y Next.js con shadcn/ui. Se conecta a redes sociales como X (Twitter) para publicar automáticamente, analizar contenido y mostrar métricas de desempeño.

---

## Funcionalidades principales

- Publicación automática de vacantes en X y Telegram  
- Filtros interactivos por ciudad y salario  
- Editor lateral estilo email para modificar vacantes  
- Análisis de tweets con IA para detectar búsquedas de empleo  
- Dashboard de métricas de tweets publicados  
- Backend estructurado con SQLAlchemy y PostgreSQL  

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
API_KEY=tu_api_key
API_SECRET=tu_secret
ACCESS_TOKEN=tu_token
ACCESS_TOKEN_SECRET=tu_token_secret
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

El script `src/bart_large_mnli.py` analiza tweets públicos con modelos de clasificación zero-shot (BART). Se puede correr desde la API:

GET /analizar/

También puedes hacer análisis local con un archivo CSV precargado (`data/tweets_obtenidos.csv`).

---

## Dashboard de métricas

La vista principal ahora incluye un panel con estadísticas de tweets publicados:

- Total de likes, retweets, respuestas e impresiones  
- Gráfica de barras comparativa por tweet  
- En el futuro, se puede expandir para mostrar rendimiento por vacante o canal  

---

## Base de datos (PostgreSQL)

Contiene campos detallados de cada vacante:

- job_id  
- titulo  
- empresa  
- descripcion  
- salario  
- ubicacion  
- pais  
- experiencia  
- tipo_trabajo  
- skills  
- contacto  
- contacto_nombre  
- beneficios  
- portal  
- role  
- fecha_publicacion  
- qualifications  
- tamano_empresa  

---

## Tecnologías usadas

**Frontend:**  
- Next.js  
- Tailwind CSS  
- shadcn/ui  
- recharts  

**Backend:**  
- FastAPI  
- Pydantic  
- SQLAlchemy  
- Tweepy  
- pandas  
- Transformers (HuggingFace)  

---

## Scripts clave

- `src/publicador.py` → Publica en Twitter (X)  
- `src/bart_large_mnli.py` → Clasifica tweets  
- `src/telegram_publicador.py` → Publica en Telegram