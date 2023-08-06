# -*- coding: utf-8 -*-
"""
Module de modélisation de courbes pour la physique appliquée
@author: David Thérincourt
"""

import numpy as np

#--------------------------
# Fonctions mathématiques
#--------------------------

# Fonction linéaire : y=a*x
def fct_lineaire(x, a) :
    """
    Fonction lineaire du type y = a*x

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    a (float) :

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return a*x


# # Fonction parabolique : y = ax^2 + bx  + c
# def fct_parabole(x, a, b, c) :
#     """
#     Fonction parabolique du type y = a*x**2 + b*x + c

#     Paramètres :
#     x (liste ou tableau Numpy) : abscisses.
#     a (float) :
#     b (float) :
#     c (float) :

#     Retourne :
#     Valeur de la fonction (float ou tableau Numpy)
#     """
#     return a*x**2+b*x+c



# Fonction exponentielle croissante : y = A*(1-exp(-(x-x0)/tau))
def fct_exponentielle_croissante(x, A, tau, x0=0):
    """
    Fonction exponenetielle croissante du type y = A*(1-exp(-(x-x0)/tau))

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.

    Paramètre optionnel :
    x0 (0 par défaut) : retard.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return A*(1-np.exp(-(x-x0)/tau))

# Fonction exponentielle décroissante : y = A*exp(-(x-x0)/tau)
def fct_exponentielle_decroissante(x, A, tau, x0=0):
    """
    Fonction exponenetielle décroissante du type y = A*exp(-(x-x0)/tau)

    Paramètres :
    x (liste ou tableau Numpy) : abscisses.
    A (float)  : limite à l'infini.
    tau (float) : constante de temps.

    Paramètre optionnel :
    x0 (0 par défaut) : retard.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return A*np.exp(-(x-x0)/tau)





############## Ordre 1 - Passe-bas  ################

def transmittance_ordre1_passe_bas(f, T0, f0):
    """
    Fonction transmittance d'un système d'ordre 1 passe-bas

    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        T0 (float)                 : amplification statique.
        f0 (float)                 : fréquence propre.

    Retourne :
        T (float)
    """
    return T0/np.sqrt(1+(f/f0)**2)

def gain_ordre1_passe_bas(f, G0, f0):
    """
    Fonction gain d'un système d'ordre 1 passe-bas

        G = G0 - 20log(sqrt(1+(f/f0)^2))

    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        G0 (float)                 : gain statique.
        f0 (float)                 : fréquence propre.

    Retourne :
        G (float)
    """
    return G0 - 20*np.log10(np.sqrt(1+(f/f0)**2))

def dephasage_ordre1_passe_bas(f, f0):
    """
    Fonction déphasage d'un système d'ordre 1 passe-bas

        phi = - arctan(f/f0)

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.

    Retourne :
        phi en degré (float)
    """
    return -np.arctan(f/f0)*180/np.pi





############## Ordre 1 - Passe-haut  ################

def transmittance_ordre1_passe_haut(f, T0, f0):
    """
    Fonction transmittance d'un système d'ordre 1 passe-haut.

    Paramètres :
    f (liste ou tableau Numpy) : fréquence.
    T0 (float)  : Amplification statique.
    f0 (float) : fréquence propre.

    Retourne :
    Valeur de la fonction (float ou tableau Numpy)
    """
    return T0*(f/f0)/np.sqrt(1+(f/f0)**2)


def gain_ordre1_passe_haut(f, G0, f0):
    """
    Fonction gain d'un système d'ordre 1 passe-haut.

        G = G0 + 20log(f/f0) - 20log(sqrt(1+(f/f0)^2))

    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        G0 (float)                 : gain statique.
        f0 (float)                 : fréquence propre.

    Retourne :
        G (float)
    """
    return G0 + 20*np.log10(f/f0) - 20*np.log10(np.sqrt(1+(f/f0)**2))


def dephasage_ordre1_passe_haut(f, f0):
    """
    Fonction déphasage d'un système d'ordre 1 passe-haut.

        phi = 90 - arctan(f/f0)

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.

    Retourne :
        phi en degré (float)
    """
    return 90 - np.arctan(f/f0)*180/np.pi



############## Ordre 2 - Passe-bas  ################

def transmittance_ordre2_passe_bas(f, T0, f0, m):
    """
    Fonction transmittance d'un système d'ordre 2 passe bas.

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        T0 (float)                  : amplification statique.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        T (float)
    """
    return T0/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)

def gain_ordre2_passe_bas(f, G0, f0, m):
    """
    Fonction gain d'un système d'ordre 2 passe bas.


    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        G0 (float)                 : gain statique.
        f0 (float)                 : fréquence propre.
        m (float)                  : coefficient d'amortissement

    Retourne :
        G (float)
    """
    return G0 - 20*np.log10(np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2))


def dephasage_ordre2_passe_bas(f, f0, m):
    """
    Fonction déphasage d'un système d'ordre 2 passe bas.


    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.
        m (float)                   : coefficient d'amortissement

    Retourne :
        phi en degré (float)
    """
    return -np.arctan((2*m*f/f0)/(1-(f/f0)**2))*180/np.pi




############## Ordre 2 - Passe-haut  ################

def transmittance_ordre2_passe_haut(f, T0, f0, m):
    """
    Fonction transmittance d'un système d'ordre 2 passe-haut.

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        T0 (float)                  : amplification statique.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        T (float)
    """
    return -T0*(f/f0)**2/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)


def gain_ordre2_passe_haut(f, G0, f0, m):
    """
    Fonction gain d'un système d'ordre 2 passe-haut.


    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        G0 (float)                  : gain statique.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        G (float)
    """
    return G0 + 20*np.log10((f/f0)**2) - 20*np.log10(np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2))


def dephasage_ordre2_passe_haut(f, f0, m):
    """
    Fonction déphasage d'un système d'ordre 2 passe-haut.


    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        phi en degré (float)
    """
    return 180 - np.arctan((2*m*f/f0)/(1-(f/f0)**2))*180/np.pi



############## Ordre 2 - Passe-bande  ################

def transmittance_ordre2_passe_bande(f, T0, f0, m):
    """
    Fonction transmittance d'un système d'ordre 2 passe-bande.

    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        T0 (float)                  : Amplification statique.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        T (float)
    """
    return T0*2*m*(f/f0)/np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2)


def gain_ordre2_passe_bande(f, G0, f0, m):
    """
    Fonction gain d'un système d'ordre 2 passe-bande.


    Paramètres :
        f (liste ou tableau Numpy) : fréquence.
        G0 (float)                 : gain statique.
        f0 (float)                 : fréquence propre.
        m  (float)                 : coefficient d'amortissement

    Retourne :
        G (float)
    """
    return G0 + 20*np.log10(2*m*f/f0) - 20*np.log10(np.sqrt((1-(f/f0)**2)**2+(2*m*f/f0)**2))


def dephasage_ordre2_passe_bande(f, f0, m):
    """
    Fonction déphasage d'un système d'ordre 2 passe-bande.


    Paramètres :
        f  (liste ou tableau Numpy) : fréquence.
        f0 (float)                  : fréquence propre.
        m  (float)                  : coefficient d'amortissement

    Retourne :
        phi en degré (float)
    """
    return 90 - np.arctan((2*m*f/f0)/(1-(f/f0)**2))*180/np.pi





