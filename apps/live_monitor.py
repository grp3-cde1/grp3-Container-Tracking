import json
import paho.mqtt.client as mqtt


# MQTT-Konfiguration festlegen
broker = "fl-17-240.zhdk.cloud.switch.ch"
port = 9001
topic = "migros/grp3/message"

# Temperatur-Grenzwerte festlegen
temp_min = 15
temp_max = 26

# Farben für Terminal festlegen
green = "\033[92m"
red = "\033[91m"
reset = "\033[0m"


# Verbindung zum MQTT-Broker herstellen
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Verbunden mit dem Broker")

        # Topic abonnieren
        client.subscribe(topic)

        print(f"Abonniert: {topic}")
    else:
        print("Verbindung fehlgeschlagen")


# Eingehende MQTT-Nachricht verarbeiten
def on_message(client, userdata, message):
    # Nachricht von Bytes in Text umwandeln
    payload = message.payload.decode()

    # JSON-Text in Dictionary umwandeln
    data = json.loads(payload)

    # Temperatur aus der Nachricht holen
    temperature = data["temperature"]

    # Prüfen, ob Temperatur den Grenzwert verletzt
    if temperature < temp_min or temperature > temp_max:
        print(red + f"{temperature} °C  WARNUNG" + reset)
    else:
        print(green + f"{temperature} °C  OK" + reset)


# MQTT-Client erstellen
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")

# Funktionen für Verbindung und Nachrichten setzen
client.on_connect = on_connect
client.on_message = on_message

# Verbindung starten
print("Verbinde mit Broker")
client.connect(broker, port)

# Endlosschleife für Live-Daten starten
client.loop_forever()

# python simulator/simulator.py simulator/data/luzern-horw.geojson -c simulator/config-switch.ini 