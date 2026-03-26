# import pandas as pd

# track_df = pd.read_csv('grp3-Container-Tracking/data/luzern-horw.csv', header=None, names=["timestamp", "latitude", "longitude", "temperature", "humidity"], index_col="timestamp")

# print(track_df['temperature'].median())

import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Grenzwerte definieren 
TEMP_MIN = 15
TEMP_MAX = 26
HUM_MAX = 72


url = 'https://fl-17-240.zhdk.cloud.switch.ch/'

response_container = requests.get(f"{url}containers")

if response_container.status_code == 200:
    data_container = response_container.json()

    print("Verfügbare Container:")
    print("--------------------")
    containers = data_container.get("containers", [])

    for i, container in enumerate(containers, start=1):
        print(f"{i}. {container}")

    try:
        index = int(input("Wähle einen Container (Nummer): ")) - 1
        chosen_container = containers[index]
    except (ValueError, IndexError):
        print("Ungültige Auswahl.")
        exit()

    if chosen_container in containers:
        print(f"\nContainer '{chosen_container}' gewählt.")
        response_route = requests.get(f"{url}containers/{chosen_container}/routes")

        if response_route.status_code == 200:
            data_route = response_route.json()

            print("\nVerfügbare Routen:")
            print("--------------------")

            routes = data_route.get("routes", [])

            for i, route in enumerate(routes, start=1):
                print(f"{i}. {route}")

            try:
                index = int(input("Wähle eine Route (Nummer): ")) - 1
                chosen_route = routes[index]
            except (ValueError, IndexError):
                print("Ungültige Auswahl.")
                exit()

            if chosen_route in routes:
                csv_url = f"{url}files/{chosen_route}.csv?path=../data/migros/{chosen_container}/{chosen_route}.csv"
                response_csv = requests.get(csv_url)

                if response_csv.status_code == 200:
                    filename = f"data/{chosen_container}_{chosen_route}.csv"

                    with open(filename, "wb") as f:
                        f.write(response_csv.content)

                    print(f"CSV gespeichert als {filename}")

                    # CSV-Datei in einen Pandas-DataFrame einlesen und Spaltennamen setzen
                    track_df = pd.read_csv(
                        filename,
                        header=None,
                        names=["timestamp", "latitude", "longitude", "temperature", "humidity"]
                        )
                    ## CSV-Datei in einen Pandas-DataFrame einlesen und Spaltennamen setzen
                    track_df["timestamp"] = pd.to_datetime(track_df["timestamp"])

                    # Erstellen neuer Spalte und Prüfen, ob Temperatur unter Minimum oder über Maximum liegt
                    track_df["temp_violation"] = ( 
                        (track_df["temperature"] < TEMP_MIN) | 
                        (track_df["temperature"] > TEMP_MAX)
                    )

                    # Erstellen neuer Spalte und prüfen, ob Feuchtigkeit über dem Maximum liegt
                    track_df["humidity_violation"] = track_df["humidity"] > HUM_MAX

                    # Erstellen neuer Spalte und prüfen ob einer der beiden Grenzwert verletzt wurde
                    track_df["any_violation"] = ( 
                        track_df["temp_violation"] |
                        track_df["humidity_violation"]
                    )

                    # Erstellen einer GeoPandas Tabelle
                    track_gdf = gpd.GeoDataFrame(
                        track_df,
                        geometry=gpd.points_from_xy(track_df["longitude"], track_df["latitude"]),
                        crs="EPSG:4326"
                    )

                    # Erstellen und anzeigen der Karte
                    track_gdf.plot(figsize=(10, 8))
                    plt.show()


                else:
                    print(f"Fehler beim Speichern des CSV:", response_csv.status_code)
            else:
                print("Bitte wähle eine Route aus dem Menü aus.")
        else:
            print("Fehler beim Abrufen der Routen:", response_route.status_code)

    else:
        print("Bitte wähle einen Container aus dem Menü aus.")

else:
    print("Fehler beim Abrufen der Container: ", response_container.status_code)

