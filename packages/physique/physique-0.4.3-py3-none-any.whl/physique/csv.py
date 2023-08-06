# -*- coding: utf-8 -*-
"""
Module d'importation et d'exportation de tableaux de données au format CSV.
Logiciels pris en compte : Latis, Regressi, RegAvi, AviMeca3

@author: David Thérincourt
"""

import numpy as np
from io import StringIO

def normalise_file_name(fileName, encodage = 'utf-8') :
    """
    Normalise les séparateurs décimaux dans un fichier CSV en remplaçant les virgules par des points.
    """
    f = open(fileName,'r', encoding = encodage)
    data = f.read()
    f.close()
    return StringIO(data.replace(",","."))

def import_txt(fileName, sep = ';', skip_header = 1) :
    """
    Importe des données au format CSV à partir du logiciel AviMéca 3
    Paramètre :
        fileName (str) : nom du fichier CSV
    Paramètre optionnel :
        sep (str) : caractère de séparation des colonnes de données (";" par défaut)
        skip (integer) : nombre de ligne à sauter au début du fichier
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    return np.genfromtxt(fileName, delimiter = sep, unpack = True, skip_header = skip_header)

def import_avimeca3_txt(fileName, sep = '\t') :
    """
    Importe des données au format CSV à partir du logiciel AviMéca 3
    Paramètre :
        fileName (str) : nom du fichier CSV
    Paramètre optionnel :
        sep (str) : caractère de séparation des colonnes de données (tabulation '\t' par défaut)
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    data = normalise_file_name(fileName, encodage = 'cp1252') # iso-8859-1 ou CP1252
    return np.genfromtxt(data, delimiter = sep, unpack = True, skip_header = 3, comments = '#')

def import_regavi_txt(fileName, sep = '\t') :
    """
    Importe des données au format CSV à partir du logiciel RegAvi
    Paramètre :
        fileName (str) : nom du fichier CSV
    Paramètre optionnel :
        sep (str) : caractère de séparation des colonnes de données (tabulation '\t' par défaut)
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    data = normalise_file_name(fileName, encodage = 'ascii')
    return np.genfromtxt(data, delimiter = sep, unpack = True, skip_header = 2, comments = '#')

def import_regressi_txt(fileName) :
    """
    Importe des données au format TXT à partir du logiciel Regressi
    Paramètre :
        fileName (str) : nom du fichier CSV
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """

    return np.genfromtxt(fileName, delimiter = "\t", unpack = True, skip_header = 2, comments = '')

def import_regressi_csv(fileName) :
    """
    Importe des données au format CSV à partir du logiciel Regressi
    Paramètre :
        fileName (str) : nom du fichier CSV
    Retourne (tuple) :
        Un tuple de tableaux Numpy
    """
    data = normalise_file_name(fileName, encodage = 'ascii')
    return np.genfromtxt(data, delimiter = ";", unpack = True, skip_header = 2, comments = '')

#######################################
# Exportation
#######################################

def export_txt(data, fileName = "data.txt", sep = ";", headerLine = ''):
    """
    Exporte des données au format CSV dans un fichier texte (txt) compatible Regressi, Latis, Libre office. Ecrase le fileName existant.
    Paramètre :
        data (tuple) : tuple de tableaux de données
    Paramètres optionnels :
        fileName (str) : nom du fichier CSV à exporter ("data.txt" par défaut)
        sep (str) : caractère de séparation des colonnes de données (";" par défaut)
        headerLine (str) : noms des variables des données séparatés par la caractère de séparation (sep)
    """
    data = np.transpose(data)
    np.savetxt(fileName, data, delimiter = sep, header = headerLine, comments='')
    return 0
