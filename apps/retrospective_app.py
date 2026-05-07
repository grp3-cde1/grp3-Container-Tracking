from pathlib import Path

import requests
import pandas as pd
import folium
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak


# Basisordner des Projekts festlegen
BASE_DIR = Path(__file__).resolve().parent.parent

# Unterordner für Dateien festlegen
DATA_DIR = BASE_DIR / "data"
MAPS_DIR = BASE_DIR / "maps"
CHARTS_DIR = BASE_DIR / "charts"
REPORTS_DIR = BASE_DIR / "reports"

# Unterordner erstellen, falls sie noch nicht existieren
DATA_DIR.mkdir(exist_ok=True)
MAPS_DIR.mkdir(exist_ok=True)
CHARTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Basis-URL des Webservice festlegen
BASE_URL = "https://fl-17-240.zhdk.cloud.switch.ch"

# Grenzwerte für Temperatur und Feuchtigkeit festlegen
TEMP_MIN = 15
TEMP_MAX = 26
HUM_MAX = 72


def fetch_containers():
    """
    Ruft alle verfügbaren Container vom Server ab.

    Rückgabe:
        Liste der Container-IDs, oder leere Liste bei Fehler
    """

    # Container vom Webservice abrufen
    response = requests.get(f"{BASE_URL}/containers", timeout=10)

    # Statuscode der Antwort prüfen
    if response.status_code != 200:
        print("Fehler beim Abrufen der Container:", response.status_code)
        return []

    # Antwort in JSON umwandeln
    data = response.json()

    # Containerliste aus der Antwort holen
    containers = data.get("containers", [])

    return containers


def fetch_routes(container):
    """
    Ruft alle Routen für einen bestimmten Container ab.

    Parameter:
        container: Container-ID als String

    Rückgabe:
        Liste der Routen-IDs, oder leere Liste bei Fehler
    """

    # Routen für den gewählten Container abrufen
    response = requests.get(f"{BASE_URL}/containers/{container}/routes", timeout=10)

    # Statuscode der Antwort prüfen
    if response.status_code != 200:
        print("Fehler beim Abrufen der Routen:", response.status_code)
        return []

    # Antwort in JSON umwandeln
    data = response.json()

    # Routenliste aus der Antwort holen
    routes = data.get("routes", [])

    return routes


def choose_item(title, items):
    """
    Zeigt eine nummerierte Liste an und gibt das gewählte Element zurück.

    Parameter:
        title:  Überschrift der Auswahl
        items:  Liste der Auswahlmöglichkeiten

    Rückgabe:
        Das gewählte Element, oder None bei ungültiger Eingabe
    """

    # Titel der Auswahl anzeigen
    print()
    print(title)
    print("-" * len(title))

    # Einträge nummeriert anzeigen
    for number, item in enumerate(items, start=1):
        print(f"{number}. {item}")

    try:
        # Benutzereingabe einlesen
        index = int(input("Bitte Nummer wählen: ")) - 1

        # Ausgewählten Eintrag zurückgeben
        return items[index]

    except (ValueError, IndexError):
        # Fehler bei ungültiger Eingabe ausgeben
        print("Ungültige Auswahl.")
        return None


def download_csv(container, route):
    """
    Lädt die CSV-Datei zur gewählten Route herunter.

    Parameter:
        container: Container-ID
        route:     Routen-ID

    Rückgabe:
        Pfad zur gespeicherten Datei, oder None bei Fehler
    """

    # Lokalen Dateinamen festlegen
    file_path = DATA_DIR / f"{container}_{route}.csv"

    # Prüfen, ob Datei bereits existiert
    if file_path.exists():
        answer = input(f"Datei '{file_path.name}' existiert bereits. Neu herunterladen? (j/n): ")

        # Download überspringen, wenn Benutzer nein wählt
        if answer.strip().lower() == "n":
            print("Download übersprungen.")
            return file_path

    # CSV-URL zusammensetzen
    csv_url = f"{BASE_URL}/files/{route}.csv?path=../data/migros/{container}/{route}.csv"

    # CSV-Datei vom Webservice abrufen
    response = requests.get(csv_url, timeout=20)

    # Statuscode der Antwort prüfen
    if response.status_code != 200:
        print("Fehler beim CSV-Download:", response.status_code)
        return None

    # CSV-Datei lokal speichern
    with open(file_path, "wb") as file:
        file.write(response.content)

    # Speicherort anzeigen
    print(f"CSV gespeichert: {file_path}")

    return file_path


def read_csv_file(file_path):
    """
    Liest eine CSV-Datei ein und gibt einen DataFrame zurück.

    Parameter:
        file_path: Pfad zur CSV-Datei

    Rückgabe:
        pandas DataFrame mit Spalten: timestamp, latitude, longitude,
        temperature, humidity
    """

    # CSV-Datei mit pandas einlesen
    data_frame = pd.read_csv(
        file_path,
        header=None,
        names=["timestamp", "latitude", "longitude", "temperature", "humidity"],
    )

    # Zeitstempel in Datumsformat umwandeln
    data_frame["timestamp"] = pd.to_datetime(data_frame["timestamp"])

    return data_frame


def calculate_violations(data_frame):
    """
    Ergänzt den DataFrame um Boolean-Spalten für Grenzwertverletzungen.

    Parameter:
        data_frame: pandas DataFrame mit temperature und humidity

    Rückgabe:
        Kopie des DataFrames mit zusätzlichen Spalten:
        temp_violation, humidity_violation, any_violation
    """

    # Kopie der Tabelle erstellen
    data_frame = data_frame.copy()

    # Temperaturverletzungen berechnen
    data_frame["temp_violation"] = (
        (data_frame["temperature"] < TEMP_MIN)
        | (data_frame["temperature"] > TEMP_MAX)
    )

    # Feuchtigkeitsverletzungen berechnen
    data_frame["humidity_violation"] = data_frame["humidity"] > HUM_MAX

    # Alle Grenzwertverletzungen zusammenfassen
    data_frame["any_violation"] = (
        data_frame["temp_violation"]
        | data_frame["humidity_violation"]
    )

    return data_frame


def calculate_statistics(data_frame):
    """
    Berechnet zusammengefasste Kennzahlen aus dem DataFrame.

    Parameter:
        data_frame: pandas DataFrame mit Violations-Spalten

    Rückgabe:
        Dictionary mit Kennzahlen
    """

    # Kennzahlen in Dictionary speichern
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


def create_temperature_chart(data_frame, container, route):
    """
    Erstellt ein Diagramm für den Temperaturverlauf.

    Parameter:
        data_frame: pandas DataFrame mit Zeitstempel und Temperatur
        container:  Container-ID (für den Dateinamen)
        route:      Routen-ID (für den Dateinamen)

    Rückgabe:
        Pfad zum gespeicherten Temperaturdiagramm
    """

    # Dateiname für Temperaturdiagramm festlegen
    chart_path = CHARTS_DIR / f"{container}_{route}_temperature.png"

    # Diagrammgrösse festlegen
    plt.figure(figsize=(10, 4))

    # Temperaturverlauf zeichnen
    plt.plot(data_frame["timestamp"], data_frame["temperature"], color="tab:red", label="Temperatur")

    # Unteren Temperaturgrenzwert einzeichnen
    plt.axhline(TEMP_MIN, linestyle="--", color="gray", label=f"Minimum {TEMP_MIN} °C")

    # Oberen Temperaturgrenzwert einzeichnen
    plt.axhline(TEMP_MAX, linestyle="--", color="black", label=f"Maximum {TEMP_MAX} °C")

    # Diagrammbeschriftung setzen
    plt.title("Temperaturverlauf")
    plt.xlabel("Zeit")
    plt.ylabel("Temperatur in °C")

    # Zeitachse besser lesbar machen
    plt.xticks(rotation=35)

    # Legende anzeigen
    plt.legend()

    # Layout automatisch anpassen
    plt.tight_layout()

    # Diagramm als Bild speichern
    plt.savefig(chart_path, dpi=150)

    # Diagramm schliessen
    plt.close()

    return chart_path


def create_humidity_chart(data_frame, container, route):
    """
    Erstellt ein Diagramm für den Feuchtigkeitsverlauf.

    Parameter:
        data_frame: pandas DataFrame mit Zeitstempel und Feuchtigkeit
        container:  Container-ID (für den Dateinamen)
        route:      Routen-ID (für den Dateinamen)

    Rückgabe:
        Pfad zum gespeicherten Feuchtigkeitsdiagramm
    """

    # Dateiname für Feuchtigkeitsdiagramm festlegen
    chart_path = CHARTS_DIR / f"{container}_{route}_humidity.png"

    # Diagrammgrösse festlegen
    plt.figure(figsize=(10, 4))

    # Feuchtigkeitsverlauf zeichnen
    plt.plot(data_frame["timestamp"], data_frame["humidity"], color="tab:blue", label="Feuchtigkeit")

    # Feuchtigkeitsgrenzwert einzeichnen
    plt.axhline(HUM_MAX, linestyle="--", color="black", label=f"Maximum {HUM_MAX} %")

    # Diagrammbeschriftung setzen
    plt.title("Feuchtigkeitsverlauf")
    plt.xlabel("Zeit")
    plt.ylabel("Feuchtigkeit in %")

    # Zeitachse besser lesbar machen
    plt.xticks(rotation=35)

    # Legende anzeigen
    plt.legend()

    # Layout automatisch anpassen
    plt.tight_layout()

    # Diagramm als Bild speichern
    plt.savefig(chart_path, dpi=150)

    # Diagramm schliessen
    plt.close()

    return chart_path


def create_violation_chart(data_frame, container, route):
    """
    Erstellt ein Balkendiagramm zu Grenzwertverletzungen.

    Parameter:
        data_frame: pandas DataFrame mit Verletzungsspalten
        container:  Container-ID (für den Dateinamen)
        route:      Routen-ID (für den Dateinamen)

    Rückgabe:
        Pfad zum gespeicherten Verletzungsdiagramm
    """

    # Dateiname für Grenzwertdiagramm festlegen
    chart_path = CHARTS_DIR / f"{container}_{route}_violations.png"

    # Beschriftungen für Balkendiagramm festlegen
    labels = ["Temperatur", "Feuchtigkeit", "Ohne Verletzung"]

    # Werte für Balkendiagramm berechnen
    values = [
        int(data_frame["temp_violation"].sum()),
        int(data_frame["humidity_violation"].sum()),
        int((~data_frame["any_violation"]).sum()),
    ]

    # Farben für Balken festlegen
    colors_list = ["tab:red", "tab:blue", "tab:green"]

    # Diagrammgrösse festlegen
    plt.figure(figsize=(8, 4))

    # Balkendiagramm erstellen
    plt.bar(labels, values, color=colors_list)

    # Diagrammbeschriftung setzen
    plt.title("Grenzwertverletzungen")
    plt.ylabel("Anzahl Messpunkte")

    # Layout automatisch anpassen
    plt.tight_layout()

    # Diagramm als Bild speichern
    plt.savefig(chart_path, dpi=150)

    # Diagramm schliessen
    plt.close()

    return chart_path


def create_static_route_chart(data_frame, container, route):
    """
    Erstellt eine statische Routendarstellung für den PDF-Bericht.

    Parameter:
        data_frame: pandas DataFrame mit Koordinaten und Verletzungsspalten
        container:  Container-ID (für den Dateinamen)
        route:      Routen-ID (für den Dateinamen)

    Rückgabe:
        Pfad zur gespeicherten Routengrafik
    """

    # Dateiname für statische Route festlegen
    chart_path = CHARTS_DIR / f"{container}_{route}_route.png"

    # Messpunkte ohne Verletzung filtern
    ok_points = data_frame[~data_frame["any_violation"]]

    # Messpunkte mit Verletzung filtern
    bad_points = data_frame[data_frame["any_violation"]]

    # Diagrammgrösse festlegen
    plt.figure(figsize=(6, 6))

    # Route als Linie zeichnen
    plt.plot(data_frame["longitude"], data_frame["latitude"], color="gray", linewidth=1, label="Route")

    # Normale Messpunkte grün zeichnen
    plt.scatter(ok_points["longitude"], ok_points["latitude"], s=18, color="green", label="OK")

    # Verletzte Messpunkte rot zeichnen
    plt.scatter(bad_points["longitude"], bad_points["latitude"], s=25, color="red", label="Verletzung")

    # Diagrammbeschriftung setzen
    plt.title("Route mit markierten Verletzungen")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Legende anzeigen
    plt.legend()

    # Layout automatisch anpassen
    plt.tight_layout()

    # Diagramm als Bild speichern
    plt.savefig(chart_path, dpi=150)

    # Diagramm schliessen
    plt.close()

    return chart_path


def create_charts(data_frame, container, route):
    # Alle Diagramme erstellen
    charts = {
        "temperature": create_temperature_chart(data_frame, container, route),
        "humidity": create_humidity_chart(data_frame, container, route),
        "violations": create_violation_chart(data_frame, container, route),
        "route": create_static_route_chart(data_frame, container, route),
    }

    return charts


def create_map(data_frame, container, route):
    """
    Erstellt eine interaktive Karte mit der Transportroute.

    Parameter:
        data_frame: pandas DataFrame mit latitude und longitude
        container:  Container-ID (für den Dateinamen)
        route:      Routen-ID (für den Dateinamen)

    Rückgabe:
        Pfad zur gespeicherten HTML-Karte
    """

    # Mittelpunkt der Karte berechnen
    center_lat = data_frame["latitude"].mean()
    center_lon = data_frame["longitude"].mean()

    # Folium-Karte erstellen
    map_object = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles="OpenStreetMap",
    )

    # Koordinaten für die Route vorbereiten
    coordinates = data_frame[["latitude", "longitude"]].values.tolist()

    # Route als Linie einzeichnen
    folium.PolyLine(
        coordinates,
        color="blue",
        weight=4,
        opacity=0.8,
        tooltip="Route",
    ).add_to(map_object)

    # Alle Messpunkte durchgehen
    for _, row in data_frame.iterrows():
        # Farbe je nach Grenzwertverletzung festlegen
        marker_color = "red" if row["any_violation"] else "green"

        # Text für Popup erstellen
        popup_text = (
            f"Zeit: {row['timestamp']}<br>"
            f"Temperatur: {row['temperature']} °C<br>"
            f"Feuchtigkeit: {row['humidity']} %<br>"
            f"Temperatur-Verletzung: {row['temp_violation']}<br>"
            f"Feuchtigkeits-Verletzung: {row['humidity_violation']}"
        )

        # Messpunkt auf Karte einzeichnen
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=5,
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=300),
        ).add_to(map_object)

    # Dateiname für HTML-Karte festlegen
    map_path = MAPS_DIR / f"{container}_{route}_map.html"

    # Karte als HTML-Datei speichern
    map_object.save(map_path)

    return map_path


def create_conclusion(statistics):
    """
    Erstellt ein kurzes automatisches Fazit.

    Parameter:
        statistics: Dictionary mit Kennzahlen und Grenzwertverletzungen

    Rückgabe:
        Fazit als Text
    """

    # Fazit ohne Grenzwertverletzungen erstellen
    if statistics["all_violations"] == 0:
        return "Der Transport war unauffällig. Es wurden keine Grenzwertverletzungen gefunden."

    # Textteile für Fazit sammeln
    conclusion_parts = []

    # Temperaturverletzungen ins Fazit aufnehmen
    if statistics["temp_violations"] > 0:
        conclusion_parts.append(f"Es gab {statistics['temp_violations']} Temperaturverletzungen.")

    # Feuchtigkeitsverletzungen ins Fazit aufnehmen
    if statistics["humidity_violations"] > 0:
        conclusion_parts.append(f"Es gab {statistics['humidity_violations']} Feuchtigkeitsverletzungen.")

    # Kurze Bewertung ergänzen
    conclusion_parts.append("Der Transport sollte genauer geprüft werden.")

    # Textteile zu einem Satz verbinden
    return " ".join(conclusion_parts)


def create_pdf_report(container, route, statistics, charts):
    """
    Erstellt einen PDF-Bericht zur ausgewählten Route.

    Parameter:
        container:  Container-ID
        route:      Routen-ID
        statistics: Dictionary mit Kennzahlen
        charts:     Dictionary mit Pfaden zu den Diagrammen

    Rückgabe:
        Pfad zum gespeicherten PDF-Bericht
    """
    
    # Dateiname für PDF-Bericht festlegen
    pdf_path = REPORTS_DIR / f"{container}_{route}_report.pdf"

    # PDF-Dokument vorbereiten
    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    # Standard-Styles von reportlab laden
    styles = getSampleStyleSheet()

    # Zusätzlichen Textstil für kleine Hinweise erstellen
    styles.add(
        ParagraphStyle(
            name="SmallText",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
        )
    )

    # Inhalte des PDF-Berichts sammeln
    story = []

    # Start- und Endzeit aus Kennzahlen holen
    start_time = statistics["start_time"]
    end_time = statistics["end_time"]

    # Titel in PDF einfügen
    story.append(Paragraph("Retrospektiver Transportbericht", styles["Title"]))
    story.append(Spacer(1, 0.4 * cm))

    # Metadaten für PDF vorbereiten
    metadata = [
        ["Container", container],
        ["Route", route],
        ["Start", start_time.strftime("%d.%m.%Y %H:%M")],
        ["Ende", end_time.strftime("%d.%m.%Y %H:%M")],
        ["Temperatur-Grenzwerte", f"{TEMP_MIN} °C bis {TEMP_MAX} °C"],
        ["Feuchtigkeits-Grenzwert", f"maximal {HUM_MAX} %"],
    ]

    # Metadaten-Tabelle erstellen
    metadata_table = Table(metadata, colWidths=[5 * cm, 10 * cm])

    # Darstellung der Metadaten-Tabelle festlegen
    metadata_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    # Metadaten-Tabelle in PDF einfügen
    story.append(metadata_table)
    story.append(Spacer(1, 0.6 * cm))

    # Überschrift für Kennzahlen einfügen
    story.append(Paragraph("Kennzahlen", styles["Heading2"]))

    # Kennzahlentabelle vorbereiten
    statistics_table_data = [
        ["Kennzahl", "Wert"],
        ["Anzahl Messpunkte", str(statistics["total_points"])],
        ["Durchschnittstemperatur", f"{statistics['avg_temperature']:.2f} °C"],
        ["Minimale Temperatur", f"{statistics['min_temperature']:.2f} °C"],
        ["Maximale Temperatur", f"{statistics['max_temperature']:.2f} °C"],
        ["Durchschnittliche Feuchtigkeit", f"{statistics['avg_humidity']:.2f} %"],
        ["Maximale Feuchtigkeit", f"{statistics['max_humidity']:.2f} %"],
        ["Temperaturverletzungen", str(statistics["temp_violations"])],
        ["Feuchtigkeitsverletzungen", str(statistics["humidity_violations"])],
        ["Alle Grenzwertverletzungen", str(statistics["all_violations"])],
    ]

    # Kennzahlentabelle erstellen
    statistics_table = Table(statistics_table_data, colWidths=[8 * cm, 6 * cm])

    # Darstellung der Kennzahlentabelle festlegen
    statistics_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9eaf7")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    # Kennzahlentabelle in PDF einfügen
    story.append(statistics_table)
    story.append(Spacer(1, 0.7 * cm))

    # Überschrift für Fazit einfügen
    story.append(Paragraph("Automatisches Fazit", styles["Heading2"]))

    # Automatisches Fazit einfügen
    story.append(Paragraph(create_conclusion(statistics), styles["Normal"]))

    # Neue PDF-Seite beginnen
    story.append(PageBreak())

    # Temperaturdiagramm einfügen
    story.append(Paragraph("Temperaturverlauf", styles["Heading2"]))
    story.append(Image(str(charts["temperature"]), width=16 * cm, height=6 * cm))
    story.append(Spacer(1, 0.5 * cm))

    # Feuchtigkeitsdiagramm einfügen
    story.append(Paragraph("Feuchtigkeitsverlauf", styles["Heading2"]))
    story.append(Image(str(charts["humidity"]), width=16 * cm, height=6 * cm))
    story.append(Spacer(1, 0.5 * cm))

    # Grenzwertdiagramm einfügen
    story.append(Paragraph("Grenzwertverletzungen", styles["Heading2"]))
    story.append(Image(str(charts["violations"]), width=14 * cm, height=6 * cm))

    # Neue PDF-Seite beginnen
    story.append(PageBreak())

    # Routendarstellung einfügen
    story.append(Paragraph("Statische Routendarstellung", styles["Heading2"]))
    story.append(Paragraph("Grüne Punkte sind normale Messpunkte. Rote Punkte zeigen Grenzwertverletzungen.", styles["SmallText"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(Image(str(charts["route"]), width=14 * cm, height=14 * cm))

    # PDF-Bericht erstellen
    document.build(story)

    return pdf_path


def main():
    # Containerliste abrufen
    containers = fetch_containers()

    # Programm beenden, wenn keine Container vorhanden sind
    if not containers:
        return

    # Container auswählen
    selected_container = choose_item("Verfügbare Container", containers)

    # Programm beenden, wenn Auswahl ungültig ist
    if selected_container is None:
        return

    # Routenliste abrufen
    routes = fetch_routes(selected_container)

    # Programm beenden, wenn keine Routen vorhanden sind
    if not routes:
        return

    # Route auswählen
    selected_route = choose_item("Verfügbare Routen", routes)

    # Programm beenden, wenn Auswahl ungültig ist
    if selected_route is None:
        return

    # CSV-Datei herunterladen
    csv_path = download_csv(selected_container, selected_route)

    # Programm beenden, wenn Download fehlgeschlagen ist
    if csv_path is None:
        return

    # CSV-Datei einlesen
    data_frame = read_csv_file(csv_path)

    # Grenzwertverletzungen berechnen
    data_frame = calculate_violations(data_frame)

    # Kennzahlen berechnen
    statistics = calculate_statistics(data_frame)

    # Diagramme erstellen
    charts = create_charts(data_frame, selected_container, selected_route)

    # Interaktive Karte erstellen
    map_path = create_map(data_frame, selected_container, selected_route)

    # PDF-Bericht erstellen
    pdf_path = create_pdf_report(selected_container, selected_route, statistics, charts)

    # Abschlussmeldung anzeigen
    print()
    print("Auswertung abgeschlossen.")
    print(f"Karte gespeichert: {map_path}")
    print(f"Bericht gespeichert: {pdf_path}")


# Programm starten
if __name__ == "__main__":
    main()