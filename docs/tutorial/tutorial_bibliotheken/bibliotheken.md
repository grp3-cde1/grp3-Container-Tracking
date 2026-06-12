# Python-Bibliotheken im Projekt

Python-Bibliotheken sind Sammlungen von vorgefertigtem Code. Sie helfen, Aufgaben zu lösen, ohne alles selbst zu programmieren.

Eine Bibliothek kann aus mehreren **Modulen** bestehen. Ein **Modul** ist meist eine einzelne Python-Datei mit Funktionen, Klassen oder Variablen.

## Installation mit pip

```bash
pip install -r requirements.txt
```

Alternativ:

```bash
python -m pip install -r requirements.txt
```

Die `requirements.txt` enthält alle Bibliotheken, die das Projekt braucht:

```text
requests   → REST/HTTP
pandas     → Datenverarbeitung
folium     → interaktive Karten
matplotlib → Diagramme
reportlab  → PDF-Berichte
paho-mqtt  → MQTT / Live-Daten
```

## Import

```python
import math
print(math.sqrt(16))

import pandas as pd          # mit Kürzel
from pathlib import Path     # einzelnes Element
```

## Welche Bibliothek gehört zu welcher App?

| App | Bibliotheken |
|---|---|
| **Live-Monitor** (Funktionen) | `paho-mqtt`, `pandas` |
| **Retrospektive-App** (OOP) | `requests`, `pandas`, `matplotlib`, `folium`, `reportlab`, `pathlib` |

## Übersicht der Tutorials

**Live-Monitor**
- [Paho-MQTT](paho-mqtt.md)

**Retrospektive-App**
- [Requests](requests.md)
- [Pandas](pandas.md)
- [Matplotlib](matplotlib.md)
- [Folium](folium.md)
- [ReportLab](reportlab.md)