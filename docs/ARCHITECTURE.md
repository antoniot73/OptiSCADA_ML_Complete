# Arquitectura

```text
┌────────────────────────────┐
│ Node-RED                   │
│ SCADA virtual / PLC demo   │
└──────────────┬─────────────┘
               │ MQTT JSON
               ▼
┌────────────────────────────┐
│ HiveMQ Cloud               │
│ Broker MQTT TLS            │
└──────────────┬─────────────┘
               │ MQTT TLS
               ▼
┌────────────────────────────┐
│ Streamlit Community Cloud  │
│ HMI + ML + Optimización    │
└──────────────┬─────────────┘
               │ MQTT recommendation
               ▼
┌────────────────────────────┐
│ Node-RED                   │
│ Visualiza recomendación    │
└────────────────────────────┘
```
