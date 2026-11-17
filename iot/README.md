# IoT integration status

The source review package did not contain ESP32 firmware, sensor pin assignments,
or an HTTP/MQTT/serial payload contract. Live sensor ingestion is intentionally
not fabricated. Before implementing the connector, document:

- ESP32 board and firmware version
- Ultrasonic sensor model and trigger/echo GPIO pins
- Bin/device identifier
- Transport: HTTP POST, MQTT topic, or serial
- Sample payload and authentication method

Never commit Wi-Fi passwords or broker credentials.
