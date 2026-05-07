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

## Grundstruktur der App

Die App besteht aus mehreren Arbeitsschritten:

1. Container abrufen
2. Container auswählen
3. Routen abrufen
4. Route auswählen
5. CSV herunterladen
6. CSV einlesen
7. Grenzwertverletzungen berechnen
8. Diagramme erstellen
9. Karte erstellen
10. PDF-Bericht erstellen

Diese Schritte werden später in der Funktion `main()` zusammengeführt.

---

## Projektordner

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
Mit `mkdir(exist_ok=True)` können Ordner automatisch erstellt werden.

---

## REST-API abrufen
Für HTTP-Anfragen verwenden wir requests.

`response = requests.get(f"{BASE_URL}/containers", timeout=10)`
Ein Statuscode von 200 bedeutet, dass die Anfrage erfolgreich war.

```python
if response.status_code != 200:
    print("Fehler")
```
Die Antwort wird mit `.json()` in Python-Daten umgewandelt.

```python
data = response.json()
containers = data.get("containers", [])
```

---

## CSV mit pandas lesen
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