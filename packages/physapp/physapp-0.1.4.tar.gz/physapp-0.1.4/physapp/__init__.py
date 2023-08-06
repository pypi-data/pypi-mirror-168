# -*- coding: utf-8 -*-
"""
Librairie Python 3 pour la physique appliquée au lycée.

Modules disponibles de la librairie "physapp" :

- modelisation :
    Modélisation de courbes (linéaire, affine, parabolique, exponentielle, ...)

    Exemple :
    >>> from physapp import ajustement_parabolique

- csv :
    Importation et exportation de données au format CSV pour Avimeca3, Regavi, Regressi, Latis, ...

    Exemple :
    >>> from physapp import import_avimeca3_txt

- pyboard :
    Exécution d'un programme MicroPython sur un microcontrôleur (Micro:bit, Pyboard, ESP32, ...)
    à partir d'un ordinateur par le port série (mode REPL RAW) à partir d'un fichier .py ou d'un
    script sous forme d'une chaîne de caractères sur plusieurs lignes

    Exemple :
    >>> from physapp import Pyboard
    >>> pyboard = Pyboard("/dev/ttyACM0")
    >>> reponse = pyboard.exec_file("hello.py")
    >>> print(reponse)


@author: David Thérincourt - 2020
"""

from physapp.modelisation import *
from physapp.csv import *
from physapp.pyboard import *
