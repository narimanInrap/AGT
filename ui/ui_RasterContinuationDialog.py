# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_RasterContinuationDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AGTRasterContinuationDialog(object):
    def setupUi(self, AGTRasterContinuationDialog):
        AGTRasterContinuationDialog.setObjectName("AGTRasterContinuationDialog")
        AGTRasterContinuationDialog.resize(356, 295)
        self.gridLayout = QtWidgets.QGridLayout(AGTRasterContinuationDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(AGTRasterContinuationDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.radioButton_method_totalfield = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_method_totalfield.setGeometry(QtCore.QRect(110, 30, 95, 20))
        self.radioButton_method_totalfield.setObjectName("radioButton_method_totalfield")
        self.radioButton_method_difference = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_method_difference.setGeometry(QtCore.QRect(230, 30, 95, 20))
        self.radioButton_method_difference.setChecked(True)
        self.radioButton_method_difference.setObjectName("radioButton_method_difference")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 121, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 121, 16))
        self.label_3.setObjectName("label_3")
        self.doubleSpinBox_topclearance = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_topclearance.setGeometry(QtCore.QRect(210, 100, 62, 22))
        self.doubleSpinBox_topclearance.setObjectName("doubleSpinBox_topclearance")
        self.doubleSpinBox_bottomclearance = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_bottomclearance.setGeometry(QtCore.QRect(210, 70, 62, 22))
        self.doubleSpinBox_bottomclearance.setObjectName("doubleSpinBox_bottomclearance")
        self.gridLayout.addWidget(self.groupBox_2, 4, 0, 1, 3)
        self.outputLabel = QtWidgets.QLabel(AGTRasterContinuationDialog)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 1, 0, 1, 1)
        self.outputFilename = QtWidgets.QLineEdit(AGTRasterContinuationDialog)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setObjectName("outputFilename")
        self.gridLayout.addWidget(self.outputFilename, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(AGTRasterContinuationDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.min_value_label = QtWidgets.QLabel(AGTRasterContinuationDialog)
        self.min_value_label.setObjectName("min_value_label")
        self.gridLayout.addWidget(self.min_value_label, 3, 0, 1, 1)
        self.ButtonBrowseRaster = QtWidgets.QPushButton(AGTRasterContinuationDialog)
        self.ButtonBrowseRaster.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ButtonBrowseRaster.setObjectName("ButtonBrowseRaster")
        self.gridLayout.addWidget(self.ButtonBrowseRaster, 1, 2, 1, 1)
        self.runButton = QtWidgets.QPushButton(AGTRasterContinuationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 6, 2, 1, 1)
        self.rastercomboBox = QtWidgets.QComboBox(AGTRasterContinuationDialog)
        self.rastercomboBox.setObjectName("rastercomboBox")
        self.gridLayout.addWidget(self.rastercomboBox, 0, 1, 1, 2)
        self.doubleSpinBox_continuation = QtWidgets.QDoubleSpinBox(AGTRasterContinuationDialog)
        self.doubleSpinBox_continuation.setObjectName("doubleSpinBox_continuation")
        self.gridLayout.addWidget(self.doubleSpinBox_continuation, 3, 2, 1, 1)

        self.retranslateUi(AGTRasterContinuationDialog)
        QtCore.QMetaObject.connectSlotsByName(AGTRasterContinuationDialog)

    def retranslateUi(self, AGTRasterContinuationDialog):
        _translate = QtCore.QCoreApplication.translate
        AGTRasterContinuationDialog.setWindowTitle(_translate("AGTRasterContinuationDialog", "Continuation"))
        self.groupBox_2.setTitle(_translate("AGTRasterContinuationDialog", "Method"))
        self.radioButton_method_totalfield.setText(_translate("AGTRasterContinuationDialog", "Total Field"))
        self.radioButton_method_difference.setText(_translate("AGTRasterContinuationDialog", "Difference"))
        self.label_2.setText(_translate("AGTRasterContinuationDialog", "Bottom clearance"))
        self.label_3.setText(_translate("AGTRasterContinuationDialog", "Top clearance"))
        self.outputLabel.setText(_translate("AGTRasterContinuationDialog", "Raster output"))
        self.label.setText(_translate("AGTRasterContinuationDialog", "Select raster layer"))
        self.min_value_label.setText(_translate("AGTRasterContinuationDialog", "Continuation"))
        self.ButtonBrowseRaster.setText(_translate("AGTRasterContinuationDialog", "Browse"))
        self.runButton.setText(_translate("AGTRasterContinuationDialog", "Run"))
