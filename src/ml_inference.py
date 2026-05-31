"""
Inferencia ML.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from src.features import row_to_feature_frame
from src.process_models import estimate_energy_consumption, estimate_product_quality


def load_models(model_dir: str = "models") -> dict[str, Any]:
    """
    Carga modelos disponibles.

    Args:
        model_dir: Carpeta de modelos.

    Returns:
        Modelos cargados.
    """
    base = Path(model_dir)
    models: dict[str, Any] = {}

    for name, filename in {
        "quality": "quality_model.joblib",
        "energy": "energy_model.joblib",
        "anomaly": "anomaly_model.joblib",
    }.items():
        path = base / filename
        if path.exists():
            models[name] = joblib.load(path)

    return models


def predict_with_available_models(row: dict[str, Any], models: dict[str, Any]) -> dict[str, Any]:
    """
    Predice usando ML o heurísticas.

    Args:
        row: Telemetría.
        models: Modelos disponibles.

    Returns:
        Predicciones.
    """
    features = row_to_feature_frame(row)
    predictions: dict[str, Any] = {}

    if "quality" in models:
        predictions["ml_quality_prediction"] = float(models["quality"].predict(features)[0])
    else:
        predictions["ml_quality_prediction"] = estimate_product_quality(
            float(row["temperature_c"]),
            float(row["pressure_bar"]),
            float(row["flow_lpm"]),
            float(row["vibration_mm_s"]),
        )

    if "energy" in models:
        predictions["ml_energy_prediction"] = float(models["energy"].predict(features)[0])
    else:
        predictions["ml_energy_prediction"] = estimate_energy_consumption(
            float(row["temperature_c"]),
            float(row["pressure_bar"]),
            float(row["flow_lpm"]),
            float(row["heater_power_pct"]),
        )

    if "anomaly" in models:
        flag = int(models["anomaly"].predict(features)[0])
        predictions["ml_anomaly_flag"] = "ANOMALY" if flag == -1 else "NORMAL"
    else:
        predictions["ml_anomaly_flag"] = "NOT_AVAILABLE"

    return predictions
