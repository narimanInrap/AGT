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

import os
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSettings, QTextCodec, QCoreApplication, Qt


from ..core.AGTEngine import Engine
from ..core.CoilEnum import CoilConfigEnum
from ..ui.ui_EM31Dialog import Ui_AGTEM31Dialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *
from ..toolbox.DefParamEnum import DefParamEnum


class EM31Dialog(QtWidgets.QDialog, Ui_AGTEM31Dialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(EM31Dialog, self).__init__(parent)
        self.setupUi(self)
        self.ButtonBrowse.clicked.connect(self.inFile)
        self.ButtonBrowseShape.clicked.connect(self.outFileBrowse)
        self.runButton.clicked.connect(self.EM31Process)
        self.encoding = ''         
        
    def tr(self, message):
        """Get the translation for a string using Qt translation API.        
        """
        return QCoreApplication.translate(u"EM31Dlg", message)        
   
    def setDefaultCRSImport(self):
        
        self.qgsProjectionSelectionImport.setCrs(Utilities.loadDefaultParameters()[DefParamEnum.crsImport])
    
    def setDefaultCRSExport(self):   
        
        self.qgsProjectionSelectionExport.setCrs(Utilities.loadDefaultParameters()[DefParamEnum.crsExport] )

    def inFile(self):
        """Opens an open file dialog"""  
        
        inputMsg = QCoreApplication.translate(u"EM31Dlg", "Input file")
        inFilePath = Utilities.openFileDialog(self, 'EM31 (*.dat)', inputMsg)
        if not inFilePath:
            return
        self.inFileLine.setText(inFilePath)   
      
    def outFileBrowse(self):
        """Opens an open file dialog"""
            
        outFilename = Utilities.saveFileDialog(self) 
        if not outFilename:
            return
        self.outputFilename.setText(outFilename)
        
    def EM31Process(self):
        
        if not self.inputCheck():
            return
        coil = CoilConfigEnum.VCP
        if self.radioButtonHCP.isChecked():
            coil = CoilConfigEnum.HCP
        self.encoding = Utilities.loadDefaultParameters()[DefParamEnum.encoding]
        self.engine = Engine(rawDataFilename = self.inFileLine.text(), dataEncoding = self.encoding, crsRefImp = self.qgsProjectionSelectionImport.crs(), crsRefExp = self.qgsProjectionSelectionExport.crs(), 
                             datOutput = self.datFilechkbox.isChecked(), addCoordFields = self.coordFieldschk.isChecked(), outputShapefile = self.outputFilename.text(),
                             sensorHeight = self.heightSpin.value(), coilConfig = coil)
        #try:
        self.runEM31()
        #except (FileDeletionError, NoFeatureCreatedError, ParserError, Exception) as e:            
            #QMessageBox.warning(self, 'AGT', e.message)
            #return      
        self.addShapeToCanvas()
        self.hideDialog()
    
    def inputCheck(self):
        """Verifies whether the input is valid."""
      
        if not self.inFileLine.text():
            msg = QCoreApplication.translate(u"EM31Dlg",'Please specify an input data file.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        if not self.outputFilename.text():
            msg = QCoreApplication.translate(u"EM31Dlg",'Please specify an output shapefile.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        root, ext = os.path.splitext(self.outputFilename.text())
        if (ext.upper() != '.SHP'):
            msg = QCoreApplication.translate(u"EM31Dlg",'The output file must have the filename.shp format.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False        
        return True
    
    def runEM31(self):
        
        self.progressBar.setValue(10)
        self.engine.EM31RawDataParser()
        self.progressBar.setValue(50)
        self.engine.ConductivityTransformation()
        self.progressBar.setValue(90)
        self.engine.createEM31Shapefile()
        if self.datFilechkbox.isChecked():
            self.engine.createEM31DatExport()
        self.progressBar.setValue(100)     
                    
    def addShapeToCanvas(self):
    
        message = QCoreApplication.translate(u"EM31Dlg",'Created output Shapfile:')
        message = '\n'.join([message, unicode(self.outputFilename.text())])
        message = '\n'.join([message, QCoreApplication.translate(u"EM31Dlg","Would you like to add the new layer to your project?")])            
        addToTOC = QtWidgets.QMessageBox.question(self, "AGT", message,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.NoButton)
        if addToTOC == QtWidgets.QMessageBox.Yes:
            Utilities.addShapeToCanvas(unicode(self.outputFilename.text()))
                 
    def hideDialog(self):
        
        self.inFileLine.setText("")
        self.outputFilename.setText("")
        self.datFilechkbox.setCheckState(Qt.Unchecked)
        self.coordFieldschk.setCheckState(Qt.Unchecked)       
        self.heightSpin.setValue(0.7)
        self.radioButtonVCP.setChecked(True)
        self.setDefaultCRSImport()    
        self.setDefaultCRSExport()
        self.hide()
    