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

import os, codecs

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSettings, QTextCodec, QCoreApplication, Qt

from qgis.core import *
from qgis.gui import *


from ..core.AGTEngine import Engine

from ..ui.ui_CalibrationDialog import Ui_AGTCalibrationDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..toolbox.AGTExceptions import *


class CalibrationDialog(QtWidgets.QDialog, Ui_AGTCalibrationDialog):
  
    def __init__(self, parent=None):
        """Constructor."""
        super(CalibrationDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.meanResisCheckBox.stateChanged.connect(self.meanResisChecked)
        #QObject.connect(self.meanResisCheckBox, SIGNAL('stateChanged(int)'), self.meanResisChecked)
        self.saveButton.clicked.connect(self.saveCalib)
#         QObject.connect(self.saveButton, SIGNAL('clicked()'), self.saveCalib)
        self.cancelButton.clicked.connect(self.hideDialog)
#         QObject.connect(self.cancelButton, SIGNAL('clicked()'), self.hideDialog)
        self.ButtonBrowse.clicked.connect(self.inFile)
#         QObject.connect(self.ButtonBrowse, SIGNAL('clicked()'), self.inFile)
#         self.iface = iface
        self.defaultInlineFile = ''
        self.defaultAltBottom = 0.02
        self.defaultAltTop = 2.0
        self.defaultLayerNb = 5
        self.defaultMeanResist = 30.0
        self.defaultLayerTh1 = 0.2
        self.defaultLayerTh2 = 0.5
        self.defaultLayerTh3 = 1.0
        self.defaultLayerTh4 = 2.0
        self.defaultResist1 = 30.0
        self.defaultResist2 = 30.0
        self.defaultResist3 = 30.0
        self.defaultResist4 = 30.0
        self.defaultResist5 = 30.0
        
    def inFile(self):
        
        inFilePath = Utilities.openFileDialog(self, 'Calibration file (*.csv)', "Open input geophysical calibration parameteres file")
        if not inFilePath:
            return
        self.inFileLine.setText(inFilePath)
        
    def meanResisChecked(self):
        
        if self.meanResisCheckBox.isChecked():
            self.layer1Thick.setEnabled(False)
            self.resistL1.setEnabled(False)
            self.layer2Thick.setEnabled(False)
            self.resistL2.setEnabled(False)
            self.layer3Thick.setEnabled(False)
            self.resistL3.setEnabled(False)
            self.layer4Thick.setEnabled(False)
            self.resistL4.setEnabled(False)
            self.resistL5.setEnabled(False)
        else:
            self.layer1Thick.setEnabled(True)
            self.resistL1.setEnabled(True)
            self.layer2Thick.setEnabled(True)
            self.resistL2.setEnabled(True)
            self.layer3Thick.setEnabled(True)
            self.resistL3.setEnabled(True)
            self.layer4Thick.setEnabled(True)
            self.resistL4.setEnabled(True)
            self.resistL5.setEnabled(True)
        
    def loadCalib(self):
        
        calibParam = Utilities.loadDefaultCalibration()
        self.defaultInlineFile = calibParam[0]
        self.defaultAltBottom = float(calibParam[1])
        self.defaultAltTop = float(calibParam[2])
        self.defaultLayerNb = int(calibParam[3])
        self.defaultMeanResist = float(calibParam[4])
        if len(calibParam) > 5:
            self.defaultLayerTh1 = float(calibParam[5])
            self.defaultLayerTh2 = float(calibParam[6])
            self.defaultLayerTh3 = float(calibParam[7])
            self.defaultLayerTh4 = float(calibParam[8])
            self.defaultResist1 = float(calibParam[9])
            self.defaultResist2 = float(calibParam[10])
            self.defaultResist3 = float(calibParam[11])
            self.defaultResist4 = float(calibParam[12])
            self.defaultResist5 = float(calibParam[13])
        
    def saveCalib(self):
        
        calibFilename = '{}/../calibration.txt'.format(os.path.dirname(__file__))
        calibFile = codecs.open(calibFilename, 'w', encoding = 'UTF-8')        
        calibFile.write(self.inFileLine.text() + '\n')
        calibFile.write(unicode(self.altSpinBottom.value()) + '\n')
        calibFile.write(unicode(self.altSpinTop.value()) + '\n')
        if self.meanResisCheckBox.isChecked():
            calibFile.write('1\n')
            calibFile.write(unicode(self.meanResist.value()) + '\n')
        else:
            calibFile.write('5\n')
            calibFile.write(unicode(self.meanResist.value()) + '\n')
            calibFile.write(unicode(self.layer1Thick.value()) + '\n')
            calibFile.write(unicode(self.layer2Thick.value()) + '\n')
            calibFile.write(unicode(self.layer3Thick.value()) + '\n')
            calibFile.write(unicode(self.layer4Thick.value())+ '\n')
            calibFile.write(unicode(self.resistL1.value()) + '\n')
            calibFile.write(unicode(self.resistL2.value())+ '\n')
            calibFile.write(unicode(self.resistL3.value())+ '\n')
            calibFile.write(unicode(self.resistL4.value())+ '\n')
            calibFile.write(unicode(self.resistL5.value())+ '\n')           
        calibFile.close()
        msg = QCoreApplication.translate(u"calibrationDlg",'Default calibration saved.')            
        QtWidgets.QMessageBox.information(self, 'AGT', msg)
        self.hideDialog()    

    def setDefault(self):
        
        self.inFileLine.setText(self.defaultInlineFile)
        self.altSpinBottom.setValue(self.defaultAltBottom)
        self.altSpinTop.setValue(self.defaultAltTop)
        self.meanResist.setValue(self.defaultMeanResist)
        self.meanResisCheckBox.setCheckState(Qt.Checked)
        if self.defaultLayerNb == 5:
            self.layer1Thick.setValue(self.defaultLayerTh1)
            self.layer2Thick.setValue(self.defaultLayerTh2)
            self.layer3Thick.setValue(self.defaultLayerTh3)
            self.layer4Thick.setValue(self.defaultLayerTh4)
            self.resistL1.setValue(self.defaultResist1)
            self.resistL2.setValue(self.defaultResist2)
            self.resistL3.setValue(self.defaultResist3)
            self.resistL4.setValue(self.defaultResist4)
            self.resistL5.setValue(self.defaultResist5)
            self.meanResisCheckBox.setCheckState(Qt.Unchecked)
    
    def hideDialog(self):         
        
        self.setDefault()
        self.hide()