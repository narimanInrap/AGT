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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ..ui.ui_ParametersDialog import Ui_ParametersDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding

class ParametersDialog(QDialog, Ui_ParametersDialog):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ParametersDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)        
        self.iface = iface
        QObject.connect(self.saveButton, SIGNAL('clicked()'), self.saveParams)
        QObject.connect(self.cancelButton, SIGNAL('clicked()'), self.hideDialog)
        self.defaultEncoding = ''
        self.defaultCrsImport = ''
        self.defaultCrsExport = ''        
        self.populateCRS(Utilities.getCRSList())        
        self.populateEncodings(AGTEnconding.getEncodings())
        
    def populateCRS(self, crsNames):
        
        self.comboCRS.clear()
        self.comboCRS.addItems(crsNames)
        self.comboCRSImport.clear()
        self.comboCRSImport.addItems(crsNames)
        self.setDefaultCRSImport()
        self.setDefaultCRSExport()
        
    def setDefaultCRSImport(self):

        index = self.comboCRSImport.findText(self.defaultCrsImport)     
        if index == -1:        
            index = 0  # Make sure some encoding is selected.            
        self.comboCRSImport.setCurrentIndex(index)
    
    def setDefaultCRSExport(self):

        index = self.comboCRS.findText(self.defaultCrsExport)     
        if index == -1:        
            index = 0  # Make sure some encoding is selected.            
        self.comboCRS.setCurrentIndex(index)
    
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
        paramFile.write(self.comboCRSImport.currentText() + '\n')
        paramFile.write(self.comboCRS.currentText() + '\n')
        paramFile.write(self.comboEncoding.currentText() + '\n')       
        paramFile.close()
        msg = QApplication.translate(u"ParamDlg",'Default parameters saved.')            
        QMessageBox.information(self, 'AGT', msg)
        self.hideDialog()
    
    def hideDialog(self):        
        
        self.setDefaultCRSImport()
        self.setDefaultCRSExport()
        self.setDefaultEncoding()  
        self.hide()
    