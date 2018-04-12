# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_rasterDialog.ui'
#
# Created: Wed Mar 28 11:11:59 2018
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

class Ui_AGTRasterDialog(object):
    def setupUi(self, AGTRasterDialog):
        AGTRasterDialog.setObjectName(_fromUtf8("AGTRasterDialog"))
        AGTRasterDialog.resize(417, 572)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AGTRasterDialog.sizePolicy().hasHeightForWidth())
        AGTRasterDialog.setSizePolicy(sizePolicy)
        AGTRasterDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.gridLayout = QtGui.QGridLayout(AGTRasterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QtGui.QWidget(AGTRasterDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.widget)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.inputLabel = QtGui.QLabel(self.widget)
        self.inputLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.inputLabel.setObjectName(_fromUtf8("inputLabel"))
        self.horizontalLayout_6.addWidget(self.inputLabel)
        self.inputShapefile = QtGui.QLineEdit(self.widget)
        self.inputShapefile.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.inputShapefile.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.inputShapefile.setObjectName(_fromUtf8("inputShapefile"))
        self.horizontalLayout_6.addWidget(self.inputShapefile)
        self.BrowseIn = QtGui.QPushButton(self.widget)
        self.BrowseIn.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.BrowseIn.setObjectName(_fromUtf8("BrowseIn"))
        self.horizontalLayout_6.addWidget(self.BrowseIn)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.outputLabel_2 = QtGui.QLabel(self.widget)
        self.outputLabel_2.setObjectName(_fromUtf8("outputLabel_2"))
        self.horizontalLayout_3.addWidget(self.outputLabel_2)
        self.outputFilename = QtGui.QLineEdit(self.widget)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.outputFilename.setObjectName(_fromUtf8("outputFilename"))
        self.horizontalLayout_3.addWidget(self.outputFilename)
        self.browseOut = QtGui.QPushButton(self.widget)
        self.browseOut.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.browseOut.setObjectName(_fromUtf8("browseOut"))
        self.horizontalLayout_3.addWidget(self.browseOut)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.runButton = QtGui.QPushButton(AGTRasterDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.gridLayout.addWidget(self.runButton, 2, 0, 1, 1)
        self.widget_4 = QtGui.QWidget(AGTRasterDialog)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_4)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.widget_4)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.fieldCombo = QtGui.QComboBox(self.widget_4)
        self.fieldCombo.setObjectName(_fromUtf8("fieldCombo"))
        self.gridLayout_2.addWidget(self.fieldCombo, 1, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.widget_4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.cellSizeSpinBox = QtGui.QDoubleSpinBox(self.widget_4)
        self.cellSizeSpinBox.setDecimals(1)
        self.cellSizeSpinBox.setProperty("value", 0.5)
        self.cellSizeSpinBox.setObjectName(_fromUtf8("cellSizeSpinBox"))
        self.horizontalLayout.addWidget(self.cellSizeSpinBox)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.widget_4)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.radiusSpinBox = QtGui.QDoubleSpinBox(self.widget_4)
        self.radiusSpinBox.setDecimals(1)
        self.radiusSpinBox.setProperty("value", 2.0)
        self.radiusSpinBox.setObjectName(_fromUtf8("radiusSpinBox"))
        self.horizontalLayout_2.addWidget(self.radiusSpinBox)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.outputLabel = QtGui.QLabel(self.widget_4)
        self.outputLabel.setTextFormat(QtCore.Qt.AutoText)
        self.outputLabel.setObjectName(_fromUtf8("outputLabel"))
        self.horizontalLayout_4.addWidget(self.outputLabel)
        self.procComboBox = QtGui.QComboBox(self.widget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.procComboBox.sizePolicy().hasHeightForWidth())
        self.procComboBox.setSizePolicy(sizePolicy)
        self.procComboBox.setObjectName(_fromUtf8("procComboBox"))
        self.horizontalLayout_4.addWidget(self.procComboBox)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.widget_4, 1, 0, 1, 1)

        self.retranslateUi(AGTRasterDialog)
        QtCore.QMetaObject.connectSlotsByName(AGTRasterDialog)

    def retranslateUi(self, AGTRasterDialog):
        AGTRasterDialog.setWindowTitle(_translate("AGTRasterDialog", "Interpolation", None))
        self.inputLabel.setText(_translate("AGTRasterDialog", "Input shapefile", None))
        self.BrowseIn.setText(_translate("AGTRasterDialog", "browse", None))
        self.outputLabel_2.setText(_translate("AGTRasterDialog", "Output raster file", None))
        self.browseOut.setText(_translate("AGTRasterDialog", "browse", None))
        self.runButton.setText(_translate("AGTRasterDialog", "run", None))
        self.label.setText(_translate("AGTRasterDialog", "Field", None))
        self.label_2.setText(_translate("AGTRasterDialog", "Cell size", None))
        self.label_3.setText(_translate("AGTRasterDialog", "Search radius", None))
        self.outputLabel.setText(_translate("AGTRasterDialog", "Interpolation process", None))

