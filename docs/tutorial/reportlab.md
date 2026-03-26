# Reportlab

Vorarbeit:
- Reportlab installieren
- Mit OS den Ordner Reports erstellen (/ Prüfen ob er existiert)
```python
os.makedirs("reports", exist_ok=True)
```

## Erste PDF-Datei mit ReportLab erstellen
Um zu prüfen, ob `ReportLab` korrekt installiert und importiert wurde, erstellen wir zuerst ein leeres PDF-Dokument.

Dafür werden am Ende des Codes folgende Zeilen eingefügt:

```python
pdf_path = "reports/test_report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4)
doc.build([])

print(f"PDF gespeichert: {pdf_path}")
```

Zuerst wird mit `pdf_path` der Speicherort der Datei festgelegt.  
Die PDF wird im zuvor erstellten Ordner `reports` gespeichert und erhält den Namen `test_report.pdf`.

Anschliessend wird mit `SimpleDocTemplate(...)` das Grundgerüst der PDF-Datei erstellt.  
Mit `pagesize=A4` wird festgelegt, dass das Dokument im A4-Format erzeugt wird.

Die Methode `doc.build([])` erstellt schliesslich die PDF-Datei. Da die Liste aktuell leer ist, enthält das Dokument noch keinen Inhalt und dient nur als Funktionstest.

Über die `print(...)`-Ausgabe kann in der Konsole überprüft werden, ob die Datei erfolgreich gespeichert wurde.

## Ersten Inhalt in die PDF einfügen
Nachdem die PDF-Erstellung grundsätzlich funktioniert, kann nun der erste Inhalt ergänzt werden.  
Dafür werden zunächst zusätzliche Module importiert:

```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from reportlab.lib.units import cm

```

`Paragraph` wird verwendet, um Textblöcke in die PDF einzufügen.  
Mit `getSampleStyleSheet()` stellt ReportLab mehrere vordefinierte Textstile bereit, zum Beispiel für Titel oder normalen Fliesstext.

Der bisherige Testcode wird anschliessend erweitert:

```python
pdf_path = "reports/test_report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4)

styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Retrospektiver Bericht", styles["Title"]))

doc.build(story)

print(f"PDF gespeichert: {pdf_path}")
```

Mit `styles = getSampleStyleSheet()` werden die Standard-Formatvorlagen geladen.  
Danach wird mit `story = []` eine leere Liste erstellt. In dieser Liste werden alle Inhalte gesammelt, die später in der PDF angezeigt werden sollen.

Die Zeile

```python
story.append(Paragraph("Retrospektiver Bericht", styles["Title"]))
```

fügt den ersten Text in die PDF ein.  
Dabei wird mit `Paragraph(...)` ein Textabschnitt erstellt und mit `styles["Title"]` als Titel formatiert.

Am Ende wird nicht mehr `doc.build([])`, sondern `doc.build(story)` verwendet.  
Dadurch wird die PDF mit dem Inhalt aus der Liste `story` erstellt.

Das Ergebnis ist eine PDF-Datei, die nun nicht mehr leer ist, sondern bereits eine erste Überschrift enthält. 

## Dynamische Daten für den Bericht verwenden
Statt feste Beispielwerte in die PDF einzutragen, können direkt die Daten aus dem bestehenden Skript verwendet werden.  
Dadurch wird der Bericht automatisch mit den Informationen der ausgewählten Route und des ausgewählten Containers gefüllt.

Ausserdem wird auch der Dateiname der PDF angepasst, damit nicht mehr jede Datei `test_report.pdf` heisst, sondern den Namen der gewählten Route enthält.

Der PDF-Block wird dafür wie folgt erweitert:

```python
pdf_path = f"reports/{chosen_route}_report.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=A4)

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

doc.build(story)

print(f"PDF gespeichert: {pdf_path}")
```

Zuerst wird mit

```python
pdf_path = f"reports/{chosen_route}_report.pdf"
```

der Dateiname der PDF dynamisch erstellt.  
Dadurch trägt jede erzeugte PDF den Namen der ausgewählten Route und wird im Ordner `reports` gespeichert.

Anschliessend werden Start- und Endzeit der Messdaten aus dem DataFrame `track_df` bestimmt:

```python
start_time = track_df["timestamp"].min()
end_time = track_df["timestamp"].max()
```

`start_time` enthält dabei den frühesten Zeitstempel, `end_time` den spätesten.

Mit `strftime(...)` werden diese Zeitstempel anschliessend in ein lesbares Format umgewandelt:

```python
date_str = start_time.strftime("%d.%m.%Y")
time_range_str = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
```

`date_str` enthält das Datum, während `time_range_str` den Zeitraum der Route als Uhrzeitbereich darstellt.

Danach werden die Informationen mit mehreren `Paragraph`-Elementen zur Liste `story` hinzugefügt.  
Neben der Überschrift werden nun auch Route, Datum, Uhrzeit und Container direkt aus den vorhandenen Daten in die PDF übernommen. `Spacer` fügt einen vertikalen Abstand zwischen den Elementen ein.

Am Ende wird mit `doc.build(story)` die PDF-Datei mit diesen Inhalten erzeugt.

Auf diese Weise wird aus der bisherigen Test-PDF ein erster einfacher aber dynamischer Bericht.

Wie folgt wird dieser nun aussehen
[Beispielbericht öffnen](docs/tutorial/example_reports/report_1.pdf)