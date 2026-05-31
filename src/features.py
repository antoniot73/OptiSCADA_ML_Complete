"""
Extracción de características ML.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

FEATURE_COLUMNS = [
    "temperature_c",
    "pressure_bar",
    "flow_lpm",
    "level_pct",
    "heater_power_pct",
    "vibration_mm_s",
]


def row_to_feature_frame(row: dict[str, Any]) -> pd.DataFrame:
    """
    Convierte una lectura en DataFrame ML.

    Args:
        row: Telemetría.

    Returns:
        DataFrame de una fila.
    """
    return pd.DataFrame({col: [float(row[col])] for col in FEATURE_COLUMNS})


def validate_training_dataframe(df: pd.DataFrame) -> None:
    """
    Valida columnas de entrenamiento.

    Args:
        df: Dataset.

    Raises:
        ValueError: Si faltan columnas.
    """
    required = FEATURE_COLUMNS + ["energy_kwh", "product_quality_pct"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")
