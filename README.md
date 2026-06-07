# OptiSCADA-ML Complete

## Descripción

OptiSCADA-ML Complete es una plataforma demostrativa de Industria 4.0 que integra:

- SCADA virtual con Node-RED
- MQTT Cloud con HiveMQ
- Streamlit Community Cloud
- Machine Learning
- Optimización de procesos industriales
- Arquitectura IoT orientada a eventos

El proyecto simula un tanque térmico industrial, genera telemetría en tiempo real, aplica modelos de Machine Learning y publica recomendaciones operativas mediante MQTT.

---

## Enlaces del proyecto

### Streamlit Cloud

https://optiscada-ml.streamlit.app/

### Node-RED (Render)

https://processmind-scada-ml.onrender.com/

### GitHub

https://github.com/antoniot73/OptiSCADA_ML_Complete

---

## Arquitectura validada

```text
Node-RED Render
        ↓
HiveMQ Cloud
        ↓
Streamlit Cloud
        ↓
Machine Learning + Optimización
        ↓
HiveMQ Cloud
        ↓
Node-RED Render
```

---

## Componentes

### Node-RED

Responsable de:

- Simulación SCADA
- Generación de telemetría
- Publicación MQTT
- Recepción de recomendaciones
- Endpoint de disponibilidad `/healthz`

### HiveMQ Cloud

Broker MQTT TLS.

```text
Host:
d7803de0bcd24ef0a342e4396a020c56.s1.eu.hivemq.cloud

Puerto:
8883
```

### Streamlit

Responsable de:

- HMI industrial
- Tendencias
- Alarmas
- Machine Learning
- Optimización
- Publicación MQTT

---

## Arranque manual de Node-RED

Durante desarrollo local:

```powershell
node-red
```

Acceso:

```text
http://localhost:1880
```

---

## Despliegue de Node-RED en Render

Node-RED se encuentra desplegado públicamente en:

```text
https://processmind-scada-ml.onrender.com/
```

Características:

- Docker
- Variables de entorno MQTT
- Reconexión automática
- Persistencia de flujos
- Integración con HiveMQ Cloud

Variables configuradas:

```text
MQTT_HOST
MQTT_PORT
MQTT_USERNAME
MQTT_PASSWORD
```

---

## Verificación de disponibilidad de Node-RED

Node-RED incluye un endpoint HTTP de verificación:

```text
https://processmind-scada-ml.onrender.com/healthz
```

Este endpoint permite distinguir entre:

```text
Render respondió
```

y:

```text
Node-RED está completamente listo para operar
```

La respuesta esperada contiene un estado tipo:

```json
{
  "service": "processmind-scada-ml",
  "status": "READY",
  "node_red": "RUNNING",
  "mqtt_flow": "ACTIVE"
}
```

Esta validación se usa para confirmar que:

- Node-RED arrancó correctamente.
- El flujo principal está activo.
- Existe telemetría reciente.
- El servicio puede integrarse con Streamlit y MQTT.

---

## Arranque automático y validación READY desde Streamlit

Cuando un usuario abre:

```text
https://optiscada-ml.streamlit.app/
```

la aplicación ejecuta una solicitud HTTP para despertar automáticamente Node-RED en Render y luego consulta:

```text
https://processmind-scada-ml.onrender.com/healthz
```

La mejora implementada en `app.py` permite que Streamlit espere el estado real de disponibilidad antes de asumir que el SCADA virtual está listo.

Flujo:

```text
Usuario abre Streamlit
        ↓
Wake-up HTTP
        ↓
Consulta /healthz
        ↓
Node-RED READY
        ↓
Conexión HiveMQ
        ↓
Telemetría disponible
        ↓
Procesamiento ML
```

Beneficios:

- Sin intervención manual.
- Recuperación automática de servicios dormidos.
- Mejor experiencia de usuario.
- Validación explícita de Node-RED antes de operar.
- Menor probabilidad de estados iniciales `NOT_AVAILABLE` en Machine Learning.

---

## Funcionalidad actualizada en `app.py`

La aplicación Streamlit incorpora una verificación de arranque para Node-RED mediante el endpoint `/healthz`.

La lógica actual realiza:

1. Activación del servicio Node-RED en Render.
2. Espera controlada hasta recibir estado `READY`.
3. Confirmación visual en Streamlit.
4. Lectura MQTT posterior.
5. Procesamiento de telemetría.
6. Evaluación de alarmas y predicciones ML.

Esto evita confundir una respuesta HTTP inicial de Render con una disponibilidad completa del flujo industrial.

Estados esperados:

```text
Node-RED Render: ACTIVANDO
Node-RED Render: READY
MQTT: TELEMETRÍA RECIBIDA
ML: PROCESADO
Anomalía ML: NORMAL / ANOMALY / NOT_AVAILABLE
```

---

## MQTT

### Telemetría

```text
factory/demo/tank01/telemetry
```

```text
Node-RED → HiveMQ → Streamlit
```

### Recomendaciones

```text
factory/demo/tank01/recommendation
```

```text
Streamlit → HiveMQ → Node-RED
```

### Alarmas

```text
factory/demo/tank01/alarm
```

---

## Machine Learning

### Calidad

Random Forest Regressor

### Energía

Random Forest Regressor

### Anomalías

Isolation Forest

---

## Optimización

Variables optimizadas:

- Temperatura
- Flujo
- Potencia del calentador

Objetivos:

- Maximizar calidad
- Minimizar energía
- Reducir riesgo operativo

Ejemplo:

```json
{
  "recommended_temperature_c": 78,
  "recommended_flow_lpm": 46,
  "recommended_heater_power_pct": 55,
  "expected_saving_pct": 11.64
}
```

---

## Estado actual

### Completado

- Node-RED Render
- HiveMQ Cloud
- Streamlit Cloud
- MQTT bidireccional
- Machine Learning
- Optimización
- Recomendaciones MQTT
- Recepción MQTT en Streamlit
- Recepción MQTT en Node-RED
- Arranque automático desde Streamlit
- Endpoint `/healthz` en Node-RED
- Validación READY desde `app.py`

### Arquitectura validada end-to-end

```text
Node-RED → HiveMQ → Streamlit → ML → HiveMQ → Node-RED
```

---

## Autor

Antonio Nicolás Toro González

Maestría en Inteligencia Artificial para la Transformación Digital

Instituto Internacional de Aguascalientes
