# Matplotlib – Diagramme erstellen

`matplotlib` erzeugt die Diagramme der Retrospektive-App: Temperaturverlauf, Feuchtigkeitsverlauf, Grenzwertverletzungen und die statische Routengrafik.

```python
import matplotlib.pyplot as plt
```

Bezug zum Code: `OutputCreator.create_temperature_chart()` und die weiteren `create_*_chart()`-Methoden.

---

## 1. Ein Liniendiagramm

```python
plt.figure(figsize=(10, 4))                 # Grösse
plt.plot(
    data_frame["timestamp"],
    data_frame["temperature"],
    color="tab:red",
    label="Temperatur",
)
plt.title("Temperaturverlauf")
plt.xlabel("Zeit")
plt.ylabel("Temperatur in °C")
plt.legend()
plt.tight_layout()
plt.savefig(chart_path, dpi=150)            # als Bild speichern
plt.close()                                 # Figur schliessen
```

`plt.close()` ist wichtig: Es gibt den Speicher frei, damit sich nicht mehrere Diagramme überlagern.

---

## 2. Grenzlinien einzeichnen

Die Grenzwerte werden als gestrichelte Linien dargestellt:

```python
plt.axhline(TEMP_MIN, linestyle="--", color="gray",  label=f"Minimum {TEMP_MIN} °C")
plt.axhline(TEMP_MAX, linestyle="--", color="black", label=f"Maximum {TEMP_MAX} °C")
```

---

## 3. Ein Balkendiagramm

Für die Grenzwertverletzungen:

```python
labels = ["Temperatur", "Feuchtigkeit", "Ohne Verletzung"]
values = [
    int(data_frame["temp_violation"].sum()),
    int(data_frame["humidity_violation"].sum()),
    int((~data_frame["any_violation"]).sum()),
]
plt.bar(labels, values, color=["tab:red", "tab:blue", "tab:green"])
```

---

## 4. Ein Streudiagramm (Routengrafik)

Die Route als Linie, Messpunkte als Punkte (grün = ok, rot = Verletzung):

```python
plt.plot(data_frame["longitude"], data_frame["latitude"], color="gray", label="Route")
plt.scatter(ok_points["longitude"],  ok_points["latitude"],  color="green", label="OK")
plt.scatter(bad_points["longitude"], bad_points["latitude"], color="red",   label="Verletzung")
```

---

## Zusammenfassung

```text
plt.figure()    → neues Diagramm
plt.plot()      → Linie
plt.bar()       → Balken
plt.scatter()   → Punkte
plt.axhline()   → waagrechte Linie (Grenzwert)
plt.savefig()   → als PNG speichern
plt.close()     → Diagramm schliessen
```