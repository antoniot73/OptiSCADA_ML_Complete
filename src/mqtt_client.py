"""
Cliente MQTT con TLS para HiveMQ Cloud.
"""

from __future__ import annotations

import ssl
import time
from dataclasses import dataclass
from typing import Optional

import paho.mqtt.client as mqtt

from src.config import MQTTConfig


@dataclass
class MQTTClientManager:
    """
    Gestor MQTT.
    """

    config: MQTTConfig

    def _create_client(self) -> mqtt.Client:
        """
        Crea cliente MQTT TLS.

        Returns:
            Cliente MQTT.
        """
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(self.config.username, self.config.password)
        client.tls_set(cert_reqs=ssl.CERT_REQUIRED)
        client.tls_insecure_set(False)
        return client

    def read_single_message(self, topic: str, timeout_seconds: int = 8) -> Optional[str]:
        """
        Lee un mensaje MQTT.

        Args:
            topic: Tópico.
            timeout_seconds: Tiempo máximo.

        Returns:
            Payload o None.
        """
        received: dict[str, str | None] = {"payload": None}

        def on_connect(client: mqtt.Client, userdata: object, flags: object, reason_code: object, properties: object = None) -> None:
            client.subscribe(topic)

        def on_message(client: mqtt.Client, userdata: object, msg: mqtt.MQTTMessage) -> None:
            received["payload"] = msg.payload.decode("utf-8")
            client.disconnect()

        client = self._create_client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(self.config.host, self.config.port, keepalive=30)
        client.loop_start()

        start = time.time()
        while received["payload"] is None and (time.time() - start) < timeout_seconds:
            time.sleep(0.2)

        client.loop_stop()
        try:
            client.disconnect()
        except Exception:
            pass

        return received["payload"]

    def publish_message(self, topic: str, payload: str) -> None:
        """
        Publica un mensaje MQTT.

        Args:
            topic: Tópico.
            payload: JSON texto.

        Returns:
            None.
        """
        client = self._create_client()
        client.connect(self.config.host, self.config.port, keepalive=30)
        client.loop_start()
        result = client.publish(topic, payload=payload, qos=1)
        result.wait_for_publish(timeout=5)
        client.loop_stop()
        client.disconnect()
