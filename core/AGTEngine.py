# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGT - Archaeological Geophysics Toolbox
                                 A QGIS plugin
 This plugin does basic processes on geophysical data for Archaeology
                             -------------------
        begin                : 2016-04-14
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Nariman HATAMI - François-Xavier SIMON / INRAP
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

#using Unicode for all strings
from __future__ import unicode_literals

import math
from operator import itemgetter
import numpy

from PyQt4.QtCore import *
from PyQt4 import QtGui
from qgis.core import *

import os
from os.path import splitext
from os.path import dirname
from os.path import basename

from CoilEnum import CoilConfigEnum
from FilterEnum import FilterEnum
from ..toolbox.AGTUtilities import Utilities
from ..toolbox.AGTExceptions import *
from SignalEM import SignalEM

class Engine(object):
    
    filteredPointNum = []   
    def __init__(self, rawDataFilename, dataEncoding, datOutput, crsRefImp = None, crsRefExp = None, projectName = None, medianPercent = None, kernelSize = None, filter = None, 
                 addCoordFields = None, decimValue = None, medRemove = None, percentile = None, percThreshold = None,
                 trendRemove = None, trendPolyOrder = None, trendPercentile = None, trendPercThreshold = None, statPtRem = None, statPtThresh = None, 
                 gpsProbe = None, outputShapefile = None, sensorHeight = None, coilConfig = None):
       
        self.rawDataFilename = rawDataFilename
        self.dataEncoding = dataEncoding
        self.gridNames = []        
        self.OriginX = []
        self.OriginY = []
        self.rawData = []
        self.basicOutputFilename = projectName
        if crsRefImp:
            self.inputCrsCode = Utilities.crsRefDict[crsRefImp]
        else:
            self.inputCrsCode = 2154 #RGF93 / Lambert-93        
        if crsRefExp:
            self.outputCrsCode = Utilities.crsRefDict[crsRefExp]
        else:
            self.outputCrsCode = 2154 #RGF93 / Lambert-93        
        self.crs = QgsCoordinateReferenceSystem(self.outputCrsCode)            
  
        #self.crs.createFromProj4("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs") #4326
        self.medianPercent = medianPercent
#         if kernelSize: 
#             self.kernelRadius = kernelSize/100.00
        if kernelSize :
            self.kernelSize = kernelSize
        self.isFilter = filter
        self.rawDataMat = []    
        self.datOutput = datOutput
        # Magnetic    
        self.isAddCoordFields = addCoordFields
        self.decimationVal = decimValue
        self.isMedianRemoval = medRemove
        self.isPercentile = percentile
        self.percThreshold = percThreshold
        self.isTrendRemoval = trendRemove
        self.trendPolyOrder = trendPolyOrder
        self.isTrendPercentile = trendPercentile
        self.trendPercThreshold = trendPercThreshold
        self.isStationPtRem = statPtRem
        if statPtThresh:
            self.stationPtThreshold = float(statPtThresh)
        self.gpsProbe = gpsProbe
        self.outputShapefile = outputShapefile
        self.sensorHeight = sensorHeight
        self.coilConfig = coilConfig
        # data
        self.magPoints = []
        self.sortedMagPoints = []    
        # profile
        self.correctedX = []
        self.profile = []
        #self.medianRemoval
        self.medianRemValues = []
        # for EM31
        self.Qppm = []
        self.I = []
        self.cond = []
        self.EM31Points = []
        self.Grad601 = False
        self.x = []
        self.y = []
        
    def getOriginX(self):
        
        return self.OriginX
    
    def getOriginY(self):
        
        return self.OriginY
    
    def getGridNbr(self):
        
        return self.gridNbr
    
    def getGridNames(self):
        
        return self.gridNames
        
    def rawDataParser(self):        
        
        rawDataFile = QFile(self.rawDataFilename)
        if not(rawDataFile.exists()):
            return
        if rawDataFile.open(QFile.ReadOnly|QFile.Text):
            # header (metadata)
            if not(rawDataFile.atEnd()):
                self.resistivimeter = rawDataFile.readLine()
            if not(rawDataFile.atEnd()):
                self.gridNbr = int(rawDataFile.readLine())
            if not(rawDataFile.atEnd()):
                self.gridLen = int(rawDataFile.readLine())
            if not(rawDataFile.atEnd()):
                self.gridWid = int(rawDataFile.readLine())
            if not(rawDataFile.atEnd()):
                self.ElectGap = float(rawDataFile.readLine())
            if not(rawDataFile.atEnd()):
                self.channelNbr = int(rawDataFile.readLine())
            if not(rawDataFile.atEnd()):
                self.ElectNbr = int(rawDataFile.readLine())
            if not(rawDataFile.atEnd()):
                self.PointDist = float(rawDataFile.readLine())
            if not(rawDataFile.atEnd()):
                self.measureType = rawDataFile.readLine()
            if not(rawDataFile.atEnd()):
                self.CurrentInt = rawDataFile.readLine()              
            for i in range(0, self.gridNbr):
                if rawDataFile.atEnd():
                    return
                self.gridNames.append(int(rawDataFile.readLine()))
                self.OriginX.append(float(rawDataFile.readLine()))
                self.OriginY.append(float(rawDataFile.readLine()))                                 
            # data            
            pointId = []
            fileNbr = self.gridNbr*self.channelNbr
            channelCount = 0
            for i in range(0, fileNbr):                
                self.rawData.append({})
                pointId.append(0)
                if self.isFilter:
                    Engine.filteredPointNum.append(0)
                    self.rawDataMat.append([])
                    measureNbr = self.channelNbr - channelCount                   
                    width = measureNbr*self.gridWid                        
                    for j in range(0, width):
                        l = []
                        for k in range(0, self.gridLen):
                            l.append(999)                            
                        self.rawDataMat[i].append(l)      
                channelCount += 1
                channelCount %= self.channelNbr           
            gridCount = 0            
            i = 0                       
            j = 0
            x = 0
            y = 0
            yStep = self.PointDist
            jStep = 1
            barLen = (self.ElectNbr - 1)*self.ElectGap                 
            while not(rawDataFile.atEnd()):
                for channelCount in range(0, self.channelNbr):
                    measureNbr = self.channelNbr - channelCount                    
                    xShift = (channelCount + 1)*self.ElectGap/2 # the measured point is in the middle of the two measuring elecrodes
                    if yStep < 0:
                        xShift = -xShift
                    filtI = 0 
                    for measureCount in range(0, measureNbr):
                        res = float(rawDataFile.readLine())
                        # real resistivity -> apparent resistivity
                        appRes = math.fabs(2*math.pi*res*(channelCount + 1)*self.ElectGap) if (res != 999) else res
                        self.rawData[gridCount*self.channelNbr + channelCount][(QgsPoint(x + xShift + self.OriginX[gridCount], y + self.OriginY[gridCount]), measureCount)] = (pointId[gridCount*self.channelNbr + channelCount], appRes)
                        if self.isFilter:
                            self.rawDataMat[gridCount*self.channelNbr + channelCount][(i*measureNbr) + filtI][j] = [QgsPoint(x + xShift + self.OriginX[gridCount], y + self.OriginY[gridCount]), appRes, 0, pointId[gridCount*self.channelNbr + channelCount]]                                                   
                            filtI += 1
                        if yStep > 0:                                                
                            xShift += self.ElectGap
                        else:
                            xShift -= self.ElectGap # U-turn of the resistivity meter 
                        pointId[gridCount*self.channelNbr + channelCount] += 1
                y += yStep
                j += jStep
                if(j == self.gridLen or j == -1):
                    yStep *= -1
                    jStep *= -1
                    y += yStep 
                    j += jStep                    
                    i += 1
                    if yStep < 0:
                        x += 2*barLen
                    if i == self.gridWid:
                        i = 0
                        x = 0
                        gridCount += 1
                if gridCount > self.gridNbr:
                    raise ParserError(self.rawDataFilename, QtGui.QApplication.translate(u"Engine",'The number of measured points does not correspond to the metadata.'))                     
        else:
            raise ParserError(self.rawDataFilename, QtGui.QApplication.translate(u"Engine",'Can not open file.'))        

    def magRawDataParser(self):
        
        rawDataFile = QFile(self.rawDataFilename)
        if not(rawDataFile.exists()):
            return
        if rawDataFile.open(QFile.ReadOnly|QFile.Text):
            while not(rawDataFile.atEnd()):
                line = str(rawDataFile.readLine())           
                data = line.rstrip('\n\r').split()
                self.magPoints.append((float(data[0]), float(data[1]), float(data[2]), str(data[3]), int(data[4]))) # (x, y, value, trace, probe)
        else:
            raise ParserError(self.rawDataFilename, QtGui.QApplication.translate(u"Engine",'Can not open file.'))       
    
    def magGridRawDataParser(self):
        
        rawDataFile = QFile(self.rawDataFilename)
        if not(rawDataFile.exists()):
            return
        if rawDataFile.open(QFile.ReadOnly|QFile.Text):
            # header (metadata)
            if not(rawDataFile.atEnd()):
                headerLine = rawDataFile.readLine()            
                rawDataFile.close()
                if ('Time' in headerLine):
                    self.Grad601GridParser()
                else:
                    self.MXPDAGridParser()                
        
    def Grad601GridParser(self):
       
        rawDataFile = QFile(self.rawDataFilename)
        if rawDataFile.open(QFile.ReadOnly|QFile.Text):
            # header (metadata)
            for i in range(14): # there are 14 lines of metadata
                if not(rawDataFile.atEnd()):
                    headerLine = rawDataFile.readLine()
            # data
            while not(rawDataFile.atEnd()):
                line = str(rawDataFile.readLine())           
                data = line.rstrip('\n\r').split()
                # the data are already sorted
                self.sortedMagPoints.append((float(data[0]), float(data[1]), float(data[2]))) # (x, y, value)
        else:
            raise ParserError(self.rawDataFilename, QtGui.QApplication.translate(u"Engine",'Can not open file.'))
        self.Grad601 = True
    
    def MXPDAGridParser(self):
        
        rawDataFile = QFile(self.rawDataFilename)
        if rawDataFile.open(QFile.ReadOnly|QFile.Text):
            # header (metadata)
            if not(rawDataFile.atEnd()):
                headerLine = rawDataFile.readLine()
            # data
            while not(rawDataFile.atEnd()):
                line = str(rawDataFile.readLine())           
                data = line.rstrip('\n\r').split()
                # the data are already sorted
                self.sortedMagPoints.append((float(data[0]), float(data[1]), float(data[2]))) # (x, y, value)
        else:
            raise ParserError(self.rawDataFilename, QtGui.QApplication.translate(u"Engine",'Can not open file.'))
               
    def filterRawData(self):    
    
        returnMsg = "" 
        kernelHalf = int(self.kernelSize/2)
        for channel in range(0, self.channelNbr):            
            for grid in range(0, self.gridNbr):
                mat = self.rawDataMat[grid*self.channelNbr + channel]
                measureNbr = self.channelNbr - channel
                width = measureNbr*self.gridWid
                for i in range(0, width):
                    for j in range(0, self.gridLen):
                        if mat[i][j][1] == 999 or mat[i][j][1] < 2:
                            continue
                        resList = []                        
                        for k in range(-kernelHalf, kernelHalf + 1):
                            for l in range(-kernelHalf, kernelHalf + 1):                        
                                if (i + k) >= 0 and (i + k) < width and (j + l) >= 0 and (j + l) < self.gridLen:
                                    if mat[i + k][j + l][1] != 999 and mat[i + k][j + l][1] >= 2:
                                        resList.append(mat[i + k][j + l][1])                                   
                        self.rawDataMat[grid*self.channelNbr + channel][i][j][2] = self.medianFilter(grid, channel, resList, mat[i][j][1])                  
                returnMsg += QtGui.QApplication.translate(u"Engine",u"{} points were filtered for grid #{} channel #{}.\n").format(Engine.filteredPointNum[grid*self.channelNbr + channel], self.gridNames[grid], channel + 1)
                Engine.filteredPointNum[grid*self.channelNbr + channel] = 0                
        self.createFilteredShapefile()        
        return returnMsg
                 
    def createFilteredShapefile(self): # provisoire, à rajouter un if dans createRelCoordShapefile en changeant son nom
        
        shapefiles = []
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        fields.append(QgsField("rel_x", QVariant.Double))
        fields.append(QgsField("rel_y", QVariant.Double))
        fields.append(QgsField("res", QVariant.Double, 'double', 6, 2))
        
        filterFieldName = "med_" + str(self.medianPercent)
        fields.append(QgsField(filterFieldName, QVariant.Double, 'double', 6, 2))
                 
        folder = dirname(self.rawDataFilename)
        basicPath = folder + '/' + self.basicOutputFilename + '/Shapefiles'        
        for channel in range(0, self.channelNbr):
            channelPath = basicPath + '/' + 'channel' + str(channel + 1)
            if not os.path.exists(channelPath):
                os.makedirs(channelPath)
            for grid in range(0, self.gridNbr):
                fileName = channelPath + '/' + self.basicOutputFilename + '_channel' + str(channel + 1) + '_grid' + str(self.gridNames[grid]) + '.shp'
                features = []
                measureNbr = self.channelNbr - channel
                width = measureNbr*self.gridWid       
                for i in range(0, width):
                    for j in range(0, self.gridLen):
                        self.rawDataMat[grid*self.channelNbr+ channel][i][j][1]
                        if(self.rawDataMat[grid*self.channelNbr+ channel][i][j][1] != 999 and self.rawDataMat[grid*self.channelNbr+ channel][i][j][1] >= 2): # points with resistivity = 999 are not real measured points - res < 2 are not relevant 
                            feature = QgsFeature()
                            feature.setGeometry(QgsGeometry.fromPoint(self.rawDataMat[grid*self.channelNbr+ channel][i][j][0]))
                            feature.setAttributes([self.rawDataMat[grid*self.channelNbr+ channel][i][j][3], self.rawDataMat[grid*self.channelNbr+ channel][i][j][0].x(), 
                                                   self.rawDataMat[grid*self.channelNbr+ channel][i][j][0].y(), self.rawDataMat[grid*self.channelNbr+ channel][i][j][1], self.rawDataMat[grid*self.channelNbr+ channel][i][j][2]])
                            features.append(feature)                    
                Utilities.createShapefile(fileName, fields, features, self.dataEncoding, self.crs)
                shapefiles.append(fileName)
                if self.datOutput:
                    attInd = [3, 4] # the list of the indices of the attributes to be written in .dat files            
                    Utilities.shapefileToDAT(fileName, attInd, filterFieldName)
        return shapefiles                   
            
            
    def filterShapefiles(self):
               
        returnMsg = ""     
        folder = dirname(self.rawDataFilename)
        basicPath = folder + '/' + self.basicOutputFilename + '/Shapefiles'
        for channel in range(0, self.channelNbr):            
            for grid in range(0, self.gridNbr):
                channelPath = basicPath + '/' + 'channel' + str(channel + 1)            
                fileName = channelPath + '/' + self.basicOutputFilename + '_channel' + str(channel + 1) + '_grid' + str(self.gridNames[grid]) + '.shp'                
                self.filterFile(fileName, grid, channel)       
                returnMsg += QtGui.QApplication.translate(u"Engine",u"{} points were filtered for grid #{} channel #{}.\n").format(Engine.filteredPointNum[grid*self.channelNbr + channel], self.gridNames[grid], channel + 1)
                Engine.filteredPointNum[grid*self.channelNbr + channel] = 0
        return returnMsg
        
             
    def filterFile(self, fileName, grid, channel):
               
        vLayer = QgsVectorLayer(fileName , "filter", "ogr")
        filterFieldName = "med_" + str(self.medianPercent)
        vLayer.dataProvider().addAttributes([QgsField(filterFieldName, QVariant.Double, 'double', 6, 2)])
        resIndx = vLayer.fieldNameIndex('res')
        featuresIter = vLayer.getFeatures()
        for feature in featuresIter:
            p = feature.geometry().asPoint()
            attrib = feature.attributes()                                
            resList = []            
            res = attrib[resIndx]
            featuresIter2 = vLayer.getFeatures()                     
            for feat2 in featuresIter2:
                p2 = feat2.geometry().asPoint()
                distanceCal = QgsDistanceArea()
                testDist = distanceCal.measureLine(p, p2)
                if (testDist <= self.kernelRadius):        
                    att = feat2.attributes()
                    resList.append(att[resIndx])       
            lastIndx = len(vLayer.pendingAllAttributesList()) # the index of the last field added is the median filter value
            attrs = {lastIndx : self.medianFilter(grid, channel, resList, res)}
            vLayer.dataProvider().changeAttributeValues({feature.id() : attrs})
        if self.datOutput:                   
            attInd = [resIndx, vLayer.fieldNameIndex(filterFieldName)] # the list of the indices of the attributes to be written in .dat files                
            Utilities.shapefileToDAT(fileName, attInd, filterFieldName)
    
    def medianFilter(self, grid, channel, resistivityList, res):
        
        if len(resistivityList) == 0 or res == 999 or res < 2: 
            return res
        resistivityList.sort()
        medianRes = resistivityList[(len(resistivityList) - 1)/2]        
        diff = (res - medianRes)/res if(res >= medianRes) else (medianRes - res)/medianRes
        if diff >= (self.medianPercent/100.00):
            Engine.filteredPointNum[grid*self.channelNbr + channel] += 1           
            return medianRes            
        else:
            return res
        

    def createRelCoordShapefile(self):
 
        shapefiles = []
        fields = QgsFields()
        fields.append(QgsField("id", QVariant.Int))
        fields.append(QgsField("rel_x", QVariant.Double))
        fields.append(QgsField("rel_y", QVariant.Double))
        fields.append(QgsField("res", QVariant.Double, 'double', 6, 2)) 
        folder = dirname(self.rawDataFilename)
        basicPath = folder + '/' + self.basicOutputFilename + '/Shapefiles'        
        for channel in range(0, self.channelNbr):
            channelPath = basicPath + '/' + 'channel' + str(channel + 1)
            if not os.path.exists(channelPath):
                os.makedirs(channelPath)     
            for grid in range(0, self.gridNbr):
                fileName = channelPath + '/' + self.basicOutputFilename + '_channel' + str(channel + 1) + '_grid' + str(self.gridNames[grid]) + '.shp'
                features = []
                for key, attr in self.rawData[grid*self.channelNbr+ channel].items():
                    if(attr[1] != 999 and attr[1] >= 2): # points with resistivity = 999 are not real measured points - res < 2 are not relevant 
                        feature = QgsFeature()
                        feature.setGeometry(QgsGeometry.fromPoint(key[0]))
                        feature.setAttributes([attr[0], key[0].x(), key[0].y(), attr[1]])
                        features.append(feature)
                Utilities.createShapefile(fileName, fields, features, self.dataEncoding, self.crs)
                shapefiles.append(fileName)
        return shapefiles
    
    def createRelCoordDatFile(self): 
                
        folder = dirname(self.rawDataFilename)
        basicPath = folder + '/' + self.basicOutputFilename + '/DATfiles'
        for channel in range(0, self.channelNbr):
            channelPath = basicPath + '/' + 'channel' + str(channel + 1)
            if not os.path.exists(channelPath):
                os.makedirs(channelPath)   
            for grid in range(0, self.gridNbr):
                fileName =  channelPath + '/' + self.basicOutputFilename + '_channel' + str(channel + 1) + '_grid' + str(self.gridNames[grid]) + '.dat'
                fileObj = open(fileName, 'w')
                pointList = []
                for key, attr in self.rawData[grid*self.channelNbr+ channel].items():
                    if attr[1] != 999:
                        pointList.append((attr, key[0]))                
                sortedList = sorted(pointList, key = lambda pt : pt[0][0])
                for point in sortedList:
                    fileObj.write(str(point[1].x()) + ', ' + str(point[1].y()) + ', ' + str(point[0][1]) + '\n')
                fileObj.close()
        
    def createMagDatExport(self):
        
        datFileName = self.outputShapefile.replace('.shp', '.dat')
        fileObj = open(datFileName, 'w')
        for i in range(0, len(self.sortedMagPoints)):            
            fileObj.write(str(self.correctedX[i]) + ', ' + str(self.sortedMagPoints[i][1])+ ', ' + str(self.medianRemValues[i]) + ', ' + 
                          str(self.sortedMagPoints[i][3]) + ', ' + str(self.sortedMagPoints[i][4]) + ', ' + str(self.profile[i]) + '\n')
        fileObj.close()
    
    def createMagGridRelCoordDatExport(self):
       
        datFileName = self.outputShapefile.replace('.shp', '.dat')
        fileObj = open(datFileName, 'w')
        for i in range(0, len(self.sortedMagPoints)):            
            fileObj.write(str(self.sortedMagPoints[i][0]) + ', ' + str(self.sortedMagPoints[i][1])+ ', ' + str(self.medianRemValues[i]) +
                          str(self.profile[i]) + '\n')
        fileObj.close()
        
    def createGeorefShapefile(self, geoPoints, fields, fileName):
        
        fields = QgsFields(fields)
        fields.append(QgsField("geo_x", QVariant.Double, 'double'))        
        fields.append(QgsField("geo_y", QVariant.Double, 'double'))        
        fileName = fileName[:-4] + '_Gref.shp'        
        features = []        
        for point in geoPoints:                 
            feature = QgsFeature()
            feature.setGeometry(QgsGeometry.fromPoint(point[0]))
            attrList = point[1]
            attrList.extend([point[0].x(), point [0].y()]) 
            feature.setAttributes(attrList)           
            features.append(feature)            
        Utilities.createShapefile(fileName, fields, features, self.dataEncoding, self.crs)
        if self.datOutput :           
            if self.basicOutputFilename is not None: #RM only
                attInd = [fields.indexFromName('res')]
                fieldList = fields.toList()                              
                filterField = filter(lambda f: f.displayName().find('med') != -1, fieldList)            
                if filterField:
                    attInd.append(fields.indexFromName(filterField[0].displayName()))
                    filterName = "med_" + str(self.medianPercent)
                else:
                    filterName = None
                Utilities.shapefileToDAT(fileName, attInd, filterName)          
            else: #magGrid
                attInd = fields.allAttributesList()
                Utilities.shapefileToDAT(fileName, attInd)


    def createMagShapefile(self):

        fields = QgsFields()
        fields.append(QgsField('value', QVariant.Double, 'double', 12, 4))   
        fields.append(QgsField('val_process', QVariant.Double, 'double', 12, 4))
        fields.append(QgsField('trace', QVariant.String))
        fields.append(QgsField('probe', QVariant.Int))
        fields.append(QgsField('profile', QVariant.Int))
        if self.isAddCoordFields:
            fields.append(QgsField('X', QVariant.Double))
            fields.append(QgsField('Y', QVariant.Double))
        features = []                
        crsSrc = QgsCoordinateReferenceSystem(self.inputCrsCode)
        xform = QgsCoordinateTransform(crsSrc, self.crs)                                             
        for i in range(0, len(self.sortedMagPoints)):
            feature = QgsFeature()
            qPoint = QgsPoint(self.correctedX[i], self.sortedMagPoints[i][1])
            xPoint = xform.transform(qPoint) #coordinate Transform
            feature.setGeometry(QgsGeometry.fromPoint(xPoint))
            if self.isAddCoordFields:            
                feature.setAttributes([self.sortedMagPoints[i][2], 
                                        self.medianRemValues[i], 
                                        self.sortedMagPoints[i][3], 
                                        self.sortedMagPoints[i][4], 
                                        self.profile[i], 
                                        self.correctedX[i], 
                                        self.sortedMagPoints[i][1]])
            else:
                feature.setAttributes([self.sortedMagPoints[i][2], 
                                       self.medianRemValues[i], 
                                       self.sortedMagPoints[i][3], 
                                       self.sortedMagPoints[i][4], 
                                       self.profile[i]])             
            features.append(feature)
        Utilities.createShapefile(self.outputShapefile, fields, features, self.dataEncoding, self.crs)
        
    def createMagGridRelCoordShapefile(self):

        fields = QgsFields()
        fields.append(QgsField('value', QVariant.Double, 'double', 12, 4))   
        fields.append(QgsField('val_process', QVariant.Double, 'double', 12, 4))
        fields.append(QgsField('profile', QVariant.Int))        
        if self.isAddCoordFields:
            fields.append(QgsField('X', QVariant.Double))
            fields.append(QgsField('Y', QVariant.Double))
        features = []
        self.x = [float("{0:.4f}".format(x)) for x in self.x]
        self.y = [float("{0:.4f}".format(y)) for y in self.y]
        for i in range(0, len(self.sortedMagPoints)):
            feature = QgsFeature()
            #qPoint = QgsPoint(self.sortedMagPoints[i][0], self.sortedMagPoints[i][1])
            qPoint = QgsPoint(self.x[i], self.y[i])
            feature.setGeometry(QgsGeometry.fromPoint(qPoint))
            if self.isAddCoordFields:            
                feature.setAttributes([self.sortedMagPoints[i][2], 
                                        self.medianRemValues[i],
                                        self.profile[i],
                                        self.sortedMagPoints[i][0], 
                                        self.sortedMagPoints[i][1]])
            else:
                feature.setAttributes([self.sortedMagPoints[i][2], 
                                       self.medianRemValues[i],
                                       self.profile[i]])             
            features.append(feature)
        Utilities.createShapefile(self.outputShapefile, fields, features, self.dataEncoding, self.crs)
        
    def georeferencing(self, grid, x1, y1, xg1, yg1, x2, y2, xg2, yg2):
        
        xg = xg2 - xg1
        yg = yg2 - yg1
        x = x2 - x1
        y = y2 - y1
        scal = x*xg + y*yg
        cosAngle = scal/(math.sqrt(x*x + y*y)*math.sqrt(xg*xg + yg*yg))
        sinAngle = math.sqrt(1 - cosAngle*cosAngle)
        rotSign = x*yg - y*xg
        if rotSign < 0:
            a = 1
            b = -1
        elif rotSign > 0:
            a = -1
            b = 1
        else:
            a = 1
            b = 1
        if (grid is not None): # electrical       
            folder = dirname(self.rawDataFilename)
            basicPath = folder + '/' + self.basicOutputFilename + '/Shapefiles'     
            for channel in range(0, self.channelNbr):
                channelPath = basicPath + '/' + 'channel' + str(channel + 1)            
                fileName = channelPath + '/' + self.basicOutputFilename + '_channel' + str(channel + 1) + '_grid' + str(self.gridNames[grid]) + '.shp'                
                self.georeferecingTrans(fileName, sinAngle, cosAngle, x1, y1, xg1, yg1, a, b)
        else: # grid magnetic
            self.georeferecingTrans(self.outputShapefile, sinAngle, cosAngle, x1, y1, xg1, yg1, a, b)
           
    def georeferecingTrans(self, fileName, sinAngle, cosAngle, x1, y1, xg1, yg1, a, b):
        
        vLayer = QgsVectorLayer(fileName , "georef", "ogr")
        geoPoints = []
        featuresIter = vLayer.getFeatures()
        for feature in featuresIter:
            p = feature.geometry().asPoint()
            attrib = feature.attributes()
            pg = self.ptTransformation(p, sinAngle, cosAngle, x1, y1, xg1, yg1, a, b)        
            geoPoints.append((pg, attrib))              
        self.createGeorefShapefile(geoPoints, vLayer.fields(), fileName)
                                    
    def ptTransformation(self, p, sinAngle, cosAngle, x1, y1, xg1, yg1, a, b):
           
        # translation
        xT = p.x() - x1
        yT = p.y() - y1
        # rotation
        xR = xT*cosAngle + yT*a*sinAngle
        yR = xT*b*sinAngle + yT*cosAngle
        # translation 
        newX = xR + xg1
        newY = yR + yg1
        return QgsPoint(newX, newY)
    
    
    def sortMagPoints(self):
        self.sortedMagPoints = sorted(self.magPoints, key = itemgetter(3, 4)) 
    
    def magDecimation(self):
        
        probeNb = max(list(zip(*self.magPoints)[4]))
        thresh = probeNb*self.decimationVal # self.decimantionVal = 1/frequency
        magDecimPoints = []
        for i in range(0, len(self.magPoints), thresh): 
            for j in range (probeNb):
                magDecimPoints.append(self.magPoints[i + j])           
        self.magPoints = magDecimPoints
    
    def medMovWinDecimation(self):        
    
        stamp = 0
        magDecimPoints = []
        probNb = max(list(zip(*self.magPoints)[4]))              
        medianList = []
        for i in range(0, probNb):
            medianList.append([])      
        for i in range (0, len(self.magPoints), probNb):
            if stamp < self.decimationVal:   # creation of list containing necessary values for calculation of median on DecimaVal points
                for j in range(0, probNb):
                    medianList[j].append(self.magPoints[i + j][2])               
                stamp += 1
            else:
                medianVals = list(map(lambda x : numpy.median(x), medianList)) # Median calculation               
                for j in range(0, probNb):
                    magDecimPoints.append((self.magPoints[i + j - (self.decimationVal/2)][0], self.magPoints[i + j - (self.decimationVal/2)][1], float(medianVals[j]), 
                                           self.magPoints[i + j - (self.decimationVal/2)][3], self.magPoints[i + j - (self.decimationVal/2)][4]))             
                medianList = []
                stamp = 1
                for j in range(0, probNb):
                    medianList.append([])                   
                    medianList[j].append(self.magPoints[i + j][2])                
        self.magPoints = magDecimPoints    
            
    def distanceFilter(self):
        
        probeNb = max(list(zip(*self.magPoints)[4]))
        magStatPoints = []
        for i in range(0, len(self.magPoints)):
            if self.gpsProbe == self.magPoints[i][4]:
                dist1 = math.sqrt((self.magPoints[i][0] - self.magPoints[i - probeNb][0])**2 + (self.magPoints[i][1] - self.magPoints[i - probeNb][1])**2)
                dist2 = math.sqrt((self.magPoints[i + (self.gpsProbe//2)][0] - self.magPoints[i - probeNb + (self.gpsProbe//2)][0])**2 + 
                                (self.magPoints[i + (self.gpsProbe//2)][1] - self.magPoints[i - probeNb + (self.gpsProbe//2)][1])**2)  
                if dist2 < (self.stationPtThreshold*dist1):
                    for j in range(probeNb):
                        loc = i - j + (self.gpsProbe//2)
                        magStatPoints.append(self.magPoints[loc])
        self.magPoints = magStatPoints
                
    
    # UTM value correction of X coordinates, and the creation of a profile column
    def createProfileList(self):
        
        utmVal = int(self.sortedMagPoints[0][0]/1000000) # determination of the UTM value (the 2 first digits of x)
        self.inputCrsCode = 32600 + utmVal
        for i in zip(*self.sortedMagPoints)[0]: # x values
            self.correctedX.append(i - (utmVal*1000000)) # x values' correction            
        n = 1
        newProfile = 1
        for i in zip(*self.sortedMagPoints)[4]: # profile correction
            if i == n:
                self.profile.append(newProfile)
            else :
                newProfile += 1
                n = i
                self.profile.append(newProfile)
        
    # Simple copy of X coordinates 
    def CreateSimpleProfileListRelCoord(self):
        
        n = self.sortedMagPoints[0][0]
        newProfile = 1
        a = 1 if self.Grad601 else 0
        for x in zip(*self.sortedMagPoints)[a]: # profile correction
            if x == n:
                self.profile.append(newProfile)
            else :
                newProfile += 1
                n = x
                self.profile.append(newProfile)                
        for i in range(len(self.sortedMagPoints)):
            self.y.append(self.sortedMagPoints[i][1])
            self.x.append(self.sortedMagPoints[i][0])
              
    def medianRemoval(self):
        
        tempVals = []
        tempY = []
        profile = 1
        valueList = []
        position=[]
        position.append(0)
        temp = 1
        x = 0    
        for i in range(1, len(self.sortedMagPoints)):
            if self.profile[i] == temp:
                x += numpy.sqrt(((self.sortedMagPoints[i][0] - self.sortedMagPoints[i-1][0])**2) + ((self.sortedMagPoints[i][2] - self.sortedMagPoints[i-1][2])**2))
                position.append(x)
            else:
                temp += 1
                x = 0
                position.append(x)     
        for i in range(len(self.sortedMagPoints)):          
            if i == len(self.sortedMagPoints) - 1: # Median correction for the last profile            
                newValPoly, a1, p1 = [], [], []   
                tempVals.append(self.sortedMagPoints[i][2])    
                tempY.append(position[i])
                if self.isMedianRemoval:
                    filtTempVals = []
                    if self.isPercentile:
                        minThresh = numpy.percentile(tempVals, self.percThreshold)
                        maxThresh = numpy.percentile(tempVals, (100 - self.percThreshold))
                    for val in tempVals:
                        if self.isPercentile:
                            if val < maxThresh and val > minThresh:
                                filtTempVals.append(val)
                        else: 
                            filtTempVals.append(val)
                    medianProf = numpy.median(filtTempVals)                
                else:
                    filtTempVals = []
                    ytemp2 = []
                    if self.isTrendPercentile:
                            minThresh = numpy.percentile(tempVals, self.trendPercThreshold)
                            maxThresh = numpy.percentile(tempVals, (100 - self.trendPercThreshold))                    
                    for val in range(len(tempVals)):
                            if self.isTrendPercentile:
                                if tempVals[val] < maxThresh and tempVals[val] > minThresh:
                                    filtTempVals.append(tempVals[val])
                                    ytemp2.append(tempY[val])
                            else:
                                filtTempVals.append(tempVals[val])
                                ytemp2.append(tempY[val])                        
                    a1 = numpy.polyfit(ytemp2, filtTempVals, self.trendPolyOrder)
                    p1 = numpy.poly1d(a1)    
                    newValPoly = [p1(val) for val in tempY]                             
                for j in range(0, len(tempVals)):
                    if self.isMedianRemoval:
                        val = tempVals[j]- medianProf 
                    else:
                        val = tempVals[j] - newValPoly[j] 
                    valueList.append(val)
                for val in valueList:
                    self.medianRemValues.append(float(val))  
                valueList = []             
                tempVals=[]
                tempY=[]  
            elif self.profile[i] == profile: # creation of a temporary vector for the correction
                tempVals.append(self.sortedMagPoints[i][2])    
                tempY.append(position[i])                
            else: # the beginning of a new profile, stop append and computation of the median or the polynomial                
                profile += 1
                newValPoly, a1, p1 = [], [], []                
                if self.isMedianRemoval:
                    filtTempVals = []
                    if self.isPercentile:
                        minThresh = numpy.percentile(tempVals, self.percThreshold)
                        maxThresh = numpy.percentile(tempVals, (100 - self.percThreshold))
                    for val in tempVals:
                        if self.isPercentile:
                            if val < maxThresh and val > minThresh:
                                filtTempVals.append(val)
                        else: 
                            filtTempVals.append(val)
                    medianProf = numpy.median(filtTempVals)                
                else:
                    filtTempVals = []
                    ytemp2 = []
                    if self.isTrendPercentile:
                            minThresh = numpy.percentile(tempVals, self.trendPercThreshold)
                            maxThresh = numpy.percentile(tempVals, (100 - self.trendPercThreshold))                    
                    for val in range(len(tempVals)):
                            if self.isTrendPercentile:
                                if tempVals[val] < maxThresh and tempVals[val] > minThresh:
                                    filtTempVals.append(tempVals[val])
                                    ytemp2.append(tempY[val])
                            else:
                                filtTempVals.append(tempVals[val])
                                ytemp2.append(tempY[val])                        
                    a1 = numpy.polyfit(ytemp2, filtTempVals, self.trendPolyOrder)
                    p1 = numpy.poly1d(a1)    
                    newValPoly = [p1(val) for val in tempY]    
                val = 0                
                for j in range(len(tempVals)):
                    if self.isMedianRemoval:
                        value = tempVals[j] - medianProf 
                    else:
                        value = tempVals[j] - newValPoly[j] 
                    valueList.append(value)
                    value = 0
                for valeur in valueList:
                    self.medianRemValues.append(float(valeur))                
                tempVals, tempY, valueList = [], [], [] 
                tempVals.append(self.sortedMagPoints[i][2]) 
                tempY.append(position[i])

    def EM31RawDataParser(self):
        
        rawDataFile = QFile(self.rawDataFilename)
        if not(rawDataFile.exists()):
            return
        if rawDataFile.open(QFile.ReadOnly|QFile.Text):
            firstline = str(rawDataFile.readLine())
            while not(rawDataFile.atEnd()):
                line = str(rawDataFile.readLine())     
                data = line.rstrip('\n\r').split()
                self.EM31Points.append((float(data[0]), float(data[1]), float(data[2]), float(data[3]), str(data[4]))) # (x, y, cond, i, time)
        else:
            raise ParserError(self.rawDataFilename, QtGui.QApplication.translate(u"Engine",'Can not open file.'))      
       
  
    def ConductivityTransformation(self):
        
        frequency = 9800.0
        spacing = 3.66       
        EM31 = SignalEM(frequency, spacing, self.sensorHeight, self.coilConfig)            
        self.Qppm = [EM31.McNeillToPpm(a) for a in zip(*self.EM31Points)[2]]
        self.I = [a*1000 for a in zip(*self.EM31Points)[3]]
        self.cond = EM31.ppmToCondList(self.Qppm)
            
  
    def createEM31Shapefile(self):
       
        self.Qppm = [float("{0:.4f}".format(x)) for x in self.Qppm]
        self.I = [float("{0:.4f}".format(x)) for x in self.I]
        self.cond = [float("{0:.4f}".format(x)) for x in self.cond]
        fields = QgsFields()
        fields.append(QgsField('Sigma_EM31', QVariant.Double, 'double', 12, 4)) 
        fields.append(QgsField('Sigma_cor', QVariant.Double, 'double', 12, 4))
        fields.append(QgsField('Q', QVariant.Double, 'double', 12, 4))   
        fields.append(QgsField('I', QVariant.Double, 'double', 12, 4))
        fields.append(QgsField('Time', QVariant.String))  
        if self.isAddCoordFields:
            fields.append(QgsField('X', QVariant.Double))
            fields.append(QgsField('Y', QVariant.Double))            
        features = []                
        crsSrc = QgsCoordinateReferenceSystem(self.inputCrsCode)
        xform = QgsCoordinateTransform(crsSrc, self.crs)                                              
        for i in range(0, len(self.EM31Points)):
            feature = QgsFeature()
            qPoint = QgsPoint(self.EM31Points[i][0], self.EM31Points[i][1])
            xPoint = xform.transform(qPoint) #coordinate Transform
            feature.setGeometry(QgsGeometry.fromPoint(xPoint))
            if self.isAddCoordFields:            
                feature.setAttributes([self.EM31Points[i][2], 
                                       self.cond[i],
                                       self.Qppm[i], 
                                       self.I[i], 
                                       self.EM31Points[i][4], 
                                       xPoint[0],
                                       xPoint[1]]) 
            else:
                feature.setAttributes([self.EM31Points[i][2],
                                       self.cond[i], 
                                       self.Qppm[i], 
                                       self.I[i], 
                                       self.EM31Points[i][4]])             
            features.append(feature)
        Utilities.createShapefile(self.outputShapefile, fields, features, self.dataEncoding, self.crs)
    
   
    def createEM31DatExport(self):
            
        datFileName = self.outputShapefile.replace('.shp', '.dat')
        fileObj = open(datFileName, 'w')
        xform = QgsCoordinateTransform(QgsCoordinateReferenceSystem(self.inputCrsCode), self.crs) # TODO clean up
                    
        for i in range(0, len(self.EM31Points)):
            qPoint = QgsPoint(self.EM31Points[i][0], self.EM31Points[i][1])
            xPoint = xform.transform(qPoint)
            fileObj.write(str(xPoint[0]) + ', ' + str(xPoint[1]) + ', ' + str (self.EM31Points[i][2]) + ', ' + str(self.cond[i]) + ', ' +
                          str(self.Qppm[i]) + ', ' + str(self.I[i])+ ', ' + str(self.EM31Points[i][4]) + '\n')
        fileObj.close()



"""
Created on June 2018

@author: François-Xavier SIMON/Nariman HATMI
"""

class EngineGEM2(object):
    
    def __init__(self, rawDataFilename, dataEncoding, sensorHeight, gnssHourShift, gnssMinuteShift, gnssSecondsShift, coilConfig, methodIp, methodQ, outputShapefile, 
                 gnssXShift, gnssYShift, calculConductivite, calculSusceptibilite, calibrationFilename = None, gnssDataFilename = None, crsRefImp = None, crsRefExp = None, paramConductCorr = False, 
                 winfilterIp = False, winfilterQ = False, spacing = 1.66, buckingCoil = 1.035, layerNbr = 5, chiP = [], chiQ = [], rho = [], e = [], 
                 qOffset = [], iOffset = [], coeffQu = [], coeffPh = [], valCoeff = -1.0, altBas = 0.02, altHaut = 2.2, resistivityReference = 30.0, decimValue = None, 
                 winSizeQ = None, winSizeIp = None):
        
        self.rawDataFilename = rawDataFilename
        self.gnssDataFilename = gnssDataFilename
        self.dataEncoding = dataEncoding
        if crsRefImp:
            self.inputCrsCode = Utilities.crsRefDict[crsRefImp]
        else:
            self.inputCrsCode = 32631 #UTM31 WGS84
        if crsRefExp:
            self.outputCrsCode = Utilities.crsRefDict[crsRefExp]
        else:
            self.outputCrsCode = 2154 #RGF93 / Lambert-93
        self.crs = QgsCoordinateReferenceSystem(self.outputCrsCode)
        self.deviceHeight = sensorHeight
        self.coilConfig = coilConfig
        self.gnssHourShift = gnssHourShift
        self.gnssMinuteShift = gnssMinuteShift
        self.gnssSecondsShift = gnssSecondsShift    
        self.methodIp = methodIp
        self.methodQ = methodQ
        self.winSizeQ = winSizeQ
        self.winSizeIp = winSizeIp
        self.conductivityCorrection = paramConductCorr
        self.decimValue = decimValue
        self.outputShapefile = outputShapefile
        self.gnssXShift = gnssXShift
        self.gnssYShift = gnssYShift
        self.calculConductivite = calculConductivite
        self.calculSusceptibilite = calculSusceptibilite
        self.winfilterIp = winfilterIp
        self.winfilterQ = winfilterQ
        self.calibrationFilename = calibrationFilename
        self.spacing = spacing
        self.buckingCoil = buckingCoil
        self.layerNbr = layerNbr
        self.chiP = chiP
        self.chiQ = chiQ        
        if not self.chiP:
            for _ in range(0, layerNbr - 1):
                self.chiP.append(0.0)
                self.chiQ.append(0.0)
        self.rho = rho
        self.e = e
        self.gem2Points = []
        self.gnssPoints = []
        self.gem2Calib = []
        self.frequencyNumber = 0
        self.frequencyList = []
        self.cond = []
        self.susc = []
        self.x = []
        self.y = []
        self.gnss = (gnssDataFilename is '')
        if self.gnss:
            self.startColonne = 11
        else:
            self.startColonne = 9
        self.qOffset = qOffset 
        self.iOffset = iOffset 
        self.coeffQu = coeffQu
        self.coeffPh = coeffPh 
        self.valCoeff = valCoeff
        self.altBas = altBas
        self.altHaut = altHaut
        self.resistivityReference = resistivityReference        
     
        self.yLengthEmp400 = 20.0
        self.emp400Points=[]
        self.Emp400 = False
     
    def rawDataParser(self):
        
        rawDataFile = QFile(self.rawDataFilename)
        if not(rawDataFile.exists()):
            return
        if rawDataFile.open(QFile.ReadOnly|QFile.Text):
            # header (metadata)
            if not(rawDataFile.atEnd()):
                headerLine = rawDataFile.readLine()            
                rawDataFile.close()
                if ('GSSI' in headerLine):
                    self.Emp400DataParser()
                    self.Emp400=True
                else:
                    self.Gem2DataParser()  


    def Emp400DataParser(self, data = True):
        
        rawDataFile = QFile(self.rawDataFilename)
        temporaryPoints = []
        if not(rawDataFile.exists()):
            return
        if not rawDataFile.open(QFile.ReadOnly|QFile.Text):
            raise ParserError(self.rawDataFilename, QtGui.QApplication.translate(u"Engine",'Can not open file.'))  
        self.frequencyNumber = 3            
        for i in range(36): #36 header's length
            if not(rawDataFile.atEnd()):
                headerLine = rawDataFile.readLine()
                if ('Ymax' in headerLine):
                    info = str(headerLine).strip().split(',')
                    self.yLengthEmp400 = float(info[1])
                if ('Frequencies:' in headerLine):
                    info = str(headerLine).strip().split(',')
                    self.frequencyList = (float(info[1]), float(info[2]), float(info[3]))
#               headerLine = []            
        while not(rawDataFile.atEnd()):
            data = str((rawDataFile.readLine())).strip().split(',')
            line = []
            if not data:
                break
            for i in range(len(data)):
                try :
                    value = float(data[i])
                except:
                    value = data[i]
                line.append(value)                    
            temporaryPoints.append(line)
                
        # Caracteristique appareil et format EMP400
        self.startColonne = 9
        self.spacing = 1.21        
        #Calcul des positions en y le long de chaque profil
        init = 0
        stamp = temporaryPoints[0][1]
        ysize = 0
        increment = 1        
        for i in range(len(temporaryPoints)):
            if i == len(temporaryPoints) - 1:
                ysize += 1
                step = self.yLengthEmp400/(ysize - 1)
                for j in range(ysize):
                    yposition = init + (j*increment*step)
                    self.y.append(yposition)
            elif temporaryPoints[i][1] == stamp :
                ysize += 1
            elif temporaryPoints[i][1] != stamp:
                step = self.yLengthEmp400/(ysize - 1)
                for j in range(ysize):
                    yposition = init + (j*increment*step)
                    self.y.append(yposition)
                if (stamp*2)%2 == 0:
                    init = 0
                    increment = 1
                else:
                    init = self.yLengthEmp400
                    increment = -1
                stamp = stamp + 0.5
                ysize = 1                
        # Détermination des numéros de profils
        stamp = temporaryPoints[0][1]
        profile = 0        
        #Rearrangement des données pour correspondre au format GEM2Points
        for i in range(len(temporaryPoints)):
                freq1ip = -temporaryPoints[i][4]
                freq2ip = -temporaryPoints[i][7]
                freq3ip = -temporaryPoints[i][10]
                freq1qu = temporaryPoints[i][5]
                freq2qu = temporaryPoints[i][8]
                freq3qu = temporaryPoints[i][11]
                long_gps = temporaryPoints[i][15]
                lat_gps = temporaryPoints[i][16]
                alt_gps = temporaryPoints[i][17]
                stat_gps = 0.0
                time = str(temporaryPoints[i][3])
                hhmmss = time.strip().split(':')
                hour = int(hhmmss[0])
                minute = int(hhmmss[1])
                sec = float(hhmmss[2])
                timeMms = (hour*3600 + minute*60 + sec)*1000.0                
                if temporaryPoints[i][1] != stamp:
                    stamp = temporaryPoints[i][1]
                    profile += 1
                    self.emp400Points.append([profile, temporaryPoints[i][1], temporaryPoints[i][1], self.y[i], timeMms, timeMms,
                                         stat_gps, alt_gps, timeMms, freq1ip, freq1qu, freq2ip, freq2qu, freq3ip, freq3qu])
                else:
                    self.emp400Points.append([profile, temporaryPoints[i][1], temporaryPoints[i][1], self.y[i], timeMms, timeMms,
                                         stat_gps, alt_gps, timeMms, freq1ip, freq1qu, freq2ip, freq2qu, freq3ip, freq3qu])
                              
        self.gem2Points = self.emp400Points
        self.updateOffsetCoeff()
        
    def Gem2DataParser(self, datafile = True):
            
        if datafile:
            startCol = self.startColonne
            rawFile = QFile(self.rawDataFilename)
        else: #calibration
            rawFile = QFile(self.calibrationFilename)
            startCol = 9
        if not(rawFile.exists()):
            return
        if not rawFile.open(QFile.ReadOnly|QFile.Text):
            raise ParserError(self.rawFilename, QtGui.QApplication.translate(u"Engine",'Can not open file.'))     
        else:
            if not rawFile.atEnd():
                data = str((rawFile.readLine())).strip().split(',')
                self.frequencyNumber = (len(data) - startCol - 1)/2 # detection du nombre de frequence utilise
                for i in range(self.frequencyNumber): # lecture des frequences et des enregistrements
                    frequencyValue = float(data[startCol + 1 + (i*2)][2:-2]) 
                    self.frequencyList.append(frequencyValue)
            while not(rawFile.atEnd()):
                data = str((rawFile.readLine())).strip().split(',')
                line = []
                if not data:
                    break
                for i in range(len(data)):
                    line.append(float(data[i]))
                if datafile:
                    self.gem2Points.append(line)
                else:
                    self.gem2Calib.append(line)                             
        self.updateOffsetCoeff()

    def gpsRawDataParser(self):
        
        gnssDataFile = QFile(self.gnssDataFilename)
        if not(gnssDataFile.exists()):
            return
        if not gnssDataFile.open(QFile.ReadOnly|QFile.Text):
            raise ParserError(self.gnssDataFilename, QtGui.QApplication.translate(u"Engine",'Can not open file.'))
        else:
            while not(gnssDataFile.atEnd()):
                data = str((gnssDataFile.readLine())).strip().split(',')            
                if not data:
                    break
                line = []        
#                try:
#                    line.append(float(data[0]))
#                except:
#                    line.append((data[0]))
                line.append(float(data[0])) # x
                line.append(float(data[1])) # y
                line.append((data[2])) # z
                time = str(data[3])
                hhmmss = time.strip().split(':')
                hour = int(hhmmss[0])
                minute = int(hhmmss[1])
                sec = int(hhmmss[2])
                timeMms = (hour*3600 + minute*60 + sec)*1000.0            
                line.append(timeMms)            
                self.gnssPoints.append(line)
    
    def updateOffsetCoeff(self):
        
        if not self.qOffset:
            for i in range(0, self.frequencyNumber):
                self.qOffset.append(0)
                self.iOffset.append(0)
                self.coeffQu.append(self.valCoeff)
                self.coeffPh.append(self.valCoeff)
                
    def correcntionXYZPosition(self):
    
        tetaList = []
        xNew, yNew = [], []
        for i in range(len(self.x) - 1): #Correction le long des profils
            if self.x[i + 1] == self.x[i]:
                x = self.x[i + 1] + 0.0001     
            else:
                x = self.x[i + 1]            
            if (x - self.x[i]) > 0:
                teta = math.atan((self.y[i + 1] - self.y[i])/(x - self.x[i]))
            else:
                teta = math.atan((self.y[i + 1] - self.y[i])/(x - self.x[i])) + numpy.pi
            tetaList.append(teta)        
        xNew.append(self.x[0])
        yNew.append(self.y[0])        
        for i in range(1, len(self.x), 1):
            if tetaList[i - 1] == numpy.pi/2.0 or tetaList[i - 1] == 3.0*numpy.pi/2.0:
                xNewVal = self.x[i] - self.gnssYShift*numpy.cos(tetaList[i - 1])
                yNewVal = self.y[i] + self.gnssYShift*numpy.sin(tetaList[i - 1])
            else:
                xNewVal = self.x[i] - self.gnssYShift*numpy.cos(tetaList[i - 1])
                yNewVal = self.y[i] - self.gnssYShift*numpy.sin(tetaList[i - 1])
            xNew.append(xNewVal)
            yNew.append(yNewVal)            
        self.x = xNew
        self.y = yNew
        xNew, yNew, tetaList = [], [], []      
        xNew.append(self.x[0])
        yNew.append(self.y[0])        
        for i in range(len(self.x) - 1): #Correction perpendiculaire au profil
            if self.x[i + 1] == self.x[i]:
                x = self.x[i + 1] + 0.0001     
            else:
                x = self.x[i + 1]            
            if (x - self.x[i]) > 0:
                teta = math.atan((self.y[i + 1] - self.y[i])/(x - self.x[i]))
            else:
                teta = math.atan((self.y[i + 1] - self.y[i])/(x - self.x[i])) + numpy.pi
            tetaList.append(teta)    
        for i in range(1, len(self.x), 1):
            if tetaList[i - 1] == numpy.pi/2.0 or tetaList[i - 1] == 3.0*numpy.pi/2.0:
                xNewVal = self.x[i] + self.gnssXShift*numpy.sin(tetaList[i - 1])
                yNewVal = self.y[i] + self.gnssXShift*numpy.cos(tetaList[i - 1])
            else:
                xNewVal = self.x[i] - self.gnssXShift*numpy.sin(tetaList[i - 1])
                yNewVal = self.y[i] + self.gnssXShift*numpy.cos(tetaList[i - 1])
            xNew.append(xNewVal)
            yNew.append(yNewVal) 
        self.x = xNew
        self.y = yNew
        
    def correctionXYGEM2(self):
        
        self.x = [self.gem2Points[i][2] for i in range(len(self.gem2Points))]
        self.y = [self.gem2Points[i][3] for i in range(len(self.gem2Points))]
        self.correcntionXYZPosition()
        
    def slidingWindow(self):
        
        gem2PointsCor = []
        winSizemax = max(self.winSizeIp,self.winSizeQ)        
        for i in range(winSizemax/2, len(self.gem2Points)-winSizemax/2):
            liste = []
            for j in range(self.startColonne):
                val = self.gem2Points[i][j]
                liste.append(val)    
            for j in range(self.startColonne, (self.startColonne + (self.frequencyNumber*2)),2):
                data = []
                if self.winfilterIp:
                    for k in range(i - (self.winSizeIp/2), i + (self.winSizeIp/2)):
                        data.append(self.gem2Points[k][j])
                        if self.methodIp == FilterEnum.MEDIAN:
                                val = numpy.median(data)
                        if self.methodIp == FilterEnum.MEAN:
                                val=numpy.mean(data)
                else:
                    val = self.gem2Points[i][j]
                liste.append(val)
                data = []
                if self.winfilterQ:
                    for k in range(i - (self.winSizeQ/2), i + (self.winSizeQ/2)):
                        data.append(self.gem2Points[k][j+1])
                        if self.methodQ == FilterEnum.MEDIAN:
                                val = numpy.median(data)
                        if self.methodQ == FilterEnum.MEAN:
                                val=numpy.mean(data)   
                else:
                    val = self.gem2Points[i][j+1]
                liste.append(val)
            gem2PointsCor.append(liste)   
        self.gem2Points = list(gem2PointsCor)      

    def gem2Decim(self):
        
        gem2PointsCor = []
        for i in range(self.decimValue/2, len(self.gem2Points)-self.decimValue/2, self.decimValue):
            liste = []
            for j in range(self.startColonne):
                val = self.gem2Points[i][j]
                liste.append(val)       
            for j in range(self.startColonne, (self.startColonne + (self.frequencyNumber*2) + 1)):
                data = []
                for k in range(i - (self.decimValue/2), i + (self.decimValue/2)):
                    data.append(self.gem2Points[k][j])
                val = numpy.median(data)
                liste.append(val)
            gem2PointsCor.append(liste)    
        self.gem2Points = list(gem2PointsCor)

    def gem2Mediane(self, quad):
                 
        gem2PointsMedian = list(self.gem2Points)
        if quad:
            startCol = self.startColonne + 1
        else:
            startCol = self.startColonne
        for j in range(startCol, self.startColonne + (self.frequencyNumber*2), 2):
            profil = 0
            newCol = [] 
            valProfil = []
            for i in range(len(self.gem2Points)):
                if i == (len(self.gem2Points) - 1):
                    valProfil.append(self.gem2Points[i][j])
                    cor = numpy.median(valProfil)
                    newVal = [k - cor for k in valProfil]
                    newCol.extend(newVal)
                elif self.gem2Points[i][0] == profil:
                    valProfil.append(self.gem2Points[i][j])
                else:
                    cor = numpy.median(valProfil)
                    newVal = [k - cor for k in valProfil]
                    newCol.extend(newVal)
                    profil += 1
                    valProfil = []
                    newVal = []
                    valProfil.append(self.gem2Points[i][j])
            for i in range(len(self.gem2Points)):
                gem2PointsMedian[i][j] = newCol[i]
        self.gem2Points = gem2PointsMedian
            
    def gem2Conductivity(self): 
        
        qResponse = []
        qppmFreq = []
        qList = []
        self.cond = [[0]*self.frequencyNumber for _ in range(len(self.gem2Points))]     
        gem2 = SignalEM(self.frequencyList[0], self.spacing, self.deviceHeight, self.coilConfig, self.buckingCoil)
        for i in range(len(self.gem2Points)):
            qList = []
            for j in range(self.startColonne + 1, (self.startColonne + 1 + (self.frequencyNumber*2)), 2):
                qList.append(self.gem2Points[i][j])
            qResponse.append(qList)             
        for j in range(self.frequencyNumber):
            conductivity = []
            gem2.frequency = self.frequencyList[j]
            qppmFreq = [(self.coeffQu[j]*a) - self.qOffset[j] for a in zip(*qResponse)[j]]
            if self.Emp400:
                conductivity = gem2.ppmToCondList(qppmFreq)
            else:
                conductivity = gem2.ppmBuckToCondList(qppmFreq)   
            for i in range(len(conductivity)):
                self.cond[i][j] = conductivity[i]    
                
    def gem2Susceptibility(self): 
        
        iResponse = []
        ippmFreq = []
        iList = []
        self.susc = [[0]*self.frequencyNumber for _ in range(len(self.gem2Points))]
        gem2 = SignalEM(self.frequencyList[0], self.spacing, self.deviceHeight, self.coilConfig, self.buckingCoil)        
        for i in range(len(self.gem2Points)):
            iList = []
            for j in range(self.startColonne, (self.startColonne + ((self.frequencyNumber)*2)), 2):
                iList.append(self.gem2Points[i][j])
            iResponse.append(iList)                    
        for j in range(self.frequencyNumber):
            susceptibility = []
            gem2.frequency=self.frequencyList[j]                                
            ippmFreq = [(self.coeffPh[j]*a) - self.iOffset[j] for a in zip(*iResponse)[j]]
#           ippmFreq = [(self.coeffPh[j]*a) - 200 for a in zip(*iResponse)[j]]
            if self.conductivityCorrection:
                for i in range(len(ippmFreq)):
                    if self.cond[i][j]*1E-3 < 1E-4:
                        conductivite_corrigee = 1E-4
                        if self.Emp400:
                            self.susc[i][j] = gem2.ppmToSusc(ippmFreq[i], (1.0/(conductivite_corrigee)))
                        else:
                            self.susc[i][j] = gem2.ppmBuckToSusc(ippmFreq[i], (1.0/(conductivite_corrigee))) 
                    else:
                        if self.Emp400:
                            self.susc[i][j] = gem2.ppmToSusc(ippmFreq[i], (1.0/(self.cond[i][j]*1E-3))) 
                        else: 
                            self.susc[i][j] = gem2.ppmBuckToSusc(ippmFreq[i], (1.0/(conductivite_corrigee)))
            else:
                if self.Emp400:
                    susceptibility = gem2.ppmToSuscList(ippmFreq, self.resistivityReference)
                else: 
                    susceptibility = gem2.ppmBuckToSuscList(ippmFreq, self.resistivityReference)
                for i in range(len(susceptibility)):
                    self.susc[i][j] = susceptibility[i]
               
    def createGEM2Shapefile(self):
        
        gem2Pointsformat = list(self.gem2Points)
        for i in range(len(self.gem2Points)):
            for j in range(len(self.gem2Points[0])):
                gem2Pointsformat[i][j]=float("{0:.4f}".format(self.gem2Points[i][j]))
        self.gem2Points = gem2Pointsformat
        suscFormat = list(self.susc)
        for i in range(len(self.susc)):
            for j in range(len(self.susc[0])):
                suscFormat[i][j] = float("{0:.4f}".format(self.susc[i][j]))
        self.susc = suscFormat
        condFormat = list(self.cond)
        for i in range(len(self.cond)):
            for j in range(len(self.cond[0])):
                condFormat[i][j] = float("{0:.4f}".format((self.cond[i][j])))
        self.cond = condFormat
        self.x = [float("{0:.4f}".format(x)) for x in self.x]
        self.y = [float("{0:.4f}".format(y)) for y in self.y]
        fields = QgsFields()
        fields.append(QgsField("X", QVariant.Double, 'double', 10, 2))    
        fields.append(QgsField("Y", QVariant.Double, 'double', 10, 2))
        for i in range(self.frequencyNumber):
            fields.append(QgsField("I %dHz"%self.frequencyList[i], QVariant.Double, 'double', 10, 2))
            fields.append(QgsField("Q %dHz"%self.frequencyList[i], QVariant.Double, 'double', 10, 2))
            if self.calculConductivite:
                fields.append(QgsField("Cond %d"%self.frequencyList[i], QVariant.Double, 'double', 10, 2))
            if self.calculSusceptibilite:
                fields.append(QgsField("X %d"%self.frequencyList[i], QVariant.Double, 'double', 10, 2))
        fields.append(QgsField("Profile", QVariant.Int))    
        if self.gnss:
            fields.append(QgsField("Time", QVariant.Double, 'double', 10, 2))
            fields.append(QgsField("GPS_stat", QVariant.Double, 'double', 10, 2))
            fields.append(QgsField("Altitude", QVariant.Double, 'double', 10, 2))    
        shape = []
        liste = []
        for i in range(len(self.gem2Points)):
            liste.append(self.x[i])
            liste.append(self.y[i])
            for j in range(self.frequencyNumber):
                liste.append(self.gem2Points[i][j*2 + self.startColonne])
                liste.append(self.gem2Points[i][j*2 + self.startColonne + 1])
                if self.calculConductivite:
                    liste.append(self.cond[i][j])
                if self.calculSusceptibilite:
                    liste.append(self.susc[i][j])
            liste.append(self.gem2Points[i][0])
            if self.gnss:            
                liste.append(self.gem2Points[i][8])
                liste.append(self.gem2Points[i][6])
                liste.append(self.gem2Points[i][7])
            shape.append(liste)
            liste = []
        features = []
        crsSrc = QgsCoordinateReferenceSystem(self.inputCrsCode)
        xform = QgsCoordinateTransform(crsSrc, self.crs)    
        for i in range(len(self.gem2Points)):
            fet = QgsFeature()
            qPoint = QgsPoint(self.x[i], self.y[i])
            xPoint = xform.transform(qPoint) #coordinate Transform
            fet.setGeometry(QgsGeometry.fromPoint(xPoint))
            fet.setAttributes(shape[i])
            features.append(fet)        
        Utilities.createShapefile(self.outputShapefile, fields, features, self.dataEncoding, self.crs)
          
    def offsetGEM2(self):
        
        self.chiP = [0.0, 0.0, 0.0, 0.0, 0.0]
        self.chiQ = [0.0, 0.0, 0.0, 0.0, 0.0] 
        gem2 = SignalEM(self.frequencyList[0], self.spacing, self.deviceHeight, self.coilConfig, self.buckingCoil, rho = self.rho, 
                        chiP = self.chiP, chiQ = self.chiQ, e = self.e, ncou = self.layerNbr) 
        theoriqueBas, theoriqueHaut = [], []
        fieldBas,fieldHaut = [], []
        self.startColonne = 9
        for i in range(self.frequencyNumber):
            gem2.frequency = self.frequencyList[i]
            gem2.height = self.altBas
            if self.Emp400:
                theoriqueBas.append(gem2.FreqEM())
            else: 
                theoriqueBas.append(gem2.FreqEMBuck())
            gem2.height = self.altHaut
            if self.Emp400:
                theoriqueHaut.append(gem2.FreqEM())
            else: 
                theoriqueHaut.append(gem2.FreqEMBuck())
        #compilation des mesures haut/bas
        compilBas, compilHaut = [], []
        pointBas, pointHaut = [], []    
        for i in range(len(self.gem2Calib)):
            if (self.gem2Calib[i][0]%2 == 0):
                for j in range(self.startColonne, self.startColonne + ((self.frequencyNumber)*2)):
                    pointBas.append(self.gem2Calib[i][j])
                compilBas.append(pointBas)
                pointBas = []
            else:
                for j in range(self.startColonne, self.startColonne + ((self.frequencyNumber)*2)):
                    pointHaut.append(self.gem2Calib[i][j])
                compilHaut.append(pointHaut)
                pointHaut = []            
        for j in range(len(compilHaut[0])):
            listeBas, listeHaut= [], []
            for i in range(len(compilHaut)):
                listeHaut.append(compilHaut[i][j])
            for i in range(len(compilBas)):
                listeBas.append(compilBas[i][j])
            medianeBas = numpy.median(listeBas)
            medianeHaut = numpy.median(listeHaut)
            fieldHaut.append(medianeHaut)
            fieldBas.append(medianeBas)
        # Definition des offsets en phase et en quadrature
        self.qOffset, self.iOffset, self.coeffQu = [], [], []
        for i in range(self.frequencyNumber):       
            self.iOffset.append(fieldHaut[i*2] - theoriqueHaut[i].real)
            difftheo = theoriqueBas[i].imag - theoriqueHaut[i].imag
            diffexp = fieldBas[i*2 + 1] - fieldHaut[i*2 + 1]
            self.coeffQu.append(difftheo/diffexp)
            self.qOffset.append(fieldHaut[i*2 + 1]*(difftheo/diffexp) - theoriqueHaut[i].imag)
        
    def gem2GPSFusion(self):
    
        timeCorList = []
        self.gnssHourShift
        self.gnssMinuteShift
        self.gnssSecondsShift
        #Correction du dÃ©calage entre instrument et GPS
        for i in range(len(self.gnssPoints)):
            timeCorrection = (self.gnssPoints[i][3] + (self.gnssHourShift*3600.0 + self.gnssMinuteShift*60.0 + self.gnssSecondsShift)*1000.0)
            timeCorList.append(timeCorrection)
        #creation des correspondances en temps entre GPS et fichier EM 
        xGPS, yGPS, gpsTime = [], [], []
        for i in range(len(self.gnssPoints) - 1):
            pastemps = (timeCorList[i + 1] - timeCorList[i])/100
            for j in range (100):
                x = self.gnssPoints[i][0] + ((self.gnssPoints[i + 1][0] - self.gnssPoints[i][0])/100.0)*j
                y = self.gnssPoints[i][1] + ((self.gnssPoints[i + 1][1] - self.gnssPoints[i][1])/100.0)*j
                newTime = timeCorList[i] + pastemps*j
                yGPS.append(y)
                xGPS.append(x)
                gpsTime.append(newTime)
        #Arrondi des marqueurs en temps pour realiser la correspondance
        gpsTime = [round(x/10.0) for x in gpsTime]
        tempsEM = [round(x/10.0)for x in zip(*self.gem2Points)[6]]
        #creation de deux tableaux avec une colonne commune pour le marqueur
        gpsData = []
        for i in range(len(gpsTime)):
            gpsData.append([gpsTime[i], [xGPS[i], yGPS[i]]])
        dataArray = []    
        for i in range(len(self.gem2Points)):
            data = []
            for j in range(len(self.gem2Points[0])):
                data.append(self.gem2Points[i][j])
            dataArray.append([tempsEM[i], data])
        #association des deux vecteurs et reecriture de EMPoints
        d = {}
        for k, v in gpsData + dataArray:
            d.setdefault(k, []).append(v)
        newFile = []
        for k, v in d.items():
            data = []
            if len(v)==2:
                try:
                    for i in range(len(self.gem2Points[0])):
                        data.append(v[1][i])
                    data[2] = v[0][0]
                    data[3] = v[0][1]
                    newFile.append(data)
                except: 
                    continue
        self.gem2Points = newFile
        