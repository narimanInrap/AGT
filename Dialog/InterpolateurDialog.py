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

import os, unicodedata

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSettings, QTextCodec, QCoreApplication, Qt

from qgis.core import QgsProject,QgsMapLayer
 
import processing
from ..core.AGTEngine import EngineRaster
from processing.core.Processing import Processing
from processing.tools import *
from osgeo import gdal
from osgeo import ogr,osr, gdal

from ..ui.ui_InterpolateurDialog import Ui_InterpolatorDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *
from ..core.InterpolatorEnum import InterpolatorEnum


class InterpolateurDialog(QtWidgets.QDialog, Ui_InterpolatorDialog):
    def __init__(self, iface,parent=None):
        """Constructor."""
        super(InterpolateurDialog, self).__init__(parent)  
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)        
        self.iface = iface
        self.populateProc()
        
        self.VectorComboBox.currentIndexChanged.connect(self.populateAttr)
        self.ButtonBrowseRaster.clicked.connect(self.outFileBrowse)            
        self.runButton.clicked.connect(self.rasterInterp)
        
       
    
    def populateProc(self):
        
        self.VectorComboBox.clear()  
        layers = [layer for layer in [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()] if layer.type() == QgsMapLayer.VectorLayer]
        layer_list = []
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                layer_list.append(layer.name())
        self.VectorComboBox.addItems(layer_list)
        if self.VectorComboBox.currentText() != '':
            self.populateAttr()
            
        
        
    def populateAttr(self):
        self.FieldsComboBox.clear()  
#        root = QgsProject.instance().layerTreeRoot()
#
#
        layers = [layer for layer in [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()] if layer.type() == QgsMapLayer.VectorLayer]
        selectedLayerIndex=self.VectorComboBox.currentIndex()
        self.shapefile = layers[selectedLayerIndex]
#        selectedLayerText = self.VectorComboBox.currentText()
#        shapefile = QgsProject.instance().mapLayersByName((selectedLayerText))[0]
        
        
        fields = self.shapefile.fields()   
        field_names = [field.name() for field in fields]
        self.FieldsComboBox.addItems(field_names)
        
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
            msg = QCoreApplication.translate(u"InterpolateurDialog", 'Please specify an output filename.')            
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        isAscii = lambda s: len(s) == len(s.encode())
        if not isAscii(os.path.basename(self.outputFilename.text())):
            msg = QCoreApplication.translate(u"InterpolateurDialog", 'The output filename should only have ASCII characters.')            
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
    
    def rasterInterp(self):

        if not self.inputCheck():
            return
        layers = [layer for layer in [tree_layer.layer() for tree_layer in QgsProject.instance().layerTreeRoot().findLayers()] if layer.type() == QgsMapLayer.VectorLayer]
        selectedLayerIndex=self.VectorComboBox.currentIndex() 
        shapefile_active = layers[selectedLayerIndex]
        fieldname_active=self.FieldsComboBox.currentText()
        self.pixel=self.doubleSpinBox_pixelsize.value()
        self.window=self.doubleSpinBox_window.value()

        interp = InterpolatorEnum.ELECTROMAGNETIC
        if self.Magnetic.isChecked():
            interp = InterpolatorEnum.MAGNETIC
        elif self.Electric.isChecked():
            interp = InterpolatorEnum.ELECTRICAL
        self.engine = EngineRaster(outputRasterfile = self.outputFilename.text(), shapefile = shapefile_active, field = fieldname_active, pixelSize = self.pixel, searchWindow = self.window, methodInterp = interp)
        self.engine.InterpolRaster()
        self.iface.addRasterLayer(self.outputFilename.text(), '{} {}'.format(self.VectorComboBox.currentText(), self.FieldsComboBox.currentText()))
        self.hideDialog()
#        self.engine.medianRaster()
#        self.engine.saveRaster()
#        QtWidgets.QMessageBox.warning(self, 'AGT', msg)

        
    def hideDialog(self):
        self.hide()
        
        
        
        
        
