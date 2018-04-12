.. AGT documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AGT's documentation!
============================================


.. toctree::
   :maxdepth: 2

   
.. index:: Présentation
 
Présentation
=================== 
AGT permet de traiter les données issues de prospections électriques (Geoscan research RM15/85 en grille), de prospections magnétiques (Sensys MXPDA et Bartington Grad601 en grille) et de prospections électomagnétiques basse-fréquence (Geonics EM31).

.. index:: électrique
Module de traitement des données électriques (Geoscan Research RM15/RM85) - Prospection en grille
====================
Ce module permet de réaliser un traitement initial des données de résistivité électrique acquises sur la base d’un carroyage et à pas régulier. Pour l’instant, seule la configuration Pôle-Pôle est proposée. 

\ **Fichier en entrée**\

Le fichier en entrée est un fichier ascii (.dat) qui contient les données et un en-tête de fichier qui rappelle l’ensemble des informations relatives à la configuration de l’appareil et au mode d’acquisition :


				\ **Fichier colonne contenant les n voies**\
	
				* RM85 	*Nom de l’appareil*
				* 2		*Nombre de grille*
				* 30 		*Longueur des grilles*
				* 30 		*Largeur des grilles*
				* 0.5 		*Ecartement entre électrodes*
				* 3			*Nombre de voies mesurées*
				* 4	 	*Nombre d’électrode*
				* 1	 	*Intervalle de mesure*
				* Pole-Pole 		*Configuration d’électrode*
				* 10 		*Intensité du courant injecté*
				* 1	  	*Nom de la première grille*
				* 0	 	*Coordonnées de la première grille (Point inférieur gauche)*
				* 0
				* 2	 	*Nom de la deuxième grille*
				* 0	 	*Coordonnées de la deuxième grille (Point inférieur gauche)*
				* 30 
				* 20.95	 	*Mesures*
				* 25		
				* 20.5
				* 8.55
				* 8.9
				* 5.26
				* .
				* .
				* .

La valeur des données non mesurées (dummy log) est fixée à 999. 

L’en-tête a une double fonction et doit être rempli rigoureusement. Il sert : 

#. au traitement des données (informations lues automatiquement par le plugin)
#. à stocker les métadonnées liées à l’acquisition


\ **Traitement**\


Le traitement de base consiste à réorganiser les données brutes pour les individualiser par voie et à associer à chaque point ses coordonnées X,Y. Les résistances mesurées sur le terrain sont transformées en résistivité apparente selon la géométrie d’électrode employée (seule la configuration Pôle-Pôle est configurée pour le moment). Les données peuvent être exportées en .shp ou en .dat. Deux sous-modules sont ensuite proposés à l’utilisateur :

	\ *Filtrage par la médiane* \

Cette fonction permet d’effectuer un filtrage par la médiane sur une fenêtre glissante et supprimer ainsi les points aberrants. L’écart à la médiane et la taille de la fenêtre sont à définir par l’utilisateur. 

	\ *Géoréférencement* \

Cette fonction permet un géoréférencement de la grille par translation et rotation. Elle est basée sur la définition de deux points de calage. 

.. index:: magnétique

.. index:: magnétique - grille

Module de traitement des données magnétiques (Sensys MXPDA) - prospection en grille
======================

Ce module permet de réaliser un traitement basique des données de prospection magnétique acquises avec le magnétomètre différentiel Sensys MXPDA ou un Bartington Grad601.

\ **Fichier en entrée**\

Le fichier en entrée est un fichier .dat issu du logiciel Magneto-Arch développé par Sensys ou .dat issu du logiciel d’export de Bartington. Ils présentent les structures suivantes :

				\ **Sensys MXPDA**\
				
				* X   Y    Value
				* 0   0     2.8
				* 0  0.1    2.87
				* 0  0.2    3.08
				* 0  0.3    2.59
				* 0  0.4    1.89
				* .
				* .
				* .
				

				\ **Bartington Grad601**\
				
				* Time = 09:16:55
				* Date = 06/10/2017
				* Grid Number = 1
				* Number of Sensors = 2
				* Grid Size = 40 x 40
				* Method of collection = ZigZag
				* Starting Direction = West
				* Data Range = 100 nT
				* Line Spacing = 1.00 m
				* Sampling = 4 samples / m
				* Sensor Spacing = 1.0 m
				* Mean = 0.50
				* Max = 21.40
				* Min = -4.01
				* 0.125 0.5 0.87	 *Y, X, valeur*
				* 0.375 0.5 0.86
				* 0.625 0.5 1.21
				* 0.875 0.5 1.78
				* 2.875 0.5 1.16
				* .
				* .
				* .

\ **Traitement** \

Le traitement de base consiste à réorganiser les données pour les individualiser par profil (un profil est défini comme l’ensemble des données à X constant). Les données peuvent être exportées en .shp et/ou en .dat. Trois modules de traitement sont proposés à l’utilisateur :

	\ *Suppression de la médiane* \

	Cette fonction permet de retirer à chacun des profils leur valeur médiane afin d’éliminer les décalages du zéro induit par l’électronique des capteurs et des perturbations magnétiques constantes (sur le porteur par exemple). Il est possible de restreindre le nombre de points utilisés pour calculer la médiane en indiquant un percentile. Cette condition permet de s’affranchir des anomalies fortement magnétiques dans le calcul de la médiane.
	
	\ *Suppression d'un polynôme* \

	Cette fonction permet de soustraire un polynôme de degré 1, 2 ou 3 à chacun des profils.

	\ *Géoréférencement* \

	Cette fonction permet un géoréférencement de la grille par translation et rotation. Elle est basée sur la définition de deux points de calage. 

.. index:: magnétique - GNSS

Module de traitement des données magnétiques (Sensys MXPDA) - prospection avec GNSS
======================

Ce module permet de réaliser un traitement basique des données de prospection magnétique acquises avec le magnétomètre différentiel Sensys MXPDA couplé à un GPS.

\ **Fichier en entrée**\

Le fichier en entrée est un fichier .asc issu du logiciel Magneto-Arch développé par Sensys.  Il présente la configuration suivante :

*X, Y, Différence de la composante verticale du champ magnétique, Nom du profil, Numéro de la sonde*

* 30694328.591 5432511.556 5.5 "20161010-110332_GZP.prm" 1
* 30694328.717 5432511.772 31.2 "20161010-110332_GZP.prm" 2
* 30694328.844 5432511.987 -21.6 "20161010-110332_GZP.prm" 3
* 30694328.971 5432512.203 -8.3 "20161010-110332_GZP.prm" 4
* 30694329.098 5432512.418 -12.3 "20161010-110332_GZP.prm" 5
* ...

Les données acquises sont géoréférencées en coordonnées UTM. Les deux premiers chiffres de la coordonnée X correspondent à la zone de l’UTM (ici UTM-30).

\ **Traitement** \

Le traitement de base consiste à réorganiser les données pour les individualiser par profil (un profil est défini comme l’ensemble des données acquises par une sonde le long d’un passage d’acquisition). Les points de mesures sont ensuite géoréférencés dans le système de projection souhaité par l’utilisateur. Les données peuvent être exportées en .shp et/ou en .dat. Quatre modules de traitement sont proposés à l’utilisateur :

	\ *Décimation* \ 
Cette fonction permet de réduire le nombre de point de mesure en n’en gardant qu’un sur n (n étant spécifié par l’utilisateur). L’utilisateur a le choix de prendre les données brutes ou bien de les filtrer par une médiane sur une fenêtre glissante de n points.

	\ *Suppression de la médiane* \
Cette fonction permet de retirer à chacun des profils leur valeur médiane afin d’éliminer les décalages du zéro induit par l’électronique des capteurs et des perturbations magnétiques constantes (sur le porteur par exemple). Il est possible de restreindre le nombre de points utilisés pour calculer la médiane en indiquant un percentile. Cette condition permet de s’affranchir des anomalies fortement magnétiques dans le calcul de la médiane.

	\ *Suppression d’un polynôme* \
Cette fonction permet de soustraire un polynôme de degré 1, 2 ou 3 à chacun des profils.

	\ *Suppression des points stationnaires* \ 
Cette fonction permet de supprimer les points de mesures lorsque l’appareil est à l’arrêt.

.. index:: électromagnétique

Module de traitement des données électromagnétiques de type EMI (EM31 de Geonics)
======================

Ce module permet de corriger les valeurs de conductivité électrique fournies par l’EM31 (calculée d’après McNeil, 1980). Ce traitement permet de dépasser le domaine de validité de l’approximation linéaire qui n’est valable qu’en première approximation pour une altitude d’appareil nulle et dans le cas du faible nombre d’induction (c’est-à-dire une conductivité électrique des sols assez faible). Il transforme ensuite ces points en fichier .shp et les charge dans le canevas.

\ **Fichier en entrée**\

Le fichier en entrée est un fichier ascii (.dat) dans le format d’export proposé par le logiciel DAT31W. Il contient les données de positionnement ainsi que les données en quadrature (QV1 en mS/m), les données en phase (IV1 en ppt) et l’heure d’acquisition en (heure : minute : seconde) :

* /EAST,  NORTH,  QV1,  IV1,  TIME/
* 642039.43420000  7097622.22880000       30.10        1.03 15:32:39.555
* 642039.43560000  7097622.22740000         30.25        1.03 15:32:39.904
* 642039.43548000  7097622.22934000         30.18        1.03 15:32:40.262
* 642039.43478000  7097622.23249000       30.13        1.01 15:32:40.614
* 642039.43402000  7097622.23591000       30.02        1.00 15:32:40.991
* 642039.50925000  7097622.14500000       29.95        1.00 15:32:41.353
* 642039.58235000  7097622.05660000       29.98        1.00 15:32:41.699
* 642039.67784000  7097621.93750000       30.18        1.02 15:32:42.071

L’utilisateur doit préciser le système de coordonnées utilisé lors de l’acquisition. 
 


\ **Traitement effectué** \

Le module de traitement propose de calculer les valeurs de conductivité électrique apparente en se basant sur la solution des intégrales et la transformée de Hankel (Thiesson et al., 2014). Cette solution tient compte de la hauteur de l’appareil et de la configuration de bobines utilisée. Elle peut être appliquée quel que soit le type de sol étudié (valable dans des contextes de sols salés). 

McNeill J.D., 1980 - Electromagnetic terrain conductivity measurement at low induction number, technical note TN6, Geonics Ltd, Toronto, 15p.

Thiesson J., Kessouri P., Schamper C., Tabbagh A. 2014 - Calibration of frequency-domain electromagnetic devices used in near-surface surveying. Near Surface Geophysics, 12, 481-491.


.. index:: code source

Code source
===========

Le code source est disponible à l’adresse suivante : 

https://github.com/narimanInrap/AGT.git

évolutions futures
===================

* Module de traitement des données électromagnétique (GeoPhex gem-2)
* Module de téléchargement RM15/RM85
* Module de traitement avancé

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

