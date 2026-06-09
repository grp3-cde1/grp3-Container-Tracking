# Ablauf der Retrospective-App steuern mit `RetrospectiveApp`

## Ziel dieses Tutorials

In diesem Tutorial wird die Datei `app.py` erklärt.

Der Fokus liegt auf der OOP-Struktur der Klasse `RetrospectiveApp` und darauf, wie sie die anderen Klassen miteinander verbindet.

```text
Warum gibt es diese Hauptklasse?
Welche Verantwortung hat sie?
Wie nutzt sie ApiClient, DataProcessor und OutputCreator?
Warum ersetzt sie die frühere main()-Funktion?
```

Die Datei befindet sich hier:

```text
apps/retrospective_oop/app.py
```

---

## 1. Aufgabe von `RetrospectiveApp`

Die Klasse `RetrospectiveApp` steuert den gesamten Ablauf der App.

Sie übernimmt den Teil der alten funktionsbasierten App, der früher in der `main()`-Funktion lag.

Die Klasse entscheidet also, was in welcher Reihenfolge passiert:

```text
Container abrufen
Container auswählen
Routen abrufen
Route auswählen
CSV herunterladen
Daten auswerten
Diagramme, Karte und PDF erstellen
```

Wichtig ist: `RetrospectiveApp` macht nicht alles selbst.

Sie verwendet dafür die anderen Klassen:

```text
ApiClient      → Daten vom Server holen
DataProcessor  → Messdaten verarbeiten
OutputCreator  → Ergebnisse erstellen
```

Merksatz:

```text
RetrospectiveApp = Ablauf steuern und Klassen verbinden
```

---

## 2. Von `main()` zur Klasse

In der funktionsbasierten Version gab es eine Funktion `main()`.

Diese Funktion hat die einzelnen Funktionen nacheinander aufgerufen.

Vereinfacht:

```python
def main():
    containers = fetch_containers()
    selected_container = choose_item(containers)

    routes = fetch_routes(selected_container)
    selected_route = choose_item(routes)

    csv_path = download_csv(selected_container, selected_route)

    data_frame = read_csv_file(csv_path)
    data_frame = calculate_violations(data_frame)
    statistics = calculate_statistics(data_frame)

    charts = create_charts(data_frame, selected_container, selected_route)
    create_map(data_frame, selected_container, selected_route)
    create_pdf_report(selected_container, selected_route, statistics, charts)
```

In der OOP-Version wird dieser Ablauf in eine Klasse verschoben:

```python
class RetrospectiveApp:
```

---

## 3. Hilfsobjekte in `__init__()`

Beim Erstellen eines `RetrospectiveApp`-Objekts werden die anderen Klassen vorbereitet.

Vereinfacht sieht das so aus:

```python
def __init__(self):
    self.api_client = ApiClient()
    self.data_processor = DataProcessor()
    self.output_creator = OutputCreator()
```

Hier werden drei Objekte erstellt und in der App gespeichert.

Das bedeutet:

```text
self.api_client      → gespeichertes ApiClient-Objekt
self.data_processor  → gespeichertes DataProcessor-Objekt
self.output_creator  → gespeichertes OutputCreator-Objekt
```

Diese Objekte werden gespeichert, damit die App sie später in ihren Methoden wiederverwenden kann.

---

## 4. Warum werden die Objekte mit `self` gespeichert?

Die App braucht den `ApiClient`, den `DataProcessor` und den `OutputCreator` nicht nur einmal in `__init__()`.

Sie braucht diese Objekte später im Ablauf der App.

Darum werden sie mit `self` gespeichert:

```python
self.api_client = ApiClient()
```

Das bedeutet:

```text
Speichere dieses ApiClient-Objekt in dieser RetrospectiveApp.
```

Später kann die Klasse wieder darauf zugreifen:

```python
containers = self.api_client.fetch_containers()
```

---

## 5. Die Methode `choose_item()`

Die Methode `choose_item()` hilft bei der Auswahl eines Eintrags.

Sie wird verwendet um den Container und die Route auszuwählen.

Vereinfacht:

```python
selected_container = self.choose_item(containers, "Container auswählen")
selected_route = self.choose_item(routes, "Route auswählen")
```

Die Methode gehört zur Hauptklasse, weil sie Teil des App-Ablaufs ist.

Sie ist nicht direkt Server-Zugriff, Datenverarbeitung oder Ausgabe.

Darum passt sie nicht in `ApiClient`, `DataProcessor` oder `OutputCreator`.

---

## 6. Die Methode `run()`

Die wichtigste Methode der Klasse ist `run()`.

Sie startet den eigentlichen Ablauf der App.

Vereinfacht macht `run()` Folgendes:

```text
1. Benötigte Ordner erstellen
2. Container vom Server abrufen
3. Container auswählen
4. Routen zum Container abrufen
5. Route auswählen
6. CSV-Datei herunterladen
7. CSV-Datei einlesen
8. Grenzwertverletzungen berechnen
9. Statistiken berechnen
10. Diagramme erstellen
11. Karte erstellen
12. PDF-Bericht erstellen
```

Die Methode `run()` ist also der zentrale Ablaufplan.

Sie enthält nicht die gesamte Detail-Logik, sondern ruft die passenden Methoden der anderen Klassen auf.

---

## 7. Zusammenspiel in `run()`

In `run()` sieht man besonders gut, wie die Klassen zusammenarbeiten.

Beispiel:

```python
containers = self.api_client.fetch_containers()
```

Hier wird der `ApiClient` verwendet, um Container vom Server zu holen.

Danach:

```python
data_frame = self.data_processor.read_csv_file(csv_path)
```

Hier wird der `DataProcessor` verwendet, um die CSV-Datei einzulesen.

Später:

```python
charts = self.output_creator.create_charts(data_frame, selected_container, selected_route)
```

Hier wird der `OutputCreator` verwendet, um Diagramme zu erstellen.

Die Hauptklasse verbindet also die einzelnen Schritte.
