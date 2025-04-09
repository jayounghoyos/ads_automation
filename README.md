# Magneto Ads - Automatización de Vacantes

Este proyecto automatiza la publicación y recomendación de vacantes laborales en redes sociales como **X (Twitter)**. Utiliza **FastAPI** + **Next.js** con **shadcn/ui** para crear una plataforma intuitiva, moderna y eficiente.

---

## Características principales

- Publicación de vacantes desde un panel web  
- Filtros por ciudad y salario en tiempo real  
- Editor lateral estilo email para modificar vacantes  
- Análisis de tweets con IA para detectar búsquedas de empleo  
- Publicación automática en X (Twitter) usando `tweepy`  
- Carga y manejo de vacantes desde DB

---

## Estructura del proyecto

```
ads_automation/
│
├── backend/           -> Backend con FastAPI (API REST y lógica)
├── frontend/          -> Next.js + Tailwind + shadcn/ui
├── jobs/              -> Contiene vacantes.csv para exposición
├── data/              -> Contiene tweets_obtenidos.csv (análisis local)
├── src/               -> Scripts para publicar y analizar
└── requirements.txt   -> Dependencias
```

---

## Cómo correr el proyecto

### 1. Clonar el repositorio

~~~bash
git clone https://github.com/jayounghoyos/ads_automation.git
cd ads_automation
~~~

### 2. Crear entorno virtual y activarlo

~~~bash
python -m venv venv
source venv/bin/activate  -> En Windows: venv\Scripts\activate
~~~

### 3. Instalar dependencias

~~~bash
pip install -r requirements.txt
~~~

### 4. Configurar variables de entorno

Crear un archivo `.env` con las claves de Twitter (X):

```
API_KEY=tu_api_key
API_SECRET=tu_secret
ACCESS_TOKEN=tu_token
ACCESS_TOKEN_SECRET=tu_token_secret
```

### 5. Iniciar backend

~~~bash
uvicorn backend.main:app --reload
~~~

### 6. Iniciar frontend

~~~bash
cd frontend
npm install
npm run dev
~~~

---

## Formato de la base de datos (PostgreSQL)

| Campo             | Descripción                                                               |
|-------------------|---------------------------------------------------------------------------|
| `job_id`          | ID único de la vacante                                                    |
| `titulo`          | Título del cargo ofrecido                                                 |
| `empresa`         | Nombre de la empresa que publica la vacante                               |
| `descripcion`     | Breve descripción del trabajo y sus responsabilidades                     |
| `salario`         | Rango salarial o monto ofrecido (texto libre, puede incluir símbolos)     |
| `ubicacion`       | Ciudad donde se encuentra el trabajo                                      |
| `Pais`            | País donde está ubicada la vacante                                        |
| `Experiencia`     | Años de experiencia requeridos                                            |
| `Tipo_trabajo`    | Tipo de contrato: Tiempo completo, medio tiempo, prácticas, etc.          |
| `skills`          | Habilidades técnicas y blandas requeridas para el puesto                  |
| `contacto`        | Información de contacto (teléfono, correo, etc.)                          |
| `contacto_nombre` | Nombre de la persona responsable del reclutamiento                        |
| `beneficios`      | Beneficios ofrecidos por la empresa (Ej: salud, bonos, horarios flexibles)|
| `Portal`          | Sitio o plataforma donde se encontró originalmente la vacante             |
| `Role`            | Rol o categoría del puesto (Ej: Frontend Developer, Ingeniero de datos)   |
| `fecha_publicacion`| Fecha en que fue publicada la vacante                                    |
| `qualifications`  | Títulos académicos o certificados requeridos                              |
| `tamano_empresa`  | Número de empleados o clasificación de la empresa (pequeña, mediana, etc.)|

Este archivo se puede editar desde la interfaz web.

---

## Tecnologías utilizadas

### 🖥️ Frontend

- Next.js (React 19)  
- Tailwind CSS  
- shadcn/ui  

### ⚙️ Backend

- FastAPI  
- SQLAlchemy + Pydantic  
- Tweepy (para Twitter/X)  
- pandas  

---

## Scripts importantes

- `src/publicador.py` → Publica vacantes en X (Twitter)  
- `src/bart_large_mnli.py` → Clasifica tweets usando BART