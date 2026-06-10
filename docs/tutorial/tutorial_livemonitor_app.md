# Tutorial: Funktionsbasierte Monitor-App

## Ziel des Tutorials

In diesem Tutorial bauen wir den **Live-Monitor** für Container-Tracking.

Er überwacht einen laufenden Containertransport in Echtzeit: Er empfängt Messpunkte über MQTT und zeigt sie im Terminal an, mit einer Warnung, wenn die Temperatur ausserhalb des erlaubten Bereichs liegt.

Der Schwerpunkt liegt auf einem zentralen Konzept: **Funktionen** und der **prozeduralen Programmierung**. Wir lernen nicht nur, wie man Funktionen schreibt, sondern auch, warum sie existieren und wie sie in einem ereignisgesteuerten Programm zusammenspielen.

Am Ende kannst du:
- erklären, was eine Funktion ist und wie man sie definiert und aufruft
- Parameter und Rückgabewerte einsetzen
- den Unterschied zwischen lokalen und globalen Variablen (Scope) beschreiben
- verstehen, was Callback-Funktionen sind
- den Aufbau einer ereignisgesteuerten, prozeduralen App nachvollziehen

Die zugehörige Datei ist:

```text
apps/live_monitor.py
```

---

## 1. Was bauen wir?

Bei einem laufenden Transport sendet ein Sensor regelmässig Messpunkte. Jeder Messpunkt ist eine kleine JSON-Nachricht, zum Beispiel:

```json
{"timestamp": "2026-06-05 13:57:46", "lat": 47.0002, "lon": 8.2581, "temp": 24, "hum": 72}
```

Der Live-Monitor empfängt diese Nachrichten über **MQTT**, sammelt sie und prüft jede Temperatur gegen die Grenzwerte:

```python
temp_min = 15
temp_max = 26
hum_max = 72
```

---

## 2. Voraussetzungen

Du solltest bereits diese Grundlagen kennen:

- Variablen und Datentypen
- Listen und Dictionaries
- Bedingungen und Schleifen
- einfache Dateioperationen

Dieses Tutorial baut darauf auf und zeigt, wie man mit Funktionen Programme sauber strukturiert.

---

## 3. Warum Funktionen?

Eine Funktion ist ein benannter Block Code, den man wiederverwenden kann. Sie bündelt eine Aufgabe an einer Stelle.

```python
def say_hello():
    print("Hallo")

say_hello()   # ruft die Funktion auf
```

Wichtig: Die `def`-Zeile **definiert** die Funktion nur. Ausgeführt wird der Code erst beim **Aufruf**.

Der Live-Monitor besteht aus mehreren Funktionen mit je einer klaren Aufgabe:

```text
evaluate_measurement(...)  → einen Messwert bewerten und farbig ausgeben
on_connect(...)            → reagiert, sobald die Verbindung steht
on_message(...)            → reagiert auf jede neue Nachricht
create_client(...)         → erstellt den MQTT-Client
main()                     → startet das Programm
```

---

## 4. Das EVA-Prinzip

Jede gut geschriebene Funktion folgt einem einfachen Schema:

```
Eingabe → Verarbeitung → Ausgabe
```

Das nennt man das **EVA-Prinzip**.

Bei `on_message` ist das gut sichtbar:
- **Eingabe:** die empfangene Nachricht (`message`)
- **Verarbeitung:** JSON auslesen, Temperatur prüfen
- **Ausgabe:** Anzeige im Terminal

Bevor du eine Funktion schreibst, stelle dir immer diese drei Fragen:

1. **Was bekommt die Funktion?** (Eingabe / Parameter)
2. **Was macht die Funktion damit?** (Verarbeitung)
3. **Was gibt die Funktion zurück?** (Ausgabe / Rückgabewert)

Dieses Denkmuster hilft dir, Funktionen sauber zu planen, bevor du überhaupt Code schreibst.

---

## 5. Funktionen definieren und aufrufen

Eine Funktion wird mit `def` definiert. Der Code darin ist eingerückt.

```python
def say_hello():
    print("Hallo")
```

Aufgerufen wird sie so:

```python
say_hello()
```

Wichtig: Die Funktion wird erst ausgeführt, wenn sie aufgerufen wird. Die `def`-Zeile alleine tut noch nichts.

---

## 6. Parameter: Informationen an eine Funktion übergeben

Funktionen können Werte von aussen erhalten. Diese Werte heissen **Parameter**.

```python
def greet(name):
    print(f"Hallo {name}")

greet("Lena")   # Ausgabe: Hallo Lena
```

Im Live-Monitor bekommt `on_connect` mehrere Parameter von der MQTT-Bibliothek übergeben:

```python
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Verbunden mit dem Broker")
        client.subscribe(topic)
        print(f"Abonniert: {topic}")
    else:
        print("Verbindung fehlgeschlagen")
```

Der wichtigste Parameter ist `rc` (return code). `rc == 0` bedeutet „Verbindung erfolgreich". Der Parameter `client` ist das MQTT-Objekt; darüber abonnieren wir mit `client.subscribe(topic)` das Topic.

---

## 7. Standardwerte für Parameter

Ein Parameter kann einen **Standardwert** haben. Dann ist die Angabe beim Aufruf optional.

Im Live-Monitor nutzen wir das in der Hilfsfunktion `evaluate_measurement`:

```python
def evaluate_measurement(name, value, unit, low=None, high=None):
    too_low = low is not None and value < low
    too_high = high is not None and value > high

    if too_low or too_high:
        print(red + f"WARNUNG: {name} ausserhalb des Bereichs: {value} {unit}" + reset)
    else:
        print(green + f"{name} OK: {value} {unit}" + reset)
```

`low` und `high` haben den Standardwert `None`. Dadurch kann dieselbe Funktion für unterschiedliche Messwerte verwendet werden:

```python
# Temperatur hat einen unteren UND einen oberen Grenzwert
evaluate_measurement("Temperatur", temperature, "°C", low=temp_min, high=temp_max)

# Feuchtigkeit hat nur einen oberen Grenzwert – low bleibt None
evaluate_measurement("Feuchtigkeit", humidity, "%", high=hum_max)
```

Das ist ein zentraler Vorteil von Funktionen mit Standardwerten: **Wiederverwendbarkeit**. Wir schreiben die Grenzwert-Logik nur einmal.

---

## 8. Rückgabewerte mit `return`

`return` beendet eine Funktion und gibt optional einen Wert zurück.

```python
def add_numbers(a, b):
    return a + b

summe = add_numbers(3, 4)   # summe ist 7
```

Im Live-Monitor erstellt `create_client()` den MQTT-Client und **gibt ihn zurück**:

```python
def create_client():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")
    client.on_connect = on_connect
    client.on_message = on_message
    return client
```

Aufruf:

```python
client = create_client()
```

Der zurückgegebene Client wird in der Variablen `client` gespeichert und danach weiterverwendet.

Frühes `return` nutzen wir in `on_message`, um eine Funktion vorzeitig zu beenden.

---

## 9. Callback-Funktionen: Funktionen als Werte

Eine Besonderheit im Live-Monitor: Wir rufen `on_connect` und `on_message` **nicht selbst** auf. Stattdessen geben wir sie dem Client **als Wert**:

```python
client.on_connect = on_connect
client.on_message = on_message
```

Beachte: Hier stehen **keine Klammern** hinter `on_connect`. Wir übergeben die Funktion selbst, nicht ihr Ergebnis. Die Bibliothek ruft sie später automatisch auf, wenn das passende Ereignis eintritt.

Solche Funktionen nennt man **Callback-Funktionen**: „Ruf mich zurück, wenn etwas passiert."

```text
Verbindung steht   → Bibliothek ruft on_connect auf
Nachricht kommt an → Bibliothek ruft on_message auf
```

Das ist **ereignisgesteuerte Programmierung**.

---

## 10. Scope: lokale und globale Variablen

Eine wichtige Frage ist: **Wo ist eine Variable sichtbar?** Das nennt man **Scope**.

**Globale Variablen** stehen ausserhalb von Funktionen und sind überall sichtbar. Im Live-Monitor sind das die Konfigurationswerte:

```python
broker = "fl-17-240.zhdk.cloud.switch.ch"
port = 9001
topic = "migros/grp3/message"
temp_min = 15
temp_max = 26
hum_max = 72
```

Wir sammeln die empfangenen Messpunkte in einem globalen DataFrame:

```python
live_data = pd.DataFrame()
```

Damit `on_message` diese globale Variable **verändern** darf, müssen wir das ausdrücklich erlauben:

```python
def on_message(client, userdata, message):
    global live_data
    ...
    live_data = pd.concat([live_data, new_row], ignore_index=True)
```

Das Schlüsselwort `global` sagt Python: „Verwende die globale Variable `live_data`, nicht eine neue lokale." Ohne `global` würde innerhalb der Funktion eine eigene, lokale Variable entstehen.

> **Faustregel:** Globale Variablen sparsam einsetzen, vor allem für Konstanten. `global` zum Schreiben ist hier nötig, weil die Nachrichten nacheinander eintreffen und sich der Zustand aufbauen muss.

---

## 11. Docstrings: Funktionen dokumentieren

Gute Funktionen enthalten eine kurze Beschreibung – einen **Docstring**.

```python
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
    ...
```

Docstrings werden mit dreifachen Anführungszeichen geschrieben und stehen direkt nach der `def`-Zeile.

Vorteile:

- Andere (und du selbst in drei Monaten) verstehen sofort, was die Funktion macht.
- Entwicklungsumgebungen zeigen Docstrings als Hilfetext an.
- Sie sind die Grundlage für automatisch generierte Dokumentation.

Eine Funktion ohne Docstring ist wie ein Knopf ohne Beschriftung.

---

## 12. Programmstart mit `if __name__ == "__main__"`

Am Ende der Datei steht:

```python
if __name__ == "__main__":
    main()
```

Das bedeutet: Die App startet nur dann, wenn diese Datei **direkt** ausgeführt wird. Nicht, wenn sie von einem anderen Modul importiert wird. So kann man die Funktionen (z. B. `evaluate_measurement`) auch importieren und testen, ohne dass sofort eine Verbindung aufgebaut wird.

---

## 13. Übungsaufgaben

### Aufgabe 1 – Funktion mit Rückgabewert
Schreibe eine Funktion `format_temperature(value)`, die `"22.3 °C"` für die Eingabe `22.3` zurückgibt.

### Aufgabe 2 – Standardwerte verstehen
Erkläre, warum `evaluate_measurement` mit `low=None, high=None` arbeitet. Was passiert beim Aufruf `evaluate_measurement("Feuchtigkeit", 80, "%", high=72)` Schritt für Schritt?

### Aufgabe 3 – Scope
Was gibt dieser Code aus und warum?

```python
x = 10

def change():
    x = 20
    return x

print(change())
print(x)
```

### Aufgabe 4 – Eine weitere Bewertung ergänzen
Die Nachrichten enthalten auch GPS-Koordinaten (`lat`, `lon`). Ergänze `on_message`, sodass zusätzlich die Position des letzten Messpunkts ausgegeben wird. Überlege: Brauchst du dafür `evaluate_measurement` oder eine neue Funktion?

### Aufgabe 5 – Callback verstehen
Erkläre in eigenen Worten, warum bei `client.on_message = on_message` keine Klammern stehen.

---

## 14. Was du gelernt hast

- wie man Funktionen definiert und aufruft
- wie Parameter, Standardwerte und Rückgabewerte funktionieren
- wie eine Funktion durch Standardwerte wiederverwendbar wird (`evaluate_measurement`)
- was lokale und globale Variablen sind und wozu `global` dient
- was Callback-Funktionen sind und wie ereignisgesteuerte Programme arbeiten
- wie ein prozeduraler Ablauf mit `create_client()`, `main()` und `loop_forever()` aufgebaut ist
- wie man JSON-Nachrichten robust mit `try`/`except` verarbeitet

Im nächsten Schritt wechseln wir zur Retrospektive-App und arbeiten mit Bibliotheken und echten Daten.
