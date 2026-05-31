# OptiSCADA-ML Complete

Proyecto demo completo para Streamlit Community Cloud:

- SCADA virtual
- MQTT Cloud con HiveMQ
- Node-RED como simulador SCADA/PLC
- HMI web
- Machine Learning para calidad, energía y anomalías
- Optimización de setpoints
- Publicación de recomendaciones por MQTT

## Arquitectura

```text
Node-RED Cloud / local
SCADA virtual
        ↓ MQTT
HiveMQ Cloud
Broker MQTT
        ↓ MQTT TLS
Streamlit Community Cloud
HMI + ML + Optimización + Alarmas
        ↓ MQTT
Node-RED recibe recomendaciones
```

## Ejecutar localmente

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Configuración MQTT

Copia `.streamlit/secrets.example.toml` como `.streamlit/secrets.toml` y coloca tus credenciales.

## Node-RED

Importa:

```text
node_red/optiscada_node_red_flow.json
```

Después configura el nodo de broker MQTT con tu host, usuario, contraseña y TLS.

## Uso recomendado

1. Ejecuta en modo simulador interno.
2. Entra a la pestaña Machine Learning.
3. Entrena modelos con el dataset incluido.
4. Prueba la optimización.
5. Configura HiveMQ.
6. Importa el flujo Node-RED.
7. Cambia a MQTT Cloud.
8. Publica recomendaciones y verifica que Node-RED las reciba.
