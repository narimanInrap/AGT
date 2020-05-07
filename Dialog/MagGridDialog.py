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

from ..ui.ui_MagGridDialog import Ui_AGTMagGridDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *
from ..toolbox.DefParamEnum import DefParamEnum
from .GeorefDialog import GeorefDialog

#FORM_CLASS, _ = uic.loadUiType(os.path.join(
#   os.path.dirname(__file__), 'AGT_dialog_base.ui'))


class MagGridDialog(QtWidgets.QDialog, Ui_AGTMagGridDialog):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(MagGridDialog, self).__init__(parent)
        self.setupUi(self)
        self.ButtonBrowse.clicked.connect(self.inFile)
        self.ButtonBrowseShape.clicked.connect(self.outFileBrowse)
        self.allProcess_button.clicked.connect(self.magProcesses)
        self.medchk.stateChanged.connect(self.medianChecked)
        self.trendchk.stateChanged.connect(self.TrendChecked)
        self.iface = iface
        self.encoding = Utilities.loadDefaultParameters()[DefParamEnum.encoding]
      
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
  
    def inFile(self):
        """Opens an open file dialog"""  
                
        inFilePath = Utilities.openFileDialog(self, 'MXPDA/Grad601 (*.dat)', "Open input geophysical data file")
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
        self.engine = Engine(rawDataFilename = self.inFileLine.text(), dataEncoding = self.encoding, datOutput = self.datFilechkbox.isChecked(),
                              addCoordFields = self.coordFieldschk.isChecked(), medRemove =  self.medchk.isChecked(), percentile = self.percentilechk.isChecked(), 
                              percThreshold = self.percentSpin.value(), trendRemove = self.trendchk.isChecked(), trendPolyOrder = self.polyOrdSpin.value(),
                              trendPercentile = self.trendPercentileChk.isChecked(), trendPercThreshold = self.trendPercentileSpinBox.value(), outputShapefile = self.outputFilename.text())
        shapefiles = [] 
        
        try:
            self.runMagGrid()
        except (FileDeletionError, NoFeatureCreatedError, ParserError, Exception) as e:
            msg = '{}'.format(e)            
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return
        self.engine.createMagGridRelCoordShapefile()
        self.progressBar.setValue(100)    
        if self.checkBox_geo.isChecked():
            geoDlg = GeorefDialog(self.iface, self.engine)
            geoDlg.show()
            result = geoDlg.exec_()                
            if result == QtWidgets.QDialog.Rejected:
                QtWidgets.QMessageBox.information(self, 'AGT', 'grid' + QCoreApplication.translate(u"MagGridDlg",u'Georeferencing canceled'))
            else:                 
                QtWidgets.QMessageBox.information(self, 'AGT', 'grid' + QCoreApplication.translate(u"MagGridDlg",u'Georeferencing done'))
                shapefiles.append(self.outputFilename.text()[:-4] + '_Gref.shp')
        else:
            shapefiles.append(self.outputFilename.text())               
            QtWidgets.QMessageBox.information(self, 'AGT', "Data exported.")
        self.addShapeToCanvas(shapefiles)
        self.hideDialog()
        
        
    def runMagGrid(self):

        self.progressBar.setValue(20)
        self.engine.magGridRawDataParser()
        self.progressBar.setValue(45)
        self.engine.CreateSimpleProfileListRelCoord()           
        self.progressBar.setValue(60)       
        self.engine.medianRemoval()
        self.progressBar.setValue(80)        
        if self.datFilechkbox.isChecked():
            self.engine.createMagGridRelCoordDatExport()      
             
    def inputCheck(self):
        """Verifies whether the input is valid."""
      
        if not self.inFileLine.text():
            msg = QCoreApplication.translate(u"MagGridDlg",'Please specify an input data file.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        if not self.outputFilename.text():
            msg = QCoreApplication.translate(u"MagGridDlg",'Please specify an output shapefile.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        root, ext = os.path.splitext(self.outputFilename.text())
        if (ext.upper() != '.SHP'):
            msg = QCoreApplication.translate(u"MagGridDlg",'The output file must have the filename.shp format.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False        
        return True
        
    def addShapeToCanvas(self, shapefiles):
    
        message = QCoreApplication.translate(u"MagGridDlg",'Created output Shapfile:')
        for sf in shapefiles:           
            message = '\n'.join([message, unicode(sf)])
        message = '\n'.join([message, QCoreApplication.translate(u"MagGridDlg","Would you like to add the new layer to your project?")])            
        addToTOC = QtWidgets.QMessageBox.question(self, "AGT", message,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.NoButton)
        if addToTOC == QtWidgets.QMessageBox.Yes:
            for sf in shapefiles:
                Utilities.addShapeToCanvas(unicode(sf))       
                 
    def hideDialog(self):
        
        self.inFileLine.setText("")
        self.outputFilename.setText("")
        self.datFilechkbox.setCheckState(Qt.Unchecked)
        self.coordFieldschk.setCheckState(Qt.Unchecked)
        self.percentilechk.setCheckState(Qt.Unchecked)       
        self.medchk.setCheckState(Qt.Checked)        
        self.trendchk.setCheckState(Qt.Unchecked)
        self.percentSpin.setValue(25)
        self.polyOrdSpin.setValue(3)
        self.progressBar.setValue(0)
        self.hide()
    
    
        