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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSettings, QTextCodec
from qgis.core import *


from os.path import splitext
from os.path import dirname
from os.path import basename
import os, sqlite3

from AGTExceptions import *
#from ..lib.serial.tools import list_ports
#import serial.tools.list_ports

# All methods of this class were adopted from 'points2one Plugin'
# Copyright (C) 2010 Pavol Kapusta
# Copyright (C) 2010, 2013 Goyo
class Utilities(object):
    
    crsRefDict = {}
    interpolProcDict = {}
    
    @staticmethod
    def createShapefile(fileName, fields, features, encoding, crs):
    
        check = QtCore.QFile(fileName)
        if check.exists():
            if not QgsVectorFileWriter.deleteShapeFile(fileName):
                raise FileDeletionError(fileName)  
        writer = QgsVectorFileWriter(fileName, encoding,
                                     fields, QGis.WKBPoint, crs)
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
    
    
    
    # Returns a tupple containing the default parameters saved in the parameters' file
    @staticmethod
    def loadDefaultParameters():
        
        defaultCrsImport = unicode('RGF93 / Lambert-93, 2154')        
        defaultCrsExport = unicode('RGF93 / Lambert-93, 2154')
        defaultEncoding = unicode('UTF-8')
        try:
            paramFilename = '{}/../param.txt'.format(os.path.dirname(__file__))
            paramFile = open(paramFilename, 'r')
            defaultCrsImport = unicode(paramFile.readline().strip())
            defaultCrsExport = unicode(paramFile.readline().strip())
            defaultEncoding = unicode(paramFile.readline().strip())
            if (defaultEncoding not in AGTEnconding.getEncodings()):
                defaultEncoding = unicode('UTF-8')
            if (defaultCrsImport not in Utilities.getCRSList()):
                defaultCrsImport = unicode('RGF93 / Lambert-93, 2154')
            if (defaultCrsExport not in Utilities.getCRSList()):
                defaultCrsExport = unicode('RGF93 / Lambert-93, 2154')
        except IOError as e:
            #msg = 'Error({0}): {1}.\n'.format(e.errno, e.strerror)
            #msg += 'Default parameters not found.'            
            pass
        finally:
            paramFile.close()
            return(defaultCrsImport, defaultCrsExport, defaultEncoding)
    
    
    @staticmethod
    def loadDefaultCalibration():
        
        defaultInlineFile = ''
        defaultAltBottom = 0.02
        defaultAltTop = 2.0
        defaultLayerNb = 5
        defaultMeanResist = 30
        defaultLayerTh1 = 0.2
        defaultLayerTh2 = 0.5
        defaultLayerTh3 = 1.0
        defaultLayerTh4 = 2.0
        defaultResist1 = 30.0
        defaultResist2 = 30.0
        defaultResist3 = 30.0
        defaultResist4 = 30.0
        defaultResist5 = 30.0
        try:
            calibFilename = '{}/../calibration.txt'.format(os.path.dirname(__file__))
            calibFile = open(calibFilename, 'r')
            defaultInlineFile = unicode(calibFile.readline().strip())
            defaultAltBottom = float(calibFile.readline().strip())
            defaultAltTop = float(calibFile.readline().strip())
            defaultLayerNb = int(calibFile.readline().strip())
            defaultMeanResist = float(calibFile.readline().strip())
            if defaultLayerNb == 1:
                calibFile.close()
                return (defaultInlineFile, defaultAltBottom, defaultAltTop, defaultLayerNb, defaultMeanResist)
            defaultLayerTh1 = float(calibFile.readline().strip())
            defaultLayerTh2 = float(calibFile.readline().strip())
            defaultLayerTh3 = float(calibFile.readline().strip())
            defaultLayerTh4 = float(calibFile.readline().strip())
            defaultResist1 = float(calibFile.readline().strip())
            defaultResist2 = float(calibFile.readline().strip())
            defaultResist3 = float(calibFile.readline().strip())
            defaultResist4 = float(calibFile.readline().strip())
            defaultResist5 = float(calibFile.readline().strip())           
        except IOError as e:
            #msg = 'Error({0}): {1}.\n'.format(e.errno, e.strerror)
            #msg += 'Default calibration parameters not found.'            
            pass
        finally:
            calibFile.close()
            return(defaultInlineFile, defaultAltBottom, defaultAltTop, defaultLayerNb, defaultMeanResist, defaultLayerTh1, defaultLayerTh2, 
                   defaultLayerTh3, defaultLayerTh4, defaultResist1, defaultResist2, defaultResist3, defaultResist4, defaultResist5)  
        
        
    # Returns the list of all CRSes and fills the CRS dictionary
    @staticmethod
    def getCRSList():
        
        conn = sqlite3.connect(QgsApplication.srsDbFilePath())
        cur = conn.cursor()
        cur.execute('select * from vw_srs')
        rows = cur.fetchall()
        crsList = []      
        for crs in rows:
            crsList.append(crs[0][:25] + ', ' + crs[6])
            try:
                code = long(crs[6])
            except ValueError:
                code = crs[6]
            Utilities.crsRefDict[crs[0][:25] + ', ' + crs[6]] = code        
        cur.close()
        conn.close()        
        return crsList
  
    # Fills the dictionary of interpolation processes and returns the list the its keys  
    @staticmethod
    def getInterProcList():
        
        Utilities.interpolProcDict['inverse distance weighted'] = 'saga:inversedistanceweighted'
        Utilities.interpolProcDict['multilevel spline interpolation'] = 'saga:multilevelbsplineinterpolation'
        return Utilities.interpolProcDict.keys()
    
    # Returns the list of available baud rates
    @staticmethod
    def getBaudRateList():
        
        baudRates = []
        baudRates.append('2400')
        baudRates.append('9600')
        baudRates.append('14400')
        baudRates.append('19200')
        baudRates.append('28800')       
        return baudRates
    
    # Returns the list of available COM ports
    @staticmethod
    def getComPortList():
        
        #ports = list(list_ports.comports())
        comPorts = []
        #for p in ports:
        #   comPorts.append(str(p))
        return comPorts 
    
    # Returns the list of available probe configurations
    @staticmethod
    def getProbeConfigList():
        
        probeConfigs = []
        probeConfigs.append(QtGui.QApplication.translate("Utility", 'pole-pole', None, QtGui.QApplication.UnicodeUTF8))
        return probeConfigs
    
    # Returns a list of names of all layers in QgsMapLayerRegistry
    @staticmethod
    def getLayerNames(geoTypes):
        
        mapLayers = QgsMapLayerRegistry.instance().mapLayers()    
        layers = []  
        for name, layer in mapLayers.iteritems():
            if (layer.type() == QgsMapLayer.VectorLayer) and (layer.geometryType() in geoTypes):
                layers.append(unicode(layer.name()))
        return layers
    
    
    #Return QgsVectorLayer from a layer name ( as string )
    #adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
    @staticmethod
    def getVectorLayerByName(layerName):
#         if layerName is None:
#             return None
        mapLayers = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in mapLayers.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == layerName:
                if layer.isValid():
                    return layer
                else:
                    return None    
    
    @staticmethod
    def saveFileDialog(parent, filExt = '.shp'): 
        """Shows a save file dialog and returns the selected file path."""
        
        settings = QtCore.QSettings()
        key = '/UI/lastShapefileDir'
        outDir = settings.value(key)
        if filExt == '.shp':
            filter = 'Shapefiles (*.shp)'
        elif filExt == '.tif':
            filter = 'Tagged image files (*.tif)'
        else:
            filter = '*' + filExt
            
        SaveOutPutShapeMsg = QtGui.QApplication.translate("Utility","Save output file", None, QtGui.QApplication.UnicodeUTF8) 
        outFilePath = QtGui.QFileDialog.getSaveFileName(parent, SaveOutPutShapeMsg, outDir, filter)
        outFilePath = unicode(outFilePath)
        if outFilePath:
            root, ext = splitext(outFilePath)
            if ext.upper() != filExt.upper():
                outFilePath = root + filExt
            outDir = dirname(outFilePath)
            settings.setValue(key, outDir)
        return outFilePath 
     
    @staticmethod
    def openFileDialog(parent, fileFilter, message):
        """Shows an open file dialog and returns the selected file path."""
        
        settings = QtCore.QSettings()
        key = '/UI/lastShapefileDir'
        workDir = settings.value(key)
        filter = fileFilter
        OpenInputShapeMsg = QtGui.QApplication.translate("Utility", message, None, QtGui.QApplication.UnicodeUTF8) 
        inFilePath = QtGui.QFileDialog.getOpenFileName(parent, OpenInputShapeMsg, workDir, filter)
        inFilePath = unicode(inFilePath)
        if inFilePath:
            #  root, ext = splitext(inFilePath)
            # if ext.upper() != '.SHP':
            #    inFilePath = '%s.shp' % inFilePath
            workDir = dirname(inFilePath)
            settings.setValue(key, workDir)
        return inFilePath
             
    # Adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
    @staticmethod
    def addShapeToCanvas(shapeFilePath):
        """adds a vector layer to the canvas based on the input shapefile path"""
        
        layerName = basename(shapeFilePath)
        root, ext = splitext(layerName)
        if ext == '.shp':
            layerName = root
        newLayer = QgsVectorLayer(shapeFilePath, layerName, "ogr")
        ret = QgsMapLayerRegistry.instance().addMapLayer(newLayer)
        return ret 

    @staticmethod
    def shapefileToDAT(shapefile, attInd, filterFieldName = None):
      
        vLayer = QgsVectorLayer(shapefile , "dat", "ogr")    
        featuresIter = vLayer.getFeatures()
        features = [f for f in featuresIter]       
        features.sort(key = lambda f : (f.geometry().asPoint().y(), f.geometry().asPoint().x()))
        if filterFieldName != None:                  
            datFileName = shapefile[:-4].replace('/Shapefiles', '/DATfiles') + '_' + filterFieldName + '.dat'
        else:
            datFileName = shapefile[:-4].replace('/Shapefiles', '/DATfiles') + '.dat'            
        fileObj = open(datFileName, 'w')        
        for feature in features:
            attString = ''   
            for i in attInd:              
                attrib = feature.attributes()
                attString += (', ' + str(attrib[i]))
            fileObj.write(str(feature.geometry().asPoint().x()) + ', ' + str(feature.geometry().asPoint().y()) + attString + '\n')
        fileObj.close()        
    
    @staticmethod
    def fRange(start, stop, step):
        i = 0
        while start + i * step < stop:
            yield start + i * step
            i += 1
    
    @staticmethod
    def isClose(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

           
# All methods of this class were adopted from 'points2one Plugin'
# Copyright (C) 2010 Pavol Kapusta
# Copyright (C) 2010, 2013 Goyo  
class AGTEnconding(object):
  
    @staticmethod
    def getEncodings():
        """Returns a list of available encodings static."""
        
        return [unicode(QTextCodec.codecForMib(mib).name())
                 for mib in QTextCodec.availableMibs()]
    
    @staticmethod    
    def getDefaultEncoding(default = 'System'):
        """Returns the default encoding. static"""
        
        settings = QSettings()
        return settings.value('/UI/encoding', default)
        
    @staticmethod
    def setDefaultEncoding(encoding):
        """Sets the default encoding. static"""
        
        # Make sure encoding is not blank.
        encoding = encoding or 'System'
        settings = QSettings()
        settings.setValue('/UI/encoding', encoding)

