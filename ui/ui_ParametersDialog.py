# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_ParametersDialog.ui'
#
# Created: Thu Apr 05 10:42:44 2018
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ParametersDialog(object):
    def setupUi(self, ParametersDialog):
        ParametersDialog.setObjectName(_fromUtf8("ParametersDialog"))
        ParametersDialog.resize(447, 205)
        self.gridLayout_2 = QtGui.QGridLayout(ParametersDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.widget_3 = QtGui.QWidget(ParametersDialog)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.widget_3)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_georefscr_2 = QtGui.QLabel(self.widget_3)
        self.label_georefscr_2.setObjectName(_fromUtf8("label_georefscr_2"))
        self.gridLayout_3.addWidget(self.label_georefscr_2, 0, 0, 1, 1)
        self.comboCRSImport = QtGui.QComboBox(self.widget_3)
        self.comboCRSImport.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboCRSImport.sizePolicy().hasHeightForWidth())
        self.comboCRSImport.setSizePolicy(sizePolicy)
        self.comboCRSImport.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboCRSImport.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.comboCRSImport.setObjectName(_fromUtf8("comboCRSImport"))
        self.gridLayout_3.addWidget(self.comboCRSImport, 0, 1, 1, 1)
        self.label_georefscr = QtGui.QLabel(self.widget_3)
        self.label_georefscr.setObjectName(_fromUtf8("label_georefscr"))
        self.gridLayout_3.addWidget(self.label_georefscr, 1, 0, 1, 1)
        self.comboCRS = QtGui.QComboBox(self.widget_3)
        self.comboCRS.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboCRS.sizePolicy().hasHeightForWidth())
        self.comboCRS.setSizePolicy(sizePolicy)
        self.comboCRS.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboCRS.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.comboCRS.setObjectName(_fromUtf8("comboCRS"))
        self.gridLayout_3.addWidget(self.comboCRS, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.widget_3, 0, 0, 1, 1)
        self.widget_2 = QtGui.QWidget(ParametersDialog)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout = QtGui.QGridLayout(self.widget_2)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_enconding = QtGui.QLabel(self.widget_2)
        self.label_enconding.setObjectName(_fromUtf8("label_enconding"))
        self.gridLayout.addWidget(self.label_enconding, 0, 0, 1, 1)
        self.comboEncoding = QtGui.QComboBox(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboEncoding.sizePolicy().hasHeightForWidth())
        self.comboEncoding.setSizePolicy(sizePolicy)
        self.comboEncoding.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.comboEncoding.setObjectName(_fromUtf8("comboEncoding"))
        self.gridLayout.addWidget(self.comboEncoding, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 1)
        self.widget = QtGui.QWidget(ParametersDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.saveButton = QtGui.QPushButton(self.widget)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_3.addWidget(self.saveButton)
        self.cancelButton = QtGui.QPushButton(self.widget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_3.addWidget(self.cancelButton)
        self.gridLayout_2.addWidget(self.widget, 2, 0, 1, 1)

        self.retranslateUi(ParametersDialog)
        QtCore.QMetaObject.connectSlotsByName(ParametersDialog)

    def retranslateUi(self, ParametersDialog):
        ParametersDialog.setWindowTitle(_translate("ParametersDialog", "Default parameters", None))
        self.label_georefscr_2.setText(_translate("ParametersDialog", "Import CRS projection (except MXPDA)", None))
        self.label_georefscr.setText(_translate("ParametersDialog", "Export CRS projection", None))
        self.label_enconding.setText(_translate("ParametersDialog", "Character encoding", None))
        self.saveButton.setText(_translate("ParametersDialog", "Save", None))
        self.cancelButton.setText(_translate("ParametersDialog", "Cancel", None))

