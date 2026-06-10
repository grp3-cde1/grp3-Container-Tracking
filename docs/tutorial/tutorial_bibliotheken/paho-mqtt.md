# Paho-MQTT – Live-Daten empfangen

`paho-mqtt` ist die Bibliothek, mit der der **Live-Monitor** Live-Daten empfängt. MQTT ist ein Protokoll für Nachrichten, das nach dem **Publish/Subscribe**-Prinzip arbeitet.

```python
import paho.mqtt.client as mqtt
```

Bezug zum Code: `apps/live_monitor.py`.

---

## 1. Die Idee: Publish / Subscribe

```text
Sensor / Simulator  → veröffentlicht (publish) Nachrichten zu einem Topic
Live-Monitor        → abonniert (subscribe) dieses Topic und empfängt sie
Broker              → vermittelt dazwischen
```

Im Projekt:

```python
broker = "fl-17-240.zhdk.cloud.switch.ch"
port = 9001
topic = "migros/grp3/message"
```

---

## 2. Einen Client erstellen

```python
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")
```

`CallbackAPIVersion.VERSION2` gehört zu paho-mqtt 2.x. `transport="websockets"` passt zu Port 9001.

---

## 3. Callback-Funktionen registrieren

MQTT ist ereignisgesteuert. Wir geben dem Client zwei Funktionen, die er bei bestimmten Ereignissen aufruft:

```python
client.on_connect = on_connect    # bei erfolgreicher Verbindung
client.on_message = on_message    # bei jeder neuen Nachricht
```

Beachte: **keine Klammern** – wir übergeben die Funktionen selbst (siehe Funktionen-Tutorial, Abschnitt Callbacks).

---

## 4. `on_connect` – das Topic abonnieren

```python
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Verbunden mit dem Broker")
        client.subscribe(topic)
        print(f"Abonniert: {topic}")
    else:
        print("Verbindung fehlgeschlagen")
```

`rc == 0` heisst „Verbindung erfolgreich". Erst dann abonnieren wir mit `client.subscribe(topic)`.

---

## 5. `on_message` – eine Nachricht verarbeiten

```python
def on_message(client, userdata, message):
    payload = message.payload.decode()      # Bytes → Text
    data = json.loads(payload)              # Text → Dictionary
    ...
```

Die Nachrichten kommen als JSON:

```json
{"timestamp": "...", "lat": 47.0, "lon": 8.25, "temp": 24, "hum": 72}
```

---

## 6. Verbinden und auf Nachrichten warten

```python
client.connect(broker, port)
client.loop_forever()
```

`loop_forever()` hält das Programm offen und ruft `on_message` bei jeder eingehenden Nachricht auf.

---

## Zusammenfassung

```text
mqtt.Client(...)        → Client erstellen
client.on_connect = ... → Callback für Verbindung
client.on_message = ... → Callback für Nachrichten
client.subscribe(topic) → Topic abonnieren
client.connect(...)     → mit Broker verbinden
client.loop_forever()   → auf Nachrichten warten
```