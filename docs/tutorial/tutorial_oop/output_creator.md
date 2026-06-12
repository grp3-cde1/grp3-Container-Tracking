# Ergebnisse erstellen mit dem `OutputCreator`

## Ziel dieses Tutorials

In diesem Tutorial wird die Datei `output_creator.py` erklärt.

Der Fokus liegt auf der OOP-Struktur der Klasse `OutputCreator` und darauf, welche Aufgabe sie in unserer Retrospective-App übernimmt.

```text
Warum gibt es diese Klasse?
Welche Verantwortung hat sie?
Welche Ausgaben erstellt sie?
Wie verwendet sie die Ergebnisse des DataProcessor?
```

Die Datei befindet sich hier:

```text
apps/retrospective_oop/output_creator.py
```

---

## 1. Aufgabe von `OutputCreator`

Die Klasse `OutputCreator` ist für die Erstellung der Ergebnisse zuständig.

Sie übernimmt den Teil der alten funktionsbasierten App, der Ausgaben erzeugt hat.

Dazu gehören:

```text
Diagramme erstellen
interaktive Karte erstellen
PDF-Bericht erstellen
automatisches Fazit erstellen
```

Der `OutputCreator` holt keine Daten vom Server und berechnet keine Grenzwertverletzungen.

Seine Aufgabe ist klar begrenzt:

```text
OutputCreator = Ergebnisse und Berichte erstellen
```

---

## 2. Vom funktionsbasierten Code zur Klasse

In der funktionsbasierten Version gab es einzelne Funktionen wie:

```python
create_charts(data_frame, container, route)
create_map(data_frame, container, route)
create_pdf_report(container, route, statistics, charts, data_frame)
```

Diese Funktionen gehörten logisch zusammen, weil sie alle Resultate der Analyse sichtbar machen.

In der OOP-Version werden sie deshalb in einer Klasse gebündelt:

```python
class OutputCreator:
```

---

## 3. Warum gibt es keine `__init__()`-Methode?

In unserer Umsetzung braucht `OutputCreator` keine eigene `__init__()`-Methode.

Der Grund ist: Die Klasse muss beim Erstellen des Objekts keine eigenen Startwerte speichern.

Bei `ApiClient` war das anders. Dort wurde die `base_url` im Objekt gespeichert:

```python
self.base_url = base_url
```

Der `OutputCreator` arbeitet aber vor allem mit Daten, die den Methoden direkt übergeben werden.

Zum Beispiel:

```python
charts = self.output_creator.create_charts(data_frame, selected_container, selected_route)
```

Die Methode bekommt also direkt die Informationen, die sie braucht:

```text
data_frame
container
route
```


---

## 4. Verwendung von Daten und Statistik

Der `OutputCreator` arbeitet mit den Ergebnissen, die vorher vom `DataProcessor` erstellt wurden.

```text
data_frame   → Messdaten mit berechneten Grenzwertverletzungen
statistics   → zusammengefasste Kennzahlen
container    → gewählter Container
route        → gewählte Route
```

Wichtig ist:

```text
OutputCreator berechnet die Analyse nicht neu.
Er verwendet die vorbereiteten Daten nur für die Ausgabe.
```

Dadurch bleiben Datenverarbeitung und Ergebnisdarstellung getrennt.

---

## 5. Methoden der Klasse

Die Klasse `OutputCreator` stellt (Hilfs-) Methoden für verschiedene Ausgaben bereit:

```text
build_file_timestamp() → erstellt Timestamp für den Dateinamen
create_temperature_chart() → erstellt Temperatur-Diagramm
create_humidity_chart() → erstellt Feuchtigkeits-Diagramm
create_violation_chart() → erstellt Violation-Diagramm
create_static_route_chart() → erstellt Route
create_charts()      → erstellt Diagramme
create_map()         → erstellt eine interaktive Karte
create_conclusion()  → erstellt ein kurzes Fazit
create_pdf_report()  → erstellt den PDF-Bericht
```

Diese Methoden gehören in dieselbe Klasse, weil sie alle Resultate der Auswertung darstellen.

---

## 6. "Hilfsmethoden"

Die Methoden welche eigen Diagramme aus den Messdaten erstellen, fassen wir hier zusammen.

Die Methoden erstellen jeweils ein eigenes Diagram und danach in der Methode `create_charts()` verwendet:

```python
charts = {
            "temperature": self.create_temperature_chart(data_frame, container, route),
            "humidity": self.create_humidity_chart(data_frame, container, route),
            "violations": self.create_violation_chart(data_frame, container, route),
            "route": self.create_static_route_chart(data_frame, container, route),
        }
```

Die Methoden erhalten den DataFrame sowie Container und Route als Parameter.

---

## 7. `create_charts(data_frame, container, route)`

Wie oben bereits beschrieben erstellt die Methode `create_charts()` Diagramme aus den Messdaten.

Sie wird später zum Beispiel so verwendet:

```python
charts = self.output_creator.create_charts(data_frame, selected_container, selected_route)
```

Dabei ist praktisch, wenn der Bericht angepasst werden will, kann die Methode `create_charts()` angepasst werden, die jeweiligen Hilfsmethoden können bestehen bleiben, erweitert oder gelöscht werden.

---

## 8. `create_map(data_frame, container, route)`

Die Methode `create_map()` erstellt eine interaktive Karte der Route.


Die Methode verwendet die GPS-Koordinaten aus dem DataFrame.

Auf der Karte können die Messpunkte und die Route dargestellt werden. Je nach Umsetzung können auffällige Messpunkte zusätzlich markiert werden.

Am Ende gibt die Methode den Pfad zur gespeicherten HTML-Karte zurück.

Beispiel:

```text
maps/grp3_kriens-horw_map.html
```

Für eine genauere Beschreibung des Inhalts der Methode verweisen wir gerne auf das [folium-Tutorial](https://python-visualization.github.io/folium/latest/)

---

## 9. `create_conclusion(statistics)`

Die Methode `create_conclusion()` erstellt ein kurzes automatisches Fazit.

Die Methode verwendet die Statistikwerte aus dem `DataProcessor`.

Das Ergebnis ist ein kurzer Text, der später im PDF-Bericht verwendet wird.

---

## 10. `create_pdf_report(container, route, statistics, charts)`

Die Methode `create_pdf_report()` erstellt den PDF-Bericht zur Route.

Sie wird so verwendet:

```python
pdf_path = self.output_creator.create_pdf_report(
    selected_container,
    selected_route,
    selected_statistics,
    charts,
)
```

Die Methode bekommt die wichtigsten Informationen:

```text
container   → gewählter Container
route       → gewählte Route
statistics  → berechnete Kennzahlen
charts      → Pfade zu den erstellten Diagrammen
```

Aus diesen Informationen wird ein Bericht erstellt.

Auch hier, besuch gerne [MatPlotLib-Tutorial](https://matplotlib.org/)

---

## 101 Verwendung in `RetrospectiveApp`

Der `OutputCreator` wird in der Hauptklasse `RetrospectiveApp` erstellt.

Dort steht vereinfacht:

```python
self.output_creator = OutputCreator()
```

Danach verwendet die Hauptklasse dieses Objekt im Ablauf:

```python
charts = self.output_creator.create_charts(data_frame, selected_container, selected_route)
map_path = self.output_creator.create_map(data_frame, selected_container, selected_route)
pdf_path = self.output_creator.create_pdf_report(
    selected_container,
    selected_route,
    statistics,
    charts,
)
```

Die Hauptklasse entscheidet also, wann die Ausgaben erstellt werden.

Die konkrete Erstellung übernimmt aber der `OutputCreator`.
