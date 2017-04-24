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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import processing
from processing.core.Processing import Processing
from processing.tools import *
from osgeo import gdal
from  osgeo import ogr, osr

from ..ui.ui_rasterDialog import Ui_AGTRasterDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *


class RasterDialog(QDialog, Ui_AGTRasterDialog):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(RasterDialog, self).__init__(parent)  
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)        
        self.iface = iface
        QObject.connect(self.BrowseIn, SIGNAL('clicked()'), self.inFile)
        QObject.connect(self.browseOut, SIGNAL('clicked()'), self.outFileBrowse)            
        QObject.connect(self.runButton, SIGNAL('clicked()'), self.interpolation)
        QObject.connect(self.inputShapefile, SIGNAL('textChanged(QString)'), self.updateFieldCombo)
        self.populateProc()
        
    
    def populateProc(self):
        
        self.procComboBox.clear()        
        self.procComboBox.addItems(Utilities.getInterProcList())     
        self.setDefaultProc()
    
    def setDefaultProc(self):    
        
        index = self.procComboBox.findText(u'multilevel spline interpolation')        
        if index == -1:
            index = 0  # Make sure some encoding is selected.            
        self.procComboBox.setCurrentIndex(index)
    
    def updateFieldCombo(self):
        
        self.fieldCombo.clear()
        if not self.inputShapefile.text():
            return
        layer = QgsVectorLayer(self.inputShapefile.text(), "raster", "ogr")
        if layer is not None:            
            fields = layer.dataProvider().fields()
            for field in fields:
                name = field.name()
                self.fieldCombo.addItem(name)
                
    def inFile(self):
        """Opens an open file dialog"""  
                
        inFilePath = Utilities.openFileDialog(self, 'Shapefile (*.shp)', "Open input shapefile")
        if not inFilePath:
            return
        self.inputShapefile.setText(inFilePath)   
      
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
    
    def interpolation(self):
        
        if self.procComboBox.currentText() == 'multilevel spline interpolation':
            processing.runalg('saga:multilevelbsplineinterpolation', 
                              self.inputShapefile.text(), 
                              self.fieldCombo.currentText(),
                              0,
                              0.0001,
                              11.0,
                              None,
                              self.cellSizeSpinBox.value(),
                              self.outputFilename.text())
#             processing.runalg('saga:multilevelbsplineinterpolation',
#                               self.inputShapefile.text(), 
#                               self.fieldCombo.currentText(), 
#                               0, 
#                               0, 
#                               0.0001, 
#                               11.0, 
#                               None, 
#                               self.cellSizeSpinBox.value(),
#                               self.outputFilename.text())
        else:
            processing.runalg('saga:inversedistanceweighted',
                              self.inputShapefile.text(),
                              self.fieldCombo.currentText(),
                              0,
                              2.0,
                              1.0,
                              0,
                              10.0,
                              0,
                              0,
                              10.0,
                              None,
                              self.cellSizeSpinBox.value(),
                              self.outputFilename.text())
        
        QMessageBox.warning(self, 'AGT', 'process finished.')