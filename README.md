# Container-Tracking

## Projektübersicht

Im Rahmen dieser Challenge entwickelt unser Team mehrere Python-Applikationen zur Analyse, Visualisierung und Bereitstellung von Container-Transportdaten.

Der fachliche Kontext stammt aus der Logistik: Während eines Containertransports entstehen laufend Daten wie Zeitstempel, geografische Koordinaten, Temperatur und Feuchtigkeit. Diese Daten sind für Transportunternehmen wichtig, um die korrekte Durchführung eines Transports nachzuweisen, vergangene Transporte nachvollziehen zu können und aktuelle Transporte live zu überwachen.

Ziel des Projekts ist es, auf Basis dieser Daten verschiedene Werkzeuge in Python zu entwickeln.

---

## Projektziele
- Transportdaten aus CSV-Dateien verarbeiten
- abgeschlossene Transporte retrospektiv analysieren
- Live-Daten eines aktuellen Transports verarbeiten
- Transportdaten verständlich visualisieren

---

## Teilapplikationen

### 1. Retrospektive Applikation
Diese Anwendung analysiert einen bereits abgeschlossenen Transport. Eine Route wird aus einer CSV-Datei geladen und anschliessend ausgewertet.

Funktionen:
- Einlesen einer Transport-Route
- Anzeige wichtiger Messwerte
- Erkennung von Temperatur-Grenzwertüberschreitungen
- Einfache Kennzahlen
- Übersicht über den Transportverlauf

### 2. Live-Monitoring Applikation
Diese Anwendung zeigt Live-Daten eines laufenden Transports an.

Mögliche Funktionen:
- Live Map
- laufende Anzeige von Temperatur oder Feuchtigkeit
- Warnung bei Grenzwertüberschreitung
