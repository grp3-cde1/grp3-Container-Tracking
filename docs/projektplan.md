# Projektplan

## Vorgehensmodell

### Phase 1: Projektsetup
- GitHub-Repository erstellen
- Projektstruktur definieren
- Entwicklungsumgebung einrichten
- Grunddokumentation erstellen

### Phase 2: Live-Monitor (Funktionen, prozedural)
- MQTT-Grundlagen verstehen (Broker, Topic, Subscribe)
- Callback-Funktionen `on_connect` und `on_message` umsetzen
- eingehende JSON-Nachrichten verarbeiten
- Temperatur-Warnungen im Terminal
- Lernfokus: Funktionen und prozeduraler Ablauf

### Phase 3: Retrospektive-App (funktionsbasiert)
- REST-API verwenden (Container, Routen, CSV)
- CSV mit pandas einlesen und analysieren
- Grenzwertverletzungen berechnen
- Diagramme, Karte und PDF-Bericht erstellen
- Lernfokus: Bibliotheken und Datenverarbeitung

### Phase 4: Retrospektive-App (OOP)
- die funktionsbasierte App in Module aufteilen
- Klassen nach Verantwortlichkeiten bilden (ApiClient, DataProcessor, OutputCreator, RetrospectiveApp)
- bessere Wartbarkeit und Wiederverwendbarkeit schaffen
- Lernfokus: objektorientierte Programmierung

### Phase 5: Abschluss
- Dokumentation und Tutorial finalisieren
- Release mit Git-Tag `RELEASE-1.0`