# -*- coding: utf-8 -*-
"""
/***************************************************************************
AGT - Archaeological Geophysics Toolbox
                                 A QGIS plugin
 This plugin does basic processes on geophysical data for Archaeology
                             -------------------
        begin                : 2016-04-14
        git sha              : $Format:%H$
        copyright            : (C) 2016 by François-Xavier SIMON / INRAP
        email                : developpement-qgis@inrap.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""


import numpy, math
from .CoilEnum import CoilConfigEnum
#from _pydev_bundle.pydev_console_utils import Null
 
 
class SignalEM(object):
     
    def __init__(self, frequency = 9800, spacing = 3.66, height = 0.3, config = CoilConfigEnum.VCP, buckingCoil = 1.035, rho = [], chiP = [], chiQ =[], eps = [], ncou = 1, e = []):
         
        #Caractéristique de l'appareil de mesure qui sert de base à la modélisation
        self.frequency = frequency
        self.spacing = spacing
        self.height = height
        self.config = config
        self.buckingcoil = buckingCoil        
        #Fonction calculé lors de la simulation mais qui se retrouve 'hérité' dans les fonctions utilisées
        self.p = complex(0,0)
        self.gam2 = complex(0,0)
        self.a = complex(0,0)        
        #Caractéristique du terrain utilisé pour faire la simulation, appelé en paramètre des fonctions
        self.rho = rho
        self.ncou = ncou
        self.e = e
        self.chiP = chiP
        self.chiQ = chiQ
        self.eps = eps
         
         
    @staticmethod    
    def CTH(z):
         
        x = z.real
        y = z.imag
        a = math.cos(y)
        b = math.sin(y)
        c = math.tanh(x)
        cth = complex(a*c, b)/complex(a, c*b)
        return cth
         
    def fun2(self, g):#Fonction utilitaire pour la simulation
       
        fun2 = complex(0, 0)    
        if(g < 1E-20):
            g = 0.0        
        if(g*self.a > 30):
            return fun2      
        al = complex(g/self.p, 0)         
        U = (self.gam2 + al*al)**0.5
        rk = -U/self.susc 
        if(self.ncou >= 2):
            for i in range(self.ncou - 2, -1, -1):
                susci = complex(1 + self.chiP[i], -self.chiQ[i])
                gam2i = complex(0, numpy.pi*numpy.pi*self.frequency*0.8E-6/self.rho[i])*susci
                U = (gam2i + al**2)**0.5
                y = U/susci
                ck = self.CTH(U*complex(self.e[i], 0))
                rk = y*(rk - y*ck)/(y - rk*ck)
        fun2 = (al + rk)/(al - rk)*complex(g/numpy.exp(g*self.a), 0)
        return fun2
    
    def fun(self,g):
        
        fun = complex(0, 0)    
        if(g < 0.01E-20):
            g = 0.0        
        if(g*self.a/self.p > 30):
            return fun      
        al = complex(g/self.p, 0)         
        U = (self.gam2 + al*al)**0.5
        rk = -U/self.susc 
        if(self.ncou >= 2):
            for i in range(self.ncou - 2, -1, -1):
                susci = complex(1 + self.chiP[i], -self.chiQ[i])
                gam2i = complex(0, numpy.pi*numpy.pi*self.frequency*0.8E-6/self.rho[i])*susci
                U = (gam2i + al**2)**0.5
                y = U/susci
                ck = self.CTH(U*complex(self.e[i],0))
                rk = y*(rk-y*ck)/(y-rk*ck)
        fun = (al+rk)/(al-rk)/complex(numpy.exp(g*self.a/self.p), 0.0)
        return fun

    def fun3(self,g):
        
        return self.fun(g)*complex(g*g, 0)
                
    def fun4(self,g):
        
        return self.fun(g)*complex(g, 0)
             
    def fun0(self, g):
         
        return self.fun2(g)*complex(g, 0)
     
    def fun00(self, g):#Fonction utilitaire pour la simulation
         
        return self.funv(g)*complex(g*g, 0)
  
    def funv(self, g):#Fonction utilitaire pour la simulation
         
        funv = 0
        if(g < 0.1E-20):
            g = 0
        if(g/self.p*self.a > 30):
            return funv
        al = complex(g/self.p, 0)
        u0 = (self.gam0 + al*al)**0.5
        if ((u0.real)*self.a*2 > 30):
            return funv
        cd = numpy.exp(u0*complex(2*self.a, 0))
        U = (self.gam2 + al*al)**0.5                   
        rk = -U/self.susc
        if(self.ncou >= 2):
                for i in range(self.ncou-2, -1, -1):                    
#                    gam0i,s1i,susci,gam2i=0,0,0,0
                    gam0i = complex(-self.frequency*self.frequency*(0.4E-15)*numpy.pi*numpy.pi/9.0, 0)
                    s1i = complex(self.eps[i], -0.18E+11*(1.0/self.rho[i])/self.frequency)
                    susci = complex(1 + self.chiP[i], -self.chiQ[i])
                    gam2i = s1i*gam0i*susci                                     
                    U = (gam2i + al**2)**0.5
                    y = U/susci
                    ck = self.CTH(U*complex(self.e[i], 0))
                    rk = y*(rk-y*ck)/(y-rk*ck)
        funv = al/u0*(u0+rk)/(u0-rk)/cd         
        return funv   
     
    @staticmethod
    def HANKSGC(J, R, FUN, K):# Hankel computation tiré de Guptsarma (rajouté bibliographie)
 
        IPREM0, IPREM1, IPREM2, IPREM3 = 0, 0, 0, 0
        X0, X1, X2, X3 = [], [], [], []
        NC0 = 61
        NC1 = 120
        NC2 = 47
        NC3 = 140
        A0 = -5.0825000000
        S0 = 1.16638303862e-01
        A1 = -8.38850000000  
        S1 = 9.04226468670e-02
        A2 = -3.05078187595
        S2 = 1.10599010095e-01
        A3 = -7.91001919000
        S3 = 8.79671439570e-02    
        W0 = [3.30220475766e-04,-1.18223623458e-03, 2.01879495264e-03,
            -2.13218719891e-03, 1.60839063172e-03,-9.09156346708e-04,
            4.37889252738e-04,-1.55298878782e-04, 7.98411962729e-05,
            4.37268394072e-06, 3.94253441247e-05, 4.02675924344e-05,
            5.66053344653e-05, 7.25774926389e-05, 9.55412535465e-05,
            1.24699163157e-04, 1.63262166579e-04, 2.13477133718e-04,
            2.79304232173e-04, 3.65312787897e-04, 4.77899413107e-04,
            6.25100170825e-04, 8.17726956451e-04, 1.06961339341e-03,
            1.39920928148e-03, 1.83020380399e-03, 2.39417015791e-03,
            3.13158560774e-03, 4.09654426763e-03, 5.35807925630e-03,
            7.00889482693e-03, 9.16637526490e-03, 1.19891721272e-02,
            1.56755740646e-02, 2.04953856060e-02, 2.67778388247e-02,
            3.49719672729e-02, 4.55975312615e-02, 5.93498881451e-02,
            7.69179091244e-02, 9.91094769804e-02, 1.26166963993e-01,
            1.57616825575e-01, 1.89707800260e-01, 2.13804195282e-01,
            2.08669340316e-01, 1.40250562745e-01,-3.65385242807e-02,
            -2.98004010732e-01,-4.21898149249e-01, 5.94373771266e-02,
            5.29621428353e-01,-4.41362405166e-01, 1.90355040550e-01,
            -6.19966386785e-02, 1.87255115744e-02,-5.68736766738e-03,
            1.68263510609e-03,-4.38587145792e-04, 8.59117336292e-05,
            -9.15853765160e-06]
        W1 = [9.62801364263e-07,-5.02069203805e-06, 1.25268783953e-05,
            -1.99324417376e-05, 2.29149033546e-05,-2.04737583809e-05,
            1.49952002937e-05,-9.37502840980e-06, 5.20156955323e-06,
            -2.62939890538e-06, 1.26550848081e-06,-5.73156151923e-07,
            2.76281274155e-07,-1.09963734387e-07, 7.38038330280e-08,
            -9.31614600001e-09, 3.87247135578e-08, 2.10303178461e-08,
            4.10556513877e-08, 4.13077946246e-08, 5.68828741789e-08,
            6.59543638130e-08, 8.40811858728e-08, 1.01532550003e-07,
            1.26437360082e-07, 1.54733678097e-07, 1.91218582499e-07,
            2.35008851918e-07, 2.89750329490e-07, 3.56550504341e-07,
            4.39299297826e-07, 5.40794544880e-07, 6.66136379541e-07,
            8.20175040653e-07, 1.01015545059e-06, 1.24384500153e-06,
            1.53187399787e-06, 1.88633707689e-06, 2.32307100992e-06,
            2.86067883258e-06, 3.52293208580e-06, 4.33827546442e-06,
            5.34253613351e-06, 6.57906223200e-06, 8.10198829111e-06,
            9.97723263578e-06, 1.22867312381e-05, 1.51305855976e-05,
            1.86329431672e-05, 2.29456891669e-05, 2.82570465155e-05,
            3.47973610445e-05, 4.28521099371e-05, 5.27705217882e-05,
            6.49856943660e-05, 8.00269662180e-05, 9.85515408752e-05,
            1.21361571831e-04, 1.49454562334e-04, 1.84045784500e-04,
            2.26649641428e-04, 2.79106748890e-04, 3.43716968725e-04,
            4.23267056591e-04, 5.21251001943e-04, 6.41886194381e-04,
            7.90483105615e-04, 9.73420647376e-04, 1.19877439042e-03,
            1.47618560844e-03, 1.81794224454e-03, 2.23860214971e-03,
            2.75687537633e-03, 3.39471308297e-03, 4.18062141752e-03,
            5.14762977308e-03, 6.33918155348e-03, 7.80480111772e-03,
            9.61064602702e-03, 1.18304971234e-02, 1.45647517743e-02,
            1.79219149417e-02, 2.20527911163e-02, 2.71124775541e-02,
            3.33214363101e-02, 4.08864842127e-02, 5.01074356716e-02,
            6.12084049407e-02, 7.45146949048e-02, 9.00780900611e-02,
            1.07940155413e-01, 1.27267746478e-01, 1.46676027814e-01,
            1.62254276550e-01, 1.68045766353e-01, 1.52383204788e-01,
            1.01214136498e-01,-2.44389126667e-03,-1.54078468398e-01,
            -3.03214415655e-01,-2.97674373379e-01, 7.93541259524e-03,
            4.26273267393e-01, 1.00032384844e-01,-4.94117404043e-01,
            3.92604878741e-01,-1.90111691178e-01, 7.43654896362e-02,
            -2.78508428343e-02, 1.09992061155e-02,-4.69798719697e-03,
            2.12587632706e-03,-9.81986734159e-04, 4.44992546836e-04,
            -1.89983519162e-04, 7.31024164292e-05,-2.40057837293e-05,
            6.23096824846e-06,-1.12363896552e-06, 1.04470606055e-07]        
        W2 = [3.17926147465e-06,-9.73811660718e-06, 1.64866227408e-05,
            -1.81501261160e-05, 1.87556556369e-05,-1.46550406038e-05,
            1.53799733803e-05,-6.95628273934e-06, 1.41881555665e-05,
            3.41445665537e-06, 2.13941715512e-05, 2.34962369042e-05,
            4.84340283290e-05, 7.33732978590e-05, 1.27703784430e-04,
            2.08120025730e-04, 3.49803898913e-04, 5.79107814687e-04,
            9.65887918451e-04, 1.60401273703e-03, 2.66903777685e-03,
            4.43111590040e-03, 7.35631696247e-03, 1.21782796293e-02,
            2.01097829218e-02, 3.30096953061e-02, 5.37143591532e-02,
            8.60516613299e-02, 1.34267607144e-01, 2.00125033067e-01,
            2.74027505792e-01, 3.18168749246e-01, 2.41655667461e-01,
            -5.40549161658e-02,-4.46912952135e-01,-1.92231885629e-01,
            5.52376753950e-01,-3.57429049025e-01, 1.41510519002e-01,
            -4.61421935309e-02, 1.48273761923e-02,-5.07479209193e-03,
            1.83829713749e-03,-6.67742804324e-04, 2.21277518118e-04,
            -5.66248732755e-05, 7.88229202853e-06]            
        W3 = [-6.76671159511e-14, 3.39808396836e-13,-7.43411889153e-13,
            8.93613024469e-13,-5.47341591896e-13,-5.84920181906e-14,
            5.20780672883e-13,-6.92656254606e-13, 6.88908045074e-13,
            -6.39910528298e-13, 5.82098912530e-13,-4.84912700478e-13,
            3.54684337858e-13,-2.10855291368e-13, 1.00452749275e-13,
            5.58449957721e-15,-5.67206735175e-14, 1.09107856853e-13,
            -6.04067500756e-14, 8.84512134731e-14, 2.22321981827e-14,
            8.38072239207e-14, 1.23647835900e-13, 1.44351787234e-13,
            2.94276480713e-13, 3.39965995918e-13, 6.17024672340e-13,
            8.25310217692e-13, 1.32560792613e-12, 1.90949961267e-12,
            2.93458179767e-12, 4.33454210095e-12, 6.55863288798e-12,
            9.78324910827e-12, 1.47126365223e-11, 2.20240108708e-11,
            3.30577485691e-11, 4.95377381480e-11, 7.43047574433e-11,
            1.11400535181e-10, 1.67052734516e-10, 2.50470107577e-10,
            3.75597211630e-10, 5.63165204681e-10, 8.44458166896e-10,
            1.26621795331e-09, 1.89866561359e-09, 2.84693620927e-09,
            4.26886170263e-09, 6.40104325574e-09, 9.59798498616e-09,
            1.43918931885e-08, 2.15798696769e-08, 3.23584600810e-08,
            4.85195105813e-08, 7.27538583183e-08, 1.09090191748e-07,
            1.63577866557e-07, 2.45275193920e-07, 3.67784458730e-07,
            5.51470341585e-07, 8.26916206192e-07, 1.23991037294e-06,
            1.85921554669e-06, 2.78777669034e-06, 4.18019870272e-06,
            6.26794044911e-06, 9.39858833064e-06, 1.40925408889e-05,
            2.11312291505e-05, 3.16846342900e-05, 4.75093313246e-05,
            7.12354794719e-05, 1.06810848460e-04, 1.60146590551e-04,
            2.40110903628e-04, 3.59981158972e-04, 5.39658308918e-04,
            8.08925141201e-04, 1.21234066243e-03, 1.81650387595e-03,
            2.72068483151e-03, 4.07274689463e-03, 6.09135552241e-03,
            9.09940027636e-03, 1.35660714813e-02, 2.01692550906e-02,
            2.98534800308e-02, 4.39060697220e-02, 6.39211368217e-02,
            9.16763946228e-02, 1.28368795114e-01, 1.73241920046e-01,
            2.19830379079e-01, 2.51193131178e-01, 2.32380049895e-01,
            1.17121080205e-01,-1.17252913088e-01,-3.52148528535e-01,
            -2.71162871370e-01, 2.91134747110e-01, 3.17192840623e-01,
            -4.93075681595e-01, 3.11223091821e-01,-1.36044122543e-01,
            5.12141261934e-02,-1.90806300761e-02, 7.57044398633e-03,
            -3.25432753751e-03, 1.49774676371e-03,-7.24569558272e-04,
            3.62792644965e-04,-1.85907973641e-04, 9.67201396593e-05,
            -5.07744171678e-05, 2.67510121456e-05,-1.40667136728e-05,
            7.33363699547e-06,-3.75638767050e-06, 1.86344211280e-06,
            -8.71623576811e-07, 3.61028200288e-07,-1.05847108097e-07,
            -1.51569361490e-08, 6.67633241420e-08,-8.33741579804e-08,
            8.31065906136e-08,-7.53457009758e-08, 6.48057680299e-08,
            -5.37558016587e-08, 4.32436265303e-08,-3.37262648712e-08,
            2.53558687098e-08,-1.81287021528e-08, 1.20228328586e-08,
            -7.10898040664e-09, 3.53667004588e-09,-1.36030600198e-09,
            3.52544249042e-10,-4.53719284366e-11]        
        I = K + J*2    
        if(I == 0):
            if(IPREM0 == 0):
                for N in range(NC0):
                    x = (10**(A0 + N*S0))  
                    X0.append(x)
                    x = 0
                IPREM0 = 1
            FR = 0
            RI = 1/R
            for N in range(NC0):
                FR = FR + FUN((X0[N]*RI))*complex(W0[N], 0)         
            HANKSGC = FR*complex(RI, 0)        
        elif(I == 1):
            if(IPREM1 == 0):
                for N in range(NC1):
                    x = 10**(A1+(N)*S1) 
                    X1.append(x)
                    x = 0
                IPREM1 = 1
            FR = 0
            RI = 1/R        
            for N in range(NC1):
                FR = FR + FUN(X1[N]*RI)*complex(W1[N], 0.)        
            HANKSGC = FR*complex(RI, 0)        
        elif(I == 2):
            if(IPREM2 == 0):        
                for N in range(NC2):
                    x = 10**(A2 + (N)*S2)
                    X2.append(x)
                    x = 0
                IPREM2 = 1    
            FR = 0
            RI = 1/R        
            for N in range(NC2):
                FR = FR + FUN(X2[N]*RI)*complex(W2[N], 0.)
            HANKSGC = FR*complex(RI, 0)        
        elif(I == 3):      
            if(IPREM3 == 0):
         
                for N in range(NC3):
                    x = 10**(A3 + (N)*S3)
                    X3.append(x)
                    x = 0
                IPREM3 = 1            
            FR = 0
            RI = 1/R            
            for N in range(NC3):
                FR = FR + FUN(X3[N]*RI)*complex(W3[N], 0.)
            HANKSGC = FR*complex(RI, 0)
        else:
            pass
        return HANKSGC
 
    def FreqEM(self): #Simulation of EM response based on full solution 
         
        self.p = (self.rho[self.ncou - 1]/self.frequency/numpy.pi/numpy.pi/0.4E-6)**0.5
        self.susc = complex(1 + self.chiP[self.ncou - 1], -self.chiQ[self.ncou - 1])
        self.gam2 = complex(0, numpy.pi*numpy.pi*self.frequency*0.8E-6/self.rho[self.ncou - 1])*self.susc   
        self.a = self.height*2/self.p       
        if self.config == CoilConfigEnum.HCP:
            B = self.spacing/self.p
            CB = complex(B, 0)
            T0 = self.HANKSGC(0, B, self.fun0, 1)
            QT = CB*CB*CB*T0*1000000       
        if self.config == CoilConfigEnum.VCP:
            B = self.spacing/self.p
            CB = complex(B, 0)
            T2 = self.HANKSGC(1, B, self.fun2, 1)
            QT = CB*CB*T2*1000000        
        if self.config == CoilConfigEnum.PERP:
            B = self.spacing/self.p
            CB = complex(B,0)
            T0 = self.HANKSGC(1,B,self.fun0,1)
            QT = CB*CB*CB*T0*1000000        
        if self.config == CoilConfigEnum.SH3:
            B = self.spacing/self.p
            CB = complex(B,0)
            T0 = CB*self.HANKSGC(0, B, self.fun0, 0) - self.HANKSGC(1, B, self.fun2, 0)/3
            QT = CB*CB*T0*1000000   
        return QT
    
    def FreqEMBuck(self):
        """Simulation of EM response for EMbuck coil device based on full solution"""
        
        qt = complex(0, 0)
#        cor = complex(0, 0)        
#        cor=complex((self.buckingcoil/self.spacing)**3.0,0.0)
        self.p = (self.rho[self.ncou - 1]/self.frequency/numpy.pi/numpy.pi/0.4E-6)**0.5
        self.susc = complex(1 + self.chiP[self.ncou - 1], - self.chiQ[self.ncou - 1])
        self.gam2 = complex(0, (numpy.pi*numpy.pi*self.frequency*0.8E-6)*(1/self.rho[self.ncou - 1]))*self.susc   
        self.a = (self.height)*1.0
#        self.A=self.height       
        if self.config == CoilConfigEnum.HCP:
            b = self.spacing/self.p
            cb = complex(b, 0)
            t1 = self.HANKSGC(0, b, self.fun3, 1)*cb*cb*cb            
            b = self.buckingcoil/self.p
            cb = complex(b, 0)
            t2 = self.HANKSGC(0, b, self.fun3, 1)*cb*cb*cb            
            qt = (t1 - t2)*1000000       
        if self.config == CoilConfigEnum.VCP:
            b = self.spacing/self.p
            cb = complex(b, 0)
            t1 = self.HANKSGC(1, b, self.fun4, 1)*cb*cb            
            b = self.buckingcoil/self.p
            cb = complex(b, 0)
            t2 = self.HANKSGC(1, b, self.fun4,1)*cb*cb
            qt = (t1 - t2)*1000000 
        return qt
        

    def FreqEMBuckFull(self):
        """ Simulation of EM response based on full solution with permittivity"""
        
        self.a = self.height
        cor = complex((self.buckingcoil/self.spacing)**3, 0.0)
        self.gam0 = complex(-self.frequency*self.frequency*(0.4E-15)*numpy.pi*numpy.pi/9.0, 0.0)
        self.p = (self.rho[self.ncou-1]/self.frequency/numpy.pi/numpy.pi/0.4E-6)**0.5
        self.s1 = complex(self.eps[self.ncou-1],-0.18E+11*(1/self.rho[self.ncou-1])/self.frequency)
        self.susc = complex(1 + self.chiP[self.ncou - 1], -self.chiQ[self.ncou - 1])
        self.csig = complex(1/self.rho[self.ncou - 1], self.eps[self.ncou - 1]*self.frequency/0.18E11)
        self.csig0 = complex(0., self.frequency/.18E11) 
        self.gam2 = self.s1*self.gam0*self.susc           
        if self.config == CoilConfigEnum.HCP:        
            b = self.spacing/self.p
            cb = complex(b,0)
            t1 = self.HANKSGC(0, b, self.fun00, 1)
            b = self.buckingcoil/self.p
            t2 = self.HANKSGC(0, b, self.fun00, 1)
            qt = (t1 - t2*cor)*cb*cb*cb*1000000
        return qt
    
    def McNeillToPpm(self, sigma):
        """transform a value of sigma (mS/m) in ppm for HCP et VCP"""
         
        omega = 2*numpy.pi*self.frequency
        mu0 = numpy.pi*4E-7
        PPM = -((omega*mu0*(sigma*1E-3)*(self.spacing)*(self.spacing))/4)*1E6        
        return PPM
         
    def ppmToMcNeill(self,value):#transform ppm in conductivity with McNeill formula for HCP et VCP
         
        omega = 2*numpy.pi*self.frequency
        mu0 = numpy.pi*4E-7        
        McNeill = -(4*(value*1E-6)/(omega*mu0*self.spacing*self.spacing))*1000
        return McNeill
     
    def ppmToCond(self, value):#transform ppm in conductivity using full solution 
         
        self.ncou = 1
        self.e = []
        SIGMA = range(1, 100, 1)
        degre = 3
        VAL = [1/(a*1E-3) for a in SIGMA]
        Mesqu = []        
        for res in VAL:
            self.rho = [res]
            self.chiP = [0.0]
            self.chiQ = [0.0]
            Mesqu.append(self.FreqEM().imag)                
        a1 = numpy.polyfit(Mesqu, SIGMA, degre)
        p1 = numpy.poly1d(a1)
        cond = p1(value)        
        return cond
    
    def ppmBuckToCond(self,value):
        """transform ppm in conductivity using full solution""" 
        
        self.ncou = 1
        self.e = []
        sigma = range(1, 300, 2)
        degre = 3
        val = [1/(a*1E-3) for a in sigma]
        mesqu = []        
        for res in val:
            self.rho = [res*1.0]
            self.chiP = [0.0]
            self.chiQ = [0.0]
            mesqu.append(self.FreqEMBuck().imag)                
        a1 = numpy.polyfit(mesqu, sigma, degre)
        p1 = numpy.poly1d(a1)
        return p1(value)
        
    def ppmBuckToSusc(self, value, resistivity):
        """Transform ppm value in susceptibility for a known resistivity value"""
        
        self.ncou = 1
        susc = range(1, 1000, 100)
        susc = [a*1E-5 for a in susc]
        degre = 3      
        mesph = []  
        self.rho = [resistivity]        
        for chi in susc:
            self.chiP = [chi]
            self.chiQ = [chi*0.6]
            mesph.append(self.FreqEMBuck().real)        
        a1 = numpy.polyfit(mesph, susc, degre)
        p1 = numpy.poly1d(a1)
        susc = p1(value)
        return susc*100000
    
    def ppmToCondList(self,vector):
        """transform ppm in conductivity using full solution"""
         
        self.ncou = 1
        self.e = []
        sigma = range(1, 100, 1)
        degre = 3
        val = [1/(a*1E-3) for a in sigma]
        mesqu = []        
        for res in val:
            self.rho = [res]
            self.chiP = [0.0]
            self.chiQ = [0.0]
            mesqu.append(self.FreqEM().imag)                
        a1 = numpy.polyfit(mesqu, sigma, degre)
        p1 = numpy.poly1d(a1)
        return [p1(a) for a in vector]
    
    def ppmToCond2f(self, value, f1, f2):
        """transform a difference of two frequencies in ppm (high frequency - low frequency) in conductivity (mS/m)"""
        
        self.ncou = 1
        self.e = []
        sigma = range(1, 100, 1)
        degre=3
        VAL=[1/(a*1E-3) for a in sigma]
        diff=[]  
        freq=self.frequency
        
        for res in VAL:
            self.rho=[res]
            self.chiP=[0.0]
            self.chiQ=[0.0]
            self.frequency=f1
            Mesqu1=self.FreqEM().imag
            self.frequency=f2
            Mesqu2=self.FreqEM().imag
            diff.append(Mesqu2-Mesqu1)
            
        a1=numpy.polyfit(diff, sigma, degre)
        p1=numpy.poly1d(a1)
        cond=p1(value)
        self.frequency=freq
        
        return cond

    def ppmToCond2fList(self, vector, f1, f2):
        
        self.ncou = 1
        self.e = []
        sigma = range(1, 100, 1)
        degre = 3
        val = [1/(a*1E-3) for a in sigma]
        diff = []  
        freq = self.frequency        
        for res in val:
            self.rho = [res]
            self.chiP = [0.0]
            self.chiQ = [0.0]
            self.frequency = f1
            mesqu1 = self.FreqEM().imag
            self.frequency = f2
            mesqu2 = self.FreqEM().imag
            diff.append(mesqu2 - mesqu1)            
        a1 = numpy.polyfit(diff, sigma, degre)
        p1 = numpy.poly1d(a1)
        vector = [p1(a) for a in vector]
        self.frequency = freq     
        return vector
    
    def ppmBuckToCondList(self, vector):
        
        self.ncou = 1
        self.e = []
        sigma = range(1, 100, 1)
        degre = 3
        val = [1/(a*1E-3) for a in sigma]
        Mesqu = []        
        for res in val:
            self.rho = [res]
            self.chiP = [0.0]
            self.chiQ = [0.0]
            Mesqu.append(self.FreqEMBuck().imag)                
        a1 = numpy.polyfit(Mesqu, sigma, degre)
        p1 = numpy.poly1d(a1)
        vector = [p1(a) for a in vector]
        return vector

    def ppmTosusc(self, value, resistivity):
        """ Transform ppm value in susceptibility for a known resistivity value"""
        
        self.ncou = 1
        susc = range(1, 1000, 100)
        susc = [a*1E-5 for a in susc]
        degre = 3      
        mesph = []  
        self.rho = [resistivity]        
        for chi in susc:
            self.chiP = [chi]
            self.chiQ = [chi*0.6]
            mesph.append(self.FreqEM().real)        
        a1 = numpy.polyfit(mesph, susc, degre)
        p1 = numpy.poly1d(a1)
        susc = p1(value)     
        return susc*100000
    
    def ppmBuckToSuscList(self, vector, resistivity):
                
        self.ncou = 1 
        susc = range(1, 1000, 100)
        susc = [a*1E-5 for a in susc]
        degre = 3      
        Mesph = []  
        self.rho = [resistivity]        
        for chi in susc:
            self.chiP = [chi]
            self.chiQ = [chi*0.6]
            Mesph.append(self.FreqEMBuck().real)        
        a1 = numpy.polyfit(Mesph, susc, degre)
        p1 = numpy.poly1d(a1)
        susc = [p1(a)*100000 for a in vector]
        return susc
    
    def ppmToSuscList(self, vector, resistivity):
                
        self.ncou = 1 
        susc = range(1, 1000, 100)
        susc = [a*1E-5 for a in susc]
        degre = 3      
        Mesph = []  
        self.rho = [resistivity]        
        for chi in susc:
            self.chiP = [chi]
            self.chiQ = [chi*0.6]
            Mesph.append(self.FreqEM().real)        
        a1 = numpy.polyfit(Mesph, susc, degre)
        p1 = numpy.poly1d(a1)
        susc = [p1(a)*100000 for a in vector]
        return susc
    
    def FreqEMMcNeill(self, method = 'cumul'):
        """Give the apparent conductivity (mS/m) from a specified model based on linear solution"""
        
        funList, depth = [], []
        prof = 0        
        for i in self.e:
            prof = prof + i
            depth.append(prof)        
        for i in range(self.ncou - 1):
            z = depth[i]/self.spacing
            if method == 'cumul':
                if self.config == CoilConfigEnum.HCP:
                    r = 1/((4*z*z + 1)**0.5)
                if self.config == CoilConfigEnum.VCP:
                    r = ((4*z*z + 1)**0.5) - 2*z
                funList.append(r)
            if method == 'relative':
                if self.config == CoilConfigEnum.HCP:
                    phi = 4*z/(4*z*z + 1)**(3/2)
                if self.config == CoilConfigEnum.VCP:
                    phi = 2-(4*z/(4*z*z + 1)**0.5)
                funList.append(phi)        
        for i in range(self.ncou):
            if i == 0:
                contribution=((1/self.rho[i])*(1 - funList[i]))
            elif i == max(range(self.ncou)):
                contribution = contribution + (1/self.rho[i])*funList[i - 1]
            else:
                contribution = contribution + ((1/self.rho[i])*(funList[i - 1] - funList[i]))
        return contribution*1000