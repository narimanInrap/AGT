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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ..core.AGTEngine import Engine


from ..ui.ui_electDialog import Ui_AGTElectDialogBase
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *
from GeorefDialog import GeorefDialog


#FORM_CLASS, _ = uic.loadUiType(os.path.join(
#   os.path.dirname(__file__), 'agt_dialog_base.ui'))


class ElectDialog(QDialog, Ui_AGTElectDialogBase):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ElectDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)      
        QObject.connect(self.ButtonBrowse, SIGNAL('clicked()'), self.inFile) 
        QObject.connect(self.allProcess_button, SIGNAL('clicked()'), self.allProcesses)
        self.iface = iface      
        self.populateEncodings(AGTEnconding.getEncodings())
     
    # adopted from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo
    def populateEncodings(self, names):
        """Populates the combo box of available encodings."""
        
        self.comboEncoding.clear()
        self.comboEncoding.addItems(names)
        index = self.comboEncoding.findText(AGTEnconding.getDefaultEncoding('UTF-8'))
        if index == -1:
            index = 0  # Make sure some encoding is selected.
        self.comboEncoding.setCurrentIndex(index)      
      
    def inputCheck(self):
        """Verifies whether the input is valid."""
        
        if not self.inFileLine.text():
            msg = QtGui.QApplication.translate(u"ElectDlg", 'Please specify an input data file.')            
            QMessageBox.warning(self, 'AGT', msg)
            return False
        if not self.outputFilename.text():
            msg = QtGui.QApplication.translate(u"ElectDlg",'Please specify a project name.')
            QMessageBox.warning(self, 'AGT', msg)
            return False       
        if os.path.exists(dirname(self.inFileLine.text()) + '/' + self.outputFilename.text()):
            msg = QtGui.QApplication.translate(u"ElectDlg", 'The project name you have chosen already exists, you might overwrite some shapefiles. Do you want to continue?')
            keepPrjName = QMessageBox.question(self, 'AGT', msg,  QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
            if keepPrjName == QMessageBox.No:
                return False
        if self.checkBox_filt.isChecked():
            if not self.spinBox_maskR.value():
                msg = QtGui.QApplication.translate(u"ElectDlg",'Please specify the kernel size.')
                QMessageBox.warning(self, 'AGT', msg)
                return False
            if not self.spinBox_mvp.value():
                msg = QtGui.QApplication.translate(u"ElectDlg",'Please specify the median value percentage.')
                QMessageBox.warning(self, 'AGT', msg)
                return False
            if self.spinBox_maskR.value()%2 == 0:
                msg = QtGui.QApplication.translate(u"ElectDlg",'The mask size must be an odd number.')
                QMessageBox.warning(self, 'AGT', msg)
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
                
        inFilePath = Utilities.openFileDialog(self, 'Electrical geophysical data (*.shp *.DAT)', "Open input geophysical data file")
        if not inFilePath:
            return
        self.inFileLine.setText(inFilePath) 
    
    def getDataEncoding(self):
        """Returns the selected encoding for the input file."""
        
        return unicode(self.comboEncoding.currentText())
    
    def hideDialog(self):
        
        self.inFileLine.setText("")
        self.outputFilename.setText("")
        self.datFilechkbox.setCheckState(Qt.Unchecked)
        self.checkBox_filt.setCheckState(Qt.Unchecked)
        self.checkBox_geo.setCheckState(Qt.Unchecked)
        self.spinBox_mvp.setValue(30)
        self.spinBox_maskR.setValue(3)
        self.progressBar.setValue(0)
        index = self.comboEncoding.findText(AGTEnconding.getDefaultEncoding('UTF-8'))
        if index == -1:
            index = 0  # Make sure some encoding is selected.
        self.comboEncoding.setCurrentIndex(index)      
      
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
        self.engine = Engine(rawDataFilename = self.inFileLine.text(), dataEncoding = self.getDataEncoding(), datOutput = self.datFilechkbox.isChecked(), 
                             projectName = self.outputFilename.text(), medianPercent = self.spinBox_mvp.value(), kernelSize = self.spinBox_maskR.value(), 
                             filter = self.checkBox_filt.isChecked())
        shapefiles = []        
        try:
            self.engine.rawDataParser()
            self.progressBar.setValue(35)
        except (ParserError, ValueError) as e:       
            QMessageBox.warning(self, 'AGT', e.message)
            QMessageBox.warning(self, 'AGT', QtGui.QApplication.translate(u"ElectDlg",'procedure stopped'))
            return    
        try:
            if self.datFilechkbox.isChecked():
                self.engine.createRelCoordDatFile()
            self.progressBar.setValue(40)
            if self.checkBox_filt.isChecked():      
                filteredPtsMsg = self.engine.filterRawData()
                shapefiles = self.engine.createFilteredShapefile()
                QMessageBox.information(self, 'AGT', filteredPtsMsg)
            else:     
                shapefiles = self.engine.createRelCoordShapefile()
        except (FileDeletionError, NoFeatureCreatedError) as e:                    
            QMessageBox.warning(self, 'AGT', e.message )
            return 
        self.progressBar.setValue(100)         
        if self.checkBox_geo.isChecked():
            for g in range(0, self.engine.getGridNbr()):                    
                geoDlg = GeorefDialog(self.iface, self.engine, g)
                geoDlg.show()
                result = geoDlg.exec_()                
                if result == QDialog.Rejected:
                    QMessageBox.information(self, 'AGT', 'grid' + str(self.engine.getGridNames()[g]) + ': ' + QtGui.QApplication.translate(u"ElectDlg",u'Georeferencing canceled.'))     
                    break              
                QMessageBox.information(self, 'AGT', 'grid' + str(self.engine.getGridNames()[g]) + ': ' + QtGui.QApplication.translate(u"ElectDlg",u'Georeferencing done.'))
            shapefiles = map(lambda st : st[:-4] + '_Gref.shp', shapefiles)
        else:
            QMessageBox.information(self, 'AGT', "Data exported.")            
        self.addShapesToCanvas(shapefiles)  
        self.hideDialog()
        
        
    def addShapesToCanvas(self, shapefiles):
    
        message = QtGui.QApplication.translate(u"ElectDlg",'Output Shapfiles:')        
        for sf in shapefiles:           
            message = '\n'.join([message, unicode(sf)])
        message = '\n'.join([message, QtGui.QApplication.translate(u"ElectDlg","Would you like to add the new layers to your project?")])            
        addToTOC = QMessageBox.question(self, "AGT", message,
            QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
        if addToTOC == QMessageBox.Yes:
            for sf in shapefiles:
                Utilities.addShapeToCanvas(unicode(sf))                
        

    
 