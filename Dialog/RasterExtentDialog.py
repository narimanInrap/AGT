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

import os

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSettings, QTextCodec, QCoreApplication, Qt

from qgis.core import QgsProject,QgsMapLayer
 
import processing
from ..core.AGTEngine import EngineRaster
from processing.core.Processing import Processing
from processing.tools import *
from osgeo import gdal
from osgeo import ogr,osr, gdal

from ..ui.ui_RasterExtentDialog import Ui_AGTRasterExtentDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *


class RasterExtentDialog(QtWidgets.QDialog, Ui_AGTRasterExtentDialog):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(RasterExtentDialog, self).__init__(parent)  
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)        
        self.iface = iface
        self.populateProc()
        self.ButtonBrowseRaster.clicked.connect(self.outFileBrowse)            
        self.runButton.clicked.connect(self.rasterExtent)
    
    def populateProc(self):
        
        self.rastercomboBox.clear()  
        #layers = self.iface.legendInterface().layers()
        layers = [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()]
        layer_list = []
        for layer in layers:
            if layer.type() == QgsMapLayer.RasterLayer:
                layer_list.append(layer.name())
        self.rastercomboBox.addItems(layer_list)
        
    def outFileBrowse(self):
        """Opens an open file dialog"""
            
        outFilename = Utilities.saveFileDialog(self, '.tif') 
        if not outFilename:
            return
        self.outputFilename.setText(outFilename)

    def tr(self, message):
        """Get the translation for a string using Qt translation API.        
        """
        return QCoreApplication.translate(u"RasterDlg", message)
    
    def inputCheck(self):
        """Verifies whether the input is valid."""
        
        if not self.outputFilename.text():
            msg = QCoreApplication.translate(u"RasterExtentDialog", 'Please specify an output filename.')            
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        isAscii = lambda s: len(s) == len(s.encode())
        if not isAscii(os.path.basename(self.outputFilename.text())):
            msg = QCoreApplication.translate(u"RasterExtentDialog", 'The output filename should only have ASCII characters.')            
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        
    def rasterExtent(self):

        if not self.inputCheck():
            return
        layers = [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()]
        layer_list = []
        for layer in layers :
            if layer.type() == QgsMapLayer.RasterLayer:
                layer_list.append(layer)
        selectedLayerIndex = self.rastercomboBox.currentIndex() 
        rasterfile = layer_list[selectedLayerIndex]  
        
        self.engine = EngineRaster(rawDataFilename = rasterfile.source(), outputRasterfile = self.outputFilename.text(), zeroExtent = self.checkBox_zeroExtent.isChecked(), kernelLimit = self.spinBox_kernelLimit.value()*2)
        self.engine.openRaster()
        self.engine.limitExtentRaster()
        self.engine.saveRaster()
        self.addRasterToCanvas()
        self.hideDialog()
    
    def addRasterToCanvas(self):
    
        message = QCoreApplication.translate(u"MagDlg",'Created output Rasterfile:')
        message = '\n'.join([message, unicode(self.outputFilename.text())])
        message = '\n'.join([message, QCoreApplication.translate(u"MagDlg","Would you like to add the new layer to your project?")])            
        addToTOC = QtWidgets.QMessageBox.question(self, "AGT", message,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.NoButton)
        if addToTOC == QtWidgets.QMessageBox.Yes:
            Utilities.addShapeToCanvas(unicode(self.outputFilename.text()))
        
    def hideDialog(self):
        self.hide()
        
        
        
        
        
