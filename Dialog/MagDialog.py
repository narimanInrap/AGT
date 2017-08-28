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



from ..core.AGTEngine import Engine

from ..ui.ui_magDialog import Ui_AGTMagDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *

#FORM_CLASS, _ = uic.loadUiType(os.path.join(
#   os.path.dirname(__file__), 'AGT_dialog_base.ui'))


class MagDialog(QDialog, Ui_AGTMagDialog):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(MagDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        QObject.connect(self.ButtonBrowse, SIGNAL('clicked()'), self.inFile)
        QObject.connect(self.ButtonBrowseShape, SIGNAL('clicked()'), self.outFileBrowse)
        QObject.connect(self.allProcess_button, SIGNAL('clicked()'), self.magProcesses)
        QObject.connect(self.medchk, SIGNAL('stateChanged(int)'), self.medianChecked)
        QObject.connect(self.trendchk, SIGNAL('stateChanged(int)'), self.TrendChecked)
        self.iface = iface    
        self.populateCRS(Utilities.getCRSList())        
        self.populateEncodings(AGTEnconding.getEncodings())       
       

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
    
    def setDefaultEncoding(self):
        
        index = self.comboEncoding.findText(AGTEnconding.getDefaultEncoding('UTF-8'))
        if index == -1:
            index = 0  # Make sure some encoding is selected.
        self.comboEncoding.setCurrentIndex(index)
    
    def setDefaultCRS(self):    
        
        index = self.comboCRS.findText(u'RGF93 / Lambert-93, 2154')        
        if index == -1:
            index = 0  # Make sure some encoding is selected.            
        self.comboCRS.setCurrentIndex(index)
    
    
    # adopted from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo
    def populateEncodings(self, names):
        """Populates the combo box of available encodings."""
        
        self.comboEncoding.clear()
        self.comboEncoding.addItems(names)       
        self.setDefaultEncoding()
      
   
    def populateCRS(self, crsNames):
        
        self.comboCRS.clear()
        self.comboCRS.addItems(crsNames)     
        self.setDefaultCRS()
    
    
    def inFile(self):
        """Opens an open file dialog"""  
                
        inFilePath = Utilities.openFileDialog(self, 'Magnetic geophysical data (*.asc)', "Open input geophysical data file")
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
        self.engine = Engine(rawDataFilename = self.inFileLine.text(), dataEncoding = self.comboEncoding.currentText(), crsRef = self.comboCRS.currentText(), 
                             datOutput = self.datFilechkbox.isChecked(), addCoordFields = self.coordFieldschk.isChecked(), decimation =self.decimChk.isChecked(), 
                             decimValue = self.decimSpin.value(), medRemove =  self.medchk.isChecked(), percentile = self.percentilechk.isChecked(), 
                             percThreshold = self.percentSpin.value(), trendRemove = self.trendchk.isChecked(), trendPolyOrder = self.polyOrdSpin.value(),
                             trendPercentile = self.trendPercentileChk.isChecked(), trendPercThreshold = self.trendPercentileSpinBox.value(), statPtRem = self.stationRmvchk.isChecked(), 
                             statPtThresh = self.thresSpin.value(), gpsProbe = self.gpsSpin.value(), outputShapefile = self.outputFilename.text())
        try:
            self.runMag()
        except (FileDeletionError, NoFeatureCreatedError, ParserError, Exception) as e:            
            QMessageBox.warning(self, 'AGT', e.message)
            return      
        self.addShapeToCanvas()
        self.hideDialog()
        
        
    def runMag(self):
        
        self.progressBar.setValue(10)
        self.engine.magRawDataParser()
        self.progressBar.setValue(20)
        if self.decimChk.isChecked():
            self.engine.magDecimation()
        self.progressBar.setValue(25)                   
        if self.stationRmvchk.isChecked():
            self.engine.distanceFilter()
        self.progressBar.setValue(35)        
        self.engine.sortMagPoints()
        self.progressBar.setValue(45)        
        self.engine.createProfileList()
        self.progressBar.setValue(60)       
        self.engine.medianRemoval()
        self.progressBar.setValue(80)        
        if self.datFilechkbox.isChecked():
            self.engine.createMagDatExport()
        self.progressBar.setValue(85)        
        self.engine.createMagShapefile()
        self.progressBar.setValue(100)
        
        
    def inputCheck(self):
        """Verifies whether the input is valid."""
      
        if not self.inFileLine.text():
            msg = QtGui.QApplication.translate(u"MagDlg",'Please specify an input data file.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        if not self.outputFilename.text():
            msg = QtGui.QApplication.translate(u"MagDlg",'Please specify an output shapefile.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        root, ext = os.path.splitext(self.outputFilename.text())
        if (ext.upper() != '.SHP'):
            msg = QtGui.QApplication.translate(u"MagDlg",'The output file must have the filename.shp format.')
            QMessageBox.warning(self, 'AGT', msg)
            return False        
        return True
        
    # adopted from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo
    def addShapeToCanvas(self):
    
        message = QtGui.QApplication.translate(u"MagDlg",'Created output Shapfile:')
        message = '\n'.join([message, unicode(self.outputFilename.text())])
        message = '\n'.join([message, QtGui.QApplication.translate(u"MagDlg","Would you like to add the new layer to your project?")])            
        addToTOC = QMessageBox.question(self, "AGT", message,
            QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
        if addToTOC == QMessageBox.Yes:
            Utilities.addShapeToCanvas(unicode(self.outputFilename.text()))
                 
    def hideDialog(self):
        
        self.inFileLine.setText("")
        self.outputFilename.setText("")
        self.datFilechkbox.setCheckState(Qt.Unchecked)
        self.coordFieldschk.setCheckState(Qt.Unchecked)
        self.percentilechk.setCheckState(Qt.Unchecked)        
        self.decimChk.setCheckState(Qt.Checked)
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
        self.setDefaultEncoding()  
        self.hide()
    
    
        