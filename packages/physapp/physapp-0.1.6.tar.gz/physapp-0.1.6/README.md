# Librairie Python pour la physique appliquée au lycée

## Installation

### A partir des dépôts de PyPi

Lancer dans un terminal :

    pip install physapp

Dépendance à installer pour le module `pyboard` :

```python
pip install pyserial
```

### A partir de l'archive de la bibliothèque

Télécharger [ici](https://pypi.org/project/physapp/#files) le fichier `physapp-x.x.whl`. Les caractères `x` sont à remplacer par les numéros de version.

Dans une console Python dans le même répertoire que l'archive et lancer la commande suivante :

    pip install physapp-x.x.whl

## Utilisation

### Le module `modelisation`

Fonctions pour réaliser une modélisation d'une courbe du type `y=f(x)`.

#### Fonctions disponibles

| Fonctions                                         | Valeurs de retour    | Type de fonction modélisée   |
| ------------------------------------------------- | -------------------- | ---------------------------- |
| `ajustement_lineaire(x, y)`                       | `a`                  | `y=ax​`                      |
| `ajustement_affine(x, y)`                         | `a`  et `b`          | `y=ax+b​`                    |
| `ajustement_parabolique(x, y)`                    | `a` , `b` et  `c`    | `y=a x^2+bx+c​`              |
| `ajustement_exponentielle_croissante(x, y)`       | `A`  et `tau`        | `y = A*(1-exp(-x/tau))`      |
| `ajustement_exponentielle_croissante_x0(x, y)`    | `A` , `tau` et  `x0` | `y = A*(1-exp(-(x-x0)/tau))` |
| `ajustement_exponentielle_decroissante(x, y)`     | `A`  et `tau`        | `y = A*exp(-x/tau)`          |
| `ajustement_exponentielle_decroissante_x0(x, y) ` | `A` , `tau` et  `x0` | `y = A*exp(-(x-x0)/tau)`     |

#### Exemple :

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

### Le module `CSV`

Module d'importation de tableau de données au format CSV à partir des logiciels Aviméca3, Regavi, ...

#### Quelques fonctions disponibles

* `import_avimeca3_txt(fichier)`  ou `import_avimeca3_txt(fichier, sep=';')`
* `import_regavi_txt(fichier)`  ou `import_regavi_txt(fichier, sep=';')` 

Le paramètre `sep` (séparateur de données) est optionnel. La tabulation (`sep='\t'`) est le séparateur par défaut.

#### Exemple :

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
