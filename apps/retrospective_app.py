import pandas as pd
import os
import requests

# Basis-URL der API
url = 'https://fl-17-240.zhdk.cloud.switch.ch/'

# Anfrage: Liste aller Container abrufen
response_container = requests.get(f"{url}containers")

# Prüfen, ob Anfrage erfolgreich war
if response_container.status_code == 200:
    data_container = response_container.json()

    print("Verfügbare Container:")
    print("--------------------")

    # Container aus der Antwort holen
    containers = data_container.get("containers", [])

    # Container nummeriert anzeigen
    for i, container in enumerate(containers, start=1):
        print(f"{i}. {container}")

    try:
        # Benutzer wählt Container (Index anpassen, da Liste bei 0 beginnt)
        index = int(input("Wähle einen Container (Nummer): ")) - 1
        chosen_container = containers[index]
    except (ValueError, IndexError):
        # Fehler bei ungültiger Eingabe
        print("Ungültige Auswahl.")
        exit()

    if chosen_container in containers:
        print(f"\nContainer '{chosen_container}' gewählt.")

        # Anfrage: Routen für gewählten Container abrufen
        response_route = requests.get(f"{url}containers/{chosen_container}/routes")

        if response_route.status_code == 200:
            data_route = response_route.json()

            print("\nVerfügbare Routen:")
            print("--------------------")

            # Routen aus der Antwort holen
            routes = data_route.get("routes", [])

            # Routen nummeriert anzeigen
            for i, route in enumerate(routes, start=1):
                print(f"{i}. {route}")

            try:
                # Benutzer wählt Route
                index = int(input("Wähle eine Route (Nummer): ")) - 1
                chosen_route = routes[index]
            except (ValueError, IndexError):
                print("Ungültige Auswahl.")
                exit()

            if chosen_route in routes:
                # Dateiname für CSV festlegen
                filename = f"data/{chosen_container}_{chosen_route}.csv"

                download_file = True

                # Prüfen, ob Datei schon existiert
                if os.path.exists(filename):
                    answer = input(f"Datei '{filename}' exisitiert bereits. Neu herunterladen? (j/n): ").strip().lower()
                    if answer == "n":
                        download_file = False
                        print("Download übersprungen")

                if download_file:
                    # URL zur CSV-Datei bauen
                    csv_url = f"{url}files/{chosen_route}.csv?path=../data/migros/{chosen_container}/{chosen_route}.csv"
                    response_csv = requests.get(csv_url)

                    # Prüfen, ob Download erfolgreich war
                    if response_csv.status_code == 200:
                        # Datei speichern (binär, da Download)
                        with open(filename, "wb") as f:
                            f.write(response_csv.content)

                        print(f"CSV gespeichert als {filename}")
                    else:
                        print(f"Fehler beim Speichern des CSV:", response_csv.status_code)
                
                # CSV in DataFrame laden
                route_df = pd.read_csv(
                    filename,
                    header=None,
                    names=["timestamp", "latitude", "longitude", "temperature", "humidity"],
                )

                # Überblick
                print("\nErste 5 Zeilen")
                print("--------------------")
                print(route_df.head())

                print("\nSpaltennamen:")
                print("--------------------")
                print(route_df.columns)

                print("\nDataframe Info:")
                print("--------------------")
                route_df.info()

                # timestamp in Datetime umwandeln
                route_df["timestamp"] = pd.to_datetime(route_df["timestamp"])

                # timestamp als Index setzen
                route_df = route_df.set_index("timestamp")

                print("\nDataframe mit 'timestamp' als Index:")
                print("--------------------")
                print(route_df.head())

                # Anzahl Messpunkte auslesen
                print("\nAnzahl Messpunkte:")
                print("--------------------")

            else:
                print("Bitte wähle eine Route aus dem Menü aus.")
        else:
            print("Fehler beim Abrufen der Routen:", response_route.status_code)
    else:
        print("Bitte wähle einen Container aus dem Menü aus.")
else:
    print("Fehler beim Abrufen der Container: ", response_container.status_code)