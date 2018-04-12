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

from PyQt4.QtCore import *
from PyQt4.QtGui import *



from ..core.AGTEngine import Engine

from ..ui.ui_MagGridDialog import Ui_AGTMagGridDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *
from GeorefDialog import GeorefDialog

#FORM_CLASS, _ = uic.loadUiType(os.path.join(
#   os.path.dirname(__file__), 'AGT_dialog_base.ui'))


class MagGridDialog(QDialog, Ui_AGTMagGridDialog):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(MagGridDialog, self).__init__(parent)
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
        self.encoding = Utilities.loadDefaultParameters()
      
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
        self.encoding = Utilities.loadDefaultParameters()[2]
        self.engine = Engine(rawDataFilename = self.inFileLine.text(), dataEncoding = self.encoding, datOutput = self.datFilechkbox.isChecked(),
                              addCoordFields = self.coordFieldschk.isChecked(), medRemove =  self.medchk.isChecked(), percentile = self.percentilechk.isChecked(), 
                              percThreshold = self.percentSpin.value(), trendRemove = self.trendchk.isChecked(), trendPolyOrder = self.polyOrdSpin.value(),
                              trendPercentile = self.trendPercentileChk.isChecked(), trendPercThreshold = self.trendPercentileSpinBox.value(), outputShapefile = self.outputFilename.text())
        shapefiles = [] 
        try:
            self.runMagGrid()
        except (FileDeletionError, NoFeatureCreatedError, ParserError, Exception) as e:            
            QMessageBox.warning(self, 'AGT', e.message)
            return
        self.engine.createMagGridRelCoordShapefile()
        self.progressBar.setValue(100)    
        if self.checkBox_geo.isChecked():
            geoDlg = GeorefDialog(self.iface, self.engine)
            geoDlg.show()
            result = geoDlg.exec_()                
            if result == QDialog.Rejected:
                QMessageBox.information(self, 'AGT', 'grid' + QtGui.QApplication.translate(u"ElectDlg",u'Georeferencing canceled.'))
            else:                 
                QMessageBox.information(self, 'AGT', 'grid' + QtGui.QApplication.translate(u"ElectDlg",u'Georeferencing done.'))
                shapefiles.append(self.outputFilename.text()[:-4] + '_Gref.shp')
        else:
            shapefiles.append(self.outputFilename.text())               
            QMessageBox.information(self, 'AGT', "Data exported.")
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
            msg = QtGui.QApplication.translate(u"MagGridDlg",'Please specify an input data file.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        if not self.outputFilename.text():
            msg = QtGui.QApplication.translate(u"MagGridDlg",'Please specify an output shapefile.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        root, ext = os.path.splitext(self.outputFilename.text())
        if (ext.upper() != '.SHP'):
            msg = QtGui.QApplication.translate(u"MagGridDlg",'The output file must have the filename.shp format.')
            QMessageBox.warning(self, 'AGT', msg)
            return False        
        return True
        
    def addShapeToCanvas(self, shapefiles):
    
        message = QtGui.QApplication.translate(u"MagGridDlg",'Created output Shapfile:')
        for sf in shapefiles:           
            message = '\n'.join([message, unicode(sf)])
        message = '\n'.join([message, QtGui.QApplication.translate(u"MagGridDlg","Would you like to add the new layer to your project?")])            
        addToTOC = QMessageBox.question(self, "AGT", message,
            QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
        if addToTOC == QMessageBox.Yes:
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
    
    
        