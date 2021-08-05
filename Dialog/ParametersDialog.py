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

from ..ui.ui_ParametersDialog import Ui_ParametersDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding

class ParametersDialog(QtWidgets.QDialog, Ui_ParametersDialog):
    def __init__(self, parent=None):
        """Constructor."""
        super(ParametersDialog, self).__init__(parent)
        self.setupUi(self)        
#         self.iface = iface
        self.saveButton.clicked.connect(self.saveParams)
        self.cancelButton.clicked.connect(self.hideDialog)
        self.defaultEncoding = ''
        self.defaultCrsImport = ''
        self.defaultCrsExport = ''      
        self.populateEncodings(AGTEnconding.getEncodings())
        
    def setDefaultCRSImport(self):
        
        self.qgsProjectionSelectionImport.setCrs(self.defaultCrsImport)
     
    def setDefaultCRSExport(self):
        
        self.qgsProjectionSelectionExport.setCrs(self.defaultCrsExport)
       
    def populateEncodings(self, names):
        """Populates the combo box of available encodings."""
        
        self.comboEncoding.clear()
        self.comboEncoding.addItems(names)       
        self.setDefaultEncoding()
    
    def setDefaultEncoding(self):
        
        index = self.comboEncoding.findText(self.defaultEncoding)
        if index == -1:
            index = 0  # Make sure some encoding is selected.
        self.comboEncoding.setCurrentIndex(index)
        
    def loadParams(self):
        
        self.defaultCrsImport, self.defaultCrsExport, self.defaultEncoding = Utilities.loadDefaultParameters()
            
    def saveParams(self):
        
        paramFilename = '{}/../param.txt'.format(os.path.dirname(__file__))
        paramFile = codecs.open(paramFilename, 'w', encoding = 'UTF-8')        
        #paramFile = open(paramFilename, 'w', encoding = 'utf-8') pour python 3
        paramFile.write('EPSG:' + str(self.qgsProjectionSelectionImport.crs().postgisSrid()) + '\n')
        paramFile.write('EPSG:' + str(self.qgsProjectionSelectionExport.crs().postgisSrid()) + '\n')
        paramFile.write(self.comboEncoding.currentText() + '\n')       
        paramFile.close()
        msg = QCoreApplication.translate(u"ParamDlg",'Default parameters saved.')            
        QtWidgets.QMessageBox.information(self, 'AGT', msg)
        self.hideDialog()
    
    def hideDialog(self):        
        
        self.setDefaultCRSImport()
        self.setDefaultCRSExport()
        self.setDefaultEncoding()  
        self.hide()
    