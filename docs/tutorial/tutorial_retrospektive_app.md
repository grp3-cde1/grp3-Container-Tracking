# Tutorial: Funktionsbasierte Retrospektive-App

## Ziel des Tutorials

In diesem Tutorial bauen wir eine Retrospektive-App für Container-Tracking.

Die App analysiert einen abgeschlossenen Transport. Dabei liegt der Fokus auf einem zentralen Konzept: **Funktionen**. Wir lernen nicht nur, wie man Funktionen schreibt – sondern warum sie existieren und wie man sie richtig einsetzt.

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

Diese Daten helfen dabei, einen Transport später zu prüfen. Unsere Retrospektive-App beantwortet Fragen wie:

- War die Temperatur immer im erlaubten Bereich?
- War die Feuchtigkeit zu hoch?
- Wo auf der Route gab es Probleme?
- Wie kann man die Ergebnisse verständlich darstellen?

---

## 2. Voraussetzungen

Du solltest bereits diese Grundlagen kennen:

- Variablen und Datentypen
- Listen und Dictionaries
- Bedingungen und Schleifen
- einfache Dateioperationen

Dieses Tutorial baut darauf auf und zeigt, wie man mit Funktionen grössere Programme sauber strukturiert.

---

## 3. Warum Funktionen?

Am Anfang schreibt man Python-Code oft einfach von oben nach unten. Das nennt man **sequenziellen Code**.

**Ohne Funktionen** würde unsere App so aussehen:

```python
# Schritt 1: Container abrufen
response = requests.get("https://example.com/containers", timeout=10)
data = response.json()
containers = data.get("containers", [])

# Schritt 2: Container anzeigen und auswählen
print("Verfügbare Container")
for number, item in enumerate(containers, start=1):
    print(f"{number}. {item}")
index = int(input("Bitte Nummer wählen: ")) - 1
selected_container = containers[index]

# Schritt 3: Routen abrufen
response = requests.get(f"https://example.com/containers/{selected_container}/routes", timeout=10)
data = response.json()
routes = data.get("routes", [])

# Schritt 4: Routen anzeigen und auswählen
print("Verfügbare Routen")
for number, item in enumerate(routes, start=1):
    print(f"{number}. {item}")
index = int(input("Bitte Nummer wählen: ")) - 1
selected_route = routes[index]

# Schritt 5: CSV herunterladen
# ... und so weiter, über hunderte Zeilen
```

Probleme dabei:

- Der Code wird sehr lang und schwer zu lesen.
- Die Auswahllogik (Schritte 2 und 4) ist fast identisch – aber doppelt geschrieben.
- Wenn man die Auswahl verbessern will, muss man es an zwei Stellen ändern.
- Ein Fehler in Zeile 200 ist schwer zu finden.

**Mit Funktionen** sieht die gleiche Logik so aus:

```python
def fetch_containers():
    ...

def fetch_routes(container):
    ...

def choose_item(title, items):
    ...

def main():
    containers = fetch_containers()
    selected_container = choose_item("Verfügbare Container", containers)

    routes = fetch_routes(selected_container)
    selected_route = choose_item("Verfügbare Routen", routes)
```

`main()` liest sich fast wie ein Plan auf Deutsch. Jede Funktion hat einen klaren Namen und eine einzige Aufgabe.

---

## 4. Das EVA-Prinzip

Jede gut geschriebene Funktion folgt einem einfachen Schema:

```
Eingabe → Verarbeitung → Ausgabe
```

Das nennt man das **EVA-Prinzip**.

Beispiel:

```python
def calculate_statistics(data_frame):   # Eingabe: eine Tabelle
    avg = data_frame["temperature"].mean()  # Verarbeitung: berechnen
    return avg                          # Ausgabe: Ergebnis zurückgeben
```

Bevor du eine Funktion schreibst, stelle dir immer diese drei Fragen:

1. **Was bekommt die Funktion?** (Eingabe / Parameter)
2. **Was macht die Funktion damit?** (Verarbeitung)
3. **Was gibt die Funktion zurück?** (Ausgabe / Rückgabewert)

Dieses Denkmuster hilft dir, Funktionen sauber zu planen, bevor du überhaupt Code schreibst.

---

## 5. Funktionen definieren und aufrufen

Eine Funktion wird mit `def` definiert. Der Code darin ist eingerückt.

```python
def say_hello():
    print("Hallo")
```

Aufgerufen wird sie so:

```python
say_hello()
```

Wichtig: Die Funktion wird erst ausgeführt, wenn sie aufgerufen wird. Die `def`-Zeile alleine tut noch nichts.

---

## 6. Rückgabewerte mit `return`

Viele Funktionen sollen ein Ergebnis zurückgeben. Dafür verwenden wir `return`.

```python
def add_numbers():
    result = 3 + 4
    return result

number = add_numbers()
print(number)  # Ausgabe: 7
```

In unserer App verwenden wir das zum Beispiel so:

```python
containers = fetch_containers()
```

Die Funktion `fetch_containers()` holt Daten vom Server und gibt eine Liste zurück. Diese Liste wird in `containers` gespeichert und kann danach weiterverwendet werden.

---

## 7. Parameter: Informationen übergeben

Manchmal braucht eine Funktion Informationen von aussen. Diese Informationen nennt man **Parameter**.

```python
def greet(name):
    print(f"Hallo {name}")

greet("Lena")   # Ausgabe: Hallo Lena
greet("Jonas")  # Ausgabe: Hallo Jonas
```

Wenn man `greet("Lena")` aufruft, passiert intern folgendes:

```
Aufruf:     greet("Lena")
              ↓
Definition: def greet(name):
              ↓
Zuweisung:  name = "Lena"
              ↓
Ausführung: print(f"Hallo {name}")  →  "Hallo Lena"
```

Der Wert `"Lena"` wird beim Aufruf übergeben und steht innerhalb der Funktion als `name` zur Verfügung.

In unserer App brauchen wir Parameter zum Beispiel hier:

```python
def fetch_routes(container):
    response = requests.get(f"{BASE_URL}/containers/{container}/routes")
    ...
```

Die Funktion kann für jeden beliebigen Container aufgerufen werden:

```python
routes_a = fetch_routes("CONT-001")
routes_b = fetch_routes("CONT-002")
```

Das ist ein zentraler Vorteil von Parametern: **Wiederverwendbarkeit**.

---

## 8. Standardwerte für Parameter

Parameter können einen Standardwert haben. Dann ist die Angabe beim Aufruf optional.

```python
def greet(name, language="de"):
    if language == "de":
        print(f"Hallo {name}")
    else:
        print(f"Hello {name}")

greet("Lena")           # Ausgabe: Hallo Lena (Standardwert wird verwendet)
greet("Lena", "en")     # Ausgabe: Hello Lena (eigener Wert wird übergeben)
```

In unserer App könnte `choose_item` so verwendet werden:

```python
def choose_item(title, items, start=1):
    for number, item in enumerate(items, start=start):
        print(f"{number}. {item}")
    ...
```

Standardwerte eignen sich gut für Optionen, die meistens gleich bleiben, aber gelegentlich angepasst werden müssen.

---

## 9. Scope: Wo gelten Variablen?

Eine wichtige Frage beim Arbeiten mit Funktionen ist: **Wo ist eine Variable sichtbar?**

Das nennt man **Scope** (deutsch: Gültigkeitsbereich).

**Lokale Variablen** existieren nur innerhalb der Funktion:

```python
def calculate():
    result = 42  # lokale Variable
    return result

print(result)  # ❌ Fehler! result existiert hier nicht
```

**Globale Variablen** werden ausserhalb von Funktionen definiert und sind überall sichtbar:

```python
BASE_URL = "https://example.com"  # globale Variable

def fetch_containers():
    response = requests.get(f"{BASE_URL}/containers")  # ✅ BASE_URL ist sichtbar
    ...
```

In unserer App definieren wir Konstanten global, damit alle Funktionen darauf zugreifen können:

```python
BASE_URL = "https://fl-17-240.zhdk.cloud.switch.ch"
TEMP_MIN = 15
TEMP_MAX = 26
HUM_MAX = 72
```

**Faustregel:** Verwende globale Variablen nur für Konstanten (Werte, die sich nie ändern). Alles andere sollte als Parameter übergeben werden.

> **Warum ist das wichtig?**
> Wenn eine Funktion nur über ihre Parameter mit dem Rest des Programms kommuniziert, ist sie viel einfacher zu verstehen und zu testen. Du siehst auf einen Blick, welche Informationen hineingehen und was herauskommt.

---

## 10. Docstrings: Funktionen dokumentieren

Gute Funktionen enthalten eine kurze Beschreibung – einen **Docstring**.

```python
def calculate_violations(data_frame):
    """
    Prüft Messwerte auf Grenzwertverletzungen.

    Parameter:
        data_frame: pandas DataFrame mit Spalten temperature und humidity

    Rückgabe:
        DataFrame mit zusätzlichen Boolean-Spalten für Verletzungen
    """
    ...
```

Docstrings werden mit dreifachen Anführungszeichen geschrieben und stehen direkt nach der `def`-Zeile.

Vorteile:

- Andere (und du selbst in drei Monaten) verstehen sofort, was die Funktion macht.
- Entwicklungsumgebungen zeigen Docstrings als Hilfetext an.
- Sie sind die Grundlage für automatisch generierte Dokumentation.

Eine Funktion ohne Docstring ist wie ein Knopf ohne Beschriftung.

---

## 11. Funktionen rufen Funktionen auf

Eine Funktion kann andere Funktionen aufrufen. Das ist ein zentrales Muster in grösseren Programmen.

```python
def main():
    containers = fetch_containers()       # ruft fetch_containers auf
    container = choose_item("Container", containers)  # ruft choose_item auf

    routes = fetch_routes(container)      # ruft fetch_routes auf
    route = choose_item("Routen", routes) # choose_item wird wiederverwendet!
```

`main()` ist hier die **übergeordnete Funktion**, die andere Funktionen koordiniert. Sie selbst enthält kaum Logik – sie delegiert Aufgaben.

Das ist wie ein Dirigent: Er spielt kein Instrument selbst, aber er weiss, wer was wann spielen soll.

---

## 12. Funktionsstruktur der Retrospektive-App

Unsere App wird in diese Funktionen aufgeteilt. Jede hat genau eine Hauptaufgabe.

```
fetch_containers()              → Liste der verfügbaren Container holen
fetch_routes(container)         → Routen zu einem Container holen
choose_item(title, items)       → Auswahl im Terminal anzeigen
download_csv(container, route)  → CSV-Datei herunterladen und speichern
read_csv_file(file_path)        → CSV-Datei mit pandas einlesen
calculate_violations(df)        → Grenzwertverletzungen berechnen
calculate_statistics(df)        → Kennzahlen zusammenfassen
create_charts(df, container, route) → Diagramme erstellen
create_map(df, container, route)    → Karte erzeugen
create_pdf_report(...)          → PDF-Bericht erstellen
main()                          → Alle Schritte verbinden
```

---

## 13. Die main-Funktion: Alles zusammensetzen

`main()` verbindet alle Funktionen. Sie enthält keine eigene Logik – sie delegiert.

```python
def main():
    # Container auswählen
    containers = fetch_containers()
    selected_container = choose_item("Verfügbare Container", containers)
    if selected_container is None:
        return

    # Route auswählen
    routes = fetch_routes(selected_container)
    selected_route = choose_item("Verfügbare Routen", routes)
    if selected_route is None:
        return

    # Daten laden und auswerten
    csv_path = download_csv(selected_container, selected_route)
    data_frame = read_csv_file(csv_path)
    data_frame = calculate_violations(data_frame)
    statistics = calculate_statistics(data_frame)

    # Ausgaben erstellen
    chart_path = CHARTS_DIR / f"{selected_container}_{selected_route}_temp.png"
    create_temperature_chart(data_frame, chart_path)
    create_map(data_frame, selected_container, selected_route)
    pdf_path = create_pdf_report(selected_container, selected_route, statistics, chart_path)

    print(f"\nBericht erstellt: {pdf_path}")
```

Lies `main()` von oben nach unten: Es liest sich fast wie eine Schritt-für-Schritt-Anleitung auf Deutsch.

---

## 14. Programmstart

Am Ende der Datei steht:

```python
if __name__ == "__main__":
    main()
```

Das bedeutet: Die App startet nur dann, wenn diese Datei direkt ausgeführt wird – nicht, wenn sie von einem anderen Modul importiert wird.

---

## 15. Übungsaufgaben

### Aufgabe 1 – Einfache Funktion mit Rückgabewert

Schreib eine Funktion `format_temperature(value)`, die eine Temperatur als formatierten String zurückgibt.

Erwartetes Ergebnis:
```python
format_temperature(22.3)   # "22.3 °C"
format_temperature(15.0)   # "15.0 °C"
```

---

### Aufgabe 2 – EVA-Analyse

Analysiere diese Funktion nach dem EVA-Prinzip. Was ist Eingabe, Verarbeitung und Ausgabe?

```python
def summarize(values):
    total = sum(values)
    average = total / len(values)
    return average
```

---

### Aufgabe 3 – Parameter und Standardwerte

Erweitere `format_temperature` um einen optionalen Parameter `unit` mit Standardwert `"°C"`.

```python
format_temperature(22.3)         # "22.3 °C"
format_temperature(72.1, "°F")   # "72.1 °F"
```

---

### Aufgabe 4 – Scope verstehen

Was gibt dieses Programm aus? Warum?

```python
x = 10

def add_five():
    x = 20
    return x + 5

result = add_five()
print(x)       # Was steht hier?
print(result)  # Was steht hier?
```

---

### Aufgabe 5 – Funktion mit Docstring

Schreib eine Funktion `count_violations(data_frame)`, die die Anzahl Zeilen zurückgibt, in denen `any_violation` den Wert `True` hat. Füge einen vollständigen Docstring hinzu.

---

## 16. Was du gelernt hast

In diesem Tutorial hast du gelernt:

- warum Funktionen Code übersichtlicher, testbarer und wiederverwendbar machen
- wie man Funktionen definiert und aufruft
- wie man Parameter und Rückgabewerte einsetzt
- wie man Standardwerte für Parameter verwendet
- was Scope bedeutet und warum er wichtig ist
- wie man Funktionen mit Docstrings dokumentiert
- wie das EVA-Prinzip (Eingabe → Verarbeitung → Ausgabe) beim Planen hilft
- wie Funktionen andere Funktionen aufrufen und wie `main()` als Koordinator wirkt
- wie man diese Konzepte in einem echten Projekt anwendet
