## **OptiSCADA-ML Complete** 

## **Descripción** 

OptiSCADA-ML Complete es una plataforma demostrativa de Industria 4.0 desarrollada para integrar: 

- SCADA virtual 

- MQTT Cloud 

- Machine Learning 

- Optimización de procesos 

- Streamlit Community Cloud 

- Node-RED 

- HiveMQ Cloud 

El proyecto simula un proceso industrial de un tanque térmico y permite: 

- Generar telemetría industrial. 

- Publicar datos mediante MQTT. 

- Visualizar variables de proceso en un HMI web. 

- Entrenar modelos de Machine Learning. 

- Detectar anomalías. 

- Optimizar setpoints operativos. 

- Publicar recomendaciones de operación. 

## **Arquitectura** 

**==> picture [152 x 271] intentionally omitted <==**

**----- Start of picture text -----**<br>
┌──────────────────────────┐<br>│ Node-RED                 │<br>│ SCADA Virtual            │<br>└────────────┬─────────────┘<br>             │ MQTT<br>             ▼<br>┌──────────────────────────┐<br>│ HiveMQ Cloud             │<br>│ Broker MQTT TLS          │<br>└────────────┬─────────────┘<br>             │ MQTT<br>             ▼<br>┌──────────────────────────┐<br>│ Streamlit                │<br>│ HMI + ML + Optimización  │<br>└────────────┬─────────────┘<br>             │ MQTT<br>             ▼<br>┌──────────────────────────┐<br>│ Node-RED                 │<br>**----- End of picture text -----**<br>


1 

```
│ Recepción de            │
│ recomendaciones          │
└──────────────────────────┘
```

## **Componentes** 

## **Streamlit** 

Funcionalidades: 

- HMI industrial 

- Tendencias 

- Alarmas 

- Entrenamiento ML 

- Optimización 

- Integración MQTT 

Archivo principal: 

```
app.py
```

## **Node-RED** 

Node-RED actúa como: 

```
SCADA Virtual
```

Genera telemetría simulada: 

- temperatura • presión • flujo • nivel • potencia • vibración • energía • calidad 

Publica datos en: 

```
factory/demo/tank01/telemetry
```

También recibe recomendaciones desde: 

2 

```
factory/demo/tank01/recommendation
```

## **HiveMQ Cloud** 

Broker MQTT utilizado: 

```
d7803de0bcd24ef0a342e4396a020c56.s1.eu.hivemq.cloud
```

Puerto TLS: 

```
8883
```

## **Tópicos MQTT** 

## **Telemetría** 

```
factory/demo/tank01/telemetry
```

Publicador: 

```
Node-RED
```

Consumidor: 

```
Streamlit
```

## **Recomendaciones** 

```
factory/demo/tank01/recommendation
```

Publicador: 

```
Streamlit
```

Consumidor: 

3 

```
Node-RED
```

## **Alarmas** 

```
factory/demo/tank01/alarm
```

Reservado para futuras versiones. 

## **Instalación** 

## **Crear entorno virtual** 

```
python-mvenv.venv
.\.venv\Scripts\Activate.ps1
```

## **Instalar dependencias** 

```
pipinstall-rrequirements.txt
```

## **Configuración MQTT** 

Crear: 

```
.streamlit/secrets.toml
```

Contenido: 

```
MQTT_HOST="d7803de0bcd24ef0a342e4396a020c56.s1.eu.hivemq.cloud"
MQTT_PORT=8883
```

```
MQTT_USERNAME="optiscada"
MQTT_PASSWORD="********"
MQTT_TOPIC_TELEMETRY="factory/demo/tank01/telemetry"
MQTT_TOPIC_RECOMMENDATION="factory/demo/tank01/recommendation"
MQTT_TOPIC_ALARM="factory/demo/tank01/alarm"
```

4 

## **Ejecución** 

## **Streamlit** 

```
python-mstreamlitrunapp.py
```

Acceso: 

```
http://localhost:8501
```

## **Node-RED** 

```
node-red
```

Acceso: 

```
http://localhost:1880
```

## **Flujo Node-RED utilizado** 

Configuración actual: 

```
inject
```

```
   ↓
function
   ↓
debug
   ↓
mqtt out
```

El nodo function genera: 

```
{
```

```
"asset_id":"tank01",
"temperature_c":78.5,
"pressure_bar":2.1,
"flow_lpm":45.2,
"level_pct":65.0,
```

5 

```
"heater_power_pct":70.0,
"vibration_mm_s":1.5,
"energy_kwh":12.8,
"product_quality_pct":93.5
}
```

## **Machine Learning** 

Modelos incluidos: 

## **Calidad** 

```
quality_model.joblib
```

Modelo: 

```
Random Forest Regressor
```

## **Energía** 

```
energy_model.joblib
```

Modelo: 

```
Random Forest Regressor
```

## **Anomalías** 

```
anomaly_model.joblib
```

Modelo: 

```
Isolation Forest
```

6 

## **Optimización** 

Variables optimizadas: 

- temperatura • flujo • potencia 

Objetivo: 

```
Maximizar calidad
Minimizar energía
Reducir riesgo
```

Salida: 

```
{
"recommended_temperature_c":78,
"recommended_flow_lpm":46,
"recommended_heater_power_pct":68,
"expected_saving_pct":8.4
}
```

## **Estado actual** 

## **Completado** 

- SCADA virtual Node-RED 

- HiveMQ Cloud 

- MQTT TLS 

- Simulación de proceso 

- Dataset sintético 

- Entrenamiento ML 

- Optimización 

- Publicación MQTT 

- Recepción MQTT en Python 

## **Pendiente** 

- Corrección final de recepción MQTT dentro de Streamlit 

- Publicación de recomendaciones desde Streamlit 

- Despliegue en Streamlit Community Cloud 

7 

## **Autor** 

Antonio Nicolás Toro González 

Maestría en Inteligencia Artificial para la Transformación Digital 

8 

