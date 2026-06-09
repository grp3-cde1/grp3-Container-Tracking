# Messdaten einlesen und auswerten

## Ziel dieses Tutorials

In diesem Tutorial wird die Datei `data_processor.py` erklärt.

Der Fokus liegt auf der OOP-Struktur der Klasse `DataProcessor` und darauf, welche Aufgabe sie in unserer Retrospective-App übernimmt.

```text
Warum gibt es diese Klasse?
Welche Verantwortung hat sie?
Welche Methoden stellt sie bereit?
Wie arbeitet sie mit den Grenzwerten aus config.py?
```

Die Datei befindet sich hier:

```text
apps/retrospective_oop/data_processor.py
```

---

## 1. Aufgabe von `DataProcessor`

Die Klasse `DataProcessor` ist für die Verarbeitung der Messdaten zuständig.

Sie übernimmt den Teil der alten funktionsbasierten App, der mit der CSV-Datei und den Daten gearbeitet hat.

Dazu gehören:

```text
CSV-Datei einlesen
Messwerte vorbereiten
Temperatur- und Feuchtigkeitsverletzungen berechnen
statistische Kennzahlen erstellen
```

Der `DataProcessor` lädt keine Daten vom Server herunter und erstellt keine Diagramme oder PDF-Berichte.

Seine Aufgabe ist klar begrenzt:

```text
DataProcessor = Messdaten einlesen und auswerten
```

---

## 2. Vom funktionsbasierten Code zur Klasse

In der funktionsbasierten Version gab es einzelne Funktionen wie:

```python
read_csv_file(file_path)
calculate_violations(data_frame)
calculate_statistics(data_frame)
```

Diese Funktionen gehörten logisch zusammen, weil sie alle mit der Datenverarbeitung zu tun hatten.

In der OOP-Version werden sie deshalb in einer Klasse gebündelt:

```python
class DataProcessor:
```

---

## 3. Grundstruktur der Klasse

Die Klasse beginnt vereinfacht so:

```python
class DataProcessor:
```

Im Gegensatz zum `ApiClient` braucht der `DataProcessor` nicht zwingend ein eigenes Attribut wie `self.base_url`.

Der Grund ist: Die Klasse muss sich keine Server-Adresse merken.

Sie arbeitet hauptsächlich mit Daten, die ihr als Parameter übergeben werden.

Zum Beispiel:

```python
data_frame = self.data_processor.read_csv_file(csv_path)
statistics = self.data_processor.calculate_statistics(data_frame)
```

Das bedeutet:

```text
Der DataProcessor bekommt Daten übergeben,
verarbeitet sie
und gibt das Ergebnis zurück.
```

---

## 4. Verwendung der Grenzwerte aus `config.py`

Für die Auswertung braucht der `DataProcessor` die Grenzwerte aus `config.py`.

Zum Beispiel:

```python
from .config import TEMP_MIN, TEMP_MAX, HUM_MAX
```

Diese Werte werden verwendet, um zu prüfen, ob Messwerte ausserhalb des erlaubten Bereichs liegen.

Beispiele:

```text
Temperatur unter TEMP_MIN
Temperatur über TEMP_MAX
Feuchtigkeit über HUM_MAX
```

Der Vorteil ist, dass die Grenzwerte nicht direkt im `DataProcessor` fest eingebaut sind.

Wenn sich ein Grenzwert ändert, wird er in `config.py` angepasst und nicht in jeder Methode einzeln.

---

## 5. Methoden der Klasse

Die Klasse `DataProcessor` stellt zentrale Methoden für die Datenverarbeitung bereit:

```text
read_csv_file()        → liest die CSV-Datei ein
calculate_violations() → berechnet Grenzwertverletzungen
calculate_statistics() → erstellt statistische Kennzahlen
```

---

## 6. `read_csv_file(file_path)`

Die Methode `read_csv_file(file_path)` liest die heruntergeladene CSV-Datei ein.

Sie wird später zum Beispiel so verwendet:

```python
data_frame = self.data_processor.read_csv_file(csv_path)
```

Die Methode bekommt den Pfad zur CSV-Datei als Parameter:

```text
file_path
```

Als Ergebnis gibt sie einen DataFrame zurück.

Ein DataFrame ist eine tabellenartige Datenstruktur von Pandas. Darin befinden sich die Messwerte der Route, zum Beispiel:

```text
Zeitstempel
GPS-Koordinaten
Temperatur
Feuchtigkeit
```

---

## 7. `calculate_violations(data_frame)`

Die Methode `calculate_violations(data_frame)` prüft die Messdaten auf Grenzwertverletzungen.

Sie wird später zum Beispiel so verwendet:

```python
data_frame = self.data_processor.calculate_violations(data_frame)
```

Die Methode bekommt den DataFrame als Parameter und ergänzt neue Informationen.

Zum Beispiel kann geprüft werden:

```text
Ist die Temperatur zu tief?
Ist die Temperatur zu hoch?
Ist die Feuchtigkeit zu hoch?
```

Daraus können zusätzliche Spalten entstehen, die anzeigen, ob bei einer Messung ein Grenzwert verletzt wurde.

---

## 8. `calculate_statistics(data_frame)`

Die Methode `calculate_statistics(data_frame)` erstellt Kennzahlen aus den Messdaten.

Sie wird später zum Beispiel so verwendet:

```python
statistics = self.data_processor.calculate_statistics(data_frame)
```

Die Methode gibt diese Werte gesammelt zurück, zum Beispiel als Dictionary.

Diese Statistik wird später vom `OutputCreator` verwendet, um den PDF-Bericht zu erstellen.

---

## 9. Verwendung in `RetrospectiveApp`

Der `DataProcessor` wird in der Hauptklasse `RetrospectiveApp` erstellt.

Dort steht vereinfacht:

```python
self.data_processor = DataProcessor()
```

Danach verwendet die Hauptklasse dieses Objekt im Ablauf:

```python
data_frame = self.data_processor.read_csv_file(csv_path)
data_frame = self.data_processor.calculate_violations(data_frame)
statistics = self.data_processor.calculate_statistics(data_frame)
```

Die Hauptklasse steuert also, wann die Daten verarbeitet werden.

Die konkrete Verarbeitung übernimmt aber der `DataProcessor`.
