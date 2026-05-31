"""
Simulador SCADA interno.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import numpy as np

from src.process_models import estimate_energy_consumption, estimate_product_quality


def simulate_scada_data(mode: str, step: int) -> dict[str, Any]:
    """
    Simula una lectura de tanque térmico.

    Args:
        mode: Modo operativo.
        step: Paso de simulación.

    Returns:
        Telemetría simulada.
    """
    t = step + 1

    base_temp = 78 + 4 * np.sin(t / 8)
    base_pressure = 2.0 + 0.15 * np.sin(t / 10)
    base_flow = 45 + 3 * np.sin(t / 6)
    base_level = 65 + 5 * np.sin(t / 12)
    base_power = 70 + 6 * np.sin(t / 9)
    base_vibration = 1.5 + 0.2 * np.sin(t / 5)

    if mode == "Alta temperatura":
        base_temp += 14
        base_power += 8
    elif mode == "Bajo flujo":
        base_flow -= 15
        base_pressure += 0.25
    elif mode == "Sobrepresión":
        base_pressure += 1.0
    elif mode == "Alta vibración":
        base_vibration += 3.0
    elif mode == "Baja calidad":
        base_temp += 8
        base_flow -= 8
        base_power += 10

    temperature = float(base_temp + np.random.normal(0, 0.8))
    pressure = float(base_pressure + np.random.normal(0, 0.05))
    flow = float(base_flow + np.random.normal(0, 0.9))
    level = float(base_level + np.random.normal(0, 1.2))
    heater_power = float(np.clip(base_power + np.random.normal(0, 1.5), 0, 100))
    vibration = float(max(0.0, base_vibration + np.random.normal(0, 0.15)))

    energy = estimate_energy_consumption(temperature, pressure, flow, heater_power)
    quality = estimate_product_quality(temperature, pressure, flow, vibration)

    return {
        "timestamp": datetime.now().isoformat(),
        "asset_id": "tank01",
        "temperature_c": round(temperature, 2),
        "pressure_bar": round(pressure, 2),
        "flow_lpm": round(flow, 2),
        "level_pct": round(level, 2),
        "heater_power_pct": round(heater_power, 2),
        "vibration_mm_s": round(vibration, 2),
        "energy_kwh": round(energy, 2),
        "product_quality_pct": round(quality, 2),
    }
