# Tutorial: Funktionsbasierte Retrospektive-App

## Ziel des Tutorials

In diesem Tutorial bauen wir eine Retrospektive-App für Container-Tracking.

Die App analysiert einen abgeschlossenen Transport. Dabei lernen wir nicht nur neue Bibliotheken kennen, sondern auch, wie man ein Python-Programm mit Funktionen sauber strukturiert.

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

Diese Daten helfen dabei, einen Transport später zu prüfen.

Zum Beispiel können wir fragen:

- War die Temperatur immer im erlaubten Bereich?
- War die Feuchtigkeit zu hoch?
- Wo auf der Route gab es Probleme?
- Wie kann man die Ergebnisse verständlich darstellen?

Unsere Retrospektive-App beantwortet genau solche Fragen.

---

## 2. Voraussetzungen

Du solltest bereits diese Grundlagen kennen:

- Variablen
- Datentypen
- Listen
- Dictionaries
- Bedingungen
- Schleifen
- einfache Dateioperationen

Dieses Tutorial erklärt nicht Python von Grund auf. Es zeigt, wie man vorhandenes Wissen praktisch in einem Projekt einsetzt.

---

## 3. Warum Funktionen?

Am Anfang schreibt man Python-Code oft einfach von oben nach unten.

Beispiel:

```python
print("Container abrufen")
print("CSV einlesen")
print("Bericht erstellen")
```

Das funktioniert bei kleinen Programmen. Bei grösseren Programmen wird es aber schnell unübersichtlich.

Bei unserer App gibt es aber viele einzelne Aufgaben:

- Daten vom Webservice holen
- Benutzerauswahl anzeigen
- CSV-Datei speichern
- Tabelle mit pandas einlesen
- Grenzwerte prüfen
- Diagramme erzeugen
- PDF schreiben

Wenn alles direkt untereinander steht, wird der Code schnell lang und schwer lesbar.

Funktionen helfen uns, den Code in kleine Bausteine aufzuteilen.

Beispiele:

```python
def fetch_containers():
    pass

def read_csv_file(file_path):
    pass

def create_pdf_report():
    pass
```

Das macht den Code:

- übersichtlicher
- einfacher zu testen
- einfacher zu erklären
- einfacher zu erweitern

---

## 4. Was ist eine Funktion?
Eine Funktion ist ein benannter Codeblock.

Man kann eine Funktion einmal definieren und später aufrufen.

Ein sehr einfaches Beispiel:

```python
def say_hello():
    print("Hallo")
```

Die Funktion wird mit def definiert.

Der Code in der Funktion ist eingerückt.

Aufgerufen wird sie so:

`say_hello()`
Dann wird der Code innerhalb der Funktion ausgeführt.

---

## 5. Funktionen mit Rückgabewert
Viele Funktionen sollen ein Ergebnis zurückgeben.

Dafür verwenden wir return.

```python
def add_numbers():
    result = 3 + 4
    return result

number = add_numbers()
print(number)
```
Die Funktion berechnet etwas und gibt das Ergebnis zurück.

In unserer App verwenden wir das zum Beispiel so:

`containers = fetch_containers()`
Die Funktion fetch_containers() holt Containerdaten und gibt eine Liste zurück.

---

## 6. Funktionen mit Parametern
Manchmal braucht eine Funktion Informationen von aussen.

Diese Informationen nennt man Parameter.

```python
def greet(name):
    print(f"Hallo {name}")
```
Aufruf:

`greet("Lena")`
In unserer App brauchen wir Parameter zum Beispiel hier:

```python
def fetch_routes(container):
    ...
```
Die Funktion braucht den gewählten Container, damit sie die passenden Routen abrufen kann.

---

## 7. Funktionsstruktur der Retrospektive-App
Unsere App wird in mehrere Funktionen aufgeteilt.

Geplante Struktur:

```python
fetch_containers()
fetch_routes(container)
choose_item(title, items)
download_csv(container, route)
read_csv_file(file_path)
calculate_violations(data_frame)
calculate_statistics(data_frame)
create_charts(data_frame, container, route)
create_map(data_frame, container, route)
create_pdf_report(container, route, statistics, charts)
main()
```

Jede Funktion hat genau eine Hauptaufgabe.

Das ist wichtig, damit der Code verständlich bleibt.

---

## 8. Projektordner vorbereiten

Die App speichert verschiedene Ausgaben:

CSV-Dateien in `data/`
Karten in `maps/`
Diagramme in `charts/`
PDF-Berichte in `reports/`
Dafür verwenden wir pathlib.

```python
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MAPS_DIR = BASE_DIR / "maps"
CHARTS_DIR = BASE_DIR / "charts"
REPORTS_DIR = BASE_DIR / "reports"
```
`mkdir(exist_ok=True)` erstellt einen Ordner, falls er noch nicht existiert.

---

## 9. Container vom Webservice abrufen
Für HTTP-Anfragen verwenden wir die Bibliothek `requests`.

```python
import requests

BASE_URL = "https://fl-17-240.zhdk.cloud.switch.ch"

def fetch_containers():
    response = requests.get(f"{BASE_URL}/containers", timeout=10)

    if response.status_code != 200:
        print("Fehler beim Abrufen der Container:", response.status_code)
        return []

    data = response.json()
    containers = data.get("containers", [])

    return containers
```
Was passiert hier?

1. requests.get() ruft eine URL auf.
2. Der Statuscode wird geprüft.
3. Die JSON-Antwort wird in Python-Daten umgewandelt.
4. Die Containerliste wird zurückgegeben.

---

## 10. Routen für einen Container abrufen
Nachdem ein Container gewählt wurde, holen wir die Routen.

```python
def fetch_routes(container):
    response = requests.get(f"{BASE_URL}/containers/{container}/routes", timeout=10)

    if response.status_code != 200:
        print("Fehler beim Abrufen der Routen:", response.status_code)
        return []

    data = response.json()
    routes = data.get("routes", [])

    return routes
```

Hier sieht man einen wichtigen Vorteil von Parametern.

Die Funktion kann für jeden Container verwendet werden.

---

## 11. Auswahl im Terminal anzeigen
Die App soll im Terminal bedient werden.

Dafür schreiben wir eine allgemeine Auswahlfunktion.

```python
def choose_item(title, items):
    print()
    print(title)
    print("-" * len(title))

    for number, item in enumerate(items, start=1):
        print(f"{number}. {item}")

    try:
        index = int(input("Bitte Nummer wählen: ")) - 1
        return items[index]
    except (ValueError, IndexError):
        print("Ungültige Auswahl.")
        return None
```

Diese Funktion kann für Container und Routen verwendet werden.

Das ist ein gutes Beispiel für Wiederverwendung.

---

## 12. CSV-Datei herunterladen
Nun laden wir die CSV-Datei zur Route herunter.

```python
def download_csv(container, route):
    file_path = DATA_DIR / f"{container}_{route}.csv"

    csv_url = f"{BASE_URL}/files/{route}.csv?path=../data/migros/{container}/{route}.csv"
    response = requests.get(csv_url, timeout=20)

    if response.status_code != 200:
        print("Fehler beim CSV-Download:", response.status_code)
        return None

    with open(file_path, "wb") as file:
        file.write(response.content)

    return file_path
```

Wichtig:

- file_path ist der lokale Speicherort.
- response.content enthält die heruntergeladene Datei.
- "wb" bedeutet: Datei binär schreiben.
- Die Funktion gibt den Pfad zur gespeicherten Datei zurück.

---
## 13. CSV mit pandas lesen
Die Transportdaten liegen als CSV-Datei vor.

```python
data_frame = pd.read_csv(
    file_path,
    header=None,
    names=["timestamp", "latitude", "longitude", "temperature", "humidity"],
)
```
Ein DataFrame ist eine Tabelle in Python.

Die Spalten enthalten:

- Zeitstempel
- Breitengrad
- Längengrad
- Temperatur
- Feuchtigkeit

---

## 14. Grenzwertverletzungen berechnen
Jetzt prüfen wir die Messwerte.

```python
TEMP_MIN = 15
TEMP_MAX = 26
HUM_MAX = 72

def calculate_violations(data_frame):
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

Wir ergänzen neue Spalten.

Diese Spalten enthalten `True` oder `False`.

`True` bedeutet: Der Grenzwert wurde verletzt.

---

## 15. Kennzahlen berechnen
Für den Bericht brauchen wir zusammengefasste Werte.

```python
def calculate_statistics(data_frame):
    statistics = {
        "total_points": len(data_frame),
        "avg_temperature": data_frame["temperature"].mean(),
        "min_temperature": data_frame["temperature"].min(),
        "max_temperature": data_frame["temperature"].max(),
        "avg_humidity": data_frame["humidity"].mean(),
        "max_humidity": data_frame["humidity"].max(),
        "temp_violations": int(data_frame["temp_violation"].sum()),
        "humidity_violations": int(data_frame["humidity_violation"].sum()),
    }

    return statistics
```

Ein Dictionary passt hier gut, weil jede Kennzahl einen Namen bekommt.

## 16. Diagramme erstellen
Mit matplotlib können wir Diagramme als Bilddateien speichern.

Beispiel: Temperaturverlauf.

```python
import matplotlib.pyplot as plt

def create_temperature_chart(data_frame, chart_path):
    plt.figure(figsize=(10, 4))
    plt.plot(data_frame["timestamp"], data_frame["temperature"])
    plt.title("Temperaturverlauf")
    plt.xlabel("Zeit")
    plt.ylabel("Temperatur in °C")
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()
```

Wichtige Befehle:

- `plt.figure()` startet ein neues Diagramm.
- `plt.plot()` zeichnet eine Linie.
- `plt.savefig()` speichert das Bild.
- `plt.close()` schliesst das Diagramm.

---

## 17. Karte mit folium erstellen
Mit folium erstellen wir eine interaktive Karte.

```python
import folium

def create_map(data_frame):
    center_lat = data_frame["latitude"].mean()
    center_lon = data_frame["longitude"].mean()

    map_object = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
    )

    coordinates = data_frame[["latitude", "longitude"]].values.tolist()

    folium.PolyLine(coordinates, color="blue").add_to(map_object)

    return map_object
```

Die Karte zeigt die Route als Linie.

Später können wir zusätzlich Messpunkte einzeichnen.

---

## 18. PDF-Bericht erstellen
Für PDF-Dateien verwenden wir reportlab.

Der PDF-Bericht enthält:

- Titel
- Container und Route
- Kennzahlen
- Diagramme
- Fazit

## 19. main-Funktion
Die Funktion `main()` verbindet alle Schritte.

```python
def main():
    containers = fetch_containers()
    selected_container = choose_item("Verfügbare Container", containers)

    routes = fetch_routes(selected_container)
    selected_route = choose_item("Verfügbare Routen", routes)

    csv_path = download_csv(selected_container, selected_route)

    data_frame = read_csv_file(csv_path)
    data_frame = calculate_violations(data_frame)

    statistics = calculate_statistics(data_frame)

    print(statistics)
```

`main()` ist der Startpunkt der App.

---

## 20. Programmstart
Am Ende der Datei steht:

```python
if __name__ == "__main__":
    main()
```

Das bedeutet:

Die App startet nur dann, wenn diese Datei direkt ausgeführt wird.

---

## 21. Was du gelernt hast
In diesem Tutorial hast du gelernt:

- was Funktionen sind
- wie man Funktionen definiert
- wie man Funktionen aufruft
- wie man Parameter verwendet
- wie man Rückgabewerte verwendet
- wie man eine App in kleine Bausteine aufteilt
- wie man Daten über REST abruft
- wie man CSV-Dateien mit pandas einliest
- wie man Grenzwertverletzungen berechnet
- wie man Diagramme und Karten vorbereitet
- wie man einen PDF-Bericht plant