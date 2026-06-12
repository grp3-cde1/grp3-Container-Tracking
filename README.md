# Container-Tracking (Gruppe 3)

## Zweck

Dieses Projekt entwickelt zwei Python-Applikationen zur Auswertung und Visualisierung von Container-Transportdaten aus dem Logistik-Kontext. Während eines Transports entstehen Messdaten (Zeitstempel, GPS-Koordinaten, Temperatur, Feuchtigkeit). Diese Daten werden retrospektiv und live ausgewertet.

Das Projekt dient zugleich als **Tutorial für Python-Einsteiger** mit Grundkenntnissen.

## Die zwei Applikationen und ihre didaktische Einordnung

| Applikation | Zweck | Paradigma / Lernfokus |
|---|---|---|
| **Live-Monitor** (`apps/live_monitor.py`) | laufenden Transport live über MQTT überwachen | **Funktionen / prozedurale Programmierung** |
| **Retrospektive-App** (`apps/retrospective_oop/`) | abgeschlossenen Transport analysieren und Bericht erstellen | **Objektorientierte Programmierung (OOP)** |

Die Datei `apps/retrospective_app.py` ist die ursprüngliche, funktionsbasierte Fassung der Retrospektive-App. Sie bleibt als Vergleichs- und Ausgangspunkt für das OOP-Tutorial erhalten.

## Voraussetzungen

- Python 3.10 oder höher
- `pip`
- Internetzugang (REST-API und MQTT-Broker des Cloud-Service)
- für Live-Daten: ein laufender Transport (Simulator)

## Installation

```bash
# 1. Repository klonen
git clone https://github.com/grp3-cde1/grp3-Container-Tracking.git
cd grp3-Container-Tracking

# 2. virtuelle Umgebung erstellen und aktivieren
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Abhängigkeiten installieren
pip install -r requirements.txt
```

Die `requirements.txt` enthält: `requests`, `pandas`, `folium`, `matplotlib`, `reportlab`, `paho-mqtt`.

## Start

### Retrospektive-App (funktionsbasierte Fassung)

```bash
python apps/retrospective_app.py
```

Die App führt durch die Auswahl von Container und Route, lädt die CSV-Datei und erzeugt Diagramme, eine Karte (`maps/`) und einen PDF-Bericht (`reports/`).

### Retrospektive-App (OOP-Fassung)

Das Paket `retrospective_oop/` enthält die Klasse `RetrospectiveApp`. Um es zu starten, muss man aus dem Projektordner folgenden Befehl ausführen:

```bash
python -m apps.retrospective_oop.app
```

### Live-Monitor

```bash
python apps/live_monitor.py
```

Der Live-Monitor verbindet sich mit dem MQTT-Broker und zeigt eingehende Messpunkte an. Damit Daten ankommen, muss parallel ein Transport laufen. Mit dem Simulator:

```bash
python simulator/simulator.py simulator/data/luzern-horw.geojson -c simulator/config-switch.ini
```

## Projektstruktur

```text
grp3-Container-Tracking/
├── README.md
├── requirements.txt
├── data/                          # heruntergeladene CSV-Dateien
├── apps/
│   ├── live_monitor.py            # Live-Monitor (Funktionen, MQTT)
│   ├── retrospective_app.py       # Retrospektive (funktionsbasiert)
│   └── retrospective_oop/         # Retrospektive (OOP)
│       ├── __init__.py
│       ├── config.py              # Pfade, URL, Grenzwerte
│       ├── api_client.py          # REST + CSV-Download
│       ├── data_processor.py      # CSV einlesen + Analyse
│       ├── output_creator.py      # Diagramme, Karte, PDF
│       └── app.py                 # Ablaufsteuerung
└── docs/
    ├── projektplan.md
    └── tutorial/                  # Tutorials
```

Die Ordner `maps/`, `charts/` und `reports/` entstehen automatisch beim ersten Lauf der Retrospektive-App.

## Tutorial

Das vollständige Tutorial liegt in `docs/tutorial/`. Empfohlene Reihenfolge:

1. [tutorial_vorgehen.md](docs/tutorial/tutorial_vorgehen.md) – Überblick
2. [tutorial_livemonitor_app.md](docs/tutorial/tutorial_livemonitor_app.md) – Funktionen am Live-Monitor
3. [tutorial_retrospektive_app_oop.md](docs/tutorial/tutorial_retrospektive_app_oop.md) – OOP an der Retrospektive-App
4. [bibliotheken.md](docs/tutorial/tutorial_bibliotheken/bibliotheken.md) – die verwendeten Bibliotheken 