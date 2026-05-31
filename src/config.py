"""
Configuración MQTT.
"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass
class MQTTConfig:
    """
    Configuración del broker MQTT.
    """

    host: str
    port: int
    username: str
    password: str

    def is_configured(self) -> bool:
        """
        Valida si la configuración mínima está disponible.

        Returns:
            True si hay host, usuario y contraseña.
        """
        return bool(self.host and self.username and self.password)


@dataclass
class MQTTTopics:
    """
    Tópicos MQTT usados por la demo.
    """

    telemetry: str = "factory/demo/tank01/telemetry"
    prediction: str = "factory/demo/tank01/prediction"
    recommendation: str = "factory/demo/tank01/recommendation"
    alarm: str = "factory/demo/tank01/alarm"


def get_mqtt_config() -> MQTTConfig:
    """
    Lee credenciales desde Streamlit secrets.

    Returns:
        Configuración MQTT.
    """
    return MQTTConfig(
        host=str(st.secrets.get("MQTT_HOST", "")),
        port=int(st.secrets.get("MQTT_PORT", 8883)),
        username=str(st.secrets.get("MQTT_USERNAME", "")),
        password=str(st.secrets.get("MQTT_PASSWORD", "")),
    )
