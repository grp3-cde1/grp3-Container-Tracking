import json
import pandas as pd
import paho.mqtt.client as mqtt


# MQTT-Konfiguration festlegen
broker = "fl-17-240.zhdk.cloud.switch.ch"
port = 9001
topic = "migros/grp3/message"

# Temperatur-Grenzwerte festlegen
temp_min = 15
temp_max = 26

# Leeren DataFrame für Live-Daten erstellen
live_data = pd.DataFrame()


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
    global live_data

    # Nachricht von Bytes in Text umwandeln
    payload = message.payload.decode()

    try:
        # JSON-Text in Dictionary umwandeln
        data = json.loads(payload)
    except json.JSONDecodeError:
        print("Nachricht ist kein gültiges JSON")
        return

    # Einzelne Nachricht in einen kleinen DataFrame umwandeln
    new_row = pd.DataFrame([data])

    # Neue Zeile an vorhandene Live-Daten anhängen
    live_data = pd.concat([live_data, new_row], ignore_index=True)

    # Letzte Zeile aus dem DataFrame holen
    last_row = live_data.iloc[-1]

    # Prüfen, ob Temperatur vorhanden ist
    if "temp" not in live_data.columns:
        print("Keine Temperatur in den Daten gefunden")
        print(data)
        return

    # Temperatur aus letzter Zeile holen
    temperature = float(last_row["temp"])

    # Live-Daten im Terminal anzeigen
    print()
    print("Neue Live-Daten:")
    print(last_row)

    # Temperatur-Grenzwert prüfen
    if temperature < temp_min or temperature > temp_max:
        print(f"WARNUNG: Temperatur ausserhalb des Bereichs: {temperature} °C")
    else:
        print(f"Temperatur OK: {temperature} °C")

    # Anzahl empfangener Messpunkte anzeigen
    print(f"Anzahl empfangene Messpunkte: {len(live_data)}")
    print("-" * 40)


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