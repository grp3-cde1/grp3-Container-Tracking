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

Im Live-Monitor gibt es zwei zentrale Funktionen:

- `on_connect(...)` – wird ausgeführt, sobald die Verbindung zum Broker steht
- `on_message(...)` – wird ausgeführt, sobald eine neue Nachricht ankommt

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

Der Parameter `properties=None` hat einen **Standardwert**. Dadurch ist die Angabe beim Aufruf optional.

---

## 7. Callback-Funktionen: Funktionen als Werte

Eine Besonderheit im Live-Monitor: Wir rufen `on_connect` und `on_message` **nicht selbst** auf. Stattdessen geben wir sie der MQTT-Bibliothek **als Wert**:

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

## 8. Scope: lokale und globale Variablen

Eine wichtige Frage ist: **Wo ist eine Variable sichtbar?** Das nennt man **Scope**.

**Globale Variablen** stehen ausserhalb von Funktionen und sind überall sichtbar. Im Live-Monitor sind das die Konfigurationswerte:

```python
broker = "fl-17-240.zhdk.cloud.switch.ch"
port = 9001
topic = "migros/grp3/message"
temp_min = 15
temp_max = 26
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

## 9. Die Funktion `on_message` Schritt für Schritt

```python
def on_message(client, userdata, message):
    global live_data

    # 1. Nachricht von Bytes in Text umwandeln
    payload = message.payload.decode()

    # 2. JSON-Text in ein Dictionary umwandeln
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print("Nachricht ist kein gültiges JSON")
        return

    # 3. Nachricht als neue Zeile anhängen
    new_row = pd.DataFrame([data])
    live_data = pd.concat([live_data, new_row], ignore_index=True)

    # 4. Letzte Zeile holen
    last_row = live_data.iloc[-1]

    # 5. Prüfen, ob eine Temperatur enthalten ist
    if "temp" not in live_data.columns:
        print("Keine Temperatur in den Daten gefunden")
        print(data)
        return

    # 6. Temperatur bewerten
    temperature = float(last_row["temp"])
    ...
```

Drei Konzepte werden hier sichtbar:

- **`try`/`except`:** Falls die Nachricht kein gültiges JSON ist, fängt `except json.JSONDecodeError` den Fehler ab, statt das Programm abstürzen zu lassen.
- **Frühes `return`:** Ist die Nachricht ungültig oder fehlt die Temperatur, beendet `return` die Funktion sofort. Der Rest wird übersprungen.
- **f-Strings:** Für lesbare Ausgaben, z. B. `f"Anzahl empfangene Messpunkte: {len(live_data)}"`.

---

## 10. Rückgabewerte mit `return`

`return` beendet eine Funktion und gibt optional einen Wert zurück.

```python
def add_numbers(a, b):
    return a + b

summe = add_numbers(3, 4)   # summe ist 7
```

Im Live-Monitor nutzen wir `return` vor allem zum **frühzeitigen Beenden** (siehe oben). Die Callback-Funktionen geben keinen Wert an uns zurück – sie informieren über Ereignisse und geben etwas aus.

---

## 10. Docstrings: Funktionen dokumentieren

Gute Funktionen enthalten eine kurze Beschreibung – einen **Docstring**.

```python
def calculate_violations(data_frame):
    """
    Prüft Messwerte auf Grenzwertverletzungen.

    Parameter:
        data_frame: pandas DataFrame mit Spalten temperature und humidity

    Rückgabe:
        DataFrame mit zusätzlichen Boolean-Spalten für Verletzungen
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

## 11. Funktionen rufen Funktionen auf

Eine Funktion kann andere Funktionen aufrufen. Das ist ein zentrales Muster in grösseren Programmen.

```python
def main():
    containers = fetch_containers()       # ruft fetch_containers auf
    container = choose_item("Container", containers)  # ruft choose_item auf

    routes = fetch_routes(container)      # ruft fetch_routes auf
    route = choose_item("Routen", routes) # choose_item wird wiederverwendet!
```

`main()` ist hier die **übergeordnete Funktion**, die andere Funktionen koordiniert. Sie selbst enthält kaum Logik – sie delegiert Aufgaben.

Das ist wie ein Dirigent: Er spielt kein Instrument selbst, aber er weiss, wer was wann spielen soll.

---

## 12. Funktionsstruktur der Retrospektive-App

Unsere App wird in diese Funktionen aufgeteilt. Jede hat genau eine Hauptaufgabe.

```
fetch_containers()              → Liste der verfügbaren Container holen
fetch_routes(container)         → Routen zu einem Container holen
choose_item(title, items)       → Auswahl im Terminal anzeigen
download_csv(container, route)  → CSV-Datei herunterladen und speichern
read_csv_file(file_path)        → CSV-Datei mit pandas einlesen
calculate_violations(df)        → Grenzwertverletzungen berechnen
calculate_statistics(df)        → Kennzahlen zusammenfassen
create_charts(df, container, route) → Diagramme erstellen
create_map(df, container, route)    → Karte erzeugen
create_pdf_report(...)          → PDF-Bericht erstellen
main()                          → Alle Schritte verbinden
```

---

## 13. Die main-Funktion: Alles zusammensetzen

`main()` verbindet alle Funktionen. Sie enthält keine eigene Logik – sie delegiert.

```python
def main():
    # Container auswählen
    containers = fetch_containers()
    selected_container = choose_item("Verfügbare Container", containers)
    if selected_container is None:
        return

    # Route auswählen
    routes = fetch_routes(selected_container)
    selected_route = choose_item("Verfügbare Routen", routes)
    if selected_route is None:
        return

    # Daten laden und auswerten
    csv_path = download_csv(selected_container, selected_route)
    data_frame = read_csv_file(csv_path)
    data_frame = calculate_violations(data_frame)
    statistics = calculate_statistics(data_frame)

    # Ausgaben erstellen
    chart_path = CHARTS_DIR / f"{selected_container}_{selected_route}_temp.png"
    create_temperature_chart(data_frame, chart_path)
    create_map(data_frame, selected_container, selected_route)
    pdf_path = create_pdf_report(selected_container, selected_route, statistics, chart_path)

    print(f"\nBericht erstellt: {pdf_path}")
```

Lies `main()` von oben nach unten: Es liest sich fast wie eine Schritt-für-Schritt-Anleitung auf Deutsch.

---

## 14. Programmstart

Am Ende der Datei steht:

```python
if __name__ == "__main__":
    main()
```

Das bedeutet: Die App startet nur dann, wenn diese Datei direkt ausgeführt wird – nicht, wenn sie von einem anderen Modul importiert wird.

---

## 15. Übungsaufgaben

### Aufgabe 1 – Einfache Funktion mit Rückgabewert

Schreib eine Funktion `format_temperature(value)`, die eine Temperatur als formatierten String zurückgibt.

Erwartetes Ergebnis:
```python
format_temperature(22.3)   # "22.3 °C"
format_temperature(15.0)   # "15.0 °C"
```

---

### Aufgabe 2 – EVA-Analyse

Analysiere diese Funktion nach dem EVA-Prinzip. Was ist Eingabe, Verarbeitung und Ausgabe?

```python
def summarize(values):
    total = sum(values)
    average = total / len(values)
    return average
```

---

### Aufgabe 3 – Parameter und Standardwerte

Erweitere `format_temperature` um einen optionalen Parameter `unit` mit Standardwert `"°C"`.

```python
format_temperature(22.3)         # "22.3 °C"
format_temperature(72.1, "°F")   # "72.1 °F"
```

---

### Aufgabe 4 – Scope verstehen

Was gibt dieses Programm aus? Warum?

```python
x = 10

def add_five():
    x = 20
    return x + 5

result = add_five()
print(x)       # Was steht hier?
print(result)  # Was steht hier?
```

---

### Aufgabe 5 – Funktion mit Docstring

Schreib eine Funktion `count_violations(data_frame)`, die die Anzahl Zeilen zurückgibt, in denen `any_violation` den Wert `True` hat. Füge einen vollständigen Docstring hinzu.

---

## 16. Was du gelernt hast

In diesem Tutorial hast du gelernt:

- warum Funktionen Code übersichtlicher, testbarer und wiederverwendbar machen
- wie man Funktionen definiert und aufruft
- wie man Parameter und Rückgabewerte einsetzt
- wie man Standardwerte für Parameter verwendet
- was Scope bedeutet und warum er wichtig ist
- wie man Funktionen mit Docstrings dokumentiert
- wie das EVA-Prinzip (Eingabe → Verarbeitung → Ausgabe) beim Planen hilft
- wie Funktionen andere Funktionen aufrufen und wie `main()` als Koordinator wirkt
- wie man diese Konzepte in einem echten Projekt anwendet
