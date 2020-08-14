# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_RasterClipDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AGTRasterClipDialog(object):
    def setupUi(self, AGTRasterClipDialog):
        AGTRasterClipDialog.setObjectName("AGTRasterClipDialog")
        AGTRasterClipDialog.resize(357, 220)
        self.gridLayout = QtWidgets.QGridLayout(AGTRasterClipDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.outputLabel = QtWidgets.QLabel(AGTRasterClipDialog)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 1, 0, 1, 1)
        self.outputFilename = QtWidgets.QLineEdit(AGTRasterClipDialog)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setObjectName("outputFilename")
        self.gridLayout.addWidget(self.outputFilename, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(AGTRasterClipDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.min_value_label = QtWidgets.QLabel(AGTRasterClipDialog)
        self.min_value_label.setObjectName("min_value_label")
        self.gridLayout.addWidget(self.min_value_label, 3, 0, 1, 1)
        self.ButtonBrowseRaster = QtWidgets.QPushButton(AGTRasterClipDialog)
        self.ButtonBrowseRaster.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ButtonBrowseRaster.setObjectName("ButtonBrowseRaster")
        self.gridLayout.addWidget(self.ButtonBrowseRaster, 1, 2, 1, 1)
        self.max_value_label = QtWidgets.QLabel(AGTRasterClipDialog)
        self.max_value_label.setObjectName("max_value_label")
        self.gridLayout.addWidget(self.max_value_label, 5, 0, 1, 1)
        self.runButton = QtWidgets.QPushButton(AGTRasterClipDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 6, 2, 1, 1)
        self.rastercomboBox = QtWidgets.QComboBox(AGTRasterClipDialog)
        self.rastercomboBox.setObjectName("rastercomboBox")
        self.gridLayout.addWidget(self.rastercomboBox, 0, 1, 1, 2)
        self.doubleSpinBox_min_value = QtWidgets.QDoubleSpinBox(AGTRasterClipDialog)
        self.doubleSpinBox_min_value.setMinimum(-1000000.0)
        self.doubleSpinBox_min_value.setMaximum(1000000.0)
        self.doubleSpinBox_min_value.setProperty("value", -100.0)
        self.doubleSpinBox_min_value.setObjectName("doubleSpinBox_min_value")
        self.gridLayout.addWidget(self.doubleSpinBox_min_value, 3, 2, 1, 1)
        self.doubleSpinBox_max_value = QtWidgets.QDoubleSpinBox(AGTRasterClipDialog)
        self.doubleSpinBox_max_value.setMaximum(1000000.0)
        self.doubleSpinBox_max_value.setProperty("value", 100.0)
        self.doubleSpinBox_max_value.setObjectName("doubleSpinBox_max_value")
        self.gridLayout.addWidget(self.doubleSpinBox_max_value, 5, 2, 1, 1)

        self.retranslateUi(AGTRasterClipDialog)
        QtCore.QMetaObject.connectSlotsByName(AGTRasterClipDialog)

    def retranslateUi(self, AGTRasterClipDialog):
        _translate = QtCore.QCoreApplication.translate
        AGTRasterClipDialog.setWindowTitle(_translate("AGTRasterClipDialog", "Raster clipping value"))
        self.outputLabel.setText(_translate("AGTRasterClipDialog", "Raster output"))
        self.label.setText(_translate("AGTRasterClipDialog", "Select raster layer"))
        self.min_value_label.setText(_translate("AGTRasterClipDialog", "Minimum value"))
        self.ButtonBrowseRaster.setText(_translate("AGTRasterClipDialog", "Browse"))
        self.max_value_label.setText(_translate("AGTRasterClipDialog", "Maximum value"))
        self.runButton.setText(_translate("AGTRasterClipDialog", "Run"))
