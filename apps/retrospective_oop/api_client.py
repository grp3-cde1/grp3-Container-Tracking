"""
API-Zugriff für die objektorientierte Retrospective-App.

Diese Datei enthält die Klasse ApiClient.
Sie ruft Container und Routen vom Webservice ab und lädt CSV-Dateien herunter.
"""

import requests

from .config import BASE_URL, DATA_DIR


class ApiClient:
    """
    Verantwortlich für die Kommunikation mit dem Webservice.
    """

    def __init__(self, base_url=BASE_URL):
        """
        Erstellt ein neues ApiClient-Objekt.

        Parameter:
            base_url: Basis-URL des Webservice
        """

        self.base_url = base_url

    def fetch_containers(self):
        """
        Ruft alle verfügbaren Container vom Server ab.

        Rückgabe:
            Liste der Container-IDs, oder leere Liste bei Fehler
        """

        response = requests.get(f"{self.base_url}/containers", timeout=10)

        if response.status_code != 200:
            print("Fehler beim Abrufen der Container:", response.status_code)
            return []

        data = response.json()
        containers = data.get("containers", [])

        return containers
    
    def fetch_routes(self, container):
        """
        Ruft alle Routen für einen bestimmten Container ab.

        Parameter:
            container: Container-ID als String

        Rückgabe:
            Liste der Routen-IDs, oder leere Liste bei Fehler
        """

        response = requests.get(
            f"{self.base_url}/containers/{container}/routes",
            timeout=10,
        )

        if response.status_code != 200:
            print("Fehler beim Abrufen der Routen:", response.status_code)
            return []

        data = response.json()
        routes = data.get("routes", [])

        return routes
    
    def download_csv(self, container, route):
        """
        Lädt die CSV-Datei zur gewählten Route herunter.

        Parameter:
            container: Container-ID
            route:     Routen-ID

        Rückgabe:
            Pfad zur gespeicherten Datei, oder None bei Fehler
        """

        file_path = DATA_DIR / f"{container}_{route}.csv"

        if file_path.exists():
            answer = input(
                f"Datei '{file_path.name}' existiert bereits. Neu herunterladen? (j/n): "
            )

            if answer.strip().lower() == "n":
                print("Download übersprungen.")
                return file_path

        csv_url = f"{self.base_url}/files/{route}.csv?path=../data/migros/{container}/{route}.csv"

        response = requests.get(csv_url, timeout=20)

        if response.status_code != 200:
            print("Fehler beim CSV-Download:", response.status_code)
            return None

        with open(file_path, "wb") as file:
            file.write(response.content)

        print(f"CSV gespeichert: {file_path}")

        return file_path
