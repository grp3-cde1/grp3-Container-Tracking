# Tutorial: Funktionsbasierte Retrospektive-App

## Ziel

In diesem Tutorial bauen wir eine Retrospektive-App für Container-Tracking.

Die App wertet abgeschlossene Transporte aus. Wir arbeiten mit echten Transportdaten und nutzen mehrere wichtige Python-Bibliotheken.

Die App kann:

- Container über eine REST-API abrufen
- Routen zu einem Container abrufen
- CSV-Dateien herunterladen
- Daten mit pandas einlesen
- Grenzwertverletzungen berechnen
- Diagramme mit matplotlib erzeugen
- Karten mit folium erstellen
- PDF-Berichte mit reportlab erzeugen

Die App bleibt in diesem Schritt bewusst funktionsbasiert.

---

## Voraussetzungen

Du solltest bereits diese Grundlagen kennen:

- Variablen
- Listen
- Dictionaries
- Bedingungen
- Schleifen
- Funktionen
- einfache Dateioperationen

Dieses Tutorial erklärt nicht Python von Grund auf. Es zeigt, wie man vorhandenes Wissen praktisch in einem Projekt einsetzt.

---

## Warum Funktionen?

Am Anfang könnte man den ganzen Code einfach untereinander schreiben.

Das funktioniert bei kleinen Programmen. Bei grösseren Programmen wird es aber schnell unübersichtlich.

Darum teilen wir die App in Funktionen auf.

Beispiele:

```python
def fetch_containers():
    pass

def read_csv_file(file_path):
    pass

def create_pdf_report():
    pass
```

Jede Funktion hat eine klare Aufgabe.

Das macht den Code:

- übersichtlicher
- einfacher zu testen
- einfacher zu erklären
- einfacher zu erweitern

---
