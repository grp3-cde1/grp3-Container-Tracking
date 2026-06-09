# Daten vom Server holen

## Ziel dieses Tutorials

In diesem Tutorial wird die Datei `api_client.py` erklärt.

Der Fokus liegt auf der OOP-Struktur der Klasse `ApiClient` und darauf, welche Aufgabe sie in unserer Retrospective-App übernimmt.

```text
Warum gibt es diese Klasse?
Welche Verantwortung hat sie?
Welche Methoden stellt sie bereit?
Wie wird sie von der Hauptklasse verwendet?
```

Die Datei befindet sich hier:

```text
apps/retrospective_oop/api_client.py
```

---

## 1. Aufgabe von `ApiClient`

Die Klasse `ApiClient` ist für den Zugriff auf den Webservice zuständig.

Sie übernimmt den Teil der alten funktionsbasierten App, der Daten vom Server geholt hat.

Dazu gehören:

```text
Container abrufen
Routen zu einem Container abrufen
CSV-Datei herunterladen
```

Der `ApiClient` analysiert keine Messdaten und erstellt keine Diagramme oder PDF-Berichte.

Seine Aufgabe ist klar begrenzt:

```text
ApiClient = Server-Zugriff und CSV-Download
```

---

## 2. Vom funktionsbasierten Code zur Klasse

In der funktionsbasierten Version gab es einzelne Funktionen wie:

```python
fetch_containers()
fetch_routes(container)
download_csv(container, route)
```

Diese Funktionen gehörten logisch zusammen, weil sie alle mit dem Webservice gearbeitet haben.

In der OOP-Version werden diese Funktionen deshalb in einer Klasse gebündelt:

```python
class ApiClient:
```

Dadurch entsteht ein eigener Aufgabenbereich für den Server-Zugriff.

---

## 3. Grundstruktur der Klasse

Die Klasse beginnt vereinfacht so:

```python
class ApiClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
```

Beim Erstellen eines `ApiClient`-Objekts wird die Basis-URL des Webservice gespeichert.

Diese Basis-URL kommt aus `config.py`:

```python
from .config import BASE_URL, DATA_DIR
```

Dadurch muss die URL nicht direkt im `ApiClient` fest eingebaut werden. Sie wird zentral in `config.py` verwaltet.

---

## 4. `__init__()` und `self.base_url`

Die Methode `__init__()` wird automatisch ausgeführt, wenn ein neues `ApiClient`-Objekt erstellt wird.

```python
def __init__(self, base_url=BASE_URL):
    self.base_url = base_url
```

Die Zeile:

```python
self.base_url = base_url
```

speichert die API-Adresse im Objekt.

Wie bereits erklärt, ist das wichtig, da mehrere Methoden der Klasse diese Adresse brauchen.


---

## 5. Methoden der Klasse

Die Klasse `ApiClient` stellt drei zentrale Methoden bereit. Diese sind deckungsgleich zu den oben erwähnten Funktionen in der ersten Datei vor OOP.

```text
fetch_containers() → ruft verfügbare Container ab
fetch_routes()     → ruft Routen zu einem Container ab
download_csv()     → lädt die CSV-Datei einer Route herunter
```

---

## 6. `fetch_containers()`

Die Methode `fetch_containers()` ruft alle verfügbaren Container vom Server ab.

In der Hauptklasse wird sie später so verwendet:

```python
containers = self.api_client.fetch_containers()
```

Die Methode sendet eine Anfrage an den Webservice und gibt eine Liste von Container-IDs zurück.

Beispiel für eine mögliche Rückgabe:

```python
["grp1", "grp2", "grp3"]
```

Falls ein Fehler passiert, gibt die Methode eine leere Liste zurück.


---

## 7. `fetch_routes(container)`

Die Methode `fetch_routes(container)` ruft alle Routen zu einem bestimmten Container ab.

Sie wird später zum Beispiel so verwendet:

```python
routes = self.api_client.fetch_routes(selected_container)
```

Die Methode braucht den Parameter `container`, damit sie weiss, für welchen Container die Routen abgefragt werden sollen.

Beispiel:

```python
self.api_client.fetch_routes("grp3")
```

Die Methode gibt eine Liste von Routen zurück, zum Beispiel:

```python
["kriens-horw", "luzern-horw"]
```

Auch hier gilt: Wenn ein Fehler passiert, wird eine leere Liste zurückgegeben.

---

## 8. `download_csv(container, route)`

Die Methode `download_csv(container, route)` lädt die CSV-Datei zu einer ausgewählten Route herunter.

Sie wird später so verwendet:

```python
csv_path = self.api_client.download_csv(selected_container, selected_route)
```

Die Methode braucht zwei Informationen:

```text
container → welcher Container?
route     → welche Route?
```

Aus diesen beiden Werten erstellt der `ApiClient` den passenden Download-Endpunkt und speichert die CSV-Datei lokal im Datenordner.

Am Ende gibt die Methode den Pfad zur gespeicherten Datei zurück.

Beispiel:

```text
data/grp3_kriens-horw.csv
```

Falls der Download fehlschlägt, gibt die Methode `None` zurück. Dadurch kann die Hauptklasse erkennen, dass der Ablauf nicht fortgesetzt werden soll.

---

## 9. Verwendung in `RetrospectiveApp`

Der `ApiClient` wird in der Hauptklasse `RetrospectiveApp` erstellt.

Dort steht vereinfacht:

```python
self.api_client = ApiClient()
```

Damit erstellt die App ein Objekt der Klasse `ApiClient` und speichert es in sich selbst.

Später kann die App dieses Objekt verwenden:

```python
containers = self.api_client.fetch_containers()
routes = self.api_client.fetch_routes(selected_container)
csv_path = self.api_client.download_csv(selected_container, selected_route)
```

Die Hauptklasse steuert also den Ablauf, während der `ApiClient` die Server-Kommunikation übernimmt.