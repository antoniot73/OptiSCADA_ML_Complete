"""
Optimización de setpoints.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from src.ml_inference import predict_with_available_models


def recommend_setpoints(row: dict[str, Any], models: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Recomienda setpoints mediante búsqueda de escenarios.

    Args:
        row: Telemetría actual.
        models: Modelos ML disponibles.

    Returns:
        Recomendación optimizada.
    """
    models = models or {}
    best_score = -np.inf
    best_case: dict[str, Any] = {}

    current_energy = max(float(row.get("energy_kwh", 0.001)), 0.001)
    pressure = float(row["pressure_bar"])
    level = float(row["level_pct"])
    vibration = float(row["vibration_mm_s"])

    for temp_sp in np.arange(74, 84, 1):
        for flow_sp in np.arange(40, 56, 2):
            for power_sp in np.arange(55, 81, 5):
                scenario = {
                    **row,
                    "temperature_c": float(temp_sp),
                    "pressure_bar": pressure,
                    "flow_lpm": float(flow_sp),
                    "level_pct": level,
                    "heater_power_pct": float(power_sp),
                    "vibration_mm_s": vibration,
                }

                preds = predict_with_available_models(scenario, models)
                quality = float(preds["ml_quality_prediction"])
                energy = float(preds["ml_energy_prediction"])

                anomaly_penalty = 15 if preds.get("ml_anomaly_flag") == "ANOMALY" else 0
                quality_penalty = 25 if quality < 88 else 0
                safety_penalty = 20 if pressure > 2.8 else 0

                score = (0.60 * quality) - (2.3 * energy) - anomaly_penalty - quality_penalty - safety_penalty

                if score > best_score:
                    best_score = score
                    best_case = {
                        "recommended_temperature_c": round(float(temp_sp), 2),
                        "recommended_flow_lpm": round(float(flow_sp), 2),
                        "recommended_heater_power_pct": round(float(power_sp), 2),
                        "expected_quality_pct": round(float(quality), 2),
                        "expected_energy_kwh": round(float(energy), 2),
                        "expected_anomaly_flag": preds.get("ml_anomaly_flag", "NOT_AVAILABLE"),
                        "score": round(float(score), 2),
                    }

    expected_energy = float(best_case["expected_energy_kwh"])
    saving = ((current_energy - expected_energy) / current_energy) * 100

    best_case["expected_saving_pct"] = round(float(max(0.0, saving)), 2)
    best_case["recommendation"] = (
        f"Ajustar temperatura a {best_case['recommended_temperature_c']} °C, "
        f"flujo a {best_case['recommended_flow_lpm']} L/min y potencia a "
        f"{best_case['recommended_heater_power_pct']} %. "
        f"Calidad esperada: {best_case['expected_quality_pct']} %, "
        f"ahorro estimado: {best_case['expected_saving_pct']} %."
    )

    return best_case
