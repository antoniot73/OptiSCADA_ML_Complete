"""
OptiSCADA-ML Complete.

Demo completa para:
- Streamlit Community Cloud
- SCADA virtual con simulador interno
- MQTT Cloud opcional con HiveMQ
- Node-RED como SCADA virtual externo
- Machine Learning
- Optimización de proceso
- Publicación de recomendaciones MQTT
"""

from __future__ import annotations

import json
import logging
from typing import Any

import requests
import pandas as pd
import plotly.express as px
import streamlit as st

from src.alarms import evaluate_alarms
from src.config import MQTTTopics, get_mqtt_config
from src.ml_inference import load_models, predict_with_available_models
from src.ml_training import train_models_from_csv
from src.mqtt_client import MQTTClientManager
from src.optimizer import recommend_setpoints
from src.simulator import simulate_scada_data
from src.utils import (
    configure_logging,
    dataframe_to_csv_bytes,
    initialize_session_state,
    parse_telemetry_payload,
)

NODE_RED_WAKE_URL = "https://processmind-scada-ml.onrender.com/"


def wake_node_red_service(url: str = NODE_RED_WAKE_URL, timeout_seconds: int = 8) -> bool:
    """
    Despierta el servicio Node-RED desplegado en Render mediante una solicitud HTTP.

    Args:
        url: URL pública del servicio Node-RED.
        timeout_seconds: Tiempo máximo de espera de la solicitud.

    Returns:
        True si Node-RED responde con código HTTP menor a 500; False en caso contrario.
    """
    try:
        response = requests.get(url, timeout=timeout_seconds)
        if response.status_code < 500:
            logging.info("Node-RED activo. Código HTTP: %s", response.status_code)
            return True

        logging.warning("Node-RED respondió con error HTTP: %s", response.status_code)
        return False

    except requests.RequestException as exc:
        logging.warning("Node-RED aún no respondió: %s", exc)
        return False


def render_node_red_wakeup_status() -> None:
    """
    Ejecuta una verificación ligera para despertar Node-RED en Render y muestra el estado.

    Returns:
        None.
    """
    if st.session_state.get("node_red_wakeup_checked", False):
        return

    with st.spinner("Despertando Node-RED en Render..."):
        is_awake = wake_node_red_service()

    st.session_state.node_red_wakeup_checked = True
    st.session_state.node_red_is_awake = is_awake

    if is_awake:
        st.success("Node-RED está activo.")
    else:
        st.warning("Node-RED aún está iniciando. Si estaba dormido, puede tardar 30-60 segundos.")



def render_header() -> None:
    """
    Configura la página y muestra el encabezado principal.

    Returns:
        None.
    """
    st.set_page_config(
        page_title="OptiSCADA-ML",
        page_icon="🏭",
        layout="wide",
    )
    st.title("🏭 OptiSCADA-ML Complete")
    st.caption("SCADA virtual + MQTT Cloud + ML + optimización de procesos.")


def render_sidebar() -> dict[str, Any]:
    """
    Renderiza la barra lateral.

    Returns:
        Configuración seleccionada por el usuario.
    """
    st.sidebar.header("Configuración")

    source_mode = st.sidebar.radio(
        "Fuente de telemetría",
        ["Simulador interno", "MQTT Cloud"],
        index=0,
    )

    simulation_mode = st.sidebar.selectbox(
        "Modo simulado",
        [
            "Normal",
            "Alta temperatura",
            "Bajo flujo",
            "Sobrepresión",
            "Alta vibración",
            "Baja calidad",
        ],
    )

    auto_mode = st.sidebar.checkbox("Auto-generar lectura por recarga", value=False)
    manual_reading = st.sidebar.button("Generar lectura", type="primary")
    reset = st.sidebar.button("Reiniciar sesión")

    st.sidebar.markdown("---")
    st.sidebar.code("Node-RED → HiveMQ → Streamlit → ML → MQTT", language="text")

    return {
        "source_mode": source_mode,
        "simulation_mode": simulation_mode,
        "auto_mode": auto_mode,
        "manual_reading": manual_reading,
        "reset": reset,
    }


def append_history(row: dict[str, Any]) -> None:
    """
    Agrega una lectura al histórico.

    Args:
        row: Registro enriquecido.

    Returns:
        None.
    """
    new_row = pd.DataFrame([row])
    if st.session_state.history.empty:
        st.session_state.history = new_row
    else:
        st.session_state.history = pd.concat(
            [st.session_state.history, new_row],
            ignore_index=True,
        )
    st.session_state.history = st.session_state.history.tail(500)


def append_events(status: str, alarms: list[str], row: dict[str, Any]) -> None:
    """
    Agrega alarmas a la bitácora.

    Args:
        status: Estado operativo.
        alarms: Alarmas activas.
        row: Registro actual.

    Returns:
        None.
    """
    if status == "NORMAL":
        return

    for alarm in alarms:
        st.session_state.events.append(
            {
                "timestamp": row["timestamp"],
                "asset_id": row["asset_id"],
                "status": status,
                "alarm": alarm,
            }
        )

    st.session_state.events = st.session_state.events[-250:]


def process_telemetry_row(row: dict[str, Any]) -> None:
    """
    Procesa una lectura: ML, alarmas, histórico y bitácora.

    Args:
        row: Lectura de telemetría.

    Returns:
        None.
    """
    models = load_models()
    predictions = predict_with_available_models(row=row, models=models)
    status, alarms = evaluate_alarms(row=row, predictions=predictions)

    row["status"] = status
    row["alarms"] = ", ".join(alarms) if alarms else "None"

    for key, value in predictions.items():
        row[key] = value

    append_history(row)
    append_events(status, alarms, row)


def process_simulated_reading(mode: str) -> None:
    """
    Genera una lectura desde el simulador interno.

    Args:
        mode: Modo de simulación.

    Returns:
        None.
    """
    row = simulate_scada_data(mode=mode, step=st.session_state.step)
    st.session_state.step += 1
    process_telemetry_row(row)


def render_mqtt_panel(key_suffix: str = "main") -> None:
    """
    Renderiza panel MQTT.

    Returns:
        None.
    """
    st.subheader("📡 MQTT Cloud")

    cfg = get_mqtt_config()
    topics = MQTTTopics()

    c1, c2, c3 = st.columns(3)
    c1.write(f"**Host:** `{cfg.host or 'no configurado'}`")
    c2.write(f"**Puerto:** `{cfg.port}`")
    c3.write(f"**Telemetría:** `{topics.telemetry}`")

    if not cfg.is_configured():
        st.warning("MQTT no está configurado. Usa `.streamlit/secrets.toml` o Streamlit Secrets.")
        st.code(
            'MQTT_HOST = "xxxxx.s1.eu.hivemq.cloud"\n'
            'MQTT_PORT = 8883\n'
            'MQTT_USERNAME = "usuario"\n'
            'MQTT_PASSWORD = "password"\n'
            'MQTT_TOPIC_TELEMETRY = "factory/demo/tank01/telemetry"\n'
            'MQTT_TOPIC_RECOMMENDATION = "factory/demo/tank01/recommendation"',
            language="toml",
        )
        return

    if st.button("Leer un mensaje MQTT", key=f"btn_read_single_mqtt_message_{key_suffix}"):
        try:
            manager = MQTTClientManager(config=cfg)
            payload = manager.read_single_message(topic=topics.telemetry, timeout_seconds=8)

            if payload is None:
                st.warning("No llegó ningún mensaje MQTT.")
                return

            row = parse_telemetry_payload(payload)
            process_telemetry_row(row)
            st.success("Mensaje MQTT recibido y procesado.")
            st.json(row)

        except Exception as exc:
            logging.exception("Error MQTT: %s", exc)
            st.error(f"Error MQTT: {exc}")


def publish_recommendation(row: dict[str, Any], recommendation: dict[str, Any]) -> None:
    """
    Publica una recomendación al tópico MQTT configurado.

    Args:
        row: Última lectura.
        recommendation: Recomendación calculada.

    Returns:
        None.
    """
    cfg = get_mqtt_config()
    topics = MQTTTopics()

    if not cfg.is_configured():
        st.info("Configura MQTT para publicar recomendaciones hacia Node-RED.")
        return

    if st.button("Publicar recomendación por MQTT"):
        try:
            payload = {
                "asset_id": row.get("asset_id", "tank01"),
                "timestamp": row.get("timestamp"),
                "recommendation": recommendation,
            }
            manager = MQTTClientManager(config=cfg)
            manager.publish_message(topics.recommendation, json.dumps(payload))
            st.success(f"Recomendación publicada en `{topics.recommendation}`.")
        except Exception as exc:
            logging.exception("Error publicando MQTT: %s", exc)
            st.error(f"No fue posible publicar: {exc}")


def render_hmi(row: dict[str, Any]) -> None:
    """
    Renderiza HMI principal.

    Args:
        row: Última lectura.

    Returns:
        None.
    """
    st.subheader("🖥️ HMI del tanque térmico")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Estado", row.get("status", "-"))
    c2.metric("Temperatura °C", row.get("temperature_c", "-"))
    c3.metric("Presión bar", row.get("pressure_bar", "-"))
    c4.metric("Calidad %", row.get("product_quality_pct", "-"))

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Flujo L/min", row.get("flow_lpm", "-"))
    c6.metric("Nivel %", row.get("level_pct", "-"))
    c7.metric("Potencia %", row.get("heater_power_pct", "-"))
    c8.metric("Energía kWh", row.get("energy_kwh", "-"))

    st.subheader("🚨 Alarmas")
    status = row.get("status", "NORMAL")
    alarms = row.get("alarms", "None")

    if status == "NORMAL":
        st.success("Sistema en operación normal.")
    elif status == "WARNING":
        st.warning(f"Advertencias: {alarms}")
    else:
        st.error(f"Alarmas críticas: {alarms}")

    st.subheader("🧠 Predicción ML")
    m1, m2, m3 = st.columns(3)
    m1.metric("Calidad ML %", round(float(row.get("ml_quality_prediction", 0)), 2))
    m2.metric("Energía ML kWh", round(float(row.get("ml_energy_prediction", 0)), 2))
    m3.metric("Anomalía ML", row.get("ml_anomaly_flag", "NOT_AVAILABLE"))


def render_trends() -> None:
    """
    Renderiza tendencias.

    Returns:
        None.
    """
    st.subheader("📈 Tendencias")

    df = st.session_state.history.copy()
    if df.empty or len(df) < 2:
        st.info("Genera al menos dos lecturas.")
        return

    variables = [
        "temperature_c",
        "pressure_bar",
        "flow_lpm",
        "level_pct",
        "heater_power_pct",
        "vibration_mm_s",
        "energy_kwh",
        "product_quality_pct",
    ]

    available = [v for v in variables if v in df.columns]
    selected = st.multiselect(
        "Variables",
        available,
        default=[v for v in ["temperature_c", "energy_kwh", "product_quality_pct"] if v in available],
    )

    if selected:
        plot_df = df[["timestamp"] + selected].melt(
            id_vars="timestamp",
            var_name="variable",
            value_name="value",
        )
        fig = px.line(
            plot_df,
            x="timestamp",
            y="value",
            color="variable",
            markers=True,
            title="Tendencias del proceso",
        )
        st.plotly_chart(fig, use_container_width=True)


def render_optimizer(row: dict[str, Any]) -> None:
    """
    Renderiza optimización.

    Args:
        row: Última lectura.

    Returns:
        None.
    """
    st.subheader("🤖 Optimización de proceso")

    models = load_models()
    recommendation = recommend_setpoints(row=row, models=models)

    st.write(recommendation.get("recommendation", "Sin recomendación."))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temp. recomendada °C", recommendation.get("recommended_temperature_c", "-"))
    c2.metric("Flujo recomendado", recommendation.get("recommended_flow_lpm", "-"))
    c3.metric("Potencia recomendada %", recommendation.get("recommended_heater_power_pct", "-"))
    c4.metric("Ahorro estimado %", recommendation.get("expected_saving_pct", "-"))

    with st.expander("Detalle JSON"):
        st.json(recommendation)

    publish_recommendation(row, recommendation)


def render_training_panel() -> None:
    """
    Renderiza entrenamiento ML.

    Returns:
        None.
    """
    st.subheader("🧠 Entrenamiento Machine Learning")

    st.write("Entrena modelos con el dataset incluido o sube un CSV compatible.")

    uploaded = st.file_uploader("Subir dataset CSV", type=["csv"])
    use_default = st.checkbox("Usar dataset sintético incluido", value=True)

    if st.button("Entrenar modelos"):
        try:
            if uploaded is not None:
                df = pd.read_csv(uploaded)
            elif use_default:
                df = pd.read_csv("data/synthetic_training_data.csv")
            else:
                st.error("Selecciona un dataset.")
                return

            report = train_models_from_csv(df=df, output_dir="models")
            st.success("Modelos entrenados correctamente.")
            st.json(report)

        except Exception as exc:
            logging.exception("Error entrenando modelos: %s", exc)
            st.error(f"No fue posible entrenar: {exc}")


def render_tables() -> None:
    """
    Renderiza tablas.

    Returns:
        None.
    """
    st.subheader("📋 Histórico")

    if st.session_state.history.empty:
        st.info("No hay histórico.")
    else:
        df = st.session_state.history.sort_values("timestamp", ascending=False)
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "Descargar histórico CSV",
            data=dataframe_to_csv_bytes(df),
            file_name="optiscada_history.csv",
            mime="text/csv",
        )

    st.subheader("🧾 Bitácora")

    if st.session_state.events:
        events = pd.DataFrame(st.session_state.events).sort_values("timestamp", ascending=False)
        st.dataframe(events, use_container_width=True)
        st.download_button(
            "Descargar eventos CSV",
            data=dataframe_to_csv_bytes(events),
            file_name="optiscada_events.csv",
            mime="text/csv",
        )
    else:
        st.info("Sin eventos registrados.")


def main() -> None:
    """
    Punto de entrada principal.

    Returns:
        None.
    """
    configure_logging()
    initialize_session_state()
    render_header()
    render_node_red_wakeup_status()

    settings = render_sidebar()

    if settings["reset"]:
        st.session_state.history = pd.DataFrame()
        st.session_state.events = []
        st.session_state.step = 0
        st.success("Sesión reiniciada.")

    if settings["source_mode"] == "Simulador interno":
        if settings["manual_reading"] or settings["auto_mode"] or st.session_state.history.empty:
            process_simulated_reading(settings["simulation_mode"])
            if settings["auto_mode"]:
                st.rerun()
    else:
        render_mqtt_panel(key_suffix="source")
        if st.session_state.history.empty:
            st.info("Conecta MQTT o usa simulador interno.")
            return

    latest = st.session_state.history.iloc[-1].to_dict()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["HMI", "Tendencias", "Optimización", "Machine Learning", "Datos", "MQTT"]
    )

    with tab1:
        render_hmi(latest)
    with tab2:
        render_trends()
    with tab3:
        render_optimizer(latest)
    with tab4:
        render_training_panel()
    with tab5:
        render_tables()
    with tab6:
        render_mqtt_panel(key_suffix="tab")


if __name__ == "__main__":
    main()
