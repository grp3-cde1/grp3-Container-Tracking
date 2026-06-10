# Pandas – Daten verarbeiten

`pandas` ist die wichtigste Bibliothek im Projekt. Beide Apps nutzen sie:
- die **Retrospektive-App**, um die CSV-Datei einzulesen und auszuwerten
- der **Live-Monitor**, um eingehende Messpunkte zu sammeln

Importiert wird sie so:

```python
import pandas as pd
```

---

## 1. Der DataFrame

Ein **DataFrame** ist eine Tabelle mit Zeilen und Spalten. Vergleichbar mit einem Excel-Blatt.

```text
timestamp              latitude    longitude   temperature  humidity
2026-06-05 13:57:46    47.00022    8.25810     24           72
2026-06-05 13:57:51    47.00028    8.25826     24           72
```

---

## 2. Eine CSV-Datei einlesen

Die CSV-Dateien des Webservice haben **keine Kopfzeile**. Deshalb geben wir die Spaltennamen selbst an:

```python
data_frame = pd.read_csv(
    file_path,
    header=None,
    names=["timestamp", "latitude", "longitude", "temperature", "humidity"],
)
```

Bezug zum Code: `DataProcessor.read_csv_file()`.

---

## 3. Den Zeitstempel umwandeln

Anfangs ist `timestamp` nur Text. Damit man damit rechnen kann, wandeln wir ihn in ein echtes Datum um:

```python
data_frame["timestamp"] = pd.to_datetime(data_frame["timestamp"])
```

Danach funktionieren z. B. `.min()` (früheste Zeit) und `.max()` (späteste Zeit).

---

## 4. Auf Spalten zugreifen

```python
data_frame["temperature"]          # eine ganze Spalte
data_frame["temperature"].mean()   # Durchschnitt
data_frame["temperature"].max()    # Maximum
len(data_frame)                    # Anzahl Zeilen
```

---

## 5. Neue Spalten berechnen (Vektorisierung)

pandas rechnet auf der ganzen Spalte auf einmal – ohne Schleife:

```python
data_frame["temp_violation"] = (
    (data_frame["temperature"] < TEMP_MIN)
    | (data_frame["temperature"] > TEMP_MAX)
)
```

`|` bedeutet „oder", `&` bedeutet „und". Das Ergebnis ist eine Spalte aus `True`/`False`. Bezug zum Code: `DataProcessor.calculate_violations()`.

---

## 6. Zeilen filtern

```python
bad_points = data_frame[data_frame["any_violation"]]    # nur Verletzungen
ok_points  = data_frame[~data_frame["any_violation"]]   # ~ bedeutet "nicht"
```

---

## 7. Über Zeilen iterieren

Für die Karte braucht der `OutputCreator` jeden Punkt einzeln:

```python
for _, row in data_frame.iterrows():
    print(row["latitude"], row["longitude"])
```

---

## 8. Daten anhängen (Live-Monitor)

Der Live-Monitor baut seinen DataFrame Nachricht für Nachricht auf:

```python
new_row = pd.DataFrame([data])
live_data = pd.concat([live_data, new_row], ignore_index=True)
last_row = live_data.iloc[-1]      # die letzte Zeile
```

---

## Zusammenfassung

```text
pd.read_csv(...)        → CSV einlesen
pd.to_datetime(...)     → Text in Datum umwandeln
df["spalte"]            → Spalte ansprechen
.mean()/.min()/.max()   → Kennzahlen
df[bedingung]           → Zeilen filtern
pd.concat([...])        → Zeilen anhängen
df.iloc[-1]             → letzte Zeile
```