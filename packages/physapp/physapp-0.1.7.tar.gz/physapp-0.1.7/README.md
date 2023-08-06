# Librairie Python pour la physique appliquée au lycée

## Installation

### A partir des dépôts de PyPi

Lancer dans un terminal :

    pip install physapp

### A partir de l'archive de la bibliothèque

Télécharger [ici](https://pypi.org/project/physapp/#files) le fichier `physapp-x.x.whl`. Les caractères `x` sont à remplacer par les numéros de version.

Dans une console Python dans le même répertoire que l'archive et lancer la commande suivante :

    pip install physapp-x.x.whl

## Module `physapp.modelisation`

Fonctions pour réaliser une modélisation d'une courbe du type `y=f(x)`.

### Fonctions

`ajustement_lineaire(x, y)`  

`ajustement_affine(x, y)`

`ajustement_parabolique(x, y)`

`ajustement_exponentielle_croissante(x, y)`

`ajustement_exponentielle_croissante_x0(x, y)`

`ajustement_exponentielle_decroissante(x, y)`

`ajustement_exponentielle_decroissante_x0(x, y)`

### Exemple

```python
import numpy as np
import matplotlib.pyplot as plt
from physapp.modelisation import ajustement_parabolique

x = np.array([0.003,0.141,0.275,0.410,0.554,0.686,0.820,0.958,1.089,1.227,1.359,1.490,1.599,1.705,1.801])
y = np.array([0.746,0.990,1.175,1.336,1.432,1.505,1.528,1.505,1.454,1.355,1.207,1.018,0.797,0.544,0.266])

[a, b, c] = ajustement_parabolique(x, y)
print(a, b, c)

x_mod = np.linspace(0,max(x),50)
y_mod = a*x_mod**2 + b*x_mod + c

plt.plot(x_mod, y_mod, '-')
plt.plot(x, y, 'x')
plt.show()
```

## Module `physapp.signal`

Module Module pour le traitement des signaux.

### Fonctions

`load_oscillo_csv(filename)`

`load_ltspice_csv(filename)`

`periode(t, y)`

`integre(x, y, xmin, xmax)`

`spectre_amplitude(t, y, T)`

̀`spectre_RMS(t, y, T)`

`spectre_RMS_dBV(t, y, T)`

### Exemple

```python
from physapp.signal import load_oscillo_csv, periode

t, u = load_oscillo_csv('scope.csv')
T = periode(t, u)
```

## Module `physapp.csv`

Module d'importation de tableau de données au format CSV à partir des logiciels Aviméca3, Regavi, ...

#### Fonctions

`import_avimeca3_txt(fichier)`  

`import_regavi_txt(fichier)`  



#### Exemple

```python
import matplotlib.pyplot as plt
from physapp.csv import import_avimeca3_txt

t, x, y = import_avimeca3_txt('data1_avimeca3.txt')

plt.plot(x,y,'.')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.grid()
plt.title("Trajectoire d'un ballon")
plt.show()
```

Le fichier `data.txt` est obtenu par l'exportation de données au format CSV dans le logiciel Aviméca3.
