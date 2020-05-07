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

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QSettings, QTextCodec, QCoreApplication, Qt

from qgis.gui import QgsMapTool, QgsMapToolEmitPoint

from ..core.AGTEngine import Engine

from ..ui.ui_georefDialog import Ui_AGTGeorefDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding


class GeorefDialog(QtWidgets.QDialog, Ui_AGTGeorefDialog):
    def __init__(self, iface, engine, grid = None, parent = None):
        """Constructor."""
        super(GeorefDialog, self).__init__(parent)        
        self.setupUi(self)
        self.mouseclickPointMap1.pressed.connect(self.button1Checked)
        self.mouseclickPointMap2.pressed.connect(self.button2Checked)
        self.runButton.clicked.connect(self.run)
        self.iface = iface
        self.engine = engine
        self.grid = grid       
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.selectPoint)
        if (grid is not None):      
            self.x1.setText(str(self.engine.getOriginX()[grid]))
            self.y1.setText(str(self.engine.getOriginY()[grid]))
        if (grid is not None):
            self.gridLabel.setText('grid ' + str(engine.getGridNames()[grid]))    
               
    def button1Checked(self):
        
        self.mouseclickPointMap2.setChecked(False)
        
    def button2Checked(self):
        
        self.mouseclickPointMap1.setChecked(False)
                
    def selectPoint(self, point, button):
        
        if self.mouseclickPointMap1.isChecked():
            self.xt1.setText(str(point.x()))
            self.yt1.setText(str(point.y()))
        elif self.mouseclickPointMap2.isChecked():
            self.xt2.setText(str(point.x()))
            self.yt2.setText(str(point.y()))
        self.activateWindow()

    def inputCheck(self):
        """Verifies whether the input is valid."""
        
        if (not self.x1.text() or not self.y1.text() or not self.xt1.text() or not self.yt1.text() or
            not self.x2.text() or not self.y2.text() or not self.xt2.text() or not self.yt2.text()):
            msg = QCoreApplication.translate(u"georefDlg",'Please specify all coordinates.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        try:
            float(self.x1.text())
            float(self.xt1.text())
            float(self.y1.text())
            float(self.yt1.text())
            float(self.x2.text())
            float(self.y2.text())
            float(self.xt2.text())
            float(self.yt2.text())
        except ValueError:
            msg = QCoreApplication.translate(u"georefDlg",'All point coordinates must be floating point numbers.')
            QtWidgets.QMessageBox.warning(self, 'AGT', msg)
            return False
        return True
    
    def run(self):
        
        if not self.inputCheck():
            return False           
        self.engine.georeferencing(self.grid, float(self.x1.text()), float(self.y1.text()), float(self.xt1.text()), float(self.yt1.text()),
                                float(self.x2.text()), float(self.y2.text()), float(self.xt2.text()), float(self.yt2.text()))
        self.accept()
                
