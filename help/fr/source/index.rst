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


.. index:: GEM2Geophex EMP400

Module de traitement des données électromagnétiques de type EMI (GEM2 de Geophex, EMP400 de GSSI)
======================

Ce module permet d’effectuer différents traitements sur les mesures réalisées avec le GEM2 (Geophex) ou l'EMP400 (GSSI) :

-	Fusion des données GNSS et GEM2/EMP400 (avec prise en compte du décalage en temps des deux horloges) 
-	Correction du décalage de la position entre l’antenne GNSS et le GEM2/EMP400
-	Décimation des points de mesures
-	Filtrage de la médiane par profil
-	Filtrage 1D glissant par la médiane ou par la moyenne
-	Calcul de la conductivité électrique
-	Calcul de la susceptibilité magnétique avec correction des effets d’induction
-	Etalonnage de l’appareil de mesure sur la base d’un sondage électrique ou d’une valeur de résistivité moyenne du terrain

\ **Fichier en entrée du GEM2** \

Le fichier en entrée est un fichier ascii (.csv) dans le format d’export proposé par le logiciel EMExport de la suite Geophex. Trois modes d’acquisition sont possibles (acquisition sans GNSS, acquisition avec GNSS connecté au GEM2, acquisition séparée du GNSS) et il contient une série de données variable en fonction du mode d’acquisition.


\ **Acquisition GEM2 avec GNSS** \

Line,Sample,X,Y,Mark,Status,GPSStat,GPSalt,Time[ms],Time[hhmmss.sss],PowerLn,I_5025Hz,Q_5025Hz,
I_10325Hz,Q_10325Hz,I_21275Hz,Q_21275Hz,I_43725Hz,Q_43725Hz,I_89925Hz,Q_89925Hz,QSum

0, 21,   509779.22,  5061220.33,   0,0,4,  575.22, 35967000.100,095927.0001,    0.3,-1.22403e+003, 6.32362e+000,-1.55238e+003,-1.78986e+002,-1.99524e+003, 1.17386e+003,-2.12842e+003, 4.58693e+003, 3.66881e+003, 3.00984e+003, 8.59797e+003

\ **Acquisition GEM2 sans GNSS** \

Line,Sample,X,Y,Mark,Status,Time[ms],Time[hhmmss.sss],PowerLn,I_5025Hz,Q_5025Hz,I_10325Hz,
Q_10325Hz,I_21275Hz,Q_21275Hz,I_43725Hz,Q_43725Hz,I_89925Hz,Q_89925Hz,QSum

0,0, 0.00, 0.00, 0, 0, 52275802.200, 143115.8022, 0.2, 1.47162e+003,
-3.85928e+002,9.69091e+002,1.29074e+001,4.03300e+002,1.14524e+003,6.69531e+001,5.15901e+003, 6.22617e+003, 5.16867e+003, 1.10741e+004,0,1, 0.00,1.06,0,0, 52275842.200,143115.8422, 0.1, 1.67830e+003, 1.36072e+001, 1.14406e+003,-1.37615e+002, 5.27930e+002, 1.16965e+003,-2.98461e+001, 5.38998e+003, 5.90062e+003, 5.46728e+003, 1.19029e+004

\ **Fichier en entrée de l’EMP400** \

Le fichier en entrée est un fichier ascii (.EMI) dans le format d’export de l’EMP400. Deux modes d’acquisition sont possibles (acquisition sans GNSS et acquisition avec un GNSS indépendant) et il contient une série de données variable en fonction des paramètres d’acquisition. Attention, l’EMP400 contient un GPS de précision métrique. Etant donné la précision, ces points GNSS ne sont pas pris en compte dans le plugin. 

\ **Acquisition EMP400** \

En tête de 36 lignes

Record#, XCoord, YCoord, Time, InPhase[15000], Quad[15000], Conductivity[15000], InPhase[8000], Quad[8000], Conductivity[8000], InPhase[5000], Quad[5000], Conductivity[5000], Remark, Mark, Lat, Long, Alt, Tilt, Errors
   31,    0.500,   18.000,07:19:22.385,-21373 ,1129 ,25.706 ,-6046 ,684 ,29.208 ,-2588 ,438 ,29.882 ,,, 45.6537417,  3.1515333,376.0000000,,NO ERRORS


Le programme reconnait automatiquement le nombre de fréquences utilisées lors de l’acquisition des mesures et détermine la valeur de chacune de ces fréquences. Il détecte également si l’acquisition a été réalisée avec un GNSS ou non. Ces informations sont ensuite utilisées dans les différents traitements appliqués sur le jeu de données.

L’utilisateur doit préciser le système de coordonnées de référence (SCR) utilisé lors de l’acquisition. Par défaut il s’agit du WGS84 UTM31Nord. Ce système peut être changé dans l’onglet Paramètres du plugin et enregistré comme système de référence par défaut.

Le fichier GNSS en entrée est un fichier ascii (.dat). Il doit contenir une suite d’informations basiques, les valeurs de la position en X et en Y ainsi que l’altitude et l’heure d’acquisition sous la forme (hh:mm:ss). Il faudra prendre soin de spécifier le SCR utilisé pour l’acquisition des points GNSS.

\ **Format du fichier GNSS** \

* /X, Y, Z, Heure/
* 1709059.979, 6946271.346, 232.25,12:11:05
* 1709059.975, 6946271.352, 232.22,12:11:06
* 1709009.729, 6946415.921, 232.15,12:42:52

\ **Traitement** \

	\ *Fusion des données GEM2/EMP400 et GNSS* \ 
	
	Cette fonction permet de fusionner un fichier du GEM2/EMP400 et un fichier GNSS sur la base de l’heure d’acquisition de chaque point de mesure. Par défaut le fichier EM en entrée est un fichier sans acquisition GNSS. Le calage se fait sur la base des horloges des deux appareils. On peut préciser le décalage en temps existant entre les deux appareils afin de s’assurer d’un positionnement optimal des points de mesures.\ *Data decimation* \
	
	\ *Décimation* \
	
	Cette fonction permet de réduire le nombre de point de mesures en n’en gardant qu’un sur n (n étant spécifié par l’utilisateur). Les points conservés sont filtrés par une médiane sur une fenêtre glissante de n points.
	
	\ *Décalage spatial/GNSS* \
	
	Dans le cas d’une acquisition avec GNSS connecté sur le système EM, il se peut qu’il y ait un décalage spatial pour des raisons pratiques entre la position de l’antenne GNSS et la mesure EM. La correction en X et en Y est réalisée suivant le sens d’avancement de l’opérateur et de l’appareil.
	
	\ *Suppression de la médiane par profil (phase et quadrature)* \
	
	Cette fonction permet de retirer à chacun des profils leur valeur médiane afin d’éliminer les effets de profil induits par des différences de hauteur entre les profils ou par une horizontalité non respectée du capteur. Le calcul de la médiane par profil peut être effectué sur les points en phase et/ou sur les points en quadrature.
	
	\ *Filtrage par fenêtre glissante* \
	
	Cette fonction permet d’effectuer un filtrage 1D par fenêtre glissante le long du profil d’acquisition. Le filtrage peut être effectué sur le signal en phase et/ou sur le signal en quadrature. On peut préciser la taille de la fenêtre glissante ainsi que la méthode utilisée pour effectuer le calcul (moyenne ou médiane).
	
	\ *Calcul des paramètres physiques* \
	
		
		\ *Etalonnage* \
		
		Le module propose d’effectuer un étalonnage de l’appareil sur la base d’une mesure haut-bas sur un point de sondage électrique ou de résistivité électrique moyenne connu. Pour réaliser l’étalonnage, cliquer sur le bouton Paramètres de calibrage. Il faut alors renseigner le fichier de calibrage EMI. Celui-ci correspond à un fichier contenant les mesures haut-bas (Thiesson et al. 2014) nécessaire au calibrage des points. Le fichier doit contenir 6 points de mesures, alternant points hauts et points bas en commençant par la mesure en bas. Le GEM2/EMP400 ne permettant pas d’acquérir des points discrets, chaque point de mesure correspond à un profil acquis en continu et moyenné pour calculer la valeur de chaque point. Il faut ensuite renseigner la hauteur de l’appareil posé au sol et de l’appareil maintenu en hauteur (tenir compte de la structure de l’appareil – pour un appareil posé au sol il faut compter 0,02 m de hauteur). On peut ensuite choisir comme niveau de référence soit une valeur de résistivité moyennée connue ou un modèle à 5 couches. Si l’utilisateur à un modèle à 3 ou 4 couches, il faut renseigner les dernières de façon identique (Exemple : pour un modèle 3 couches, e1, e2, e3, e4 et rau1, rau2, rau3, rau4, rau5 avec rau3=rau4=rau5). Cliquer sur Enregistrer pour sauver les valeurs de paramétrage de l’étalonnage.
		
		\ *Conductivité électrique et susceptibilité magnétique* \
		
		Le module de traitement propose de calculer les valeurs de conductivité électrique apparente et de susceptibilité magnétique en se basant sur la solution des intégrales et la transformée de Hankel (Thiesson et al. 2014). Cette solution tient compte de la hauteur de l’appareil et de la configuration de bobines utilisée. Elle peut être appliquée quel que soit le type de sol étudié (valable également dans des contextes de sols très conducteurs).
		
		Dans le cas de la susceptibilité magnétique, le module permet de retirer l’effet de la conductivité sur le signal en phase. Pour cela, il faut cocher la case Correction de conductivité. Attention cette option entraîne un temps de traitement relativement long. Il faut aussi s’assurer dans un premier temps que les valeurs de conductivités calculées auparavant (nécessaires à ce calcul) ne soient pas négatives auquel cas l’estimation de la susceptibilité sera erronée. 

Les points sont ensuite enregistrés dans un fichier .shp dans le système de coordonnées défini par l’utilisateur. Le fichier contient les positions en X et Y, les valeurs en phase et en quadrature (après application des différents filtres), ainsi que les valeurs de conductivité et de susceptibilité pour chaque fréquence. Il contient également le numéro de profil, le temps et la qualité du signal GNSS ainsi que l’altitude du point de mesure (dans le cas d’une acquisition GNSS). 


Thiesson J., Kessouri P., Schamper C., Tabbagh A. 2014 - Calibration of frequency-domain electromagnetic devices used in near-surface surveying. Near Surface Geophysics, 12, 481-491.


Code source
===========

Le code source est disponible à l’adresse suivante : 

https://github.com/narimanInrap/AGT.git

évolutions futures
===================

* Module de téléchargement RM15/RM85
* Module de traitement avancé

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

