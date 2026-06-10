# Folium – interaktive Karten

`folium` erzeugt die interaktive HTML-Karte der Retrospektive-App. Im Browser kann man zoomen, die Route verfolgen und einzelne Messpunkte anklicken.

```python
import folium
```

Bezug zum Code: `OutputCreator.create_map()`.

---

## 1. Eine Karte erstellen

Die Karte wird auf den Mittelpunkt der Route zentriert:

```python
center_lat = data_frame["latitude"].mean()
center_lon = data_frame["longitude"].mean()

map_object = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13,
    tiles="OpenStreetMap",
)
```

---

## 2. Die Route als Linie

```python
coordinates = data_frame[["latitude", "longitude"]].values.tolist()

folium.PolyLine(
    coordinates,
    color="blue",
    weight=4,
    opacity=0.8,
    tooltip="Route",
).add_to(map_object)
```

`.add_to(map_object)` fügt das Element der Karte hinzu.

---

## 3. Messpunkte als Marker

Für jeden Messpunkt ein Kreis, eingefärbt nach Grenzwertverletzung:

```python
for _, row in data_frame.iterrows():
    marker_color = "red" if row["any_violation"] else "green"

    popup_text = (
        f"Zeit: {row['timestamp']}<br>"
        f"Temperatur: {row['temperature']} °C<br>"
        f"Feuchtigkeit: {row['humidity']} %"
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
```

Der `popup_text` nutzt HTML (`<br>` = Zeilenumbruch) und erscheint beim Anklicken eines Punktes.

---

## 4. Die Karte speichern

```python
map_object.save(map_path)   # z. B. maps/grp3_kriens-horw_..._map.html
```

Die Datei kann anschliessend im Browser geöffnet werden.

---

## Zusammenfassung

```text
folium.Map()           → Karte mit Mittelpunkt und Zoom
folium.PolyLine()      → Route als Linie
folium.CircleMarker()  → Messpunkt als Kreis
folium.Popup()         → Info beim Anklicken
.add_to(map)           → Element zur Karte hinzufügen
map.save(pfad)         → als HTML speichern
```