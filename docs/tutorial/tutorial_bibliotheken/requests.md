# Requests – REST/HTTP in der Retrospektive-App

`requests` ist die Bibliothek, mit der die Retrospektive-App mit dem Webservice spricht. Sie holt Container, Routen und CSV-Dateien über HTTP.

Bezug zum Code: `apps/retrospective_oop/api_client.py` (Klasse `ApiClient`) bzw. die funktionsbasierte Fassung in `apps/retrospective_app.py`.

---

## 1. Basis-URL

Die Adresse des Webservice wird zentral gespeichert:

```python
BASE_URL = "https://fl-17-240.zhdk.cloud.switch.ch"
```

So muss sie nicht in jeder Anfrage neu geschrieben werden.

---

## 2. Eine GET-Anfrage senden

```python
response = requests.get(f"{BASE_URL}/containers", timeout=10)
```

`timeout=10` sorgt dafür, dass die App nicht ewig wartet, wenn der Server nicht antwortet.

---

## 3. Statuscode prüfen

```python
if response.status_code != 200:
    print("Fehler beim Abrufen der Container:", response.status_code)
    return []
```

`200` bedeutet Erfolg. Nur dann wird weitergearbeitet. Bei einem Fehler gibt die Funktion eine leere Liste zurück – das macht das Programm robust.

---

## 4. JSON-Antwort auslesen

```python
data = response.json()
containers = data.get("containers", [])
```

`.json()` wandelt die Antwort in ein Python-Dictionary um. `.get("containers", [])` liest die Liste – oder gibt `[]` zurück, falls der Schlüssel fehlt.

---

## 5. Ressourcen über die URL ansprechen

Bei REST beschreibt die URL, welche Ressource gemeint ist:

```python
response = requests.get(f"{BASE_URL}/containers/{container}/routes", timeout=10)
```

Hier steht der gewählte Container direkt im Pfad.

---

## 6. Eine Datei herunterladen

```python
csv_url = f"{BASE_URL}/files/{route}.csv?path=../data/migros/{container}/{route}.csv"
response = requests.get(csv_url, timeout=20)
```

---

## 7. Datei lokal speichern

```python
with open(file_path, "wb") as file:
    file.write(response.content)
```

`"wb"` bedeutet „write binary". `response.content` enthält die rohen Bytes der Antwort. Genau so werden CSV-Dateien gespeichert.

---

## Zusammenfassung

```text
requests.get(url)        → Anfrage senden
response.status_code     → Erfolg prüfen (200)
response.json()          → JSON in ein Dictionary
response.content         → rohe Bytes (für Dateien)
```