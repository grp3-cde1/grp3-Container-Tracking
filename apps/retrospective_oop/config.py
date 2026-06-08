"""
Zentrale Konfiguration für die objektorientierte Retrospective-App.

Diese Datei enthält globale Einstellungen wie Projektpfade,
API-URL und Grenzwerte für Temperatur und Feuchtigkeit.
"""


from pathlib import Path


# Basisordner des Projekts
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Unterordner für gespeicherte Dateien
DATA_DIR = BASE_DIR / "data"
MAPS_DIR = BASE_DIR / "maps"
CHARTS_DIR = BASE_DIR / "charts"
REPORTS_DIR = BASE_DIR / "reports"

# Basis-URL des Webservice
BASE_URL = "https://fl-17-240.zhdk.cloud.switch.ch"

# Grenzwerte
TEMP_MIN = 15
TEMP_MAX = 26
HUM_MAX = 72


def create_directories():
    """
    Erstellt alle benötigten Unterordner, falls sie noch nicht existieren.
    """

    DATA_DIR.mkdir(exist_ok=True)
    MAPS_DIR.mkdir(exist_ok=True)
    CHARTS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)