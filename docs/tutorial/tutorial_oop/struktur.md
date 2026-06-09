# Struktur der objektorientierten Retrospective-App

## Ziel dieses Tutorials

In diesem Tutorial geht es um die konkrete Struktur unserer objektorientierten Retrospective-App.

Die allgemeine Idee von OOP wurde bereits im Haupttutorial erklärt. Hier geht es nun darum, wie wir unsere bestehende funktionsbasierte `retrospective_app.py` in ein OOP-Projekt überführen.

Im Fokus stehen diese Fragen:

```text
Wie wird aus einer funktionsbasierten Datei eine objektorientierte Projektstruktur?
Warum erstellen wir einen eigenen Ordner?
Warum brauchen wir mehrere Dateien?
Welche Aufgabe hat __init__.py?
Wie hängen die Dateien zusammen?
```

Viele Einzelheiten des allgemeinen Tutorials werden in diesem erneut aufgegriffen, dies dient zum Wissens-Refresh. Andere Informationen greifen bereits ein wenig vor, um den Kontext zu zeigen.

---

## 1. Ausgangspunkt: Die funktionsbasierte App

Die ursprüngliche Retrospective-App bestand aus einer Datei mit mehreren Funktionen.

Beispiele:

```python
fetch_containers()
fetch_routes(container)
download_csv(container, route)
read_csv_file(file_path)
calculate_violations(data_frame)
calculate_statistics(data_frame)
create_charts(data_frame, container, route)
create_map(data_frame, container, route)
create_pdf_report(...)
main()
```

Diese Funktionen waren nicht falsch. Im Gegenteil: Sie hatten bereits klare Aufgaben.

Für die objektorientierte Version überlegen wir nun:

```text
Welche Funktionen gehören fachlich zusammen?
```

Genau daraus entstehen unsere Klassen und Dateien.

---

## 2. Vom funktionsbasierten Design zum OOP-Design

Beim Umbau zur OOP-Version gruppieren wir die bestehenden Funktionen nach Aufgabenbereich.

Aus den API-Funktionen wird die Klasse `ApiClient`:

```text
fetch_containers()
fetch_routes(container)
download_csv(container, route)
```

Diese Funktionen haben alle mit dem Server zu tun. Deshalb gehören sie zusammen.

Aus den Analyse-Funktionen wird die Klasse `DataProcessor`:

```text
read_csv_file(file_path)
calculate_violations(data_frame)
calculate_statistics(data_frame)
```

Diese Funktionen arbeiten alle mit den Messdaten.

Aus den Ausgabe-Funktionen wird die Klasse `OutputCreator`:

```text
create_charts(...)
create_map(...)
create_pdf_report(...)
```

Diese Funktionen erstellen Ergebnisse wie Diagramme, Karte und PDF-Bericht.

Die bisherige `main()`-Funktion wird durch die Klasse `RetrospectiveApp` ersetzt. Diese Klasse koordiniert den Ablauf.

---

## 3. Neue Projektstruktur

Die OOP-Version erhält einen eigenen Unterordner:

```text
apps/
└── retrospective_oop/
    ├── __init__.py
    ├── config.py
    ├── api_client.py
    ├── data_processor.py
    ├── output_creator.py
    └── app.py
```

Der Ordner `retrospective_oop` enthält alle Dateien der objektorientierten Retrospective-App.

Dadurch bleibt die alte funktionsbasierte Version erhalten und die neue OOP-Version ist sauber davon getrennt.

---

## 4. Warum ein eigener Ordner?

Ein eigener Ordner ist sinnvoll, weil die OOP-Version aus mehreren Dateien besteht.

Ohne eigenen Ordner würden diese Dateien direkt im Ordner `apps` liegen und sich mit anderen Apps vermischen (bei uns der Live-Monitor)

---

## 5. Aufgabe der einzelnen Dateien

Die Dateien entsprechen den Aufgabenbereichen unserer App.

```text
config.py          → zentrale Einstellungen
api_client.py      → Daten vom Server holen
data_processor.py  → Messdaten einlesen und auswerten
output_creator.py  → Diagramme, Karte und PDF erstellen
app.py             → Ablauf der App steuern
__init__.py        → Ordner als Python-Paket kennzeichnen
```

Wichtig ist: Die Dateien sind nicht zufällig gewählt. Sie entstehen direkt aus der Gruppierung der ursprünglichen Funktionen.

---

## 6. `config.py`

In `config.py` speichern wir Werte, die von mehreren Dateien gebraucht werden.

Dazu gehören zum Beispiel:

```text
BASE_URL
DATA_DIR
MAPS_DIR
CHARTS_DIR
REPORTS_DIR
TEMP_MIN
TEMP_MAX
HUM_MAX
```

Diese Werte stehen nicht direkt in jeder Klasse, sondern zentral in einer Datei.

Der Vorteil:

```text
Wenn sich ein Grenzwert oder ein Pfad ändert, muss man ihn nur an einer Stelle anpassen.
```

`config.py` ist bei uns keine grosse Klasse, sondern eine Konfigurationsdatei mit Konstanten und einer kleinen Hilfsfunktion zum Erstellen der Ordner.

---

## 7. `api_client.py`

In `api_client.py` liegt die Klasse `ApiClient`.

Sie übernimmt den Teil der alten App, der mit dem Webservice arbeitet.

Dazu gehören:

```text
Container abrufen
Routen abrufen
CSV herunterladen
```

Der `ApiClient` gibt die Daten nur weiter. Er analysiert sie nicht und erstellt keine Ausgaben.

---

## 8. `data_processor.py`

In `data_processor.py` liegt die Klasse `DataProcessor`.

Sie übernimmt den Teil der alten App, der mit den CSV- und Messdaten arbeitet.

Dazu gehören:

```text
CSV-Datei einlesen
Grenzwertverletzungen berechnen
Statistiken berechnen
```

Der `DataProcessor` lädt keine Daten vom Server und erstellt keinen PDF-Bericht. Er konzentriert sich auf die Verarbeitung der Daten.

---

## 9. `output_creator.py`

In `output_creator.py` liegt die Klasse `OutputCreator`.

Sie übernimmt den Teil der alten App, der Ergebnisse erstellt.

Dazu gehören:

```text
Temperaturdiagramm
Feuchtigkeitsdiagramm
Verletzungsdiagramm
Routengrafik
interaktive Karte
PDF-Bericht
```

Diese Methoden gehören zusammen, weil sie alle Ausgaben der App erzeugen.

---

## 10. `app.py`

In `app.py` liegt die Klasse `RetrospectiveApp`.

Sie ersetzt die frühere `main()`-Funktion.

Die Hauptaufgabe dieser Klasse ist nicht, alles selbst zu berechnen. Sie steuert den Ablauf und verwendet dafür die anderen Klassen.

Vereinfacht:

```python
self.api_client = ApiClient()
self.data_processor = DataProcessor()
self.output_creator = OutputCreator()
```

Danach kann die App die einzelnen Schritte ausführen:

```text
1. Container abrufen
2. Route auswählen
3. CSV herunterladen
4. Daten auswerten
5. Diagramme, Karte und PDF erstellen
```

Die Klasse `RetrospectiveApp` ist also die Koordination der App.

---

## 11. Warum braucht es `__init__.py`?

Die Datei `__init__.py` bleibt in unserem Projekt leer.

Trotzdem ist sie nützlich, weil sie Python zeigt:

```text
Dieser Ordner gehört zu einem Python-Paket.
```

Dadurch können wir innerhalb des Ordners mit relativen Imports arbeiten.

Beispiel aus `app.py`:

```python
from .api_client import ApiClient
from .data_processor import DataProcessor
from .output_creator import OutputCreator
```

Der Punkt `.` bedeutet:

```text
Suche die Datei im gleichen Paketordner.
```

Ohne saubere Paketstruktur können solche Imports schnell zu Problemen führen.

Darum erstellen wir `__init__.py`, auch wenn die Datei leer bleibt.

---

## 12. Wie arbeitet die Struktur zusammen?

Das Zusammenspiel sieht vereinfacht so aus:

```text
RetrospectiveApp
│
├── ApiClient
│   └── holt Container, Routen und CSV-Dateien
│
├── DataProcessor
│   └── liest und analysiert die Messdaten
│
└── OutputCreator
    └── erstellt Diagramme, Karte und PDF
```

Die Hauptklasse `RetrospectiveApp` steuert den Ablauf.

Die anderen Klassen übernehmen spezialisierte Aufgaben.

Das ist der wichtigste Unterschied zur alten funktionsbasierten Version:

```text
Früher: viele Funktionen nebeneinander
Jetzt: Funktionen sind nach Verantwortung in Klassen und Dateien gruppiert
```

