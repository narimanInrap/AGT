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
from qgis.gui import QgsMapTool, QgsMapToolEmitPoint

from ..ui.ui_GridDialog import Ui_AGTGridDialog
from ..toolbox.AGTUtilities import Utilities


class GridDialog(QDialog, Ui_AGTGridDialog):
    def __init__(self, iface, engine, grid, parent = None):
        """Constructor."""
        super(GridDialog, self).__init__(parent)        
        self.setupUi(self)
        QObject.connect(self.runButton, SIGNAL('clicked()'), self.run)
        self.iface = iface
        self.engine = engine
        self.grid = grid       
        self.gridLabel.setText(QApplication.translate(u"gridDlg",'grid number ') + str(grid))        

        
    def inputCheck(self):
    
        if (not self.nameSpin.text() or not self.xSpin.text() or not self.ySpin.text()):
            msg = QApplication.translate(u"gridDlg",'Please fill out all fields.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        return True
        
    def run(self):
        
        if not self.inputCheck():
            return False           
        self.engine.grids.extend([self.nameSpin, self.xSpin, self.ySpin])
        self.accept()        
    
                    
        