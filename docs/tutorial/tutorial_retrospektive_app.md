# Tutorial: Funktionsbasierte Retrospektive-App

## Ziel des Tutorials

In diesem Tutorial bauen wir eine Retrospektive-App für Container-Tracking.

Die App analysiert einen abgeschlossenen Transport. Dabei liegt der Fokus auf einem zentralen Konzept: **Funktionen**. Wir lernen nicht nur, wie man Funktionen schreibt – sondern warum sie existieren und wie man sie richtig einsetzt.

Am Ende kann die App:

- Container über eine REST-API abrufen
- Routen zu einem Container abrufen
- eine CSV-Datei herunterladen
- Messdaten mit pandas einlesen
- Grenzwertverletzungen berechnen
- Diagramme erstellen
- eine Karte erzeugen
- einen PDF-Bericht erstellen

---

## 1. Was bauen wir?

Im Logistik-Kontext entstehen bei einem Containertransport viele Messdaten.

Typische Daten sind:

- Zeitstempel
- geografische Koordinaten
- Temperatur
- Feuchtigkeit

Diese Daten helfen dabei, einen Transport später zu prüfen. Unsere Retrospektive-App beantwortet Fragen wie:

- War die Temperatur immer im erlaubten Bereich?
- War die Feuchtigkeit zu hoch?
- Wo auf der Route gab es Probleme?
- Wie kann man die Ergebnisse verständlich darstellen?

---

## 2. Voraussetzungen

Du solltest bereits diese Grundlagen kennen:

- Variablen und Datentypen
- Listen und Dictionaries
- Bedingungen und Schleifen
- einfache Dateioperationen

Dieses Tutorial baut darauf auf und zeigt, wie man mit Funktionen grössere Programme sauber strukturiert.

---

## 3. Warum Funktionen? Ein Vorher/Nachher-Vergleich

Am Anfang schreibt man Python-Code oft einfach von oben nach unten. Das nennt man **sequenziellen Code**.

**Ohne Funktionen** würde unsere App so aussehen:

```python
# Schritt 1: Container abrufen
response = requests.get("https://example.com/containers", timeout=10)
data = response.json()
containers = data.get("containers", [])

# Schritt 2: Container anzeigen und auswählen
print("Verfügbare Container")
for number, item in enumerate(containers, start=1):
    print(f"{number}. {item}")
index = int(input("Bitte Nummer wählen: ")) - 1
selected_container = containers[index]

# Schritt 3: Routen abrufen
response = requests.get(f"https://example.com/containers/{selected_container}/routes", timeout=10)
data = response.json()
routes = data.get("routes", [])

# Schritt 4: Routen anzeigen und auswählen
print("Verfügbare Routen")
for number, item in enumerate(routes, start=1):
    print(f"{number}. {item}")
index = int(input("Bitte Nummer wählen: ")) - 1
selected_route = routes[index]

# Schritt 5: CSV herunterladen
# ... und so weiter, über hunderte Zeilen
```

Probleme dabei:

- Der Code wird sehr lang und schwer zu lesen.
- Die Auswahllogik (Schritte 2 und 4) ist fast identisch – aber doppelt geschrieben.
- Wenn man die Auswahl verbessern will, muss man es an zwei Stellen ändern.
- Ein Fehler in Zeile 200 ist schwer zu finden.

**Mit Funktionen** sieht die gleiche Logik so aus:

```python
def fetch_containers():
    ...

def fetch_routes(container):
    ...

def choose_item(title, items):
    ...

def main():
    containers = fetch_containers()
    selected_container = choose_item("Verfügbare Container", containers)

    routes = fetch_routes(selected_container)
    selected_route = choose_item("Verfügbare Routen", routes)
```

`main()` liest sich fast wie ein Plan auf Deutsch. Jede Funktion hat einen klaren Namen und eine einzige Aufgabe.

---

## 4. Das EVA-Prinzip

Jede gut geschriebene Funktion folgt einem einfachen Schema:

```
Eingabe → Verarbeitung → Ausgabe
```

Das nennt man das **EVA-Prinzip**.

Beispiel:

```python
def calculate_statistics(data_frame):   # Eingabe: eine Tabelle
    avg = data_frame["temperature"].mean()  # Verarbeitung: berechnen
    return avg                          # Ausgabe: Ergebnis zurückgeben
```

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

## 6. Rückgabewerte mit `return`

Viele Funktionen sollen ein Ergebnis zurückgeben. Dafür verwenden wir `return`.

```python
def add_numbers():
    result = 3 + 4
    return result

number = add_numbers()
print(number)  # Ausgabe: 7
```

In unserer App verwenden wir das zum Beispiel so:

```python
containers = fetch_containers()
```

Die Funktion `fetch_containers()` holt Daten vom Server und gibt eine Liste zurück. Diese Liste wird in `containers` gespeichert und kann danach weiterverwendet werden.

---

## 7. Parameter: Informationen übergeben

Manchmal braucht eine Funktion Informationen von aussen. Diese Informationen nennt man **Parameter**.

```python
def greet(name):
    print(f"Hallo {name}")

greet("Lena")   # Ausgabe: Hallo Lena
greet("Jonas")  # Ausgabe: Hallo Jonas
```

Wenn man `greet("Lena")` aufruft, passiert intern folgendes:

```
Aufruf:     greet("Lena")
              ↓
Definition: def greet(name):
              ↓
Zuweisung:  name = "Lena"
              ↓
Ausführung: print(f"Hallo {name}")  →  "Hallo Lena"
```

Der Wert `"Lena"` wird beim Aufruf übergeben und steht innerhalb der Funktion als `name` zur Verfügung.

In unserer App brauchen wir Parameter zum Beispiel hier:

```python
def fetch_routes(container):
    response = requests.get(f"{BASE_URL}/containers/{container}/routes")
    ...
```

Die Funktion kann für jeden beliebigen Container aufgerufen werden:

```python
routes_a = fetch_routes("CONT-001")
routes_b = fetch_routes("CONT-002")
```

Das ist ein zentraler Vorteil von Parametern: **Wiederverwendbarkeit**.

---

## 8. Standardwerte für Parameter

Parameter können einen Standardwert haben. Dann ist die Angabe beim Aufruf optional.

```python
def greet(name, language="de"):
    if language == "de":
        print(f"Hallo {name}")
    else:
        print(f"Hello {name}")

greet("Lena")           # Ausgabe: Hallo Lena (Standardwert wird verwendet)
greet("Lena", "en")     # Ausgabe: Hello Lena (eigener Wert wird übergeben)
```

In unserer App könnte `choose_item` so verwendet werden:

```python
def choose_item(title, items, start=1):
    for number, item in enumerate(items, start=start):
        print(f"{number}. {item}")
    ...
```

Standardwerte eignen sich gut für Optionen, die meistens gleich bleiben, aber gelegentlich angepasst werden müssen.

---

## 9. Scope: Wo gelten Variablen?

Eine wichtige Frage beim Arbeiten mit Funktionen ist: **Wo ist eine Variable sichtbar?**

Das nennt man **Scope** (deutsch: Gültigkeitsbereich).

**Lokale Variablen** existieren nur innerhalb der Funktion:

```python
def calculate():
    result = 42  # lokale Variable
    return result

print(result)  # ❌ Fehler! result existiert hier nicht
```

**Globale Variablen** werden ausserhalb von Funktionen definiert und sind überall sichtbar:

```python
BASE_URL = "https://example.com"  # globale Variable

def fetch_containers():
    response = requests.get(f"{BASE_URL}/containers")  # ✅ BASE_URL ist sichtbar
    ...
```

In unserer App definieren wir Konstanten global, damit alle Funktionen darauf zugreifen können:

```python
BASE_URL = "https://fl-17-240.zhdk.cloud.switch.ch"
TEMP_MIN = 15
TEMP_MAX = 26
HUM_MAX = 72
```

**Faustregel:** Verwende globale Variablen nur für Konstanten (Werte, die sich nie ändern). Alles andere sollte als Parameter übergeben werden.

> **Warum ist das wichtig?**
> Wenn eine Funktion nur über ihre Parameter mit dem Rest des Programms kommuniziert, ist sie viel einfacher zu verstehen und zu testen. Du siehst auf einen Blick, welche Informationen hineingehen und was herauskommt.

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

## 13. Projektordner vorbereiten

Die App speichert verschiedene Ausgaben in eigenen Ordnern. Dafür verwenden wir `pathlib`.

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR    = BASE_DIR / "data"
MAPS_DIR    = BASE_DIR / "maps"
CHARTS_DIR  = BASE_DIR / "charts"
REPORTS_DIR = BASE_DIR / "reports"

for directory in [DATA_DIR, MAPS_DIR, CHARTS_DIR, REPORTS_DIR]:
    directory.mkdir(exist_ok=True)
```

`mkdir(exist_ok=True)` erstellt einen Ordner, falls er noch nicht existiert. Der Parameter `exist_ok=True` verhindert einen Fehler, wenn der Ordner bereits da ist.

---

## 14. Container vom Webservice abrufen

Für HTTP-Anfragen verwenden wir die Bibliothek `requests`.

```python
import requests

BASE_URL = "https://fl-17-240.zhdk.cloud.switch.ch"

def fetch_containers():
    """
    Ruft alle verfügbaren Container vom Server ab.

    Rückgabe:
        Liste der Container-IDs, oder leere Liste bei Fehler
    """
    response = requests.get(f"{BASE_URL}/containers", timeout=10)

    if response.status_code != 200:
        print("Fehler beim Abrufen der Container:", response.status_code)
        return []

    data = response.json()
    containers = data.get("containers", [])

    return containers
```

EVA-Analyse dieser Funktion:

- **Eingabe:** keine Parameter (die URL kommt aus der globalen Konstante)
- **Verarbeitung:** HTTP-Anfrage senden, Antwort prüfen, JSON umwandeln
- **Ausgabe:** Liste der Container

---

## 15. Routen für einen Container abrufen

```python
def fetch_routes(container):
    """
    Ruft alle Routen für einen bestimmten Container ab.

    Parameter:
        container: Container-ID als String

    Rückgabe:
        Liste der Routen-IDs, oder leere Liste bei Fehler
    """
    response = requests.get(
        f"{BASE_URL}/containers/{container}/routes",
        timeout=10
    )

    if response.status_code != 200:
        print("Fehler beim Abrufen der Routen:", response.status_code)
        return []

    data = response.json()
    routes = data.get("routes", [])

    return routes
```

Diese Funktion ist fast identisch mit `fetch_containers()` – aber der Parameter `container` macht den Unterschied. Dieselbe Funktion funktioniert für jeden beliebigen Container.

---

## 16. Auswahl im Terminal anzeigen

Diese Funktion wird für Container und Routen gleichermassen verwendet.

```python
def choose_item(title, items, start=1):
    """
    Zeigt eine nummerierte Liste an und gibt das gewählte Element zurück.

    Parameter:
        title:  Überschrift der Auswahl
        items:  Liste der Auswahlmöglichkeiten
        start:  Startnummer der Liste (Standard: 1)

    Rückgabe:
        Das gewählte Element, oder None bei ungültiger Eingabe
    """
    print()
    print(title)
    print("-" * len(title))

    for number, item in enumerate(items, start=start):
        print(f"{number}. {item}")

    try:
        index = int(input("Bitte Nummer wählen: ")) - 1
        return items[index]
    except (ValueError, IndexError):
        print("Ungültige Auswahl.")
        return None
```

Diese Funktion ist ein gutes Beispiel für **Wiederverwendung**: einmal schreiben, mehrfach verwenden.

---

## 17. CSV-Datei herunterladen

```python
def download_csv(container, route):
    """
    Lädt die CSV-Datei zur gewählten Route herunter.

    Parameter:
        container: Container-ID
        route:     Routen-ID

    Rückgabe:
        Pfad zur gespeicherten Datei, oder None bei Fehler
    """
    file_path = DATA_DIR / f"{container}_{route}.csv"

    csv_url = f"{BASE_URL}/files/{route}.csv?path=../data/migros/{container}/{route}.csv"
    response = requests.get(csv_url, timeout=20)

    if response.status_code != 200:
        print("Fehler beim CSV-Download:", response.status_code)
        return None

    with open(file_path, "wb") as file:
        file.write(response.content)

    print(f"CSV gespeichert: {file_path}")
    return file_path
```

Wichtig:

- `"wb"` bedeutet: Datei binär schreiben (für Nicht-Text-Inhalte).
- Die Funktion gibt den Pfad zurück, damit die nächste Funktion ihn verwenden kann.

---

## 18. CSV mit pandas einlesen

```python
import pandas as pd

def read_csv_file(file_path):
    """
    Liest eine CSV-Datei ein und gibt einen DataFrame zurück.

    Parameter:
        file_path: Pfad zur CSV-Datei

    Rückgabe:
        pandas DataFrame mit Spalten: timestamp, latitude, longitude,
        temperature, humidity
    """
    data_frame = pd.read_csv(
        file_path,
        header=None,
        names=["timestamp", "latitude", "longitude", "temperature", "humidity"],
    )
    return data_frame
```

Ein DataFrame ist eine Tabelle in Python. Jede Spalte ist durch einen Namen ansprechbar.

---

## 19. Grenzwertverletzungen berechnen

Jetzt prüfen wir die Messwerte auf Grenzwertverletzungen.

```python
TEMP_MIN = 15
TEMP_MAX = 26
HUM_MAX  = 72

def calculate_violations(data_frame):
    """
    Ergänzt den DataFrame um Boolean-Spalten für Grenzwertverletzungen.

    Parameter:
        data_frame: pandas DataFrame mit temperature und humidity

    Rückgabe:
        Kopie des DataFrames mit zusätzlichen Spalten:
        temp_violation, humidity_violation, any_violation
    """
    data_frame = data_frame.copy()

    data_frame["temp_violation"] = (
        (data_frame["temperature"] < TEMP_MIN)
        | (data_frame["temperature"] > TEMP_MAX)
    )

    data_frame["humidity_violation"] = data_frame["humidity"] > HUM_MAX

    data_frame["any_violation"] = (
        data_frame["temp_violation"]
        | data_frame["humidity_violation"]
    )

    return data_frame
```

EVA-Analyse:

- **Eingabe:** ein DataFrame mit Messwerten
- **Verarbeitung:** neue Spalten mit `True`/`False` berechnen
- **Ausgabe:** ein erweiterter DataFrame

`True` bedeutet: Grenzwert wurde verletzt. `.copy()` stellt sicher, dass das Original nicht verändert wird.

---

## 20. Kennzahlen berechnen

```python
def calculate_statistics(data_frame):
    """
    Berechnet zusammengefasste Kennzahlen aus dem DataFrame.

    Parameter:
        data_frame: pandas DataFrame mit Violations-Spalten

    Rückgabe:
        Dictionary mit Kennzahlen
    """
    statistics = {
        "total_points":         len(data_frame),
        "avg_temperature":      data_frame["temperature"].mean(),
        "min_temperature":      data_frame["temperature"].min(),
        "max_temperature":      data_frame["temperature"].max(),
        "avg_humidity":         data_frame["humidity"].mean(),
        "max_humidity":         data_frame["humidity"].max(),
        "temp_violations":      int(data_frame["temp_violation"].sum()),
        "humidity_violations":  int(data_frame["humidity_violation"].sum()),
    }
    return statistics
```

Ein Dictionary passt hier gut: Jede Kennzahl bekommt einen sprechenden Namen.

---

## 21. Diagramme erstellen

```python
import matplotlib.pyplot as plt

def create_temperature_chart(data_frame, chart_path):
    """
    Erstellt ein Liniendiagramm des Temperaturverlaufs.

    Parameter:
        data_frame: pandas DataFrame
        chart_path: Pfad zum Speichern des Diagramms
    """
    plt.figure(figsize=(10, 4))
    plt.plot(data_frame["timestamp"], data_frame["temperature"])
    plt.axhline(y=TEMP_MIN, color="blue",  linestyle="--", label=f"Min ({TEMP_MIN}°C)")
    plt.axhline(y=TEMP_MAX, color="red",   linestyle="--", label=f"Max ({TEMP_MAX}°C)")
    plt.title("Temperaturverlauf")
    plt.xlabel("Zeit")
    plt.ylabel("Temperatur in °C")
    plt.legend()
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()
```

Wichtige Befehle:

- `plt.figure()` – startet ein neues Diagramm
- `plt.plot()` – zeichnet eine Linie
- `plt.axhline()` – zeichnet eine horizontale Grenzlinie
- `plt.savefig()` – speichert das Bild
- `plt.close()` – gibt den Speicher frei

---

## 22. Karte mit folium erstellen

```python
import folium

def create_map(data_frame, container, route):
    """
    Erstellt eine interaktive Karte mit der Transportroute.

    Parameter:
        data_frame: pandas DataFrame mit latitude und longitude
        container:  Container-ID (für den Dateinamen)
        route:      Routen-ID (für den Dateinamen)

    Rückgabe:
        Pfad zur gespeicherten HTML-Karte
    """
    center_lat = data_frame["latitude"].mean()
    center_lon = data_frame["longitude"].mean()

    map_object = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
    )

    coordinates = data_frame[["latitude", "longitude"]].values.tolist()
    folium.PolyLine(coordinates, color="blue").add_to(map_object)

    map_path = MAPS_DIR / f"{container}_{route}.html"
    map_object.save(str(map_path))
    return map_path
```

Die Karte wird als HTML-Datei gespeichert und kann im Browser geöffnet werden.

---

## 23. PDF-Bericht erstellen

Für PDF-Dateien verwenden wir `reportlab`. Der Bericht enthält Titel, Container- und Routeninfo, Kennzahlen sowie die erstellten Diagramme.

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_pdf_report(container, route, statistics, chart_path):
    """
    Erstellt einen PDF-Bericht mit Kennzahlen und Diagramm.

    Parameter:
        container:   Container-ID
        route:       Routen-ID
        statistics:  Dictionary mit Kennzahlen
        chart_path:  Pfad zum Temperaturdiagramm

    Rückgabe:
        Pfad zum erstellten PDF
    """
    pdf_path = REPORTS_DIR / f"{container}_{route}.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 60, "Transport-Retrospektive")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Container: {container}")
    c.drawString(50, height - 120, f"Route:     {route}")

    c.drawString(50, height - 160, f"Messpunkte gesamt:      {statistics['total_points']}")
    c.drawString(50, height - 180, f"Temperaturverletzungen: {statistics['temp_violations']}")
    c.drawString(50, height - 200, f"Feuchtigkeitsverletz.:  {statistics['humidity_violations']}")

    c.drawImage(str(chart_path), 50, height - 420, width=480, height=200)

    c.save()
    return pdf_path
```

---

## 24. Die main-Funktion: Alles zusammensetzen

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

## 25. Programmstart

Am Ende der Datei steht:

```python
if __name__ == "__main__":
    main()
```

Das bedeutet: Die App startet nur dann, wenn diese Datei direkt ausgeführt wird – nicht, wenn sie von einem anderen Modul importiert wird.

---

## 26. Übungsaufgaben

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

## 27. Was du gelernt hast

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
