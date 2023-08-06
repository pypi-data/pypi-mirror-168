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


def integre(x, y, xmin, xmax, plot_axes=None):
    """ Calcule numériquement l'intégrale de la fonction y=f(x) entre
    les bornes xmin et xmax.
    """
    y = y[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    x = x[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    if plot_axes != None:
        plot_axes.fill_between(x,y,hatch='\\',facecolor='linen',  edgecolor='gray')
        
    return trapz(y)*(x[-1]-x[0])/len(x)


def spectre_amplitude(x, y, xmin, xmax):
    ''' Retourne le spectre d'amplitude d'un signal y(x).
    Le calcul se fait sur une période allant de xmin à xmax.
    '''
    y = y[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    x = x[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    T = x[-1]-x[0]                   # Durée totale
    N = len(x)                       # Nb points
    freq = np.arange(N)*1.0/T        # Tableau des fréquences
    ampl = np.absolute(fft(y))/N     # Tableau des amplitudes
    ampl[1:-1] = ampl[1:-1]*2        #
    return freq, ampl                # Retourne fréquences et amplitudes

def spectre_RMS(x, y, xmin, xmax):
    ''' Retourne le spectre d'amplitude d'un signal y(x).
    Le calcul se fait sur une période allant de xmin à xmax.
    '''
    y = y[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    x = x[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    T = x[-1]-x[0]                   # Durée totale
    N = len(x)                       # Nb points
    freq = np.arange(N)*1.0/T        # Tableau des fréquences
    ampl = np.absolute(fft(y))/N     # Tableau des amplitudes
    ampl[1:-1] = ampl[1:-1]*2        #
    return freq, ampl/np.sqrt(2)     # Retourne fréquences et valeurs RMS


def spectre_RMS_dBV(x, y, xmin, xmax):
    ''' Retourne le spectre d'amplitude d'un signal y(x).
    Le calcul se fait sur une période allant de xmin à xmax.
    '''
    y = y[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    x = x[(x >= xmin) & (x < xmax)]  # Sélection sur une période
    T = x[-1]-x[0]                   # Durée totale
    N = len(x)                       # Nb points
    freq = np.arange(N)*1.0/T        # Tableau des fréquences
    ampl = np.absolute(fft(y))/N     # Tableau des amplitudes
    ampl[1:-1] = ampl[1:-1]*2        #
    return freq, 20*np.log10(ampl/np.sqrt(2))     # Retourne fréquences et valeurs RMS dBV
