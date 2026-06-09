"""
Ausgabe-Erstellung für die objektorientierte Retrospective-App.

Diese Datei enthält die Klasse OutputCreator.
Sie erstellt Diagramme, interaktive Karten und PDF-Berichte.
"""

import folium
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
)

from .config import (
    MAPS_DIR,
    CHARTS_DIR,
    REPORTS_DIR,
    TEMP_MIN,
    TEMP_MAX,
    HUM_MAX,
)

class OutputCreator:
    """
    Verantwortlich für die Erstellung von Diagrammen, Karten und PDF-Berichten.
    """

    def build_file_timestamp(self, data_frame):
        """
        Erstellt einen Zeitstempel für Dateinamen (erster Messpunkt).

        Parameter:
            data_frame: pandas DataFrame mit timestamp-Spalte

        Rückgabe:
            Formatierter Zeitstempel als String, z. B. 2026-06-09_14-30
        """

        first_timestamp = data_frame["timestamp"].min()
        return first_timestamp.strftime("%Y-%m-%d_%H-%M")
    
    def create_temperature_chart(self, data_frame, container, route):
        """
        Erstellt ein Diagramm für den Temperaturverlauf.

        Parameter:
            data_frame: pandas DataFrame mit Zeitstempel und Temperatur
            container:  Container-ID für den Dateinamen
            route:      Routen-ID für den Dateinamen

        Rückgabe:
            Pfad zum gespeicherten Temperaturdiagramm
        """

        timestamp_string = self.build_file_timestamp(data_frame)
        chart_path = CHARTS_DIR / f"{container}_{route}_{timestamp_string}_temperature.png"

        plt.figure(figsize=(10, 4))

        plt.plot(
            data_frame["timestamp"],
            data_frame["temperature"],
            color="tab:red",
            label="Temperatur",
        )

        plt.axhline(
            TEMP_MIN,
            linestyle="--",
            color="gray",
            label=f"Minimum {TEMP_MIN} °C",
        )

        plt.axhline(
            TEMP_MAX,
            linestyle="--",
            color="black",
            label=f"Maximum {TEMP_MAX} °C",
        )

        plt.title("Temperaturverlauf")
        plt.xlabel("Zeit")
        plt.ylabel("Temperatur in °C")
        plt.xticks(rotation=35)
        plt.legend()
        plt.tight_layout()

        plt.savefig(chart_path, dpi=150)
        plt.close()

        return chart_path

    def create_humidity_chart(self, data_frame, container, route):
        """
        Erstellt ein Diagramm für den Feuchtigkeitsverlauf.

        Parameter:
            data_frame: pandas DataFrame mit Zeitstempel und Feuchtigkeit
            container:  Container-ID für den Dateinamen
            route:      Routen-ID für den Dateinamen

        Rückgabe:
            Pfad zum gespeicherten Feuchtigkeitsdiagramm
        """

        timestamp_string = self.build_file_timestamp(data_frame)
        chart_path = CHARTS_DIR / f"{container}_{route}_{timestamp_string}_humidity.png"

        plt.figure(figsize=(10, 4))

        plt.plot(
            data_frame["timestamp"],
            data_frame["humidity"],
            color="tab:blue",
            label="Feuchtigkeit",
        )

        plt.axhline(
            HUM_MAX,
            linestyle="--",
            color="black",
            label=f"Maximum {HUM_MAX} %",
        )

        plt.title("Feuchtigkeitsverlauf")
        plt.xlabel("Zeit")
        plt.ylabel("Feuchtigkeit in %")
        plt.xticks(rotation=35)
        plt.legend()
        plt.tight_layout()

        plt.savefig(chart_path, dpi=150)
        plt.close()

        return chart_path

    def create_violation_chart(self, data_frame, container, route):
        """
        Erstellt ein Balkendiagramm zu Grenzwertverletzungen.

        Parameter:
            data_frame: pandas DataFrame mit Violation-Spalten
            container:  Container-ID für den Dateinamen
            route:      Routen-ID für den Dateinamen

        Rückgabe:
            Pfad zum gespeicherten Violations-Diagramm
        """

        timestamp_string = self.build_file_timestamp(data_frame)
        chart_path = CHARTS_DIR / f"{container}_{route}_{timestamp_string}_violations.png"

        labels = ["Temperatur", "Feuchtigkeit", "Ohne Verletzung"]

        values = [
            int(data_frame["temp_violation"].sum()),
            int(data_frame["humidity_violation"].sum()),
            int((~data_frame["any_violation"]).sum()),
        ]

        colors_list = ["tab:red", "tab:blue", "tab:green"]

        plt.figure(figsize=(8, 4))
        plt.bar(labels, values, color=colors_list)

        plt.title("Grenzwertverletzungen")
        plt.ylabel("Anzahl Messpunkte")
        plt.tight_layout()

        plt.savefig(chart_path, dpi=150)
        plt.close()

        return chart_path

    def create_static_route_chart(self, data_frame, container, route):
        """
        Erstellt eine statische Routendarstellung für den PDF-Bericht.

        Parameter:
            data_frame: pandas DataFrame mit Koordinaten und Violation-Spalten 
            container:  Container-ID für den Dateinamen
            route:      Routen-ID für den Dateinamen

        Rückgabe:
            Pfad zur gespeicherten Routengrafik
        """

        timestamp_string = self.build_file_timestamp(data_frame)
        chart_path = CHARTS_DIR / f"{container}_{route}_{timestamp_string}_route.png"

        ok_points = data_frame[~data_frame["any_violation"]]
        bad_points = data_frame[data_frame["any_violation"]]

        plt.figure(figsize=(6, 6))

        plt.plot(
            data_frame["longitude"],
            data_frame["latitude"],
            color="gray",
            linewidth=1,
            label="Route",
        )

        plt.scatter(
            ok_points["longitude"],
            ok_points["latitude"],
            s=18,
            color="green",
            label="OK",
        )

        plt.scatter(
            bad_points["longitude"],
            bad_points["latitude"],
            s=25,
            color="red",
            label="Verletzung",
        )

        plt.title("Route mit markierten Verletzungen")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend()
        plt.tight_layout()

        plt.savefig(chart_path, dpi=150)
        plt.close()

        return chart_path
    
    def create_charts(self, data_frame, container, route):
        """
        Erstellt alle Diagramme für den Transport.

        Parameter:
            data_frame: pandas DataFrame mit Messdaten und Verletzungsspalten
            container:  Container-ID für die Dateinamen
            route:      Routen-ID für die Dateinamen

        Rückgabe:
            Dictionary mit Pfaden zu allen Diagrammen
        """

        charts = {
            "temperature": self.create_temperature_chart(data_frame, container, route),
            "humidity": self.create_humidity_chart(data_frame, container, route),
            "violations": self.create_violation_chart(data_frame, container, route),
            "route": self.create_static_route_chart(data_frame, container, route),
        }

        return charts
    
    def create_conclusion(self, statistics):
        """
        Erstellt ein kurzes automatisches Fazit.

        Parameter:
            statistics: Dictionary mit Kennzahlen und Grenzwertverletzungen

        Rückgabe:
            Fazit als Text
        """

        if statistics["all_violations"] == 0:
            return "Der Transport war unauffällig. Es wurden keine Grenzwertverletzungen gefunden."

        conclusion_parts = []

        if statistics["temp_violations"] > 0:
            conclusion_parts.append(
                f"Es gab {statistics['temp_violations']} Temperaturverletzungen."
            )

        if statistics["humidity_violations"] > 0:
            conclusion_parts.append(
                f"Es gab {statistics['humidity_violations']} Feuchtigkeitsverletzungen."
            )

        conclusion_parts.append("Der Transport sollte genauer geprüft werden.")

        return " ".join(conclusion_parts)
    
    def create_pdf_report(self, container, route, statistics, charts, data_frame):
        """
        Erstellt einen PDF-Bericht zur ausgewählten Route.

        Parameter:
            container:  Container-ID
            route:      Routen-ID
            statistics: Dictionary mit Kennzahlen
            charts:     Dictionary mit Pfaden zu den Diagrammen
            data_frame: pandas DataFrame für den Zeitstempel im Dateinamen

        Rückgabe:
            Pfad zum gespeicherten PDF-Bericht
        """

        timestamp_string = self.build_file_timestamp(data_frame)
        pdf_path = REPORTS_DIR / f"{container}_{route}_{timestamp_string}_report.pdf"

        document = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )

        styles = getSampleStyleSheet()

        styles.add(
            ParagraphStyle(
                name="SmallText",
                parent=styles["Normal"],
                fontSize=9,
                leading=12,
            )
        )

        story = []

        start_time = statistics["start_time"]
        end_time = statistics["end_time"]

        story.append(Paragraph("Retrospektiver Transportbericht", styles["Title"]))
        story.append(Spacer(1, 0.4 * cm))

        metadata = [
            ["Container", container],
            ["Route", route],
            ["Start", start_time.strftime("%d.%m.%Y %H:%M")],
            ["Ende", end_time.strftime("%d.%m.%Y %H:%M")],
            ["Temperatur-Grenzwerte", f"{TEMP_MIN} °C bis {TEMP_MAX} °C"],
            ["Feuchtigkeits-Grenzwert", f"maximal {HUM_MAX} %"],
        ]

        metadata_table = Table(metadata, colWidths=[5 * cm, 10 * cm])

        metadata_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("PADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        story.append(metadata_table)
        story.append(Spacer(1, 0.6 * cm))

        story.append(Paragraph("Kennzahlen", styles["Heading2"]))

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

        statistics_table = Table(statistics_table_data, colWidths=[8 * cm, 6 * cm])

        statistics_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d9eaf7")),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("PADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )

        story.append(statistics_table)
        story.append(Spacer(1, 0.7 * cm))

        story.append(Paragraph("Automatisches Fazit", styles["Heading2"]))
        story.append(Paragraph(self.create_conclusion(statistics), styles["Normal"]))

        story.append(PageBreak())

        story.append(Paragraph("Temperaturverlauf", styles["Heading2"]))
        story.append(Image(str(charts["temperature"]), width=16 * cm, height=6 * cm))
        story.append(Spacer(1, 0.5 * cm))

        story.append(Paragraph("Feuchtigkeitsverlauf", styles["Heading2"]))
        story.append(Image(str(charts["humidity"]), width=16 * cm, height=6 * cm))
        story.append(Spacer(1, 0.5 * cm))

        story.append(Paragraph("Grenzwertverletzungen", styles["Heading2"]))
        story.append(Image(str(charts["violations"]), width=14 * cm, height=6 * cm))

        story.append(PageBreak())

        story.append(Paragraph("Statische Routendarstellung", styles["Heading2"]))
        story.append(
            Paragraph(
                "Grüne Punkte sind normale Messpunkte. Rote Punkte zeigen Grenzwertverletzungen.",
                styles["SmallText"],
            )
        )
        story.append(Spacer(1, 0.2 * cm))
        story.append(Image(str(charts["route"]), width=14 * cm, height=14 * cm))

        document.build(story)

        return pdf_path

    def create_map(self, data_frame, container, route):
        """
        Erstellt eine interaktive Karte mit der Transportroute.

        Parameter:
            data_frame: pandas DataFrame mit latitude und longitude
            container:  Container-ID für den Dateinamen
            route:      Routen-ID für den Dateinamen

        Rückgabe:
            Pfad zur gespeicherten HTML-Karte
        """

        timestamp_string = self.build_file_timestamp(data_frame)
        map_path = MAPS_DIR / f"{container}_{route}_{timestamp_string}_map.html"

        center_lat = data_frame["latitude"].mean()
        center_lon = data_frame["longitude"].mean()

        map_object = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=13,
            tiles="OpenStreetMap",
        )

        coordinates = data_frame[["latitude", "longitude"]].values.tolist()

        folium.PolyLine(
            coordinates,
            color="blue",
            weight=4,
            opacity=0.8,
            tooltip="Route",
        ).add_to(map_object)

        for i, row in data_frame.iterrows():
            marker_color = "red" if row["any_violation"] else "green"

            popup_text = (
                f"Zeit: {row['timestamp']}<br>"
                f"Temperatur: {row['temperature']} °C<br>"
                f"Feuchtigkeit: {row['humidity']} %<br>"
                f"Temperatur-Verletzung: {row['temp_violation']}<br>"
                f"Feuchtigkeits-Verletzung: {row['humidity_violation']}"
            )

            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=5,
                color=marker_color,
                fill=True,
                fill_color=marker_color,
                fill_opacity=0.8,
                popup=folium.Popup(popup_text, max_width=300),
            ).add_to(map_object)

        map_object.save(map_path)

        return map_path