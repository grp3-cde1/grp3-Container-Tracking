# Zentrale Einstellungen der Retrospective-App

## Ziel dieses Tutorials

In diesem Tutorial wird die Datei `config.py` der objektorientierten Retrospective-App erklärt.

Der Fokus liegt nicht auf komplizierter OOP-Theorie, sondern auf der Frage:

```text
Warum lagern wir Pfade, API-Adresse und Grenzwerte in eine eigene Datei aus?
```

Die Datei `config.py` gehört zur Struktur unserer OOP-Version und befindet sich hier:

```text
apps/retrospective_oop/config.py
```

---

## 1. Aufgabe von `config.py`

`config.py` enthält zentrale Einstellungen, die an mehreren Stellen in der App gebraucht werden.

Dazu gehören:

```text
Projektpfade
Ordner für Daten, Karten, Diagramme und Berichte
API-Adresse
Grenzwerte für Temperatur und Feuchtigkeit
```

Diese Werte sollen nicht in jeder Klasse einzeln stehen. Stattdessen werden sie zentral in `config.py` definiert und von anderen Dateien importiert.

Merksatz:

```text
config.py = zentrale Einstellungen der App
```

---

## 2. Warum ist `config.py` eine eigene Datei?

In der funktionsbasierten App standen Konstanten wie `BASE_URL`, `TEMP_MIN`, `TEMP_MAX` und `HUM_MAX` direkt oben in der Hauptdatei.

In der OOP-Version besteht die App aber aus mehreren Dateien:

```text
api_client.py
data_processor.py
output_creator.py
app.py
```

In anderen Projekten brauchen mehrere Dateien dieselben Einstellungen.
Zur Visualisierung haben auch wir Standardwerte in die `config.py` gelegt, da jede unserer Dateien jeweils solche verwendet:

Beispiele:

```text
api_client.py      → braucht BASE_URL und DATA_DIR
data_processor.py  → braucht TEMP_MIN, TEMP_MAX und HUM_MAX
output_creator.py  → braucht MAPS_DIR, CHARTS_DIR, REPORTS_DIR und Grenzwerte
```

Der Vorteil:

```text
Eine Änderung muss nur an einer Stelle gemacht werden.
```

---

## 3. Inhalt von `config.py`

Die Datei enthält zuerst den Import für `Path`:

```python
from pathlib import Path
```

`Path` wird verwendet, um sauber mit Datei- und Ordnerpfaden zu arbeiten.

Danach wird der Basisordner des Projekts berechnet:

```python
BASE_DIR = Path(__file__).resolve().parent.parent.parent
```

Diese Zeile sorgt dafür, dass die App den Hauptordner des Projekts findet.

Da `config.py` in diesem Ordner liegt:

```text
apps/retrospective_oop/config.py
```

müssen wir drei Ebenen nach oben gehen:

```text
config.py
→ retrospective_oop
→ apps
→ Projektordner
```

Darum verwenden wir:

```python
.parent.parent.parent
```

---

## 4. Projektpfade

Ausgehend von `BASE_DIR` werden die benötigten Unterordner definiert:

```python
DATA_DIR = BASE_DIR / "data"
MAPS_DIR = BASE_DIR / "maps"
CHARTS_DIR = BASE_DIR / "charts"
REPORTS_DIR = BASE_DIR / "reports"
```

Diese Pfade werden später von anderen Klassen und deren Methoden verwendet.

Beispiel aus output_creator:

```text
DATA_DIR     → CSV-Dateien speichern
MAPS_DIR     → HTML-Karten speichern
CHARTS_DIR   → Diagramme speichern
REPORTS_DIR  → PDF-Berichte speichern
```

---

## 5. API-Adresse

Die Basis-URL des Webservice wird ebenfalls zentral gespeichert:

```python
BASE_URL = "https://fl-17-240.zhdk.cloud.switch.ch"
```

Diese URL wird vom `ApiClient` verwendet.

Zum Beispiel wird daraus später die Adresse für das Abrufen der Container:

```text
https://fl-17-240.zhdk.cloud.switch.ch/containers
```

Wenn sich die Server-Adresse ändern würde, müsste man nur diesen Wert in `config.py` anpassen.

---

## 6. Grenzwerte

Auch die Grenzwerte für Temperatur und Feuchtigkeit stehen in `config.py`:

```python
TEMP_MIN = 15
TEMP_MAX = 26
HUM_MAX = 72
```

Diese Werte werden vor allem vom `DataProcessor` benötigt.

Damit wird geprüft:

```text
Ist die Temperatur zu tief?
Ist die Temperatur zu hoch?
Ist die Feuchtigkeit zu hoch?
```

Auch der `OutputCreator` verwendet diese Werte, zum Beispiel um Grenzlinien in Diagrammen oder Angaben im PDF-Bericht darzustellen.

---

## 7. Ordner erstellen mit `create_directories()`

In `config.py` gibt es zusätzlich die Funktion:

```python
def create_directories():
    """
    Erstellt alle benötigten Unterordner, falls sie noch nicht existieren.
    """

    DATA_DIR.mkdir(exist_ok=True)
    MAPS_DIR.mkdir(exist_ok=True)
    CHARTS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
```

Diese Funktion erstellt die benötigten Ordner, falls sie noch nicht vorhanden sind.

Das ist wichtig, weil die App später Dateien speichern möchte.

Beispiele:

```text
CSV-Dateien in data/
Diagramme in charts/
Karten in maps/
PDF-Berichte in reports/
```

Ohne diese Ordner könnte es beim Speichern zu Fehlern kommen.

---

## 8. Warum ist `create_directories()` keine Klasse?

Nicht alles in einem OOP-Projekt muss zwingend eine Klasse sein.

`create_directories()` ist eine kleine Hilfsfunktion. Sie speichert keine eigenen Objektzustände und braucht kein `self`.

Darum reicht hier eine normale Funktion.

Das ist wichtig zu verstehen:

```text
OOP bedeutet nicht, dass wirklich alles eine Klasse sein muss.
```

Für unsere App ist es sinnvoll, die Konfiguration einfach und übersichtlich zu halten.

---

## 9. Verwendung in anderen Dateien

Andere Dateien importieren die Werte aus `config.py`.

Beispiel aus `api_client.py`:

```python
from .config import BASE_URL, DATA_DIR
```

Beispiel aus `data_processor.py`:

```python
from .config import TEMP_MIN, TEMP_MAX, HUM_MAX
```

Beispiel aus `output_creator.py`:

```python
from .config import MAPS_DIR, CHARTS_DIR, REPORTS_DIR
```

Der Punkt `.` bedeutet:

```text
Importiere aus dem gleichen Paketordner.
```

Das funktioniert sauber, weil der Ordner `retrospective_oop` durch `__init__.py` als Paket verwendet wird.
