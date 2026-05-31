
# Industrial AI Prototype

## Descripción

Sistema web industrial estilo SCADA con:

- Simulación de variables de proceso
- Historian SQLite
- Backend FastAPI
- Dashboard Streamlit
- Machine Learning supervisado
- Arquitectura Industria 4.0

---

# Arquitectura General

```text
Simulador Industrial
        ↓
SQLite Historian
        ↓
FastAPI API
        ↓
RandomForest ML
        ↓
Dashboard Streamlit
        ↓
Render Cloud
```

---

# Variables industriales

- Temperatura
- Presión
- Flujo
- Vibración

---

# Machine Learning

Modelo utilizado:

```text
RandomForestRegressor
```

Predicción:

```text
temperatura = f(presion, flujo, vibracion)
```

---

# Estructura del proyecto

```text
industrial_ai_prototype/
│
├── app/
│   ├── main.py
│   ├── api.py
│   ├── api_ml.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── simulator.py
│   └── ml_model.py
│
├── dashboard/
│   └── streamlit_app.py
│
├── data/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Requisitos

## Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecutar FastAPI

```bash
uvicorn app.main:app --reload
```

---

# Ejecutar Dashboard Streamlit

Abrir nueva terminal:

```bash
streamlit run dashboard/streamlit_app.py
```

---

# URLs locales

## FastAPI

```text
http://127.0.0.1:8000/docs
```

## Streamlit

```text
http://localhost:8501
```

---

# Endpoints principales

- `/health`
- `/current`
- `/history`
- `/predict`

---

# Variables simuladas

El simulador genera:

- presión
- flujo
- vibración
- temperatura

La temperatura depende matemáticamente de las otras variables para permitir aprendizaje supervisado realista.

---

# Dashboard Industrial

El dashboard incluye:

- KPIs industriales
- Tendencias históricas
- Gauges industriales
- Tabla histórica
- Predicción IA
- Temperatura real vs predicha
- Error MAE

---

# Machine Learning Supervisado

Modelo:

```text
RandomForestRegressor
```

Variables de entrada:

```text
presion
flujo
vibracion
```

Variable objetivo:

```text
temperatura
```

Métrica utilizada:

```text
MAE (Mean Absolute Error)
```

---

# Deploy Cloud

## Tecnologías

- GitHub
- Render.com

---

# Deploy FastAPI

## Build command

```bash
pip install -r requirements.txt
```

## Start command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

# Deploy Streamlit

## Start command

```bash
streamlit run dashboard/streamlit_app.py --server.port $PORT
```

---

# Tecnologías utilizadas

- Python
- FastAPI
- Streamlit
- Plotly
- SQLite
- SQLAlchemy
- Scikit-learn
- Pandas
- Render
- GitHub

---

# Capacidades actuales

✔ Dashboard industrial  
✔ Historian  
✔ Tiempo real  
✔ IA supervisada  
✔ Predicción industrial  
✔ Arquitectura cloud-ready  

---

# Próximas mejoras posibles

- OPC UA real
- MQTT
- PostgreSQL
- Docker
- Alertas industriales
- Detección de anomalías
- Autenticación
- Kubernetes

---

# Autor

Proyecto prototipo Industria 4.0 orientado a integración:

- SCADA-like
- Historian
- Machine Learning
- Web Industrial Dashboard
