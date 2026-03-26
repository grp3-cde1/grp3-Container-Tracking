import os
import requests
import pandas as pd
import folium
#import geopandas as gpd

# Grenzwerte definieren 
TEMP_MIN = 15
TEMP_MAX = 26
HUM_MAX = 72


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
                csv_url = f"{url}files/{chosen_route}.csv?path=../data/migros/{chosen_container}/{chosen_route}.csv"
                response_csv = requests.get(csv_url)
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
                #track_gdf = gpd.GeoDataFrame(
                #    track_df,
                #    geometry=gpd.points_from_xy(track_df["longitude"], track_df["latitude"]),
                #    crs="EPSG:4326"
                #)

                # Erstellen und anzeigen der Karte
                #track_gdf.plot(figsize=(10, 8))
                #plt.show()

                # Mittelpunkt der Karte berechnen
                center_lat = track_df["latitude"].mean()
                center_lon = track_df["longitude"].mean()

                # Karte erstellen (Folium)
                m = folium.Map(
                    location=[center_lat, center_lon],
                    zoom_start=12,
                    tiles="OpenStreetMap"
                )

                # Route einzeichnen
                coordinates = track_df[["latitude", "longitude"]].values.tolist()

                folium.PolyLine(
                    coordinates,
                    color="blue",
                    weight=4,
                    opacity=0.8,
                    tooltip="Route"
                ).add_to(m)

                # Punkte einzeln der Map hinzufügen

                for index, row in track_df.iterrows():
                    if row["any_violation"]:
                        color = "red"
                    else:
                        color = "green"

                    popup_text = (
                        f"Zeit: {row['timestamp']}<br>"
                        f"Temperatur: {row['temperature']} °C<br>"
                        f"Feuchtigkeit: {row['humidity']} %<br>"
                        f"Temp-Verletzung: {row['temp_violation']}<br>"
                        f"Humidity-Verletzung: {row['humidity_violation']}"
                    )

                    folium.CircleMarker(
                        location=[row["latitude"], row["longitude"]],
                        radius=5,
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.8,
                        popup=folium.Popup(popup_text, max_width=300)
                    ).add_to(m)

                # Filename der Map erstellen
                os.makedirs("maps", exist_ok=True)
                map_filename = f"maps/{chosen_container}_{chosen_route}_map.html"
                m.save(map_filename)

                # Ausgabe wo die Datei gespeichert wurde
                print(f"Karte gespeichert als {map_filename}")
                print("Öffne die HTML-Datei im Browser.")



            else:
                print("Bitte wähle eine Route aus dem Menü aus.")
        else:
            print("Fehler beim Abrufen der Routen:", response_route.status_code)

    else:
        print("Bitte wähle einen Container aus dem Menü aus.")

else:
    print("Fehler beim Abrufen der Container: ", response_container.status_code)

