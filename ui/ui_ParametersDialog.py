# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_ParametersDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ParametersDialog(object):
    def setupUi(self, ParametersDialog):
        ParametersDialog.setObjectName("ParametersDialog")
        ParametersDialog.resize(573, 324)
        self.gridLayout_2 = QtWidgets.QGridLayout(ParametersDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget = QtWidgets.QWidget(ParametersDialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.saveButton = QtWidgets.QPushButton(self.widget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_3.addWidget(self.saveButton)
        self.cancelButton = QtWidgets.QPushButton(self.widget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_3.addWidget(self.cancelButton)
        self.gridLayout_2.addWidget(self.widget, 2, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(ParametersDialog)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_enconding = QtWidgets.QLabel(self.widget_2)
        self.label_enconding.setObjectName("label_enconding")
        self.gridLayout.addWidget(self.label_enconding, 0, 0, 1, 1)
        self.comboEncoding = QtWidgets.QComboBox(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboEncoding.sizePolicy().hasHeightForWidth())
        self.comboEncoding.setSizePolicy(sizePolicy)
        self.comboEncoding.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.comboEncoding.setObjectName("comboEncoding")
        self.gridLayout.addWidget(self.comboEncoding, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 1)
        self.widget_3 = QtWidgets.QWidget(ParametersDialog)
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.qgsProjectionSelectionImport = QgsProjectionSelectionWidget(self.widget_3)
        self.qgsProjectionSelectionImport.setObjectName("qgsProjectionSelectionImport")
        self.gridLayout_3.addWidget(self.qgsProjectionSelectionImport, 0, 1, 1, 1)
        self.label_georefscr_2 = QtWidgets.QLabel(self.widget_3)
        self.label_georefscr_2.setObjectName("label_georefscr_2")
        self.gridLayout_3.addWidget(self.label_georefscr_2, 0, 0, 1, 1)
        self.label_georefscr = QtWidgets.QLabel(self.widget_3)
        self.label_georefscr.setObjectName("label_georefscr")
        self.gridLayout_3.addWidget(self.label_georefscr, 1, 0, 1, 1)
        self.qgsProjectionSelectionExport = QgsProjectionSelectionWidget(self.widget_3)
        self.qgsProjectionSelectionExport.setObjectName("qgsProjectionSelectionExport")
        self.gridLayout_3.addWidget(self.qgsProjectionSelectionExport, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.widget_3, 0, 0, 1, 1)

        self.retranslateUi(ParametersDialog)
        QtCore.QMetaObject.connectSlotsByName(ParametersDialog)

    def retranslateUi(self, ParametersDialog):
        _translate = QtCore.QCoreApplication.translate
        ParametersDialog.setWindowTitle(_translate("ParametersDialog", "Default parameters"))
        self.saveButton.setText(_translate("ParametersDialog", "Save"))
        self.cancelButton.setText(_translate("ParametersDialog", "Cancel"))
        self.label_enconding.setText(_translate("ParametersDialog", "Character encoding"))
        self.label_georefscr_2.setText(_translate("ParametersDialog", "Import CRS projection (except MXPDA)"))
        self.label_georefscr.setText(_translate("ParametersDialog", "Export CRS projection"))
from qgsprojectionselectionwidget import QgsProjectionSelectionWidget
