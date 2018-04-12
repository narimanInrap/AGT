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
from ..toolbox.AGTUtilities import Utilities
from ..toolbox.AGTExceptions import *

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
        self.Cond = []
        self.EM31Points = []   
        
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
                self.sortedMagPoints.append((float(data[1]), float(data[0]), float(data[2]))) # (x, y, value)
        else:
            raise ParserError(self.rawDataFilename, QtGui.QApplication.translate(u"Engine",'Can not open file.'))
    
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
                self.createShapefile(fileName, fields, features)
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
                self.createShapefile(fileName, fields, features)
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
        self.createShapefile(fileName, fields, features)
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
            
            

    def createShapefile(self, fileName, fields, features):
    
        check = QFile(fileName)
        if check.exists():
            if not QgsVectorFileWriter.deleteShapeFile(fileName):
                raise FileDeletionError(fileName)  
        writer = QgsVectorFileWriter(fileName, self.dataEncoding,
                                     fields, QGis.WKBPoint, self.crs)
        #if writer.hasError() != QgsVectorFileWriter.NoError:
        #   print "Error when creating shapefile: ",  w.errorMessage() lever une exception        
        featCounter = 0       
        for feature in features:
            writer.addFeature(feature)
            featCounter += 1
        if featCounter == 0:
            del writer    
            if not QgsVectorFileWriter.deleteShapeFile(fileName):
                msg = QtGui.QApplication.translate(u"Engine",u'No feature was created. The {} shapefile was deleted.\n').format(fileName)
                raise FileDeletionError(msg + fileName)
            raise NoFeatureCreatedError(fileName)          
        del writer


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
        self.createShapefile(self.outputShapefile, fields, features)
        
    def createMagGridRelCoordShapefile(self):

        fields = QgsFields()
        fields.append(QgsField('value', QVariant.Double, 'double', 12, 4))   
        fields.append(QgsField('val_process', QVariant.Double, 'double', 12, 4))
        fields.append(QgsField('profile', QVariant.Int))        
        if self.isAddCoordFields:
            fields.append(QgsField('X', QVariant.Double))
            fields.append(QgsField('Y', QVariant.Double))
        features = []                                    
        for i in range(0, len(self.sortedMagPoints)):
            feature = QgsFeature()
            qPoint = QgsPoint(self.sortedMagPoints[i][0], self.sortedMagPoints[i][1])           
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
        self.createShapefile(self.outputShapefile, fields, features)
        
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
        for x in zip(*self.sortedMagPoints)[0]: # profile correction
            if x == n:
                self.profile.append(newProfile)
            else :
                newProfile += 1
                n = x
                self.profile.append(newProfile)                
                        
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
                    value=0
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
        self.Cond = EM31.ppmToCondList(self.Qppm)
            
  
    def createEM31Shapefile(self):
       
        self.Qppm = [float("{0:.4f}".format(x)) for x in self.Qppm]
        self.I = [float("{0:.4f}".format(x)) for x in self.I]
        self.Cond = [float("{0:.4f}".format(x)) for x in self.Cond]
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
                                       self.Cond[i],
                                       self.Qppm[i], 
                                       self.I[i], 
                                       self.EM31Points[i][4], 
                                       xPoint[0],
                                       xPoint[1]]) 
            else:
                feature.setAttributes([self.EM31Points[i][2],
                                       self.Cond[i], 
                                       self.Qppm[i], 
                                       self.I[i], 
                                       self.EM31Points[i][4]])             
            features.append(feature)
        self.createShapefile(self.outputShapefile, fields, features)
    
   
    def createEM31DatExport(self):
            
        datFileName = self.outputShapefile.replace('.shp', '.dat')
        fileObj = open(datFileName, 'w')
        xform = QgsCoordinateTransform(QgsCoordinateReferenceSystem(self.inputCrsCode), self.crs) # TODO clean up
                    
        for i in range(0, len(self.EM31Points)):
            qPoint = QgsPoint(self.EM31Points[i][0], self.EM31Points[i][1])
            xPoint = xform.transform(qPoint)
            fileObj.write(str(xPoint[0]) + ', ' + str(xPoint[1]) + ', ' + str (self.EM31Points[i][2]) + ', ' + str(self.Cond[i]) + ', ' +
                          str(self.Qppm[i]) + ', ' + str(self.I[i])+ ', ' + str(self.EM31Points[i][4]) + '\n')
        fileObj.close()


"""
Created on Thu Sep 15 17:56:09 2016

@author: François-Xavier SIMON
"""

class SignalEM():
    
    def __init__(self, frequency = 9800, spacing = 3.66, height = 0.3, config = CoilConfigEnum.VCP, buckingcoil = 1.035):
        
        #Caractéristique de l'appareil de mesure qui sert de base à la modélisation
        self.frequency = frequency
        self.spacing = spacing
        self.height = height
        self.config = config
        self.buckingcoil = buckingcoil        
        #Fonction calculé lors de la simulation mais qui se retrouve 'hérité' dans les fonctions utilisées
        self.P = complex(0,0)
        self.gam2 = complex(0,0)
        self.A = complex(0,0)        
        #Caractéristique du terrain utilisé pour faire la simulation, appellé en paramètre des fonctions
        self.ncou = 2
        self.e = []
        self.chip = []
        self.chiq = []   
        self.rau = []
        self.eps = []
        
        
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
      
        fun2 = 0    
        if(g < 1E-20):
            g = 0.0        
        if(g*self.A > 30):
            return fun2      
        al = complex(g/self.P, 0)         
        U = (self.gam2 + al*al)**0.5
        rk = -U/self.susc 
        if(self.ncou >= 2):
            for i in range(self.ncou - 2, -1, -1):
                susci = complex(1 + self.chip[i], -self.chiq[i])
                gam2i = complex(0, numpy.pi*numpy.pi*self.frequency*0.8E-6/self.rau[i])*susci
                U = (gam2i + al**2)**0.5
                y = U/susci
                ck = self.CTH(U*complex(self.e[i], 0))
                rk = y*(rk - y*ck)/(y - rk*ck)
        fun2 = (al + rk)/(al - rk)*complex(g/numpy.exp(g*self.A), 0)
        return fun2
    
    def fun0(self, g):
        
        fun0 = self.fun2(g)*complex(g, 0)
        return fun0
    
    def fun00(self, g):#Fonction utilitaire pour la simulation
        
        fun00 = self.funv(g)*complex(g*g, 0)
        return fun00    
 
    def funv(self, g):#Fonction utilitaire pour la simulation
        
        funv = 0
        if(g < 0.1E-20):
            g=0
        if(g/self.P*self.A > 30):
            return funv
        al = complex(g/self.P, 0)
        U0 = (self.gam0 + al*al)**0.5
        if ((U0.real)*self.A*2 > 30):
            return funv
        CD = numpy.exp(U0*complex(2*self.A, 0))
        U = (self.gam2 + al*al)**0.5                   
        rk = -U/self.susc
        if(self.ncou >= 2):
                for i in range(self.ncou-2, -1, -1):                    
#                    gam0i,s1i,susci,gam2i=0,0,0,0
                    gam0i = complex(-self.frequency*self.frequency*(0.4E-15)*numpy.pi*numpy.pi/9.0, 0)
                    s1i = complex(self.eps[i], -0.18E+11*(1.0/self.rau[i])/self.frequency)
                    susci = complex(1 + self.chip[i], -self.chiq[i])
                    gam2i = s1i*gam0i*susci                                     
                    U = (gam2i + al**2)**0.5
                    y = U/susci
                    ck = self.CTH(U*complex(self.e[i], 0))
                    rk = y*(rk-y*ck)/(y-rk*ck)
        funv = al/U0*(U0+rk)/(U0-rk)/CD         
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

    def FreqEM(self, ncou, e, rau, chip, chiq): #Simulation of EM response based on full solution 
        
        self.ncou = ncou
        self.e = e
        self.chip = chip
        self.chiq = chiq
        self.rau = rau        
        self.P = (rau[ncou - 1]/self.frequency/numpy.pi/numpy.pi/0.4E-6)**0.5
        self.susc = complex(1 + chip[ncou - 1], -chiq[ncou - 1])
        self.gam2 = complex(0, numpy.pi*numpy.pi*self.frequency*0.8E-6/rau[ncou - 1])*self.susc   
        self.A = self.height*2/self.P       
        if self.config == CoilConfigEnum.HCP:
            B = self.spacing/self.P
            CB = complex(B, 0)
            T0 = self.HANKSGC(0, B, self.fun0, 1)
            QT = CB*CB*CB*T0*1000000       
        if self.config == CoilConfigEnum.VCP:
            B = self.spacing/self.P
            CB = complex(B, 0)
            T2 = self.HANKSGC(1, B, self.fun2, 1)
            QT = CB*CB*T2*1000000        
        if self.config == CoilConfigEnum.PERP:
            B = self.spacing/self.P
            CB = complex(B,0)
            T0 = self.HANKSGC(1,B,self.fun0,1)
            QT = CB*CB*CB*T0*1000000        
        if self.config == CoilConfigEnum.SH3:
            B = self.spacing/self.P
            CB = complex(B,0)
            T0 = CB*self.HANKSGC(0, B, self.fun0, 0) - self.HANKSGC(1, B, self.fun2, 0)/3
            QT = CB*CB*T0*1000000   
        return QT

    def McNeillToPpm(self, sigma):# transform a value of sigma (mS/m) in ppm for HCP et VCP
        
        omega = 2*numpy.pi*self.frequency
        mu0 = numpy.pi*4E-7
        PPM = -((omega*mu0*(sigma*1E-3)*(self.spacing)*(self.spacing))/4)*1E6        
        return PPM
        
    def ppmToMcNeill(self,value):#transform ppm in conductivity with McNeill formula for HCP et VCP
        
        omega = 2*numpy.pi*self.frequency
        mu0 = numpy.pi*4E-7        
        McNeill = -(4*(value*1E-6)/(omega*mu0*self.spacing*self.spacing))*1000
        return McNeill
    
    def ppmToCond(self,value):#transform ppm in conductivity using full solution 
        
        self.ncou = 1
        self.e = []
        SIGMA = range(1, 100, 1)
        degre = 3
        VAL = [1/(a*1E-3) for a in SIGMA]
        Mesqu = []        
        for res in VAL:
            self.rau = [res]
            self.chip = [0.0]
            self.chiq = [0.0]
            Mesqu.append(self.FreqEM(self.ncou, self.e, self.rau, self.chip, self.chiq).imag)                
        a1 = numpy.polyfit(Mesqu, SIGMA, degre)
        p1 = numpy.poly1d(a1)
        cond = p1(value)        
        return cond
        
    def ppmToCondList(self,vector):#transform ppm in conductivity using full solution 
        
        self.ncou = 1
        self.e = []
        SIGMA = range(1, 100, 1)
        degre = 3
        VAL = [1/(a*1E-3) for a in SIGMA]
        Mesqu = []        
        for res in VAL:
            self.rau = [res]
            self.chip = [0.0]
            self.chiq = [0.0]
            Mesqu.append(self.FreqEM(self.ncou, self.e, self.rau, self.chip, self.chiq).imag)                
        a1 = numpy.polyfit(Mesqu, SIGMA, degre)
        p1 = numpy.poly1d(a1)
        vector = [p1(a) for a in vector]
        return vector