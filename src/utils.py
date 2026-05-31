"""
Utilidades generales.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st


def configure_logging() -> None:
    """
    Configura logging.

    Returns:
        None.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def initialize_session_state() -> None:
    """
    Inicializa estado de sesión.

    Returns:
        None.
    """
    if "history" not in st.session_state:
        st.session_state.history = pd.DataFrame()
    if "events" not in st.session_state:
        st.session_state.events = []
    if "step" not in st.session_state:
        st.session_state.step = 0


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """
    Convierte DataFrame a bytes CSV.

    Args:
        df: DataFrame.

    Returns:
        CSV en bytes.
    """
    return df.to_csv(index=False).encode("utf-8")


def parse_telemetry_payload(payload: str) -> dict[str, Any]:
    """
    Parsea payload JSON de MQTT.

    Args:
        payload: JSON como texto.

    Returns:
        Telemetría validada.

    Raises:
        ValueError: Si faltan campos.
    """
    data = json.loads(payload)

    required = [
        "temperature_c",
        "pressure_bar",
        "flow_lpm",
        "level_pct",
        "heater_power_pct",
        "vibration_mm_s",
        "energy_kwh",
        "product_quality_pct",
    ]

    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Payload incompleto. Faltan: {missing}")

    data.setdefault("asset_id", "tank01")
    data.setdefault("timestamp", datetime.now().isoformat())

    for key in required:
        data[key] = float(data[key])

    return data
