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

# Farbe für Grenzüberschreitungen im Terminal
green = "\033[92m"
red = "\033[91m"
reset = "\033[0m"

# Leeren DataFrame für Live-Daten erstellen
live_data = pd.DataFrame()

def evaluate_measurement(name, value, unit, low=None, high=None):
    """
    Gibt eine farbige Statuszeile für einen Messwert aus.

    Parameter:
        name:  Bezeichnung des Messwerts, z. B. "Temperatur"
        value: gemessener Wert
        unit:  Einheit, z. B. "°C"
        low:   unterer Grenzwert (optional)
        high:  oberer Grenzwert (optional)
    """

    # Prüfen, ob der Wert ausserhalb der Grenzwerte liegt
    too_low = low is not None and value < low
    too_high = high is not None and value > high

    # Passende Meldung ausgeben
    if too_low or too_high:
        print(red + f"WARNUNG: {name} ausserhalb des Bereichs: {value} {unit}" + reset)
    else:
        print(green + f"{name} OK: {value} {unit}" + reset)

# Verbindung zum MQTT-Broker herstellen
def on_connect(client, userdata, flags, rc, properties=None):
    """
    Wird aufgerufen, sobald die Verbindung zum Broker steht.

    Parameter:
        rc: return code; 0 bedeutet erfolgreiche Verbindung
    """
        
    if rc == 0:
        print("Verbunden mit dem Broker")

        # Topic abonnieren
        client.subscribe(topic)

        print(f"Abonniert: {topic}")
    else:
        print("Verbindung fehlgeschlagen")


# Eingehende MQTT-Nachricht verarbeiten
def on_message(client, userdata, message):
    """
    Wird bei jeder eingehenden Nachricht aufgerufen.

    Parameter:
        message: die empfangene MQTT-Nachricht (JSON als Bytes)
    """
        
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

    # Live-Daten im Terminal anzeigen
    print()
    print("Neue Live-Daten:")
    print(last_row)

    # Temperatur aus letzter Zeile holen
    temperature = float(last_row["temp"])

    # Temperatur bewerten
    evaluate_measurement("Temperatur", temperature, "°C", low=temp_min, high=temp_max)

    # Feuchtigkeit bewerten
    if "hum" in live_data.columns:
        humidity = float(last_row["hum"])
        evaluate_measurement("Feuchtigkeit", humidity, "%", high=hum_max)

    # Anzahl empfangener Messpunkte anzeigen
    print(f"Anzahl empfangene Messpunkte: {len(live_data)}")
    print("-" * 40)

def create_client():
    """
    Erstellt einen MQTT-Client und registriert die Callback-Funktionen.

    Rückgabe:
        der vorbereitete MQTT-Client
    """

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")

    # Callback-Funktionen registrieren (ohne Klammern: die Funktion selbst)
    client.on_connect = on_connect
    client.on_message = on_message

    return client

def main():
    """
    Startet den Live-Monitor: Verbindung herstellen und auf Nachrichten warten.
    """

    client = create_client()

    print("Verbinde mit Broker")
    client.connect(broker, port)

    # Endlosschleife für Live-Daten
    client.loop_forever()


# Programm nur starten, wenn diese Datei direkt ausgeführt wird
if __name__ == "__main__":
    main()

# python simulator/simulator.py simulator/data/luzern-horw.geojson -c simulator/config-switch.ini 