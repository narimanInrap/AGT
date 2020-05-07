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

from os.path import dirname

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSettings, QTextCodec, QCoreApplication, Qt


from ..core.AGTEngine import Engine


from ..ui.ui_electDialog import Ui_AGTElectDialogBase
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *
from ..toolbox.DefParamEnum import DefParamEnum
from .GeorefDialog import GeorefDialog


#FORM_CLASS, _ = uic.loadUiType(os.path.join(
#   os.path.dirname(__file__), 'agt_dialog_base.ui'))


class ElectDialog(QtWidgets.QDialog, Ui_AGTElectDialogBase):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ElectDialog, self).__init__(parent)
        self.setupUi(self)      
        self.ButtonBrowse.clicked.connect(self.inFile)
        self.allProcess_button.clicked.connect(self.allProcesses)
        self.iface = iface
        self.encoding = Utilities.loadDefaultParameters()[DefParamEnum.encoding]        
      
    def inputCheck(self):
        """Verifies whether the input is valid."""
        
        if not self.inFileLine.text():
            msg = QCoreApplication.translate(u"ElectDlg", 'Please specify an input data file.')            
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        if not self.outputFilename.text():
            msg = QCoreApplication.translate(u"ElectDlg",'Please specify a project name.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False       
        if os.path.exists(dirname(self.inFileLine.text()) + '/' + self.outputFilename.text()):
            msg = QCoreApplication.translate(u"ElectDlg", 'The project name you have chosen already exists, you might overwrite some shapefiles. Do you want to continue?')
            keepPrjName = QtWidgets.QMessageBox.question(self, 'AGT', msg,  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.NoButton)
            if keepPrjName == QtWidgets.QMessageBox.No:
                return False
        if self.checkBox_filt.isChecked():
            if not self.spinBox_maskR.value():
                msg = QCoreApplication.translate(u"ElectDlg",'Please specify the kernel size.')
                QtWidgets.QMessageBox.warning(self, 'AGT', msg)
                return False
            if not self.spinBox_mvp.value():
                msg = QCoreApplication.translate(u"ElectDlg",'Please specify the median value percentage.')
                QtWidgets.QMessageBox.warning(self, 'AGT', msg)
                return False
            if self.spinBox_maskR.value()%2 == 0:
                msg = QCoreApplication.translate(u"ElectDlg",'The mask size must be an odd number.')
                QtWidgets.QMessageBox.warning(self, 'AGT', msg)
                return False
        return True    

    def outRelCoordFile(self): 
        """Opens a save file dialog and sets the output file path."""
        
        outRelCoordFilePath = Utilities.saveFileDialog(self)
        if not outRelCoordFilePath:
            return
        self.setOutRelCoordFilePath(outRelCoordFilePath)
        
    def inFile(self):
        """Opens an open file dialog"""  
                
        inFilePath = Utilities.openFileDialog(self, 'RM15/RM85 *.DAT', "Open input geophysical data file")
        if not inFilePath:
            return
        self.inFileLine.setText(inFilePath) 
      
    def hideDialog(self):
        
        self.inFileLine.setText("")
        self.outputFilename.setText("")
        self.datFilechkbox.setCheckState(Qt.Unchecked)
        self.checkBox_filt.setCheckState(Qt.Unchecked)
        self.checkBox_geo.setCheckState(Qt.Unchecked)
        self.spinBox_mvp.setValue(30)
        self.spinBox_maskR.setValue(3)
        self.progressBar.setValue(0)              
        self.hide()
        
#     def relativeCoordProc(self):
#        
#         try:
#             self.engine.rawDataParser()
#         except (ParserError, ValueError) as e:               
#             QMessageBox.warning(self, 'AGT', e.message)
#             return False
#         try:
#             self.engine.createRelCoordShapefile()
#         except (FileDeletionError, NoFeatureCreatedError) as e:                    
#             QMessageBox.warning(self, 'AGT', e.message )  
#         if self.datFilechkbox.isChecked():
#             self.engine.createRelCoordDatFile()
    
          
    def allProcesses(self):
        
        if not self.inputCheck():
            return
        self.encoding = Utilities.loadDefaultParameters()[DefParamEnum.encoding]
        self.engine = Engine(rawDataFilename = self.inFileLine.text(), dataEncoding = self.encoding, datOutput = self.datFilechkbox.isChecked(), 
                             projectName = self.outputFilename.text(), medianPercent = self.spinBox_mvp.value(), kernelSize = self.spinBox_maskR.value(), 
                             filter = self.checkBox_filt.isChecked())
        shapefiles = []        
        try:
            self.engine.rawDataParser()
            self.progressBar.setValue(35)
        except (ParserError, ValueError) as e:
            msg = '{}'.format(e)
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            QtWidgets.QMessageBox.warning(self, 'AGT', QCoreApplication.translate(u"ElectDlg",'procedure stopped'))
            return    
        try:
            if self.datFilechkbox.isChecked():
                self.engine.createRelCoordDatFile()
            self.progressBar.setValue(40)
            if self.checkBox_filt.isChecked():      
                filteredPtsMsg = self.engine.filterRawData()
                shapefiles = self.engine.createFilteredShapefile()
                QtWidgets.QMessageBox.information(self, 'AGT', filteredPtsMsg)
            else:     
                shapefiles = self.engine.createRelCoordShapefile()
        except (FileDeletionError, NoFeatureCreatedError) as e:
            msg = '{}'.format(e)                   
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return 
        self.progressBar.setValue(100)         
        if self.checkBox_geo.isChecked():
            for g in range(0, self.engine.getGridNbr()):                    
                geoDlg = GeorefDialog(self.iface, self.engine, g)
                geoDlg.show()
                result = geoDlg.exec_()                
                if result == QtWidgets.QDialog.Rejected:
                    QtWidgets.QMessageBox.information(self, 'AGT', 'grid' + str(self.engine.getGridNames()[g]) + ': ' + QCoreApplication.translate(u"ElectDlg",u'Georeferencing canceled'))     
                    break              
                QtWidgets.QMessageBox.information(self, 'AGT', 'grid' + str(self.engine.getGridNames()[g]) + ': ' + QCoreApplication.translate(u"ElectDlg",u'Georeferencing done'))
            shapefiles = list(map(lambda st : st[:-4] + '_Gref.shp', shapefiles))
        else:
            QtWidgets.QMessageBox.information(self, 'AGT', "Data exported.")            
        self.addShapesToCanvas(shapefiles)  
        self.hideDialog()
        
        
    def addShapesToCanvas(self, shapefiles):
        
        message = QCoreApplication.translate(u"ElectDlg",'Output Shapfiles:')        
        for sf in shapefiles:           
            message = '\n'.join([message, unicode(sf)])
        message = '\n'.join([message, QCoreApplication.translate(u"ElectDlg","Would you like to add the new layers to your project?")])            
        addToTOC = QtWidgets.QMessageBox.question(self, "AGT", message,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.NoButton)
        if addToTOC == QtWidgets.QMessageBox.Yes:
            for sf in shapefiles:
                Utilities.addShapeToCanvas(unicode(sf))
           