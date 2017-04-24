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

from PyQt4 import QtGui
from fileinput import filename

class FileDeletionError(Exception):
    """Exception raised when a file can't be deleted."""
    
    def __init__(self, fileName):
        self.fileName = fileName
        self.message = self.__str__()
        
    def __str__(self):
        msg = QtGui.QApplication.translate("Exceptions","Error deleting Shapefile {}.", None, QtGui.QApplication.UnicodeUTF8)
        return msg.format(repr(self.fileName))

class NoFeatureCreatedError(Exception):
    """Exception raised when no feature were created"""
    
    def __init__(self, filename):
        self.filename = filename
        self.message = self.__str__()
    
    def __str__(self):
        msg = QtGui.QApplication.translate("Exceptions", "No feature was created. The shapefile was deleted {}.\n", None, QtGui.QApplication.UnicodeUTF8)
        return msg.format(self.filename)

class ParserError(Exception):
    """Exception raised when there are errors reading input raw data."""
    
    def __init__(self, filename, msg):
        self.filename = filename
        self.message = self.__str__() + msg
        
    def __str__(self):
        msg = QtGui.QApplication.translate("Exceptions", "Error reading {}.\n", None, QtGui.QApplication.UnicodeUTF8)
        return msg.format(self.filename)
