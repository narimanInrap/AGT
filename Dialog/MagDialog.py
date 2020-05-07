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

from ..ui.ui_magDialog import Ui_AGTMagDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *
from ..toolbox.DefParamEnum import DefParamEnum

#FORM_CLASS, _ = uic.loadUiType(os.path.join(
#   os.path.dirname(__file__), 'AGT_dialog_base.ui'))


class MagDialog(QtWidgets.QDialog, Ui_AGTMagDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(MagDialog, self).__init__(parent)
        self.setupUi(self)
        self.ButtonBrowse.clicked.connect(self.inFile)
        self.ButtonBrowseShape.clicked.connect(self.outFileBrowse)
        self.allProcess_button.clicked.connect(self.magProcesses)
        self.medchk.stateChanged.connect(self.medianChecked)
        self.trendchk.stateChanged.connect(self.TrendChecked)
        self.encoding = ''        
  

    def tr(self, message):
        """Get the translation for a string using Qt translation API.        
        """
        return QCoreApplication.translate(u"MagDlg", message)
    
    def medianChecked(self):
    
        if self.medchk.isChecked():
            self.percentilechk.setEnabled(True)
            self.trendchk.setCheckState(Qt.Unchecked)
        else:
            self.percentilechk.setCheckState(Qt.Unchecked)
            self.percentilechk.setDisabled(True)
            self.trendchk.setCheckState(Qt.Checked)
    
    def TrendChecked(self):
        
        if self.trendchk.isChecked():
            self.trendPercentileChk.setEnabled(True)    
            self.medchk.setCheckState(Qt.Unchecked)
        else:
            self.trendPercentileChk.setCheckState(Qt.Unchecked)
            self.medchk.setCheckState(Qt.Checked)
            self.trendPercentileChk.setDisabled(True)  
    
    def setDefaultCRS(self):
 
        self.qgsProjectionSelectionExport.setCrs(Utilities.loadDefaultParameters()[DefParamEnum.crsExport])      
        
    def inFile(self):
        """Opens an open file dialog"""  
                
        inFilePath = Utilities.openFileDialog(self, 'MXPDA (*.asc)', "Open input geophysical data file")
        if not inFilePath:
            return
        self.inFileLine.setText(inFilePath)   
      
    def outFileBrowse(self):
        """Opens an open file dialog"""
            
        outFilename = Utilities.saveFileDialog(self) 
        if not outFilename:
            return
        self.outputFilename.setText(outFilename)
        
    def magProcesses(self):
        
        if not self.inputCheck():
            return
        self.encoding = Utilities.loadDefaultParameters()[DefParamEnum.encoding]
        self.engine = Engine(rawDataFilename = self.inFileLine.text(), dataEncoding = self.encoding, crsRefExp = self.qgsProjectionSelectionExport.crs(), 
                             datOutput = self.datFilechkbox.isChecked(), addCoordFields = self.coordFieldschk.isChecked(), decimValue = self.decimSpin.value(), 
                             medRemove =  self.medchk.isChecked(), percentile = self.percentilechk.isChecked(), percThreshold = self.percentSpin.value(), 
                             trendRemove = self.trendchk.isChecked(), trendPolyOrder = self.polyOrdSpin.value(), trendPercentile = self.trendPercentileChk.isChecked(), 
                             trendPercThreshold = self.trendPercentileSpinBox.value(), statPtRem = self.stationRmvchk.isChecked(), 
                             statPtThresh = self.thresSpin.value(), gpsProbe = self.gpsSpin.value(), outputShapefile = self.outputFilename.text())
        #try:
        self.runMag()
        #except (FileDeletionError, NoFeatureCreatedError, ParserError, Exception) as e:            
         #   QMessageBox.warning(self, 'AGT', e.message)
          #  return      
        self.addShapeToCanvas()
        self.hideDialog()
        
        
    def runMag(self):
        
        self.progressBar.setValue(5)
        self.engine.magRawDataParser()
        self.progressBar.setValue(20)
        if self.MedianDecimRadioBut.isChecked():
            self.engine.medMovWinDecimation()
        else:
            self.engine.magDecimation()
        self.progressBar.setValue(35)                   
        if self.stationRmvchk.isChecked():
            self.engine.distanceFilter()
        self.progressBar.setValue(40)        
        self.engine.sortMagPoints()
        self.progressBar.setValue(45)        
        self.engine.createProfileList()
        self.progressBar.setValue(60)       
        self.engine.medianRemoval()
        self.progressBar.setValue(70)        
        if self.datFilechkbox.isChecked():
            self.engine.createMagDatExport()
        self.progressBar.setValue(80)        
        self.engine.createMagShapefile()
        self.progressBar.setValue(100)
        
        
    def inputCheck(self):
        """Verifies whether the input is valid."""
      
        if not self.inFileLine.text():
            msg = QCoreApplication.translate(u"MagDlg",'Please specify an input data file.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        if not self.outputFilename.text():
            msg = QCoreApplication.translate(u"MagDlg",'Please specify an output shapefile.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        root, ext = os.path.splitext(self.outputFilename.text())
        if (ext.upper() != '.SHP'):
            msg = QCoreApplication.translate(u"MagDlg",'The output file must have the filename.shp format.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False        
        return True
        
    def addShapeToCanvas(self):
    
        message = QCoreApplication.translate(u"MagDlg",'Created output Shapfile:')
        message = '\n'.join([message, unicode(self.outputFilename.text())])
        message = '\n'.join([message, QCoreApplication.translate(u"MagDlg","Would you like to add the new layer to your project?")])            
        addToTOC = QtWidgets.QMessageBox.question(self, "AGT", message,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.NoButton)
        if addToTOC == QtWidgets.QMessageBox.Yes:
            Utilities.addShapeToCanvas(unicode(self.outputFilename.text()))
                 
    def hideDialog(self):
        
        self.inFileLine.setText("")
        self.outputFilename.setText("")
        self.datFilechkbox.setCheckState(Qt.Unchecked)
        self.coordFieldschk.setCheckState(Qt.Unchecked)
        self.percentilechk.setCheckState(Qt.Unchecked)        
        self.MedianDecimRadioBut.setChecked(True)
        self.medchk.setCheckState(Qt.Checked)        
        self.trendchk.setCheckState(Qt.Unchecked)
        self.stationRmvchk.setCheckState(Qt.Unchecked)
        self.decimSpin.setValue(10)
        self.percentSpin.setValue(25)
        self.polyOrdSpin.setValue(3)
        self.thresSpin.setValue(1.2)
        self.gpsSpin.setValue(3)
        self.progressBar.setValue(0)
        self.setDefaultCRS()
        self.hide()
    
    
        