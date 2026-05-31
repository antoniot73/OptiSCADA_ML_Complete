"""
Alarmas inteligentes.
"""

from __future__ import annotations

from typing import Any


def evaluate_alarms(
    row: dict[str, Any],
    predictions: dict[str, Any] | None = None,
) -> tuple[str, list[str]]:
    """
    Evalúa alarmas por reglas y ML.

    Args:
        row: Telemetría.
        predictions: Predicciones ML.

    Returns:
        Estado y alarmas.
    """
    predictions = predictions or {}
    alarms: list[str] = []
    status = "NORMAL"

    temperature = float(row["temperature_c"])
    pressure = float(row["pressure_bar"])
    flow = float(row["flow_lpm"])
    vibration = float(row["vibration_mm_s"])
    quality = float(row["product_quality_pct"])

    if temperature > 90:
        alarms.append("Temperatura crítica")
    elif temperature > 85:
        alarms.append("Temperatura alta")

    if pressure > 2.8:
        alarms.append("Sobrepresión crítica")
    elif pressure > 2.5:
        alarms.append("Presión elevada")

    if flow < 32:
        alarms.append("Flujo críticamente bajo")
    elif flow < 38:
        alarms.append("Flujo bajo")

    if vibration > 4.0:
        alarms.append("Vibración crítica")
    elif vibration > 2.8:
        alarms.append("Vibración elevada")

    if quality < 85:
        alarms.append("Calidad estimada baja")

    if predictions.get("ml_quality_prediction") is not None and float(predictions["ml_quality_prediction"]) < 85:
        alarms.append("ML predice baja calidad")

    if predictions.get("ml_anomaly_flag") == "ANOMALY":
        alarms.append("ML detecta anomalía")

    if any("crítica" in alarm.lower() or "críticamente" in alarm.lower() for alarm in alarms):
        status = "CRITICAL"
    elif alarms:
        status = "WARNING"

    return status, alarms
