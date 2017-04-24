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

from ..core.AGTEngine import Engine

from ..ui.ui_georefDialog import Ui_AGTGeorefDialog
from ..toolbox.AGTUtilities import Utilities, AGTEnconding


class GeorefDialog(QDialog, Ui_AGTGeorefDialog):
    def __init__(self, iface, engine, grid, parent = None):
        """Constructor."""
        super(GeorefDialog, self).__init__(parent)        
        self.setupUi(self)
        QObject.connect(self.mouseclickPointMap1, SIGNAL('pressed()'), self.button1Checked)
        QObject.connect(self.mouseclickPointMap2, SIGNAL('pressed()'), self.button2Checked)    
        QObject.connect(self.runButton, SIGNAL('clicked()'), self.run)
        #QObject.connect(self., QtCore.SIGNAL(_fromUtf8("accepted()")), Ui_AGTGeorefDialog.AGTGeorefDialog.accept)
        self.iface = iface
        self.engine = engine
        self.grid = grid       
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())
        self.iface.mapCanvas().setMapTool(self.clickTool)
        self.clickTool.canvasClicked.connect(self.selectPoint)        
        self.x1.setText(str(self.engine.getOriginX()[grid]))
        self.y1.setText(str(self.engine.getOriginY()[grid]))
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
            msg = QApplication.translate(u"georefDlg",'Please specify all coordinates.')
            QMessageBox.warning(self, 'AGT', msg)
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
            msg = QApplication.translate(u"georefDlg",'All point coordinates must be floating point numbers.')
            QMessageBox.warning(self, 'AGT', msg)
            return False
        return True
    
    def run(self):
        
        if not self.inputCheck():
            return False           
        self.engine.georeferencing(self.grid, float(self.x1.text()), float(self.y1.text()), float(self.xt1.text()), float(self.yt1.text()),
                                float(self.x2.text()), float(self.y2.text()), float(self.xt2.text()), float(self.yt2.text()))
        self.accept()
                
