# OptiSCADA-ML Complete
# Guía de Usuario (USER GUIDE)

## Acceso a la Plataforma

### Aplicación Web

https://optiscada-ml.streamlit.app/

### SCADA Virtual (Node-RED)

https://processmind-scada-ml.onrender.com/

---

# 1. Introducción

OptiSCADA-ML Complete es una plataforma demostrativa de Industria 4.0 que integra:

- SCADA Virtual
- MQTT Cloud
- HiveMQ Cloud
- Node-RED
- Streamlit
- Machine Learning
- Optimización de Procesos Industriales

El sistema simula un tanque térmico industrial y permite monitorear variables de proceso, generar predicciones mediante inteligencia artificial y publicar recomendaciones operativas hacia el SCADA virtual.

---

# 2. Arquitectura General

```text
Node-RED
      ↓
HiveMQ Cloud
      ↓
Streamlit
      ↓
Machine Learning
      ↓
Optimización
      ↓
HiveMQ Cloud
      ↓
Node-RED
```

Esta arquitectura permite una comunicación bidireccional completamente funcional.

---

# 3. Barra Lateral de Configuración

La barra lateral permite configurar el origen de los datos.

## Fuente de Telemetría

Opciones:

- Simulador interno
- MQTT Cloud

## Modo Simulado

Modos disponibles:

- Normal
- Alta temperatura
- Bajo flujo
- Sobrepresión
- Alta vibración
- Baja calidad

## Generar lectura

Genera una nueva observación del proceso.

## Reiniciar sesión

Limpia el histórico y reinicia la simulación.

---

# 4. Pestaña HMI

La pestaña HMI muestra el estado operativo actual del tanque térmico.

Variables principales:

- Temperatura
- Presión
- Flujo
- Nivel
- Potencia
- Energía
- Calidad

Estados posibles:

## NORMAL

Operación dentro de parámetros aceptables.

## WARNING

Condición operativa anormal moderada.

## CRITICAL

Condición operativa crítica que requiere atención.

---

# 5. Alarmas

El sistema analiza automáticamente:

- Temperatura
- Presión
- Vibración
- Calidad
- Consumo energético

Las alarmas son registradas automáticamente en la bitácora de eventos.

---

# 6. Predicciones de Machine Learning

La plataforma utiliza modelos entrenados para generar predicciones en tiempo real.

## Calidad del producto

Modelo:

Random Forest Regressor

Salida:

```text
ml_quality_prediction
```

## Consumo energético

Modelo:

Random Forest Regressor

Salida:

```text
ml_energy_prediction
```

## Detección de anomalías

Modelo:

Isolation Forest

Salida:

```text
ml_anomaly_flag
```

---

# 7. Tendencias

La pestaña Tendencias permite visualizar la evolución temporal de:

- temperature_c
- pressure_bar
- flow_lpm
- level_pct
- heater_power_pct
- vibration_mm_s
- energy_kwh
- product_quality_pct

Las gráficas son interactivas y permiten analizar el comportamiento histórico del proceso.

---

# 8. Optimización

La pestaña Optimización calcula automáticamente recomendaciones operativas.

Variables optimizadas:

- Temperatura
- Flujo
- Potencia del calentador

Objetivos:

- Maximizar calidad
- Minimizar consumo energético
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

# 9. Publicación MQTT

La plataforma puede enviar recomendaciones mediante MQTT.

Tópico:

```text
factory/demo/tank01/recommendation
```

Flujo:

```text
Streamlit
      ↓
HiveMQ
      ↓
Node-RED
```

Cuando la recomendación es recibida correctamente, Node-RED muestra:

```text
Recomendación recibida
```

---

# 10. Entrenamiento de Machine Learning

La pestaña Machine Learning permite:

- Cargar datasets CSV
- Entrenar nuevos modelos
- Actualizar modelos existentes
- Generar métricas de desempeño

---

# 11. Datos

La pestaña Datos contiene:

## Histórico

Listado completo de observaciones.

## Exportación CSV

Permite descargar el histórico.

## Bitácora

Registro de eventos y alarmas.

---

# 12. MQTT

La pestaña MQTT permite:

## Leer un mensaje MQTT

Recibir telemetría desde HiveMQ Cloud.

## Procesamiento automático

Cada mensaje recibido es enriquecido con:

- Alarmas
- Predicciones ML
- Indicadores operativos

---

# 13. Arranque Automático del SCADA Virtual

Cuando un usuario abre:

https://optiscada-ml.streamlit.app/

la aplicación realiza automáticamente una solicitud HTTP hacia:

https://processmind-scada-ml.onrender.com/

para activar el servicio Node-RED desplegado en Render.

Flujo:

```text
Usuario abre Streamlit
        ↓
Wake-up HTTP
        ↓
Node-RED Render
        ↓
Conexión MQTT
        ↓
Telemetría disponible
```

Beneficios:

- No requiere intervención manual.
- Reduce tiempos de espera.
- Garantiza disponibilidad del SCADA virtual.

---

# 14. Caso de Uso Completo

1. Node-RED genera telemetría.
2. HiveMQ distribuye mensajes.
3. Streamlit recibe datos.
4. Machine Learning genera predicciones.
5. Optimización calcula recomendaciones.
6. Las recomendaciones son enviadas nuevamente a Node-RED.

Resultado:

```text
Node-RED → HiveMQ → Streamlit → ML → HiveMQ → Node-RED
```

Arquitectura Industria 4.0 completamente funcional.

---

# Autor

## Antonio Nicolás Toro González

Maestría en Inteligencia Artificial para la Transformación Digital

Instituto Internacional de Aguascalientes

Ciudad de México, México

GitHub:
https://github.com/antoniot73

Proyecto:
https://github.com/antoniot73/OptiSCADA_ML_Complete
