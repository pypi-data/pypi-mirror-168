"""
Librairie Python 3 pour les sciences physiques au lycée.

Modules disponibles de la librairie (package) physique :

- modelisation :
    Modélisation de courbes (linéaire, affine, parabolique, exponentielle, ...)

    Exemple :
    >>> from physique.modelisation import ajustement_parabolique

- csv :
    Importation et exportation de données au format CSV pour Avimeca3, Regavi, Regressi, Latis, ...

    Exemple :
    >>> from physique.csv import import_avimeca3_txt




@author: David Thérincourt - 2020
"""

from physique.modelisation import *
from physique.csv import *
