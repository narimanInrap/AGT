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



from ..core.AGTEngine import Engine, EngineGEM2

from ..ui.ui_MultiFreqDialog import Ui_AGTMultiFreqDialog
from CalibrationDialog import CalibrationDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *
from ..toolbox.DefParamEnum import DefParamEnum
from ..core.CoilEnum import CoilConfigEnum
from ..core.FilterEnum import FilterEnum

class GEM2Dialog(QDialog, Ui_AGTMultiFreqDialog):
    
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(GEM2Dialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        QObject.connect(self.ButtonBrowseData, SIGNAL('clicked()'), self.dataInFile)
        QObject.connect(self.ButtonBrowseGnss, SIGNAL('clicked()'), self.gnssInFile)
        QObject.connect(self.ButtonBrowseShape, SIGNAL('clicked()'), self.outFileBrowse)             
        QObject.connect(self.calibButton, SIGNAL('clicked()'), self.openCalib)
        QObject.connect(self.runButton, SIGNAL('clicked()'), self.gem2Process)  
        QObject.connect(self.magSusceptChkBox, SIGNAL('stateChanged(int)'), self.magSusceptChecked) 
        QObject.connect(self.decimChkBox, SIGNAL('stateChanged(int)'), self.decimChecked)
        self.iface = iface
        self.populateCRS(Utilities.getCRSList())     
        self.encoding = ''
        self.calib = None
        self.calibInlineFile = None
     
    def setDefaultCRSImport(self):    
        
        #index = self.comboCRS.findText(u'WGS 84 / UTM zone 31N, 32631')
        self.defaultCrsImport = Utilities.loadDefaultParameters()[DefParamEnum.crsImport]        
        index = self.comboCRSImport.findText(self.defaultCrsImport)      
        if index == -1:        
            index = 0  # Make sure some encoding is selected.            
        self.comboCRSImport.setCurrentIndex(index)   
    
    def setDefaultCRSExport(self):    
        
        #index = self.comboCRS.findText(u'WGS 84 / UTM zone 31N, 32631')
        self.defaultCrs = Utilities.loadDefaultParameters()[DefParamEnum.crsExport]        
        index = self.comboCRS.findText(self.defaultCrs)      
        if index == -1:        
            index = 0  # Make sure some encoding is selected.            
        self.comboCRS.setCurrentIndex(index)
   
    def populateCRS(self, crsNames):
        
        self.comboCRSImport.clear()
        self.comboCRSImport.addItems(crsNames)     
        self.setDefaultCRSImport()
        self.comboCRS.clear()
        self.comboCRS.addItems(crsNames)     
        self.setDefaultCRSExport()     
  
    def magSusceptChecked(self):
        
        if self.magSusceptChkBox.isChecked():
            self.conductCorrectChkBox.setEnabled(True)
        else:
            self.conductCorrectChkBox.setCheckState(Qt.Unchecked)
            self.conductCorrectChkBox.setDisabled(True)
            
    def decimChecked(self):
        
        if self.decimChkBox.isChecked():
            self.decimSpin.setEnabled(True)
        else:
            self.decimSpin.setDisabled(True)
            
    def dataInFile(self):
        
#        inFilePath = Utilities.openFileDialog(self, 'EMI file (*.csv)', "Open input geophysical data file")
        inFilePath = Utilities.openFileDialog(self, 'gem2 files (*.csv);;Emp400 files (*.EMI)', "Open input geophysical data file")
        if not inFilePath:
            return
        self.dataInFileLine.setText(inFilePath)
    
    def gnssInFile(self):
        
        inFilePath = Utilities.openFileDialog(self, 'GNSS file (*.dat)', "Open input GNSS data file")
        if not inFilePath:
            return
        self.gnssInFileLine.setText(inFilePath)   
    
    def outFileBrowse(self):
        """Opens an open file dialog"""
            
        outFilename = Utilities.saveFileDialog(self) 
        if not outFilename:
            return
        self.outputFilename.setText(outFilename)
    
    def openCalib(self):
    
        calibDlg = CalibrationDialog(self.iface)
        calibDlg.loadCalib()
        calibDlg.setDefault()
        calibDlg.show()
        result = calibDlg.exec_()
    
    def gem2Process(self):
        
        meanResist = 30.0
        layerNb = 5
        eLoaded = []
        rhoLoaded = []
        altBottom = 0.2
        altTop = 2.2
        if self.CalibrationChkBox.isChecked():
            calibParam = Utilities.loadDefaultCalibration()
            self.calibInlineFile = calibParam[0]
            altBottom = float(calibParam[1])
            altTop = float(calibParam[2])
            layerNb = int(calibParam[3])
            meanResist = float(calibParam[4])
            eLoaded = [float(calibParam[5]), float(calibParam[6]), float(calibParam[7]), float(calibParam[8])]
            rhoLoaded = [float(calibParam[9]), float(calibParam[10]), float(calibParam[11]), float(calibParam[12]), float(calibParam[13])]
        if not self.inputCheck():
            return
        self.encoding = Utilities.loadDefaultParameters()[DefParamEnum.encoding]
        coil = CoilConfigEnum.HCP
        if self.radioButtonVCP.isChecked():
            coil = CoilConfigEnum.VCP
        filterIp = FilterEnum.MEAN
        if self.windowSlideMedianIp.isChecked():
            filterIp = FilterEnum.MEDIAN      
        filterQ = FilterEnum.MEAN
        if self.windowSlideMedianQ.isChecked():
            filterQ = FilterEnum.MEDIAN
        self.engine = EngineGEM2(rawDataFilename = self.dataInFileLine.text(), dataEncoding = self.encoding, crsRefImp = self.comboCRSImport.currentText(), crsRefExp = self.comboCRS.currentText(), 
                                 sensorHeight = self.altSpin.value(), gnssHourShift = self.gnssHourShift.value(),gnssMinuteShift = self.gnssMinuteShift.value(), gnssSecondsShift = self.gnssSecondsShift.value(),
                                 gnssXShift = self.gnssXShift.value(), gnssYShift = self.gnssYShift.value(), calculConductivite = self.elecConductChkBox.isChecked(), calculSusceptibilite = self.magSusceptChkBox.isChecked(), 
                                 calibrationFilename = self.calibInlineFile, coilConfig = coil, paramConductCorr = self.conductCorrectChkBox.isChecked(), winfilterIp = self.SlidingWindowChkBoxIp.isChecked(), 
                                 winfilterQ = self.SlidingWindowChkBoxQ.isChecked(), gnssDataFilename = self.gnssInFileLine.text(), methodIp = filterIp, methodQ = filterQ, outputShapefile = self.outputFilename.text(), 
                                 valCoeff = -1.0, layerNbr = layerNb, e = eLoaded, rho = rhoLoaded, altBas = altBottom, altHaut = altTop, resistivityReference = meanResist, decimValue = self.decimSpin.value(), 
                                 winSizeQ=self.windowSizeSpinQ.value(),winSizeIp=self.windowSizeSpinIp.value())
        self.runGEM2()
        self.addShapeToCanvas()
        self.hideDialog()
    
    def runGEM2(self):
        
        self.engine.rawDataParser()        
        self.progressBar.setValue(20)        
        if self.gnssInFileLine.text():
            self.engine.gpsRawDataParser()
            self.engine.gem2GPSFusion()        
        if self.SlidingWindowChkBoxIp.isChecked() or self.SlidingWindowChkBoxQ.isChecked():
            self.engine.slidingWindow()            
        if self.decimChkBox.isChecked():
            self.engine.gem2Decim()            
        self.progressBar.setValue(30)            
        if self.CalibrationChkBox.isChecked():
            self.engine.rawDataParser(False) #calibration        
            self.engine.offsetGEM2()                   
        self.progressBar.setValue(40)
        if self.inphaseChkBox.isChecked():
            self.engine.gem2Mediane(False)
        if self.quadChkBox.isChecked():
            self.engine.gem2Mediane(True)
        self.progressBar.setValue(50)
        if self.elecConductChkBox.isChecked():
            self.engine.gem2Conductivity()
        self.progressBar.setValue(60)
        if self.magSusceptChkBox.isChecked():
            self.engine.gem2Susceptibility()        
        self.engine.correctionXYGEM2()
        self.progressBar.setValue(85)
        self.engine.createGEM2Shapefile()
        self.progressBar.setValue(100)
        
        
    def addShapeToCanvas(self):
    
        message = QtGui.QApplication.translate(u"Gem2Dlg",'Created output Shapfile:')
        message = '\n'.join([message, unicode(self.outputFilename.text())])
        message = '\n'.join([message, QtGui.QApplication.translate(u"Gem2Dlg","Would you like to add the new layer to your project?")])            
        addToTOC = QMessageBox.question(self, "AGT", message,
            QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
        if addToTOC == QMessageBox.Yes:
            Utilities.addShapeToCanvas(unicode(self.outputFilename.text()))
                
    def inputCheck(self):
        """Verifies whether the input is valid."""
      
        if not self.dataInFileLine.text():
            msg = QtGui.QApplication.translate(u"Gem2Dlg",'Please specify an input data file.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        if not self.outputFilename.text():
            msg = QtGui.QApplication.translate(u"Gem2Dlg",'Please specify an output shapefile.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        root, ext = os.path.splitext(self.outputFilename.text())
        if (ext.upper() != '.SHP'):
            msg = QtGui.QApplication.translate(u"Gem2Dlg",'The output file must have the filename.shp format.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        if self.CalibrationChkBox.isChecked() and not self.calibInlineFile:
            msg = QtGui.QApplication.translate(u"Gem2Dlg",'Please specify an calibration data file (calibration parameters), or unselect the calibration option.')
            QMessageBox.warning(self, 'AGT', msg)
            return False            
        return True
        
    def hideDialog(self):
        
        self.dataInFileLine.setText("")
        self.gnssInFileLine.setText("")
        self.outputFilename.setText("")
        self.radioButtonHCP.setChecked(True)
        self.inphaseChkBox.setCheckState(Qt.Unchecked)        
        self.CalibrationChkBox.setCheckState(Qt.Unchecked)
        self.elecConductChkBox.setCheckState(Qt.Unchecked)
        self.magSusceptChkBox.setCheckState(Qt.Unchecked)
        self.conductCorrectChkBox.setCheckState(Qt.Unchecked)
        self.decimChkBox.setCheckState(Qt.Unchecked)        
        self.altSpin.setValue(0.3)
        self.gnssXShift.setValue(-0.2)
        self.gnssYShift.setValue(-0.4)
        self.decimSpin.setValue(5)
        self.progressBar.setValue(0)
        self.setDefaultCRSImport()
        self.setDefaultCRSExport()
        self.hide()