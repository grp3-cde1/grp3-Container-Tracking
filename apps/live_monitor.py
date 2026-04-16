import paho.mqtt.client as mqtt

# Konfiguration
broker = "fl-17-240.zhdk.cloud.switch.ch"
port = 9001
topic = "migros/grp3/message"

# Verbdinung herstellen
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Verbunden mit dem Broker")
        client.subscribe(topic)
        print(f"Abonniert: {topic}")
    else:
        print("Verbindung fehlgeschlagen")

def on_message(client, userdata, message):
    print(f"Nachricht auf: {message.topic}")
    print(message.payload.decode())
    print("-"*40)

# MQTT Client erstellen
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")

client.on_connect = on_connect
client.on_message = on_message

# Verbidnung starten
print("Verbinde mit Broker")
client.connect(broker, port)

client.loop_forever()
