# -*- coding: utf-8 -*-
"""
Librairie Python 3 pour la physique appliquée au lycée.

Modules disponibles de la librairie "physapp" :

- modelisation :
    Modélisation de courbes (linéaire, affine, parabolique, exponentielle, ...)

    Exemple :
    >>> from physapp.modelisation import ajustement_parabolique

- csv :
    Importation et exportation de données au format CSV pour Avimeca3, Regavi, Regressi, Latis, ...

    Exemple :
    >>> from physapp.csv import import_avimeca3_txt

- signal :
    Routines pour le traitement des signaux.
    
    Exemple :
    >>> from physapp.signal import spectre_amplitude


@author: David Thérincourt - 2022
"""

from physapp.modelisation import *
from physapp.csv import import_txt, import_avimeca3_txt, import_regressi_csv, import_regressi_txt
from physapp.signal import import_ltspice_csv, import_oscillo_csv, integre, spectre_amplitude, spectre_RMS, spectre_RMS_dBV
