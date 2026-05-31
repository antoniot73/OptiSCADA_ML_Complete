"""
Modelos sintéticos del proceso.
"""

from __future__ import annotations

import numpy as np


def estimate_energy_consumption(
    temperature_c: float,
    pressure_bar: float,
    flow_lpm: float,
    heater_power_pct: float,
) -> float:
    """
    Estima consumo energético.

    Args:
        temperature_c: Temperatura.
        pressure_bar: Presión.
        flow_lpm: Flujo.
        heater_power_pct: Potencia.

    Returns:
        kWh estimado.
    """
    energy = 4.0 + 0.08 * heater_power_pct + 0.03 * temperature_c + 0.60 * pressure_bar - 0.015 * flow_lpm
    return float(max(0.0, energy))


def estimate_product_quality(
    temperature_c: float,
    pressure_bar: float,
    flow_lpm: float,
    vibration_mm_s: float,
) -> float:
    """
    Estima calidad del producto.

    Args:
        temperature_c: Temperatura.
        pressure_bar: Presión.
        flow_lpm: Flujo.
        vibration_mm_s: Vibración.

    Returns:
        Calidad de 0 a 100.
    """
    quality = (
        96
        - abs(temperature_c - 78) * 0.75
        - abs(pressure_bar - 2.0) * 5.0
        - abs(flow_lpm - 45) * 0.25
        - max(0.0, vibration_mm_s - 2.0) * 4.0
    )
    return float(np.clip(quality, 0, 100))
