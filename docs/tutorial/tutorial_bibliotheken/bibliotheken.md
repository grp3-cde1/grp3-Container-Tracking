# Python Bibliotheken

Python-Bibliotheken sind Sammlungen von vorgefertigtem Code, die zusätzliche Funktionen bereitstellen.  
Sie helfen dabei, Probleme schneller zu lösen, ohne alles selbst programmieren zu müssen.

Eine Bibliothek kann aus mehreren **Modulen** bestehen.  
Ein **Modul** ist meistens eine einzelne Python-Datei mit Funktionen, Klassen oder Variablen.

Beispiel:
- **Bibliothek:** `math`, diese Bibliothek beinhaltet verschiedene vorgefertigte Lösungen zu Mathematischen Problemmstellungen
- **Modul/Funktionen daraus:** `sqrt()`, `pi`, `sin()`

Bibliotheken machen Python flexibler und effizienter, da man für viele Aufgaben bereits bestehende Lösungen nutzen kann.

## Installation

Viele Bibliotheken müssen zuerst installiert werden, bevor man sie verwenden kann.  
Das geschieht zum Beispiel mit dem Paketmanager `pip`.

(Installation PIP: https://pip.pypa.io/en/stable/installation/)

Beispiel zur Installation einer Bibliothek mit pip:

```bash
pip install numpy
```

Falls mehrere Python-Versionen installiert sind, kann auch dieser Befehl nötig sein:

```bash
pip3 install numpy
```

Um zu prüfen, ob eine Bibliothek erfolgreich installiert wurde, kann man sie danach in Python importieren.

## Import

Nach der Installation muss eine Bibliothek in das Python-Programm eingebunden werden.  
Das geschieht mit dem Befehl `import`.

Beispiel für den Import einer ganzen Bibliothek:

```python
import math
```

Danach kann man auf die Inhalte der Bibliothek zugreifen:

```python
print(math.sqrt(16))
```

Man kann Bibliotheken auch mit einem Kürzel importieren:

```python
import numpy as np
```

Das ist besonders praktisch bei Bibliotheken, die oft verwendet werden.

```python
import numpy as np

array = np.array([1, 2, 3, 4, 5])
print(array)
```

### Import einzelner Module

Statt eine komplette Bibliothek zu importieren, kann man auch gezielt einzelne Bestandteile importieren.

Beispiel:

```python
from math import sqrt
```

Dann kann die Funktion direkt verwendet werden:

```python
print(sqrt(16))
```

Es können auch mehrere Elemente gleichzeitig importiert werden:

```python
from math import sqrt, pi
```

## Übersicht der behandelten Bibliotheken

Im Folgenden findest du eine Übersicht der Bibliotheken sowie das dazugehörige Tutorial

- [GeoPandas](geopandas.md)
- [OS](os.md)
- [ReportLab](reportlab.md)
- [Folium](folium.md)
