from pathlib import Path

p = Path("app.py")
s = p.read_text(encoding="utf-8")

s = s.replace(
    "def render_mqtt_panel() -> None:",
    'def render_mqtt_panel(key_suffix: str = "main") -> None:'
)

s = s.replace(
    'key="btn_read_single_mqtt_message"',
    'key=f"btn_read_single_mqtt_message_{key_suffix}"'
)

s = s.replace(
    "render_mqtt_panel()\n        if st.session_state.history.empty:",
    'render_mqtt_panel(key_suffix="source")\n        if st.session_state.history.empty:'
)

s = s.replace(
    "render_mqtt_panel()\n\n\nif __name__ == \"__main__\":",
    'render_mqtt_panel(key_suffix="tab")\n\n\nif __name__ == "__main__":'
)

p.write_text(s, encoding="utf-8")
print("app.py corregido")
