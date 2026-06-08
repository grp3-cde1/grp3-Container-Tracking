# Tutorial: Objektorientierte Retrospektive-App

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