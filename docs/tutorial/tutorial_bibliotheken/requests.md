### 1. Verbindung zum Webservice

Zu Beginn wird die Basis-URL des Cloud-Services festgelegt:

```python
url = 'https://fl-17-240.zhdk.cloud.switch.ch/'
```

Diese URL dient als Ausgangspunkt für alle weiteren HTTP-Requests. Statt die vollständige Adresse bei jeder Anfrage erneut zu schreiben, wird sie in einer Variablen gespeichert.

Danach wird der erste Request ausgeführt:

```python
response_container = requests.get(f"{url}containers")
```

Hier wird der Endpoint `/containers` aufgerufen. Dieser liefert eine Übersicht über alle verfügbaren Container.

---

### 2. Statuscode prüfen

Nach einem HTTP-Request sollte immer geprüft werden, ob die Anfrage erfolgreich war:

```python
if response_container.status_code == 200:
```

Der Statuscode `200` bedeutet, dass der Request erfolgreich verarbeitet wurde. Nur in diesem Fall wird mit den erhaltenen Daten weitergearbeitet.

Falls der Request fehlschlägt, wird eine Fehlermeldung ausgegeben:

```python
print("Fehler beim Abrufen der Container: ", response_container.status_code)
```

Diese Prüfung ist wichtig, damit das Programm nicht mit ungültigen oder fehlenden Daten weiterläuft.

---

### 3. JSON-Antwort verarbeiten

Die Antwort des Webservices wird in ein Python-Objekt umgewandelt:

```python
data_container = response_container.json()
```

In diesem Fall handelt es sich um ein Dictionary. Daraus wird anschliessend die Liste der Container gelesen:

```python
containers = data_container.get("containers", [])
```

Mit `.get("containers", [])` wird der Wert zum Schlüssel `"containers"` gelesen. Falls der Schlüssel nicht vorhanden ist, wird stattdessen eine leere Liste verwendet. Dadurch wird das Programm robuster.

---

### 4. Container im Terminal anzeigen

Die verfügbaren Container werden nummeriert ausgegeben:

```python
for i, container in enumerate(containers, start=1):
    print(f"{i}. {container}")
```

Hier wird `enumerate()` verwendet, um jeder Ausgabe automatisch eine Nummer zu geben. Das ist praktisch, weil die Benutzerin oder der Benutzer später einfach eine Zahl eingeben kann.

Beispielausgabe:

```text
1. frodo
2. grp3
3. alpha
```

---

### 5. Benutzerauswahl mit Fehlerbehandlung

Anschliessend wird ein Container ausgewählt:

```python
index = int(input("Wähle einen Container (Nummer): ")) - 1
chosen_container = containers[index]
```

Da Listen in Python bei Index `0` beginnen, die Anzeige aber bei `1`, wird `1` abgezogen.

Zusätzlich wird die Eingabe mit `try/except` abgesichert:

```python
except (ValueError, IndexError):
    print("Ungültige Auswahl.")
    exit()
```

Dabei werden zwei mögliche Fehler behandelt:

- `ValueError`: wenn keine gültige Zahl eingegeben wurde
- `IndexError`: wenn die eingegebene Nummer ausserhalb der Liste liegt

Damit wird verhindert, dass das Programm bei einer falschen Eingabe abstürzt.

---

### 6. Routen des gewählten Containers abrufen

Sobald ein gültiger Container gewählt wurde, werden dessen Routen geladen:

```python
response_route = requests.get(f"{url}containers/{chosen_container}/routes")
```

Dieser Endpoint enthält den gewählten Container direkt im Pfad. Das ist ein typisches Muster bei REST-Schnittstellen: Die URL beschreibt genau, welche Ressource angefragt wird.

Auch hier wird wieder geprüft, ob der Request erfolgreich war:

```python
if response_route.status_code == 200:
```

Danach wird erneut die JSON-Antwort verarbeitet:

```python
data_route = response_route.json()
routes = data_route.get("routes", [])
```

Die Routen werden danach wie schon die Container im Terminal angezeigt.

---

### 7. Route auswählen

Die Auswahl der Route funktioniert nach demselben Prinzip wie die Auswahl des Containers:

```python
for i, route in enumerate(routes, start=1):
    print(f"{i}. {route}")
```

Danach wird eine Nummer eingelesen und in den passenden Listeneintrag übersetzt:

```python
index = int(input("Wähle eine Route (Nummer): ")) - 1
chosen_route = routes[index]
```

Auch hier sorgt `try/except` dafür, dass ungültige Eingaben sauber abgefangen werden.

---

### 8. CSV-Datei herunterladen

Sobald Container und Route feststehen, wird die URL zur CSV-Datei zusammengesetzt:

```python
csv_url = f"{url}files/{chosen_route}.csv?path=../data/migros/{chosen_container}/{chosen_route}.csv"
```

Diese URL verweist auf die konkrete Route als CSV-Datei.

Danach wird erneut ein `GET`-Request ausgeführt:

```python
response_csv = requests.get(csv_url)
```

Wenn der Download erfolgreich war, wird die Datei lokal gespeichert.

---

### 9. Datei lokal speichern

Die empfangenen CSV-Daten werden im `data`-Ordner gespeichert:

```python
filename = f"data/{chosen_container}_{chosen_route}.csv"
```

Dann wird die Datei im Binärmodus geschrieben:

```python
with open(filename, "wb") as f:
    f.write(response_csv.content)
```

Hier ist `response_csv.content` wichtig: Damit werden die rohen Daten der Antwort gespeichert.

Die Ausgabe bestätigt anschliessend den Erfolg:

```python
print(f"CSV gespeichert als {filename}")
```

