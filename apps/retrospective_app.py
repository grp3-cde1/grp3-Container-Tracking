import os
import requests
import pandas as pd
import folium
#import geopandas as gpd
import matplotlib.pyplot as plt

# Import einzelner Module
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Table, TableStyle
from reportlab.lib import colors

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Erstellen von Unterordnern falls noch nicht vorhanden
DATA_DIR = BASE_DIR / "data"
MAPS_DIR = BASE_DIR / "maps"
REPORTS_DIR = BASE_DIR / "reports"
CHARTS_DIR = BASE_DIR / "charts"

DATA_DIR.mkdir(exist_ok=True)
MAPS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
CHARTS_DIR.mkdir(exist_ok=True)

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
                filename = DATA_DIR / f"{chosen_container}_{chosen_route}.csv"

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
                
                # Diagramm für Temperaturverlauf
                temp_chart = CHARTS_DIR / f"{chosen_container}_{chosen_route}_temperature.png"

                plt.figure(figsize=(10, 4))
                plt.plot(track_df["timestamp"], track_df["temperature"])
                plt.axhline(TEMP_MIN, linestyle="--", label=f"Temp Min ({TEMP_MIN}°C)")
                plt.axhline(TEMP_MAX, linestyle="--", label=f"Temp Max ({TEMP_MAX}°C)")
                plt.title("Temperaturverlauf")
                plt.xlabel("Zeit")
                plt.ylabel("Temperatur (°C)")
                plt.xticks(rotation=45)
                plt.legend()
                plt.tight_layout()
                plt.savefig(temp_chart)
                plt.close()

                # Feuchtigkeitsverlauf
                hum_chart = CHARTS_DIR / f"{chosen_container}_{chosen_route}_humidity.png"

                plt.figure(figsize=(10, 4))
                plt.plot(track_df["timestamp"], track_df["humidity"])
                plt.axhline(HUM_MAX, linestyle="--", label=f"Humidity Max ({HUM_MAX}%)")
                plt.title("Feuchtigkeitsverlauf")
                plt.xlabel("Zeit")
                plt.ylabel("Feuchtigkeit (%)")
                plt.xticks(rotation=45)
                plt.legend()
                plt.tight_layout()
                plt.savefig(hum_chart)
                plt.close()

                # Histogramm der Temperatur
                hist_chart = CHARTS_DIR / f"{chosen_container}_{chosen_route}_temperature_hist.png"

                plt.figure(figsize=(8, 4))
                plt.hist(track_df["temperature"], bins=10)
                plt.axvline(TEMP_MIN, linestyle="--", label=f"Temp Min ({TEMP_MIN}°C)")
                plt.axvline(TEMP_MAX, linestyle="--", label=f"Temp Max ({TEMP_MAX}°C)")
                plt.title("Verteilung der Temperatur")
                plt.xlabel("Temperatur (°C)")
                plt.ylabel("Häufigkeit")
                plt.legend()
                plt.tight_layout()
                plt.savefig(hist_chart)
                plt.close()


                # Diagramm der Grenzwertverletzungen
                violation_chart = CHARTS_DIR / f"{chosen_container}_{chosen_route}_violations.png"

                temp_violations = int(track_df["temp_violation"].sum())
                humidity_violations = int(track_df["humidity_violation"].sum())
                no_violations = int((~track_df["any_violation"]).sum())

                labels = ["Temp-Verletzungen", "Feuchtigkeits-Verletzungen", "Ohne Verletzung"]
                values = [temp_violations, humidity_violations, no_violations]

                plt.figure(figsize=(8, 4))
                plt.bar(labels, values)
                plt.title("Grenzwertverletzungen")
                plt.ylabel("Anzahl Messpunkte")
                plt.tight_layout()
                plt.savefig(violation_chart)
                plt.close()

                # Karte der Verletzungen
                route_chart = CHARTS_DIR / f"{chosen_container}_{chosen_route}_route.png"

                plt.figure(figsize=(6, 6))

                ok_points = track_df[~track_df["any_violation"]]
                bad_points = track_df[track_df["any_violation"]]

                plt.plot(track_df["longitude"], track_df["latitude"], linewidth=1, label="Route")
                plt.scatter(ok_points["longitude"], ok_points["latitude"], s=20, label="OK")
                plt.scatter(bad_points["longitude"], bad_points["latitude"], s=20, label="Verletzung")

                plt.title("Route mit Grenzwertverletzungen")
                plt.xlabel("Longitude")
                plt.ylabel("Latitude")
                plt.legend()
                plt.tight_layout()
                plt.savefig(route_chart)
                plt.close()

                # Kennzahlen berechnen
                avg_temp = track_df["temperature"].mean()
                min_temp = track_df["temperature"].min()
                max_temp = track_df["temperature"].max()

                avg_humidity = track_df["humidity"].mean()
                max_humidity = track_df["humidity"].max()

                temp_violations = int(track_df["temp_violation"].sum())
                humidity_violations = int(track_df["humidity_violation"].sum())
                any_violations = int(track_df["any_violation"].sum())
                total_points = len(track_df)


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
                map_filename = MAPS_DIR / f"{chosen_container}_{chosen_route}_map.html"
                m.save(map_filename)

                # Ausgabe wo die Datei gespeichert wurde
                print(f"Karte gespeichert als {map_filename}")
                print("Öffne die HTML-Datei im Browser.")

                # PDF erstellen
                pdf_path = REPORTS_DIR / f"{chosen_route}_report.pdf"
                doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)

                styles = getSampleStyleSheet()
                story = []

                start_time = track_df["timestamp"].min()
                end_time = track_df["timestamp"].max()

                date_str = start_time.strftime("%d.%m.%Y")
                time_range_str = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"

                story.append(Paragraph("Retrospektiver Bericht", styles["Title"]))
                story.append(Spacer(1, 0.5 * cm))
                story.append(Paragraph(f"Route: {chosen_route}", styles["Normal"]))
                story.append(Paragraph(f"Datum: {date_str}", styles["Normal"]))
                story.append(Paragraph(f"Uhrzeit: {time_range_str}", styles["Normal"]))
                story.append(Paragraph(f"Container: {chosen_container}", styles["Normal"]))
                story.append(Spacer(1, 0.4 * cm))

                # Kennzahlen gruppieren
                table_data = [
                    ["Kennzahl", "Wert"],
                    ["Anzahl Messpunkte", str(total_points)],
                    ["Durchschnittstemperatur", f"{avg_temp:.2f} °C"],
                    ["Minimale Temperatur", f"{min_temp:.2f} °C"],
                    ["Maximale Temperatur", f"{max_temp:.2f} °C"],
                    ["Durchschnittliche Feuchtigkeit", f"{avg_humidity:.2f} %"],
                    ["Maximale Feuchtigkeit", f"{max_humidity:.2f} %"],
                    ["Temperaturverletzungen", str(temp_violations)],
                    ["Feuchtigkeitsverletzungen", str(humidity_violations)],
                    ["Messpunkte mit irgendeiner Verletzung", str(any_violations)],
                ]

                table = Table(table_data, colWidths=[8 * cm, 6 * cm])
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    ("PADDING", (0, 0), (-1, -1), 4),
                ]))
                story.append(table)
                story.append(Spacer(1, 0.7 * cm))

                # Temperatur-Diagramm einfügen
                story.append(Paragraph("1. Temperaturverlauf", styles["Heading2"]))
                story.append(Image(temp_chart, width=16 * cm, height=6 * cm))
                story.append(Spacer(1, 0.4 * cm))
                
                # Feuchtigkeitsverlauf einfügen
                story.append(Paragraph("2. Feuchtigkeitsverlauf", styles["Heading2"]))
                story.append(Image(hum_chart, width=16 * cm, height=6 * cm))
                story.append(Spacer(1, 0.4 * cm))
                
                # Histogramm der Temperatur einfügen
                story.append(Paragraph("3. Temperaturverteilung", styles["Heading2"]))
                story.append(Image(hist_chart, width=14 * cm, height=6 * cm))
                story.append(Spacer(1, 0.4 * cm))

                # Diagramm der Grenzwertverletzungen einfügen
                story.append(Paragraph("4. Grenzwertverletzungen", styles["Heading2"]))
                story.append(Image(violation_chart, width=14 * cm, height=6 * cm))
                story.append(Spacer(1, 0.4 * cm))

                # Karte der Verletzungen einfügen
                story.append(Paragraph("5. Route mit markierten Verletzungen", styles["Heading2"]))
                story.append(Image(route_chart, width=14 * cm, height=14 * cm))
                story.append(Spacer(1, 0.4 * cm))

                doc.build(story)

                print(f"PDF gespeichert: {pdf_path}")

            else:
                print("Bitte wähle eine Route aus dem Menü aus.")
        else:
            print("Fehler beim Abrufen der Routen:", response_route.status_code)

    else:
        print("Bitte wähle einen Container aus dem Menü aus.")

else:
    print("Fehler beim Abrufen der Container: ", response_container.status_code)



