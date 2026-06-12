# Tutorial

Ein zentraler Bestandteil dieses Projekts ist ein Tutorial, das sich an Personen richtet, die bereits erste Schritte mit Python gemacht haben und die grundlegenden Konzepte der Sprache beherrschen. 

Ziel ist es nicht, Python von Grund auf neu zu erklären, sondern bestehendes Wissen anhand konkreter, praxisnaher Anwendungen zu vertiefen.

Der Fokus liegt deshalb auf der Frage, wie sich bekannte Grundlagen in einem realen Projekt sinnvoll einsetzen lassen. Statt isolierte Beispiele zu behandeln, orientiert sich das Tutorial direkt an den Anwendungen und Strukturen des Projekts. Dadurch entsteht ein praxisbezogener Zugang, der nicht nur das Verständnis für Python stärkt, sondern auch zeigt, wie Code in einem grösseren Zusammenhang aufgebaut, organisiert und weiterentwickelt werden kann.


## Schritt 0: Voraussetzungen (Need-to-know)

Für dieses Tutorial werden grundlegende Python-Kenntnisse vorausgesetzt. Dazu gehören insbesondere:

- Variablen
- Datentypen
- Listen
- Dictionaries
- Schleifen
- Bedingungen

Diese Inhalte werden im Tutorial nicht im Detail neu eingeführt, sondern vorausgesetzt. Sie bilden die Grundlage, auf der die weiteren Schritte aufbauen.

Falls du eines der oben genannten Themen lernen oder repetieren willst empfehlen wir folgende Webseite:
https://pyflo.net

### Schritt 1: Live-Monitor – Funktionen und prozedurale Programmierung

Wir starten mit der kleineren App, dem Live-Monitor. Er empfängt Live-Daten eines laufenden Transports über MQTT und zeigt sie im Terminal an.

**Behandelte Themen**
- Funktionen definieren und aufrufen
- Parameter und Rückgabewerte
- Scope (Gültigkeitsbereich von Variablen)
- Callback-Funktionen (`on_connect`, `on_message`)
- prozeduraler Programmablauf
- MQTT-Grundlagen mit `paho-mqtt`

→ [tutorial_livemonitor_app.md](tutorial_livemonitor_app.md)

## Schritt 2: Einfache Single-File-Version Retrospektive App

Anschliessend bauen wir die Retrospektive-App in einer funktionsbasierten Erstfassung. Sie analysiert einen abgeschlossenen Transport.

Gleichzeitig dient dieser Schritt dazu, die Stärken, aber auch die Grenzen einer kompakten Single-File-Lösung sichtbar zu machen. So entsteht ein erstes funktionierendes Programm, das als Ausgangspunkt für spätere Verbesserungen dient.

### Behandelte Themen

- Datei-Verarbeitung mit CSV
- Arbeit mit verschiedenen Python-Bibliotheken:
  - `pandas`
  - `matplotlib`
  - `requests`
  - `folium`
  - `reportlab`

→ `tutorial_bibliotheken/bibliotheken.md` 

### Schritt 3: Retrospektive-App (OOP) – objektorientierte Programmierung

Zuletzt überführen wir die funktionsbasierte Retrospektive-App in eine objektorientierte Struktur. Dabei wird gezeigt, wie man ein Programm übersichtlicher, wartbarer und erweiterbarer macht.

**Behandelte Themen**
- Klassen und Objekte
- Attribute und Methoden
- `self` und `__init__()`
- Module und Pakete (`__init__.py`, relative Imports)
- Strukturierung nach Verantwortlichkeiten

→ `tutorial_retrospektive_app_oop.md`

## Warum diese Reihenfolge?

Der Live-Monitor ist klein und eignet sich, um **Funktionen** ohne Ablenkung zu verstehen. Die Retrospektive-App ist grösser und zeigt zuerst, wie man mit Funktionen und Bibliotheken arbeitet und danach, warum sich **OOP** für grössere Programme lohnt.