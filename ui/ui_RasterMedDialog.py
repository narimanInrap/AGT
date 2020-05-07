# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_RasterMedDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AGTRasterMedDialog(object):
    def setupUi(self, AGTRasterMedDialog):
        AGTRasterMedDialog.setObjectName("AGTRasterMedDialog")
        AGTRasterMedDialog.resize(357, 220)
        self.gridLayout = QtWidgets.QGridLayout(AGTRasterMedDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.outputLabel = QtWidgets.QLabel(AGTRasterMedDialog)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 1, 0, 1, 1)
        self.outputFilename = QtWidgets.QLineEdit(AGTRasterMedDialog)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setObjectName("outputFilename")
        self.gridLayout.addWidget(self.outputFilename, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(AGTRasterMedDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.kernel = QtWidgets.QLabel(AGTRasterMedDialog)
        self.kernel.setObjectName("kernel")
        self.gridLayout.addWidget(self.kernel, 3, 0, 1, 1)
        self.ButtonBrowseRaster = QtWidgets.QPushButton(AGTRasterMedDialog)
        self.ButtonBrowseRaster.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ButtonBrowseRaster.setObjectName("ButtonBrowseRaster")
        self.gridLayout.addWidget(self.ButtonBrowseRaster, 1, 2, 1, 1)
        self.threshold = QtWidgets.QLabel(AGTRasterMedDialog)
        self.threshold.setObjectName("threshold")
        self.gridLayout.addWidget(self.threshold, 5, 0, 1, 1)
        self.runButton = QtWidgets.QPushButton(AGTRasterMedDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 6, 2, 1, 1)
        self.rastercomboBox = QtWidgets.QComboBox(AGTRasterMedDialog)
        self.rastercomboBox.setObjectName("rastercomboBox")
        self.gridLayout.addWidget(self.rastercomboBox, 0, 1, 1, 2)
        self.spinBox_kernel = QtWidgets.QSpinBox(AGTRasterMedDialog)
        self.spinBox_kernel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_kernel.setProperty("value", 3)
        self.spinBox_kernel.setObjectName("spinBox_kernel")
        self.gridLayout.addWidget(self.spinBox_kernel, 3, 2, 1, 1)
        self.spinBox_threshold = QtWidgets.QSpinBox(AGTRasterMedDialog)
        self.spinBox_threshold.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBox_threshold.setProperty("value", 15)
        self.spinBox_threshold.setObjectName("spinBox_threshold")
        self.gridLayout.addWidget(self.spinBox_threshold, 5, 2, 1, 1)

        self.retranslateUi(AGTRasterMedDialog)
        QtCore.QMetaObject.connectSlotsByName(AGTRasterMedDialog)

    def retranslateUi(self, AGTRasterMedDialog):
        _translate = QtCore.QCoreApplication.translate
        AGTRasterMedDialog.setWindowTitle(_translate("AGTRasterMedDialog", "Raster median process"))
        self.outputLabel.setText(_translate("AGTRasterMedDialog", " Raster output"))
        self.label.setText(_translate("AGTRasterMedDialog", "Select raster layer"))
        self.kernel.setText(_translate("AGTRasterMedDialog", "Window size"))
        self.ButtonBrowseRaster.setText(_translate("AGTRasterMedDialog", "browse"))
        self.threshold.setText(_translate("AGTRasterMedDialog", "Threshold"))
        self.runButton.setText(_translate("AGTRasterMedDialog", "run"))
