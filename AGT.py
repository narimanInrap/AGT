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

import os.path

# Import the PyQt and QGIS libraries
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the dialog
from .Dialog.ElectDialog import ElectDialog
from .Dialog.MagDialog import MagDialog
#from Dialog.ElecDownDialog import ElecDownDialog
from .Dialog.EM31Dialog import EM31Dialog
from .Dialog.MagGridDialog import MagGridDialog
from .Dialog.ParametersDialog import ParametersDialog
from .Dialog.GEM2Dialog import GEM2Dialog
from .Dialog.RasterMedDialog import RasterMedDialog
from .Dialog.InterpolateurDialog import InterpolateurDialog

class AGT:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale              
        locale = QSettings().value('locale/userLocale')[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'AGT_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ElectDialog(self.iface)
        self.magDlg = MagDialog()
        self.em31Dlg = EM31Dialog()
        #self.elecDownDlg = ElecDownDialog()
        self.magGridDlg = MagGridDialog(self.iface)
        self.paramDlg = ParametersDialog()
        self.gem2Dlg = GEM2Dialog()
        self.rasterMedDlg = RasterMedDialog(self.iface)
        self.interpDlg = InterpolateurDialog(self.iface)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&AGT')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AGT')
        self.toolbar.setObjectName(u'AGT')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate(u"AGT", message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        
#         icon_path = ':/plugins/AGT/icons/download_icon.png'
#         self.add_action(
#             icon_path,
#             text=self.tr(u'RM15/RM85 download'),
#             callback=self.runElecDown,
#             parent=self.iface.mainWindow())        

        icon_path = ':/plugins/AGT/icons/elec_icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'RM15/RM85 processing'),
            callback=self.runElec,
            parent=self.iface.mainWindow())
        
        icon_path = ':/plugins/AGT/icons/magGrid_icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'MXPDA/Grad601 processing - Grid survey'),
            callback=self.runMagGrid,
            parent=self.iface.mainWindow())
        
        icon_path = ':/plugins/AGT/icons/mag_icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'MXPDA processing - GNSS survey'),
            callback=self.runMag,
            parent=self.iface.mainWindow())
        
        icon_path = ':/plugins/AGT/icons/em31_icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'EM31 processing'),
            callback=self.runEM31,
            parent=self.iface.mainWindow())
     
        icon_path = ':/plugins/AGT/icons/GEM2_icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GEM2/EMP400 processing'),
            callback=self.runGEM2,
            parent=self.iface.mainWindow())
        
        icon_path = ':/plugins/AGT/icons/interpolator_icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Interpolator'),
            callback=self.runInterpolateur,
            parent=self.iface.mainWindow())     
        icon_path = ':/plugins/AGT/icons/rasterMed_icon.png'
        
        self.add_action(
            icon_path,
            text=self.tr(u'Raster med processing'),
            callback=self.runRasterMed,
            parent=self.iface.mainWindow())        
                   
        icon_path = ':/plugins/AGT/icons/param_icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Default parameters'),
            callback=self.parameters,
            parent=self.iface.mainWindow(),
            add_to_toolbar = True)  
              
        icon_path = ':/plugins/AGT/icons/help.svg'        
        self.add_action(
            icon_path,
            text=self.tr(u'help'),
            callback=self.help,
            parent=self.iface.mainWindow(),
            add_to_toolbar = False)
        # separator
        self.toolbar.addSeparator()
        
    def help(self):
        if QCoreApplication.translate(u"AGT", "help") == "aide":
            help_file = "file:///{}/help/build/html/fr/index.html".format(os.path.dirname(__file__))
        else:
            help_file = "file:///{}/help/build/html/en/index.html".format(os.path.dirname(__file__)) 
        QDesktopServices().openUrl(QUrl(help_file))
        
    def parameters(self):
        
        self.paramDlg.loadParams()
        self.paramDlg.setDefaultEncoding()
        self.paramDlg.setDefaultCRSImport()        
        self.paramDlg.setDefaultCRSExport()
        self.paramDlg.show()
        self.paramDlg.exec_()              
        
    
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&AGT'),
                action)
            self.iface.removeToolBarIcon(action)


    def runElec(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        else:
            self.dlg.hideDialog()
    
    def runMag(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.magDlg.show()        
        self.magDlg.setDefaultCRS()
        # Run the dialog event loop
        result = self.magDlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        else:
            self.magDlg.hideDialog()
            
    def runMagGrid(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.magGridDlg.show()
        # Run the dialog event loop
        result = self.magGridDlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        else:
            self.magGridDlg.hideDialog()
    
#     def runElecDown(self):
#         """Run method that performs all the real work"""
#         # show the dialog
#         self.elecDownDlg.show()
#         # Run the dialog event loop
#         result = self.elecDownDlg.exec_()
#         # See if OK was pressed
#         if result:
#             # Do something useful here - delete the line containing pass and
#             # substitute with your code.
#             pass
#         else:
#             self.elecDownDlg.hideDialog()
    
    def runEM31(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.em31Dlg.show()
        # Run the dialog event loop
        self.em31Dlg.setDefaultCRSImport()        
        self.em31Dlg.setDefaultCRSExport()
        result = self.em31Dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        else:
            self.em31Dlg.hideDialog()
    
    def runGEM2(self):
        # show the dialog
        self.gem2Dlg.show()
        # Run the dialog event loop
        self.gem2Dlg.setDefaultCRSImport()
        self.gem2Dlg.setDefaultCRSExport()
        result = self.gem2Dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        else:
            self.gem2Dlg.hideDialog() 
             
    def runRasterMed(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.rasterMedDlg.show()
        self.rasterMedDlg.populateProc()
        # Run the dialog event loop
        result = self.rasterMedDlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        else:
            self.rasterMedDlg.hideDialog()

    def runInterpolateur(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.interpDlg.show()
        self.interpDlg.populateProc()
        # Run the dialog event loop
        result = self.interpDlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        else:
            self.interpDlg.hideDialog()       


