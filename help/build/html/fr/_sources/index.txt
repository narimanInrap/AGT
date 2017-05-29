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
Le plugin permet de traiter les données issues de prospections électriques (Geoscan Research RM15/RM85) et de prospections magnétiques (Sensys MXPDA).

.. index:: électrique
Module de traitement des données électriques (Geoscan Research RM15/RM85)
====================
Ce module permet de réaliser un traitement initial des données de résistivité électrique acquises sur la base d’un carroyage et à pas régulier. Pour l’instant, seule la configuration Pôle-Pôle est proposée. 

\ **fichier en entrée**\

Le fichier en entrée est un fichier ascii (.dat) qui contient les données et un en-tête de fichier qui rappelle l’ensemble des informations relatives à la configuration de l’appareil et au mode d’acquisition :


				\ **Fichier colonne contenant les n voies**\
	
				* RM85	Nom de l’appareil
				* 2		Nombre de grille
				* 30		Longueur des grilles			
				* 30		Largeur des grilles
				* 0.5		Ecartement entre électrodes
				* 3		Nombre de voies mesurées
				* 4		Nombre d’électrode
				* 1		Intervalle de mesure
				* Pole-Pole		Configuration d’électrode
				* 10		Intensité du courant injecté
				* 1		Nom de la première grille 
				* 0		Coordonnées de la première grille (Point inférieur gauche)
				* 0
				* 2		Nom de la deuxième grille
				* 0		Coordonnées de la deuxième grille (Point inférieur gauche)
				* 30
				* 20.95		Mesures
				* 25		
				* 20.5
				* 8.55
				* 8.9
				* 5.26
				* .
				* .
				* .

La valeur des données non mesurées (dummy log) est fixée à 999. 

L’en-tête a une double fonction :

#. il sert au traitement des données et doit donc être rempli rigoureusement
#. il sert à stocker les métadonnées liées à l’acquisition


\ **Traitement effectué**\


Le traitement de base consiste à réorganiser les données brutes pour les individualiser par \ *voie* \. Les résistances mesurées sur le terrain sont transformées en résistivité apparente selon la géométrie d’électrode employée (seule la configuration Pôle-Pôle est configurée pour le moment). Les données peuvent être exportées en .shp et/ou en .dat. Deux sous-modules sont ensuite proposés à l’utilisateur :

	\ *Filtrage par la médiane* \

Cette fonction permet d’effectuer un filtrage par la médiane sur une fenêtre glissante et supprimer ainsi les points aberrants. L’écart à la médiane et la taille de la fenêtre sont à définir par l’utilisateur. 

	\ *Géoréférencement* \

Cette fonction permet un géoréférencement de la grille par translation et rotation (pas de mise à l’échelle, ni de déformation). Elle est basée sur la définition de deux points de calage. 

.. index:: magnétique

Module de traitement des données magnétiques (Sensys MXPDA)
======================

Ce module permet de réaliser un traitement basique des données de prospection magnétique acquises avec le magnétomètre différentiel Sensys MXPDA couplé à un GPS.

\ **Fichier en entrée**\

Le fichier en entrée est un fichier .asc issu du logiciel Magneto-Arch développé par Sensys.  Il présente la configuration suivante :

X, Y, Différence de la composante verticale du champ magnétique, Nom du profil, Numéro de la sonde

* 30694328.591 5432511.556 5.5 "20161010-110332_GZP.prm" 1
* 30694328.717 5432511.772 31.2 "20161010-110332_GZP.prm" 2
* 30694328.844 5432511.987 -21.6 "20161010-110332_GZP.prm" 3
* 30694328.971 5432512.203 -8.3 "20161010-110332_GZP.prm" 4
* 30694329.098 5432512.418 -12.3 "20161010-110332_GZP.prm" 5
* ...

Les données acquises sont géoréférencées en coordonnées UTM. Les deux premiers chiffres de la coordonnées X correspondent à la zone de l’UTM (ici UTM-30).

\ **Traitement effectué** \

Le traitement de base consiste à réorganiser les données pour les individualiser par \ *profil* \(un profil est défini comme l’ensemble des données acquises par une sonde le long d’un passage d’acquisition). Les points de mesures sont ensuite géoréférencés dans le système de projection souhaité par l’utilisateur. Les données peuvent être exportées en .shp et/ou en .dat. Quatre modules de traitement sont proposés à l’utilisateur :

	\ *Décimation* \ 
Cette fonction permet de réduire le nombre de point de mesure en n’en gardant qu’un sur n (n étant spécifié par l’utilisateur).

	\ *Suppression de la médiane* \
Cette fonction permet de retirer à chacun des profils leur valeur médiane afin d’éliminer les décalages du zéro induit par l’électronique des capteurs et des perturbations magnétiques constantes (sur le porteur par exemple). Il est possible de restreindre le nombre de points utilisés pour calculer la médiane en indiquant un percentile. Cette condition permet de s’affranchir des anomalies fortement magnétiques dans le calcul de la médiane. 

	\ *Suppression d’un polynôme* \
Cette fonction permet de soustraire un polynôme de degré 1, 2 ou 3 à chacun des profils.

	\ *Suppression des points stationnaires* \ 
Cette fonction permet de supprimer les points de mesures lorsque l’appareil est à l’arrêt.


.. index:: code source

Code source
===========

Le code source est disponible à l’adresse suivante : 

https://github.com/narimanInrap/AGT.git

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

