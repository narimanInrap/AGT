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
import sys
 
from os.path import dirname
 
from PyQt4.QtCore import *
from PyQt4.QtGui import *
 
from ..ui.ui_ElecDownDialog import Ui_AGTElecDownDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding
from ..core.DownloadEngine import DownloadEngine
from GridDialog import GridDialog
 
 
class ElecDownDialog(QDialog, Ui_AGTElecDownDialog):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ElecDownDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)    
        self.iface = iface
        QObject.connect(self.ButtonBrowse, SIGNAL('clicked()'), self.outFile)
        QObject.connect(self.runButton, SIGNAL('clicked()'), self.run)            
        self.populateProbeConfig(Utilities.getProbeConfigList())
        self.populateComCombo(Utilities.getComPortList())
        self.populateBaudCombo(Utilities.getBaudRateList())
        self.grids = []
     
    def populateProbeConfig(self, names):
        """Populates the combo box of available probe configurations."""
         
        self.probeConfigCombo.clear()
        self.probeConfigCombo.addItems(names)        
        self.probeConfigCombo.setCurrentIndex(0)      
      
    def populateComCombo(self, names):
        """Populates the combo box of available serial(COM) ports."""
         
        self.comCombo.clear()
        self.comCombo.addItems(names)
        index = self.comCombo.findText('COM1')
        if index == -1:
            index = 0
        self.comCombo.setCurrentIndex(index)      
     
    def populateBaudCombo(self, names):
        """Populates the combo box of available serial(COM) ports."""
         
        self.baudCombo.clear()
        self.baudCombo.addItems(names)
        index = self.baudCombo.findText('9600') 
        if index == -1:
            index = 0    
        self.baudCombo.setCurrentIndex(index)  
     
    def outFile(self):
         
        outFilePath = Utilities.saveFileDialog(self, '.dat')        
        if not outFilePath:
            return
        self.outputFilename.setText(outFilePath)
     
    def inputCheck(self):
        """Verifies whether the input is valid."""
         
        if not self.outputFilename.text():
            msg = QApplication.translate(u"ElecDownDlg",'Please specify an output file name.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        return True
     
    def run(self):
         
         
        if not self.inputCheck():
            return
        self.engine = DownloadEngine(self.outputFilename.text(), self.radioButton85.isChecked(), self.nbGridSpin.value(), self.gridSizeSpinX.value(), self.gridSizeSpinY.value(), self.probeSpaceSpin.value(),
                                     self.nbChannelSpin.value(), self.nbProbeSpin.value(), self.collectedPtNbSpin.value(), self.lineStepSpin.value(), self.probeConfigCombo.currentText(), self.currentIntSpin.value(), 
                                     self.comCombo.currentText(), self.baudCombo.currentText())
        for g in range(0, self.nbGridSpin.value()):                    
            gridDlg = GridDialog(self.iface, self.engine, g)
            gridDlg.show()
            result = gridDlg.exec_()              
            if result == QDialog.Rejected:
                QMessageBox.information(self, 'AGT', 'grid ' + str(g) + ': ' + QApplication.translate(u"ElectDlg",u'Procedure canceled.'))     
                return       
            self.engine.RMDownload()        
        try:
        #    self.engine.RMDownload()
            pass            
        except:       
            QMessageBox.warning(self, 'AGT', QApplication.translate(u"ElecDownDlg",'Unexpected error, procedure stopped.'))
            QMessageBox.warning(self, 'AGT', str(sys.exc_info()[0]))
            return
        QMessageBox.information(self, 'AGT', "Data download completed. data exported in: \n {}".format(self.outputFilename.text())) 
        self.hideDialog()
 
    def hideDialog(self):
         
        self.outputFilename.setText("")
        self.radioButton85.setChecked(True)
        self.radioButton15.setChecked(False)        
        self.nbGridSpin.setValue(1)        
        self.gridSizeSpinX.setValue(30)
        self.gridSizeSpinX.setValue(30)      
        self.nbChannelSpin.setValue(3)
        self.nbProbeSpin.setValue(4)
        self.nbProbeSpin.setValue(0.5)
        self.currentIntSpin.setValue(10)
        self.probeConfigCombo.setCurrentIndex(0)
        index = self.comCombo.findText('COM4')
        if index == -1:
            index = 0
        self.comCombo.setCurrentIndex(index)
        index = self.baudCombo.findText('9600')
        if index == -1:
            index = 0
        self.baudCombo.setCurrentIndex(index)     
        self.hide()