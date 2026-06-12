# Tutorial: Objektorientierte Retrospective-App

## Ziel des Tutorials

In diesem Tutorial bauen wir eine objektorientierte Version der Retrospective-App für Container-Tracking.

Die App analysiert einen abgeschlossenen Transport. Dabei werden Messdaten wie Zeitstempel, GPS-Koordinaten, Temperatur und Feuchtigkeit ausgewertet. Am Ende erstellt die App Diagramme, eine interaktive Karte und einen PDF-Bericht.

Der Schwerpunkt dieses Tutorials liegt nicht nur auf dem fertigen Code, sondern vor allem auf dem Verständnis von objektorientierter Programmierung. Wir lernen, wie man ein grösseres Programm sinnvoll in Klassen aufteilt und warum bestimmte Designentscheidungen getroffen wurden.

Am Ende kannst du erklären:

- was Klassen und Objekte sind
- was Attribute und Methoden sind
- wofür `self` verwendet wird
- welche Aufgabe `__init__()` hat
- warum wir die App in mehrere Dateien aufteilen
- warum die Klassen `ApiClient`, `DataProcessor`, `OutputCreator` und `RetrospectiveApp` sinnvoll sind
- welche alternativen Designs möglich wären

---

## 1. Ausgangslage: Die funktionsbasierte Retrospective-App

Die ursprüngliche Retrospective-App war funktionsbasiert aufgebaut. Das bedeutet, dass die App aus mehreren einzelnen Funktionen bestand.

Zum Beispiel:

```python
fetch_containers()
fetch_routes(container)
download_csv(container, route)
read_csv_file(file_path)
calculate_violations(data_frame)
calculate_statistics(data_frame)
create_charts(data_frame, container, route)
create_map(data_frame, container, route)
create_pdf_report(container, route, statistics, charts)
main()
```

Diese Struktur ist grundsätzlich gut verständlich. Jede Funktion hat eine bestimmte Aufgabe. Die Funktion `main()` verbindet alle Einzelschritte und steuert den Ablauf der App.

Bei kleineren Programmen ist ein funktionsbasierter Aufbau oft völlig ausreichend. Wenn ein Projekt jedoch grösser wird, kann es schwieriger werden, den Überblick zu behalten. Die Funktionen gehören dann zwar logisch zusammen, sind aber nicht klar nach Verantwortlichkeiten gruppiert.

Bei unserer App gibt es verschiedene Aufgabenbereiche:

- Daten vom Server abrufen
- CSV-Dateien einlesen und analysieren
- Diagramme, Karten und PDF-Berichte erstellen
- den gesamten Ablauf der App koordinieren

Genau hier hilft objektorientierte Programmierung.

---

## 2. Warum objektorientierte Programmierung?

Objektorientierte Programmierung, kurz OOP, hilft dabei, ein Programm nach Verantwortlichkeiten zu strukturieren.

Anstatt nur einzelne Funktionen zu schreiben, erstellt man Klassen. Eine Klasse bündelt Daten und Funktionen, die logisch zusammengehören.

Eine Klasse kann man sich wie einen Bauplan vorstellen. Aus diesem Bauplan können Objekte erstellt werden. Diese Objekte besitzen eigene Daten und können bestimmte Aktionen ausführen.

Ein einfaches Beispiel:

```python
class Auto:
    def __init__(self, marke, farbe):
        self.marke = marke
        self.farbe = farbe

    def fahren(self):
        print("Das Auto fährt.")
```

Die Klasse `Auto` ist der Bauplan. Ein konkretes Objekt könnte so erstellt werden:

```python
mein_auto = Auto("BMW", "schwarz")
```

`mein_auto` ist dann ein konkretes Objekt der Klasse `Auto`.

In unserer Retrospective-App verwenden wir dieses Prinzip, um die App sauber aufzuteilen. Wir gruppieren nach Aufgabenbereich, anstatt alle Funktionen "einfach so" nacheinander aufzureihen.

---

## 3. Wie plant man Klassen?

Bei der Planung einer objektorientierten App stellt man sich eine zentrale Frage:

> Welche Teile des Programms gehören logisch zusammen?

In unserer App gibt es drei grosse Arbeitsbereiche.

Der erste Arbeitsbereich ist der Zugriff auf den Webservice. Dazu gehören API-Anfragen, Serverantworten und der CSV-Download. Deshalb erstellen wir dafür die Klasse `ApiClient`.

Der zweite Arbeitsbereich ist die Datenverarbeitung. Dazu gehören das Einlesen der CSV-Datei, das Berechnen von Temperatur- und Feuchtigkeitsverletzungen sowie das Erstellen von Kennzahlen. Deshalb erstellen wir dafür die Klasse `DataProcessor`.

Der dritte Arbeitsbereich ist die Ausgabe der Ergebnisse. Dazu gehören Diagramme, Karten und PDF-Berichte. Deshalb erstellen wir dafür die Klasse `OutputCreator`.

Zusätzlich brauchen wir eine Klasse, welche den Gesamtablauf koordiniert. Diese Klasse heisst `App`.

---

## 4. Grundidee unseres Designs

Wir teilen die App in vier zentrale Klassen auf:

```text
ApiClient
DataProcessor
OutputCreator
RetrospectiveApp
```

Jede Klasse hat eine klare Verantwortung.

`ApiClient` kümmert sich um alles, was mit dem Server zu tun hat. Sie ruft Container und Routen ab und lädt CSV-Dateien herunter.

`DataProcessor` steuert die Verarbeitung der Messdaten. Sie liest CSV-Dateien ein, berechnet Grenzwertverletzungen und erstellt statistische Kennzahlen.

`OutputCreator` beinhaltet alle Ausgaben. Sie erstellt Diagramme, eine interaktive Karte und den PDF-Bericht.

`APP` ist die Hauptklasse. Sie steuert den gesamten Ablauf und verbindet die anderen Klassen miteinander.

Diese Aufteilung folgt dem Prinzip der klaren Verantwortlichkeiten. Jede Klasse soll möglichst nur für einen Aufgabenbereich zuständig sein.

---

## 5. Warum nicht einfach eine grosse Klasse?

Eine mögliche Alternative wäre eine einzige grosse Klasse:

```python
class RetrospectiveApp:
    def fetch_containers(self):
        ...

    def fetch_routes(self, container):
        ...

    def download_csv(self, container, route):
        ...

    def read_csv_file(self, file_path):
        ...

    def calculate_statistics(self, data_frame):
        ...

    def create_pdf_report(self):
        ...
```

Das wäre zwar objektorientiert, aber nicht besonders sauber. Die Klasse hätte zu viele Aufgaben. Sie würde gleichzeitig API-Client, Datenverarbeiter, Diagramm-Ersteller, Karten-Ersteller, PDF-Generator und Ablaufsteuerung sein.

Das Problem dabei ist: Wenn eine Klasse zu viele Verantwortlichkeiten hat, wird sie schwer zu verstehen, schwer zu testen und schwer zu erweitern.

Deshalb teilen wir die App bewusst in mehrere kleinere Klassen auf.

---

## 6. Warum nicht für alles eine eigene Klasse?

Man könnte auch sehr viele kleine Klassen erstellen, zum Beispiel:

```text
ContainerService
RouteService
CsvDownloader
CsvReader
ViolationCalculator
StatisticsCalculator
TemperatureChartCreator
HumidityChartCreator
MapCreator
PdfCreator
```

Das wäre theoretisch möglich. Für ein grosses professionelles Projekt kann eine solche Aufteilung sinnvoll sein.

Für unser Projekt wäre das aber zu komplex. Die App würde aus sehr vielen kleinen Dateien bestehen, obwohl die Logik noch überschaubar ist.

Deshalb wählen wir einen Mittelweg:

```text
ApiClient        → Server und Download
DataProcessor    → CSV und Analyse
OutputCreator    → Diagramme, Karte und PDF
RetrospectiveApp → Ablaufsteuerung
```

Diese Struktur ist sauber, aber noch einfach genug, um sie gut zu verstehen.

---

## 7. Vorteile unseres Designs

Unser Design hat mehrere Vorteile.

1. Die App ist übersichtlicher. Jede Datei und jede Klasse hat eine klare Aufgabe.

2. Der Code kann einfacher abgeändert werden (Wartung). Wenn sich zum Beispiel die API ändert, müssen wir hauptsächlich `api_client.py` anpassen. Wenn wir den PDF-Bericht ändern möchten, arbeiten wir vor allem in `output_creator.py`.

3. Die App ist besser erweiterbar. Wenn später weitere Ausgaben dazukommen, zum Beispiel ein Excel-Bericht, kann man diese Erweiterung im Bereich `OutputCreator` ergänzen, ohne den API-Zugriff oder die Datenverarbeitung zu verändern.

---

## 8. Projektstruktur

Die objektorientierte Version der App wird in mehrere Dateien aufgeteilt:

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

Die genaue Erklärung der Projektstruktur befindet sich im Klassentutorial [`struktur.md`](struktur.md).

---

## 9. Grundbegriffe der objektorientierten Programmierung

Bevor wir den Code der App im Detail anschauen, müssen einige Grundbegriffe der objektorientierten Programmierung verstanden werden.

Die wichtigsten Begriffe sind:

```text
Klasse
Objekt
Attribut
Methode
self
__init__()
```

Diese Begriffe erklären wir direkt anhand unserer Retrospective-App.

---

## 9.1 Klasse

Wie bereits beschrieben ist eine Klasse ein Bauplan für Objekte.

In unserer App gibt es zum Beispiel die Klasse `ApiClient`:

```python
class ApiClient:
    """
    Verantwortlich für die Kommunikation mit dem Webservice.
    """
```

Diese Klasse beschreibt, was ein API-Client können soll. Der API-Client ist zuständig dafür, Daten vom Webservice abzurufen und CSV-Dateien herunterzuladen.

Die Klasse selbst führt aber noch nichts aus. Sie ist zuerst nur der Bauplan.

---

## 9.2 Objekt

Ein Objekt entsteht, wenn eine Klasse verwendet wird.

In unserer Hauptklasse `RetrospectiveApp` erstellen wir ein Objekt der Klasse `ApiClient`:

```python
self.api_client = ApiClient()
```

Dadurch wird ein konkreter API-Client erstellt.

Dieses Objekt kann danach Methoden ausführen, zum Beispiel:

```python
self.api_client.fetch_containers()
```

Das bedeutet:

> Verwende das konkrete `ApiClient`-Objekt und rufe darauf die Methode `fetch_containers()` auf.

Aus einer Klasse können auch mehrere Objekte erstellt werden. In unserem Projekt brauchen wir aber nur ein `ApiClient`-Objekt, weil wir nur mit einem Webservice arbeiten.

Unterschied Klasse und Objekt:

```text
Klasse = Bauplan
Objekt = konkretes Exemplar aus diesem Bauplan
```

---

## 9.3 Methode

Eine Methode ist eine Funktion innerhalb einer Klasse.

Beispiel:

```python
class ApiClient:
    def fetch_containers(self):
        ...
```

`fetch_containers()` ist eine Methode der Klasse `ApiClient`.

Der Unterschied zu einer normalen Funktion ist, dass eine Methode zu einem Objekt gehört.

Eine normale Funktion wird so aufgerufen:

```python
fetch_containers()
```

Eine Methode wird über ein Objekt aufgerufen:

```python
self.api_client.fetch_containers()
```

Das bedeutet:

> Führe `fetch_containers()` auf dem gespeicherten `ApiClient`-Objekt aus.

---

## 9.4 Attribut

Ein Attribut ist eine Variable, die in einem Objekt gespeichert ist.

In der Klasse `ApiClient` speichern wir zum Beispiel die Basis-URL des Webservice:

```python
class ApiClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
```

Hier ist `self.base_url` ein Attribut.

Es gehört nicht nur kurzfristig zur Methode `__init__()`, sondern wird dauerhaft im Objekt gespeichert.

Dadurch kann jede Methode der Klasse später darauf zugreifen:

```python
response = requests.get(f"{self.base_url}/containers", timeout=10)
```

Das ist praktisch, weil die URL nicht in jeder Methode neu übergeben werden muss. Das Objekt merkt sie sich selbst.

---

## 9.5 `__init__()`

`__init__()` ist eine spezielle Methode in Python.

Sie wird automatisch ausgeführt, wenn ein neues Objekt erstellt wird.

Beispiel:

```python
api_client = ApiClient()
```

Dabei wird automatisch diese Methode ausgeführt:

```python
def __init__(self, base_url=BASE_URL):
    self.base_url = base_url
```

Die Aufgabe von `__init__()` ist es, ein neues Objekt vorzubereiten und wichtige Startwerte zu speichern.

In unserem Beispiel wird beim Erstellen eines `ApiClient`-Objekts die API-Adresse gespeichert.

Das bedeutet:

```python
api_client = ApiClient()
```

führt dazu, dass im Objekt gespeichert wird:

```python
api_client.base_url = "https://fl-17-240.zhdk.cloud.switch.ch"
```

Man ruft `__init__()` normalerweise nicht direkt auf. Python macht das automatisch beim Erstellen eines Objekts.

---

## 9.6 `self`

`self` ist ein wichtiger Begriff in der objektorientierten Programmierung. 

Ein einfacher Merksatz ist:

```text
self = dieses Objekt selbst
```

Das bedeutet: `self` zeigt immer auf das konkrete Objekt, mit dem gerade gearbeitet wird.

---

### 9.6.1. Wo steht `self` in unserem Code?

Wir verwenden `self` zum Beispiel in der Klasse `ApiClient`:

```python
class ApiClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def fetch_containers(self):
        response = requests.get(f"{self.base_url}/containers", timeout=10)
```

Hier sieht man `self` an drei wichtigen Stellen:

```python
def __init__(self, base_url=BASE_URL):
```

```python
self.base_url = base_url
```

```python
def fetch_containers(self):
```

---

### 9.6.2. Warum steht `self` in der Methode?

Eine Methode gehört immer zu einem Objekt.

Wenn wir später ein Objekt aus der Klasse erstellen:

```python
api_client = ApiClient()
```

dann entsteht ein konkretes `ApiClient`-Objekt.

Dieses Objekt kann danach Methoden ausführen:

```python
api_client.fetch_containers()
```

Beim Aufruf schreiben wir `self` nicht in die Klammer. Python übergibt das Objekt automatisch an `self`.

Vereinfacht kann man sich das so vorstellen:

```text
api_client.fetch_containers()
```

bedeutet intern ungefähr:

```text
Führe fetch_containers() mit dem Objekt api_client aus.
```

Innerhalb der Methode ist `self` also dieses konkrete Objekt `api_client`.

---

### 9.6.3. Warum brauchen wir `self.base_url`?

In der Klasse `ApiClient` speichern wir beim Erstellen des Objekts die Basis-URL:

```python
def __init__(self, base_url=BASE_URL):
    self.base_url = base_url
```

Diese Zeile:

```python
self.base_url = base_url
```

bedeutet:

```text
Speichere die base_url in diesem konkreten ApiClient-Objekt.
```

Dadurch merkt sich das Objekt die URL.

Später kann eine andere Methode wieder darauf zugreifen:

```python
def fetch_containers(self):
    response = requests.get(f"{self.base_url}/containers", timeout=10)
```

Hier bedeutet:

```python
self.base_url
```

```text
Nimm die base_url, die in diesem ApiClient-Objekt gespeichert ist.
```

Ohne `self` wäre `base_url` nur eine normale lokale Variable und nach `__init__()` nicht mehr verfügbar.

---

### 9.6.4. Unterschied zwischen `base_url` und `self.base_url`

Diese beiden Begriffe sehen ähnlich aus, haben aber unterschiedliche Bedeutungen.

```python
base_url
```

ist ein Parameter der Methode `__init__()`.

```python
self.base_url
```

ist ein Attribut des Objekts.

Das bedeutet:

```python
def __init__(self, base_url=BASE_URL):
    self.base_url = base_url
```

Rechts steht der Wert, der übergeben wird:

```python
base_url
```

Links wird dieser Wert im Objekt gespeichert:

```python
self.base_url
```

Man kann die Zeile so lesen:

```text
Speichere den Parameter base_url im Objekt unter self.base_url.
```

---

### 9.6.5. Warum steht manchmal `self.api_client = ApiClient()`?

In der Klasse `RetrospectiveApp` verwenden wir `self` ebenfalls:

```python
class RetrospectiveApp:
    def __init__(self):
        self.api_client = ApiClient()
        self.data_processor = DataProcessor()
        self.output_creator = OutputCreator()
```

Hier bedeutet:

```python
self.api_client = ApiClient()
```

```text
Erstelle ein neues ApiClient-Objekt und speichere es in dieser RetrospectiveApp.
```

Wichtig ist die Trennung:

```python
self.api_client
```

ist der Speicherplatz im aktuellen `RetrospectiveAp`-Objekt.

```python
ApiClient()
```

erstellt ein neues Objekt aus der Klasse `ApiClient`.

Die ganze Zeile bedeutet also:

```text
Die RetrospectiveApp erstellt einen ApiClient und merkt ihn sich.
```

Dadurch kann die RetrospectiveApp später in der Methode `run()` wieder darauf zugreifen:

```python
containers = self.api_client.fetch_containers()
```

Hier bedeutet:

```python
self.api_client
```

```text
Nimm den ApiClient, der in dieser App gespeichert wurde.
```

---

### 9.6.6. Merksätze

```text
self = dieses Objekt selbst
```

```text
self.attribut = Wert im Objekt speichern
```

```text
self.methode() = Methode dieses Objekts aufrufen
```

```text
Beim Definieren einer Methode schreibt man self.
Beim Aufrufen der Methode schreibt man self nicht selbst.
```

Beispiel:

```python
class ApiClient:
    def fetch_containers(self):
        ...
```

Aufruf:

```python
api_client.fetch_containers()
```

Python übergibt das Objekt automatisch an `self`.

---

### 9.6.9. Kurz zusammengefasst

`self` verbindet eine Methode mit dem Objekt, zu dem sie gehört.

Ohne `self` könnte ein Objekt keine eigenen Werte speichern und später wiederverwenden.

In unserer App brauchen wir `self`, damit:

- `ApiClient` seine `base_url` speichern kann
- `OutputCreator` eigene Methoden aufrufen kann
- `RetrospectiveApp` ihre Hilfsobjekte speichern und später verwenden kann

Deshalb ist `self` ein zentraler Bestandteil der objektorientierten Version unserer Retrospective-App.


## 9.7 Zusammenspiel der Begriffe

Am Beispiel `ApiClient` sieht man alle Begriffe zusammen:

```python
class ApiClient:
    """
    Verantwortlich für die Kommunikation mit dem Webservice.
    """

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def fetch_containers(self):
        response = requests.get(f"{self.base_url}/containers", timeout=10)
        ...
```

Erklärung:

```text
ApiClient          = Klasse
api_client         = Objekt
__init__()         = Startmethode beim Erstellen des Objekts
self.base_url      = Attribut
fetch_containers() = Methode
self               = das aktuelle Objekt
```

Diese Begriffe bilden die Grundlage für die objektorientierte Version unserer Retrospective-App.

---

## 10 Praxis

Anhand der vorgestellten Konzepte kann nun das File "retrospective_app.py" zu einem OOP-Projekt umgesetzt werden.
Der Code besteht funktionsbasiert, anhand der vorgestellten Struktur und den unten ersichtlichen Tutorials zu den einzelnen Klassen, kann die Retrospektive-App wie im Ordner "retrospective-oop" nachgebaut werden.

Besonders ist das Tutorial zur Struktur hervorzuheben, darin wird gezeigt wie man ein OOP strukturiert.

---

## 11 Klassen Tutorials
Folgend sind alle Klassen erklärt.

Die Tutorials sind einzeln und deckungsgleich Aufgebaut, damit die Redundanz dient der ständigen Wiederholung und Visualisierung des OOPs. 

Es ist beabsichtigt, dass nicht ganze Code-Snippets im Tutorial stehen, die "Fertige" Lösung findest du im Projektordner.

- [struktur.md](tutorial_oop/struktur.md)
- [config.md](tutorial_oop/config.md)
- [api_client](tutorial_oop/api_client.md)
- [data_processor](tutorial_oop/data_processor.md)
- [output_creator](tutorial_oop/output_creator.md)
- [RetrospectiveApp](tutorial_oop/app.md)


