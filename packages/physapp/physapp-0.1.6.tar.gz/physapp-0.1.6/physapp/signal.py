# David THERINCOURT - 2020
#
# This file is a modification of the original pyboard.py edit by  MicroPython project, http://micropython.org/
#
# The MIT License (MIT)
#
# Copyright (c) 2014-2019 Damien P. George
# Copyright (c) 2017 Paul Sokolovsky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
Module for signal traitement


"""
import numpy as np
from scipy.integrate import trapz
from numpy.fft import fft


def import_oscillo_csv(fileName):
    """
    Importe des données au format CSV à partir d'un oscilloscope numérique
    Keysight InfiniiVision 2000 X-Series
    
    Paramètre :
        fileName (str) : nom du fichier CSV
        
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    return np.genfromtxt(fileName, delimiter = ",", unpack = True, skip_header = 2, comments = '#')

def import_ltspice_csv(fileName):
    """
    Importe des données au format CSV à partir du logiciel LTSpice
    
    Paramètre :
        fileName (str) : nom du fichier CSV
        
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    return np.genfromtxt(fileName, delimiter = "\t", unpack = True, skip_header = 1, comments = '#')


def autocorrelation(y, N, i, M):
    """
    y : signal
    N : nombre de point de la fonction d'autocorrélation
    i : indice départ (i>N)
    M : nb points pour calculer la fonction d'autocorrélation
    
    """
    C = np.zeros(N)
    for k in range(i,i+M):
        for n in range(N):
            C[n] += y[k]*y[k-n]
    return C

def periode(t, u, period_axes=None, period_start=None):
    Te = t[1]-t[0]             # Période d'échantillonnage
    #N0 = np.where(t==0)[0][0] # Indice de t=0
    Ns = len(t)                # Nb points total
    N = Ns//2                  # Nb points pour autocorrélation = moitié
    tau = t[0:N]               # Retard de la fonction d'autocorrélation
    c = autocorrelation(u, N, N, Ns-N)
    N_periode = np.where(c == max(c))[0]     # Recherche indice premier maximum (a revoir !)
    T = (N_periode[0]+1)*Te                   # Calcul de la période
    if period_start == None:
        period_start = t[0]
    if period_axes != None:
        period_axes.axvspan(period_start, period_start+T , color='linen')
        
    return T

def integre(x, y, xmin, xmax, plot_axes=None):
    """ Calcule numériquement l'intégrale de la fonction y=f(x) entre
    les bornes xmin et xmax avec la méthode des trapèzes
    
    Paramètres :
        x         (numpy.ndarray)   : tableau Numpy de x
        y         (numpy.ndarray)   : tableau Numpy de y
        xmin      (float)           : borne inférieure pour l'intégration
        xmax      (float)           : borne supérieure pour l'intégration
        
    Paramètre optionnel :
        plot_axes = None (matplotlib.axes) : repère (axes) sur lequel tracé l'aire de l'intégration
        
    Retourne :
        Valeur (float)  : résultat de l'intégration.
    """
    if (xmin<x[0]) or (xmin>x[-2]):
        raise ValueError("Valeur de xmin en dehors de l'intervalle de x")
    if (xmax<x[1]) or (xmax>x[-1]):
        raise ValueError("Valeur de xmax en dehors de l'intervalle de x")
    if xmin>=xmax:
        raise ValueError("Valeur de xmin supérieure à la valeur de xmax")
    
    y = y[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    x = x[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    
    if plot_axes != None:
        plot_axes.fill_between(x,y,hatch='\\',facecolor='linen',  edgecolor='gray')
        
    return trapz(y)*(x[-1]-x[0])/len(x)




def spectre_amplitude(t, y, T, tmin=0, plot_period_axes=None):
    ''' Retourne le spectre d'amplitude d'un signal y(t).
    
    Paramètres :
        t     (numpy.ndarray)   : tableau Numpy de t
        y     (numpy.ndarray)   : tableau Numpy de y
        T     (float)           : période du signal y
        
    Paramètres optionnels :
        tmin = 0                (float)           : borne inférieure le calcul du spectre
        plot_period_axes = None (matplotlib.axes) : repère (axes) sur lequel tracer la sélection de la période
        
    Retourne :
        f, A  (numpy.ndarray, numpy.ndarray)    : Tableau Numpy des fréquences et des amplitudes
    '''
    
    if T>(t[-1]-t[0]):
        raise ValueError("Période T trop grande")
    
    if (tmin<t[0]) or (tmin>t[-2]):
        raise ValueError("Valeur de tmin en dehors de l'intervalle de t")
    
    tmax = tmin + T
    if tmax>t[-1]:
        raise ValueError("Valeur de tmin trop grande")
    
    if plot_period_axes != None:
        plot_period_axes.axvspan(tmin, tmax , color='linen')
    
    y = y[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    t = t[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    T = t[-1]-t[0]                   # Durée totale
    N = len(t)                       # Nb points
    freq = np.arange(N)*1.0/T        # Tableau des fréquences
    ampl = np.absolute(fft(y))/N     # Tableau des amplitudes
    ampl[1:-1] = ampl[1:-1]*2        #
    
    return freq, ampl                # Retourne fréquences et amplitudes



def spectre_RMS(t, y, T, tmin=0, plot_period_axes=None):
    ''' Retourne le spectre RMS d'un signal y(t).
    
    Paramètres :
        t     (numpy.ndarray)   : tableau Numpy de t
        y     (numpy.ndarray)   : tableau Numpy de y
        T     (float)           : période du signal y
        
    Paramètres optionnels :
        tmin = 0                (float)           : borne inférieure le calcul du spectre
        plot_period_axes = None (matplotlib.axes) : repère (axes) sur lequel tracer la sélection de la période
        
    Retourne :
        f, U  (numpy.ndarray, numpy.ndarray)    : Tableau Numpy des fréquences et des valeurs efficaces
    '''
    
    if T>(t[-1]-t[0]):
        raise ValueError("Période T trop grande")
    
    if (tmin<t[0]) or (tmin>t[-2]):
        raise ValueError("Valeur de tmin en dehors de l'intervalle de t")
    
    tmax = tmin + T
    if tmax>t[-1]:
        raise ValueError("Valeur de tmin trop grande")
    
    if plot_period_axes != None:
        plot_period_axes.axvspan(tmin, tmax , color='linen')
    
    y = y[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    t = t[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    T = t[-1]-t[0]                   # Durée totale
    N = len(t)                       # Nb points
    freq = np.arange(N)*1.0/T        # Tableau des fréquences
    ampl = np.absolute(fft(y))/N     # Tableau des amplitudes
    ampl[1:-1] = ampl[1:-1]*2        #
    
    return freq, ampl/np.sqrt(2)     # Retourne fréquences et valeurs RMS


def spectre_RMS_dBV(t, y, T, tmin=0, plot_period_axes=None):
    ''' Retourne le spectre RMS en dBV d'un signal y(t).
    
    Paramètres :
        t     (numpy.ndarray)   : tableau Numpy de t
        y     (numpy.ndarray)   : tableau Numpy de y
        T     (float)           : période du signal y
        
    Paramètres optionnels :
        tmin = 0                  (float)           : borne inférieure le calcul du spectre
        plot_period_axes = None   (matplotlib.axes) : repère (axes) sur lequel tracer la sélection de la période
        
    Retourne :
        f, U_dBV  (numpy.ndarray, numpy.ndarray)    : Tableau Numpy des fréquences et des valeurs efficaces en dBV
    '''
    
    if T>(t[-1]-t[0]):
        raise ValueError("Période T trop grande")
    if (tmin<t[0]) or (tmin>t[-2]):
        raise ValueError("Valeur de tmin en dehors de l'intervalle de t")
    
    tmax = tmin + T
    if tmax>t[-1]:
        raise ValueError("Valeur de tmin trop grande")
    
    if plot_period_axes != None:
        plot_period_axes.axvspan(tmin, tmax , color='linen')
    
    y = y[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    t = t[(t >= tmin) & (t < tmax)]  # Sélection sur une période
    T = t[-1]-t[0]                   # Durée totale
    N = len(t)                       # Nb points
    freq = np.arange(N)*1.0/T        # Tableau des fréquences
    ampl = np.absolute(fft(y))/N     # Tableau des amplitudes
    ampl[1:-1] = ampl[1:-1]*2        #Tableau des amplitudes
    ampl[1:-1] = ampl[1:-1]*2        #
    
    return freq, 20*np.log10(ampl/np.sqrt(2))     # Retourne fréquences et valeurs RMS dBV
