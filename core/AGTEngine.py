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
from __future__ import unicode_literals

#debug
import sys
sys.path.append(unicode('C:\Program Files\eclipse\plugins\org.python.pydev_3.4.1.201403181715\pysrc'))
from pydevd import *
#debug


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

from ..toolbox.AGTUtilities import Utilities
from ..toolbox.AGTExceptions import *

class Engine(object):
    
    filteredPointNum = []   
    def __init__(self, rawDataFilename, dataEncoding, datOutput, crsRef = None, projectName = None, medianPercent = None, kernelSize = None, filter = None, 
                 addCoordFields = None, decimation = None, decimValue = None, medRemove = None, percentile = None, percThreshold = None,
                 trendRemove = None, trendPolyOrder = None, statPtRem = None, statPtThresh = None, gpsProbe = None, outputShapefile = None):
        self.rawDataFilename = rawDataFilename
        self.dataEncoding = dataEncoding
        self.gridNames = []        
        self.OriginX = []
        self.OriginY = []
        self.rawData = []
        self.basicOutputFilename = projectName
        if crsRef:
            self.outputCrsCode = Utilities.crsRefDict[crsRef]
        else:
            self.outputCrsCode = 2154 #RGF93 / Lambert-93
        self.inputCrsCode = 0
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
        self.isDecimation = decimation
        self.decimationVal = decimValue
        self.isMedianRemoval = medRemove
        self.isPercentile = percentile
        self.percThreshold = percThreshold
        self.isTrendRemoval = trendRemove
        self.trendPolyOrder = trendPolyOrder
        self.isStationPtRem = statPtRem
        if statPtThresh:
            self.stationPtThreshold = float(statPtThresh)
        self.gpsProbe = gpsProbe
        self.outputShapefile = outputShapefile
        # data
        self.magPoints = []      
        # profile
        self.correctedX = []
        self.profile = []
        #self.medianRemoval
        self.medianRemValues = []              
        
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
        fields.append(QgsField("rel_x", QVariant.Int))
        fields.append(QgsField("rel_y", QVariant.Int))
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
        fields.append(QgsField("rel_x", QVariant.Int))
        fields.append(QgsField("rel_y", QVariant.Int))
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
    
    def createGeorefShapefile(self, grid, channel, geoPoints, fields, fileName):
        
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
        if self.datOutput:
            attInd = [fields.indexFromName('res')]
            fieldList = fields.toList()            
            filterField = filter(lambda f: f.displayName().find('med') != -1, fieldList)            
            if filterField:
                attInd.append(fields.indexFromName(filterField[0].displayName()))
                filterName = "med_" + str(self.medianPercent)
            else:
                filterName = None
            Utilities.shapefileToDAT(fileName, attInd, filterName)

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
        folder = dirname(self.rawDataFilename)
        basicPath = folder + '/' + self.basicOutputFilename + '/Shapefiles'
        for channel in range(0, self.channelNbr):
            channelPath = basicPath + '/' + 'channel' + str(channel + 1)            
            fileName = channelPath + '/' + self.basicOutputFilename + '_channel' + str(channel + 1) + '_grid' + str(self.gridNames[grid]) + '.shp'                
            vLayer = QgsVectorLayer(fileName , "georef", "ogr")
            geoPoints = []
            featuresIter = vLayer.getFeatures()
            for feature in featuresIter:
                p = feature.geometry().asPoint()
                attrib = feature.attributes()
                pg = self.ptTransformation(p, sinAngle, cosAngle, x1, y1, xg1, yg1, a, b)        
                geoPoints.append((pg, attrib))              
            self.createGeorefShapefile(grid, channel, geoPoints, vLayer.fields(), fileName)
                                  
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
    
#     def runMag(self):
#         self.magRawDataParser()
#         if self.isDecimation:
#             self.magDecimation()       
#         if self.isStationPtRem:
#             self.distanceFilter()
#         self.sortedMagPoints = sorted(self.magPoints, key = itemgetter(3, 4))
#         self.createProfileList()
#         self.medianRemoval()
#         if self.datOutput:
#             self.createMagDatExport()
#         self.createMagShapefile()
    
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
                
    
    #Correction de la valeur UTM en x et creation d une colonne profil
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
        
        
    
    def medianRemoval(self):
        
        tempVals = [self.sortedMagPoints[0][2]]
        tempY = [1]
        profile = 1
        valueList = []
        step = 1    
        for i in range(1, len(self.sortedMagPoints)):
            if i == len(self.sortedMagPoints) - 1: # Median correction for the last profile            
                tempVals.append(self.sortedMagPoints[i][2])    
                tempY.append(step) # fictive Y for the polynomial
                step += 1                
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
                    a1 = numpy.polyfit(tempY, tempVals, self.trendPolyOrder)
                    p1 = numpy.poly1d(a1)    
                    newValPoly = [p1(val) for val in tempY]    
                val = 0                
                for i in range(0, len(tempVals)):
                    if self.isMedianRemoval:
                        val = tempVals[i] - medianProf 
                    else:
                        val = tempVals[i] - newValPoly[i] 
                    valueList.append(val)
                for val in valueList:
                    self.medianRemValues.append(float(val))   
                valueList = []                
            elif self.profile[i] == profile: # creation of a temporary vector for the correction
                tempVals.append((self.sortedMagPoints)[i][2])    
                tempY.append(step)
                step += 1    
            else: # the beginning of a new profile, stop append and computation of the median or the polynomial                
                profile += 1
                newValPoly, a1, p1 = [], [], []
                step += 1
                
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
                    a1 = numpy.polyfit(tempY, tempVals, self.trendPolyOrder)
                    p1 = numpy.poly1d(a1)    
                    newValPoly = [p1(val) for val in tempY]    
                for i in range(0, len(tempVals)):
                    if self.isMedianRemoval:
                        val = tempVals[i] - medianProf
                    else:
                        val = tempVals[i] - newValPoly[i]  
                    valueList.append(val)               
                for val in valueList:
                    self.medianRemValues.append(float(val))                
                tempVals, tempY, valueList = [], [], []                
                step = 1
                tempVals.append(self.sortedMagPoints[i][2])    
                tempY.append(step)
        
        
