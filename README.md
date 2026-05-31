# OptiSCADA-ML Complete

**OptiSCADA-ML Complete** es un proyecto demostrativo de Industria 4.0 que integra un SCADA virtual, MQTT Cloud, Machine Learning y optimización de procesos industriales en una aplicación web desarrollada con Streamlit.

El sistema simula un proceso industrial tipo **tanque térmico**, publica telemetría mediante MQTT, procesa los datos en Streamlit, aplica modelos de Machine Learning y genera recomendaciones de operación para mejorar calidad, consumo energético y seguridad del proceso.

---

## 1. Objetivo del proyecto

Construir una demo funcional que permita validar una arquitectura industrial moderna basada en:

- SCADA virtual con Node-RED.
- Broker MQTT Cloud con HiveMQ.
- Dashboard HMI en Streamlit.
- Modelos de Machine Learning para predicción de calidad, energía y anomalías.
- Optimización de setpoints operativos.
- Publicación de recomendaciones hacia el SCADA virtual.

---

## 2. Arquitectura general

```text
+-----------------------------+
| Node-RED                    |
| SCADA virtual / simulador   |
+-------------+---------------+
              |
              | MQTT telemetry
              v
+-----------------------------+
| HiveMQ Cloud                |
| Broker MQTT TLS             |
+-------------+---------------+
              |
              | MQTT subscription
              v
+-----------------------------+
| Streamlit                   |
| HMI + ML + Optimización     |
+-------------+---------------+
              |
              | MQTT recommendation
              v
+-----------------------------+
| Node-RED                    |
| Recepción de recomendaciones|
+-----------------------------+
```

---

## 3. Componentes principales

### 3.1 Streamlit

Streamlit es la capa web del proyecto.

Incluye:

- HMI industrial.
- Visualización de telemetría.
- Tendencias.
- Alarmas.
- Entrenamiento de modelos ML.
- Inferencia ML.
- Optimización de setpoints.
- Lectura MQTT desde HiveMQ.
- Publicación de recomendaciones MQTT.

Archivo principal:

```text
app.py
```

---

### 3.2 Node-RED

Node-RED actúa como SCADA virtual y simulador de proceso.

Genera variables industriales simuladas:

- `temperature_c`
- `pressure_bar`
- `flow_lpm`
- `level_pct`
- `heater_power_pct`
- `vibration_mm_s`
- `energy_kwh`
- `product_quality_pct`

Publica telemetría en HiveMQ mediante MQTT.

---

### 3.3 HiveMQ Cloud

HiveMQ Cloud funciona como broker MQTT externo.

Configuración utilizada:

```text
Host: d7803de0bcd24ef0a342e4396a020c56.s1.eu.hivemq.cloud
Puerto TLS: 8883
```

> La contraseña real no debe guardarse en GitHub.

---

## 4. Tópicos MQTT

### Telemetría del proceso

```text
factory/demo/tank01/telemetry
```

Flujo:

```text
Node-RED -> HiveMQ Cloud -> Streamlit
```

---

### Recomendaciones de optimización

```text
factory/demo/tank01/recommendation
```

Flujo:

```text
Streamlit -> HiveMQ Cloud -> Node-RED
```

---

### Alarmas

```text
factory/demo/tank01/alarm
```

Reservado para extensión futura.

---

## 5. Estructura del proyecto

```text
OptiSCADA_ML_Complete/
|
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
|
├── src/
│   ├── alarms.py
│   ├── config.py
│   ├── features.py
│   ├── ml_inference.py
│   ├── ml_training.py
│   ├── mqtt_client.py
│   ├── optimizer.py
│   ├── process_models.py
│   ├── simulator.py
│   └── utils.py
|
├── data/
│   └── synthetic_training_data.csv
|
├── models/
│   └── .gitkeep
|
├── node_red/
│   └── optiscada_node_red_flow.json
|
├── docs/
│   ├── ARCHITECTURE.md
│   └── IMPLEMENTATION_STAGES.md
|
└── .streamlit/
    ├── config.toml
    └── secrets.example.toml
```

---

## 6. Instalación local

### 6.1 Crear entorno virtual

```powershell
python -m venv .venv
```

Activar entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

### 6.2 Instalar dependencias

```powershell
pip install -r requirements.txt
```

---

### 6.3 Ejecutar Streamlit

```powershell
python -m streamlit run app.py
```

Abrir en el navegador:

```text
http://localhost:8501
```

---

## 7. Configuración segura de secretos

Crear localmente el archivo:

```text
.streamlit/secrets.toml
```

Contenido:

```toml
MQTT_HOST = "d7803de0bcd24ef0a342e4396a020c56.s1.eu.hivemq.cloud"
MQTT_PORT = 8883

MQTT_USERNAME = "optiscada"
MQTT_PASSWORD = "TU_PASSWORD_REAL"

MQTT_TOPIC_TELEMETRY = "factory/demo/tank01/telemetry"
MQTT_TOPIC_RECOMMENDATION = "factory/demo/tank01/recommendation"
MQTT_TOPIC_ALARM = "factory/demo/tank01/alarm"
```

Este archivo **no debe subirse a GitHub**.

El repositorio sólo debe incluir:

```text
.streamlit/secrets.example.toml
```

con valores de ejemplo.

---

## 8. Archivos sensibles

El archivo `.gitignore` debe incluir:

```gitignore
.streamlit/secrets.toml
test*.py
.venv/
__pycache__/
*.pyc
models/*.joblib
models/training_report.json
```

No subir a GitHub:

- `.streamlit/secrets.toml`
- `test_mqtt.py`
- `test_mqtt_sub.py`
- contraseñas reales
- modelos entrenados pesados, salvo que se decida versionarlos explícitamente

---

## 9. Ejecución de Node-RED

Iniciar Node-RED:

```powershell
node-red
```

Abrir en el navegador:

```text
http://localhost:1880
```

---

## 10. Flujo Node-RED validado

El flujo local validado usa:

```text
inject -> function -> debug
                  -> mqtt out
```

Además, para recibir recomendaciones desde Streamlit:

```text
mqtt in -> debug
```

---

### 10.1 Nodo `inject`

Configuración sugerida:

```text
Name: Cada 5 segundos
Repeat: interval
Every: 5 seconds
```

---

### 10.2 Nodo `function`

Nombre:

```text
Simular tanque térmico
```

Este nodo genera el mensaje MQTT con telemetría industrial.

Ejemplo de payload:

```json
{
  "asset_id": "tank01",
  "timestamp": "2026-05-31T03:38:21.396Z",
  "temperature_c": 78.5,
  "pressure_bar": 2.1,
  "flow_lpm": 45.2,
  "level_pct": 65.0,
  "heater_power_pct": 70.0,
  "vibration_mm_s": 1.5,
  "energy_kwh": 12.8,
  "product_quality_pct": 93.5
}
```

---

### 10.3 Nodo `mqtt out`

Configuración:

```text
Name: Publicar HiveMQ
Topic: factory/demo/tank01/telemetry
QoS: 1
Server: HiveMQ Cloud
Port: 8883
TLS: activado
```

El broker debe mostrar estado:

```text
connected
```

---

### 10.4 Nodo `mqtt in`

Configuración:

```text
Name: Recomendación Streamlit
Topic: factory/demo/tank01/recommendation
QoS: 1
Server: HiveMQ Cloud
Port: 8883
TLS: activado
```

---

## 11. Validaciones realizadas

### 11.1 Conexión Python a HiveMQ

Se validó conexión MQTT con TLS:

```text
Conectado: Success
```

---

### 11.2 Suscripción MQTT con Python

Se validó recepción desde el tópico:

```text
factory/demo/tank01/telemetry
```

Resultado:

```text
Conectado: Success
Mensaje recibido:
factory/demo/tank01/telemetry
{...}
```

---

### 11.3 Conexión Node-RED a HiveMQ

Se validó conexión del broker MQTT en Node-RED:

```text
Connected to broker: node-red-optiscada-clean@mqtts://d7803de0bcd24ef0a342e4396a020c56.s1.eu.hivemq.cloud:8883
```

---

## 12. Machine Learning

El sistema incluye entrenamiento de modelos para:

### Calidad del producto

Archivo generado:

```text
quality_model.joblib
```

Modelo:

```text
Random Forest Regressor
```

---

### Consumo energético

Archivo generado:

```text
energy_model.joblib
```

Modelo:

```text
Random Forest Regressor
```

---

### Detección de anomalías

Archivo generado:

```text
anomaly_model.joblib
```

Modelo:

```text
Isolation Forest
```

---

## 13. Dataset sintético

El proyecto incluye:

```text
data/synthetic_training_data.csv
```

Este dataset permite entrenar los modelos sin depender de datos industriales reales.

---

## 14. Optimización de proceso

El sistema recomienda valores operativos para:

- temperatura
- flujo
- potencia del calentador

La función de optimización busca:

```text
Maximizar calidad
Minimizar consumo energético
Reducir riesgo operativo
```

Ejemplo de salida:

```json
{
  "recommended_temperature_c": 78,
  "recommended_flow_lpm": 46,
  "recommended_heater_power_pct": 68,
  "expected_quality_pct": 90.2,
  "expected_energy_kwh": 11.7,
  "expected_saving_pct": 8.4
}
```

---

## 15. Despliegue en GitHub

Inicializar repositorio:

```powershell
git init
git add .
git commit -m "Initial complete OptiSCADA ML project"
```

Configurar remoto:

```powershell
git remote add origin https://github.com/antoniot73/OptiSCADA_ML_Complete.git
git branch -M main
git push -u origin main
```

Si el remoto ya existe:

```powershell
git remote set-url origin https://github.com/antoniot73/OptiSCADA_ML_Complete.git
git push origin main
```

---

## 16. Despliegue en Streamlit Community Cloud

1. Subir el proyecto seguro a GitHub.
2. Crear una nueva app en Streamlit Community Cloud.
3. Seleccionar el repositorio.
4. Usar `app.py` como archivo principal.
5. Configurar secretos en:

```text
App -> Settings -> Secrets
```

Pegar los valores reales de:

```toml
MQTT_HOST = "..."
MQTT_PORT = 8883
MQTT_USERNAME = "..."
MQTT_PASSWORD = "..."
MQTT_TOPIC_TELEMETRY = "factory/demo/tank01/telemetry"
MQTT_TOPIC_RECOMMENDATION = "factory/demo/tank01/recommendation"
MQTT_TOPIC_ALARM = "factory/demo/tank01/alarm"
```

---

## 17. Estado actual del proyecto

### Completado

- Simulador SCADA en Node-RED.
- Broker MQTT en HiveMQ Cloud.
- Publicación MQTT desde Node-RED.
- Recepción MQTT validada con Python.
- Dataset sintético.
- Entrenamiento ML.
- Optimización de proceso.
- Configuración segura de secretos.
- Preparación para GitHub.

### Pendiente

- Validación final de recepción MQTT dentro de Streamlit.
- Publicación de recomendaciones desde Streamlit hacia Node-RED.
- Despliegue público en Streamlit Community Cloud.

---

## 18. Autor

**Antonio Nicolás Toro González**

Maestría en Inteligencia Artificial para la Transformación Digital
