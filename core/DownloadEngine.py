# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGT - Archaeological Geophysics Toolbox
                                 A QGIS plugin
 This plugin does basic processes on geophysical data for Archaeology
                             -------------------
        begin                : 2016-04-14
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Nariman HATAMI / INRAP
        email                : nariman.hatami@inrap.fr
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

#using Unicode for all strings
# from __future__ import unicode_literals
# 
# from PyQt4.QtCore import *
# from PyQt4 import QtGui
# from qgis.core import *
# 
# import os.path
# from ..lib.serial import *
# import numpy as np
# import sys
#   
# from PyQt4.QtGui import QFileDialog
#  
#  
# from ..toolbox.AGTUtilities import Utilities
# from ..toolbox.AGTExceptions import *
#  
# class DownloadEngine(object):
#     
#     def __init__(self, datOutput, isRM85, gridNb, gridX, gridY, probeSpacing, channelNb, probeNb, collectedPointNb, lineStep, probeConfig, currentInt, 
#                   comPort, baudRate):
#         
#         self.outputFileName = datOutput
#         self.resMeter = 'RM85' if isRM85 else 'RM15'
#         self.gridNb = gridNb
#         self.grids = []
#         self.gridX = gridX
#         self.gridY = gridY
#         self.probeSpacing = probeSpacing
#         self.channelNb = channelNb
#         self.probeNb = probeNb
#         self.measuredNb = collectedPointNb
#         self.lineStep = lineStep
#         self.probConfig = probeConfig
#         self.currentInt = currentInt
#         self.serialPort = comPort[:4]
#         self.baudRate = baudRate
#                  
#     def RMDownload(self):        
#    
#         ser = Serial()
#         ser.baudrate = self.baudRate
#         ser.port = self.serialPort       
#         ser.open() 
#         ser.flushInput()
#         ser.flushOutput()
#         data = []      
#         totalData = 0
#         while totalData == 0:
#             bytesToRead = ser.readline()
#             if bytesToRead != '':                               
#                 totalData = int(self.gridNb*self.gridX*self.gridY*self.measuredNb/self.lineStep)          
#                 for x in range(totalData):
#                     if x == 0:
#                         dataline = str(bytesToRead)
#                     else :
#                         dataline = str(ser.readline())                        
#                     metadataline = str(ser.readline())                  
#                     if '4095' in dataline:
#                         value = '999'
#                     elif '4094' in dataline:
#                         value = '999'
#                     else:
#                         if '00' in metadataline:
#                             value = int(dataline.strip())/0.2
#                         elif ('10' in metadataline) or ('01' in metadataline) :
#                             value = int(dataline.strip())/2.0
#                         elif ('20' in metadataline) or ('11' in metadataline) or ('02' in metadataline):
#                             value = int(dataline.strip())/20.0
#                         elif ('21' in metadataline) or ('12' in metadataline):
#                             value = int(dataline.strip())/200.0
#                         elif ('22' in metadataline):
#                             value = int(dataline.strip())/2000.0
#                         else:
#                             value = int(dataline.strip())
#                         value = round(value, 2) #conversion to resistance values                    
#                     data.append(value)  
#         ser.close()         
#         outputFile = open(self.outputFileName,'w')
#         outputFile.write(self.resMeter + '\n')
#         outputFile.write(str(self.gridNb) + '\n')
#         outputFile.write(str(self.gridX) + '\n')
#         outputFile.write(str(self.gridY) + '\n')
#         outputFile.write(str(self.probeSpacing) + '\n')
#         outputFile.write(str(self.channelNb) + '\n')
#         outputFile.write(str(self.probeNb) + '\n')
#         outputFile.write(str(self.lineStep) + '\n')
#         outputFile.write(self.probConfig + '\n')
#         outputFile.write(str(self.currentInt) + '\n')
#         for grid in self.grids:
#             outputFile.write(str(grid[0]) + '\n')
#             outputFile.write(str(grid[1]) + '\n')
#             outputFile.write(str(grid[2]) + '\n')         
#         for i in range(len(data)):
#             outputFile.write(str(data[i]) + '\n')        
#         outputFile.close()
#         self.grids = []
#     