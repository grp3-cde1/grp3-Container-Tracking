"""
Datenverarbeitung für die objektorientierte Retrospective-App.

Diese Datei enthält die Klasse DataProcessor.
Sie liest CSV-Dateien ein, berechnet Grenzwertverletzungen
und erstellt statistische Kennzahlen.
"""

import pandas as pd

from .config import TEMP_MIN, TEMP_MAX, HUM_MAX

class DataProcessor:
    """
    Verantwortlich für das Einlesen und Auswerten der Messdaten.
    """

    def read_csv_file(self, file_path):
        """
        Liest eine CSV-Datei ein und gibt einen DataFrame zurück.

        Parameter:
            file_path: Pfad zur CSV-Datei

        Rückgabe:
            pandas DataFrame mit den Messdaten
        """

        data_frame = pd.read_csv(
            file_path,
            header=None,
            names=["timestamp", "latitude", "longitude", "temperature", "humidity"],
        )

        data_frame["timestamp"] = pd.to_datetime(data_frame["timestamp"])

        return data_frame
    
    def calculate_violations(self, data_frame):
        """
        Ergänzt den DataFrame um Boolean-Spalten für Grenzwertverletzungen.

        Parameter:
            data_frame: pandas DataFrame mit temperature und humidity

        Rückgabe:
            Kopie des DataFrames mit zusätzlichen Spalten:
            temp_violation, humidity_violation, any_violation
        """

        data_frame = data_frame.copy()

        data_frame["temp_violation"] = ((data_frame["temperature"] < TEMP_MIN) | (data_frame["temperature"] > TEMP_MAX))

        data_frame["humidity_violation"] = data_frame["humidity"] > HUM_MAX

        data_frame["any_violation"] = (data_frame["temp_violation"] | data_frame["humidity_violation"])

        return data_frame
    
    def calculate_statistics(self, data_frame):
        """
        Berechnet Kennzahlen aus dem DataFrame.

        Parameter:
            data_frame: pandas DataFrame mit Violations-Spalten

        Rückgabe:
            Dictionary mit Kennzahlen
        """

        statistics = {
            "total_points": len(data_frame),
            "start_time": data_frame["timestamp"].min(),
            "end_time": data_frame["timestamp"].max(),
            "avg_temperature": data_frame["temperature"].mean(),
            "min_temperature": data_frame["temperature"].min(),
            "max_temperature": data_frame["temperature"].max(),
            "avg_humidity": data_frame["humidity"].mean(),
            "max_humidity": data_frame["humidity"].max(),
            "temp_violations": int(data_frame["temp_violation"].sum()),
            "humidity_violations": int(data_frame["humidity_violation"].sum()),
            "all_violations": int(data_frame["any_violation"].sum()),
        }

        return statistics
    