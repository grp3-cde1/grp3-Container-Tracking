# ReportLab – PDF-Berichte erstellen

`reportlab` erzeugt den PDF-Bericht der Retrospektive-App mit Titel, Metadaten-Tabelle, Kennzahlen, Fazit, Diagrammen und Routengrafik.

Bezug zum Code: `OutputCreator.create_pdf_report()`.

---

## 1. Importe

```python
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak,
)
```

---

## 2. Ein PDF-Dokument vorbereiten

```python
document = SimpleDocTemplate(
    str(pdf_path),
    pagesize=A4,
    rightMargin=1.5 * cm,
    leftMargin=1.5 * cm,
    topMargin=1.5 * cm,
    bottomMargin=1.5 * cm,
)
```

`SimpleDocTemplate` ist das Grundgerüst. `str(pdf_path)` wandelt den `Path` in Text um.

---

## 3. Die „story": Inhalte sammeln

In ReportLab sammelt man alle Inhalte in einer Liste namens `story`:

```python
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Retrospektiver Transportbericht", styles["Title"]))
story.append(Spacer(1, 0.4 * cm))
```

- `Paragraph(text, stil)` ist ein Textabschnitt.
- `styles["Title"]`, `styles["Heading2"]`, `styles["Normal"]` sind vordefinierte Stile.
- `Spacer` fügt vertikalen Abstand ein.

---

## 4. Eine Tabelle einfügen

```python
metadata = [
    ["Container", container],
    ["Route", route],
    ["Start", start_time.strftime("%d.%m.%Y %H:%M")],
    ["Ende", end_time.strftime("%d.%m.%Y %H:%M")],
]
metadata_table = Table(metadata, colWidths=[5 * cm, 10 * cm])
metadata_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
    ])
)
story.append(metadata_table)
```

`strftime("%d.%m.%Y %H:%M")` formatiert ein Datum lesbar.

---

## 5. Bilder (Diagramme) einfügen

```python
story.append(Paragraph("Temperaturverlauf", styles["Heading2"]))
story.append(Image(str(charts["temperature"]), width=16 * cm, height=6 * cm))
```

`charts` ist das Dictionary mit den Pfaden zu den von matplotlib erstellten PNG-Dateien.

---

## 6. Seitenumbruch

```python
story.append(PageBreak())
```

---

## 7. PDF erzeugen

```python
document.build(story)
```

`build()` schreibt alle Elemente der `story` nacheinander in die PDF-Datei. Der Dateiname enthält Container, Route und einen Zeitstempel, z. B. `reports/grp3_kriens-horw_2026-06-05_13-57_report.pdf`.

---

## Zusammenfassung

```text
SimpleDocTemplate  → das PDF-Grundgerüst
getSampleStyleSheet → vordefinierte Textstile
Paragraph / Spacer → Text und Abstände
Table / TableStyle → Tabellen
Image              → Diagramme einfügen
PageBreak          → neue Seite
document.build()   → PDF erzeugen
```