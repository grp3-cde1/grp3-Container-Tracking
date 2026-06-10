"""
Hauptprogramm der objektorientierten Retrospective-App.

Diese Datei enthält die Klasse RetrospectiveApp.
Sie verbindet API-Zugriff, Datenverarbeitung und Ausgabe-Erstellung.
"""

from .api_client import ApiClient
from .data_processor import DataProcessor
from .output_creator import OutputCreator
from .config import create_directories

class RetrospectiveApp:
    """
    Steuert den gesamten Ablauf der Retrospective-App.
    """

    def __init__(self):
        """
        Erstellt die benötigten Objekte für die App.
        """

        create_directories()

        self.api_client = ApiClient()
        self.data_processor = DataProcessor()
        self.output_creator = OutputCreator()

    def choose_item(self, title, items):
        """
        Zeigt eine nummerierte Liste an und gibt das gewählte Element zurück.

        Parameter:
            title: Überschrift der Auswahl
            items: Liste der Auswahlmöglichkeiten

        Rückgabe:
            Das gewählte Element, oder None bei ungültiger Eingabe
        """

        print()
        print(title)
        print("-" * len(title))

        for number, item in enumerate(items, start=1):
            print(f"{number}. {item}")

        try:
            index = int(input("Bitte Nummer wählen: ")) - 1
            return items[index]

        except (ValueError, IndexError):
            print("Ungültige Auswahl.")
            return None

    def run(self):
        """
        Führt die Retrospective-App aus.
        """

        containers = self.api_client.fetch_containers()

        if not containers:
            print("Keine Container gefunden.")
            return

        selected_container = self.choose_item("Verfügbare Container", containers)

        if selected_container is None:
            return

        routes = self.api_client.fetch_routes(selected_container)

        if not routes:
            print("Keine Routen gefunden.")
            return

        selected_route = self.choose_item("Verfügbare Routen", routes)

        if selected_route is None:
            return

        csv_path = self.api_client.download_csv(selected_container, selected_route)

        if csv_path is None:
            return

        data_frame = self.data_processor.read_csv_file(csv_path)
        data_frame = self.data_processor.calculate_violations(data_frame)
        statistics = self.data_processor.calculate_statistics(data_frame)

        charts = self.output_creator.create_charts(
            data_frame,
            selected_container,
            selected_route,
        )

        pdf_path = self.output_creator.create_pdf_report(
            selected_container,
            selected_route,
            statistics,
            charts,
            data_frame,
        )

        map_path = self.output_creator.create_map(
            data_frame,
            selected_container,
            selected_route,
        )

        print()
        print(f"Bericht gespeichert: {pdf_path}")
        print(f"Karte gespeichert: {map_path}")
        print("Auswertung abgeschlossen.")


if __name__ == "__main__":
    RetrospectiveApp().run()