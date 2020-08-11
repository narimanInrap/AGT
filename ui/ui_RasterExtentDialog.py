# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_RasterExtentDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AGTRasterExtentDialog(object):
    def setupUi(self, AGTRasterExtentDialog):
        AGTRasterExtentDialog.setObjectName("AGTRasterExtentDialog")
        AGTRasterExtentDialog.resize(446, 221)
        self.gridLayout = QtWidgets.QGridLayout(AGTRasterExtentDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.outputLabel = QtWidgets.QLabel(AGTRasterExtentDialog)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 1, 0, 1, 1)
        self.outputFilename = QtWidgets.QLineEdit(AGTRasterExtentDialog)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setObjectName("outputFilename")
        self.gridLayout.addWidget(self.outputFilename, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(AGTRasterExtentDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.min_value_label = QtWidgets.QLabel(AGTRasterExtentDialog)
        self.min_value_label.setObjectName("min_value_label")
        self.gridLayout.addWidget(self.min_value_label, 3, 0, 1, 1)
        self.ButtonBrowseRaster = QtWidgets.QPushButton(AGTRasterExtentDialog)
        self.ButtonBrowseRaster.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ButtonBrowseRaster.setObjectName("ButtonBrowseRaster")
        self.gridLayout.addWidget(self.ButtonBrowseRaster, 1, 2, 1, 1)
        self.runButton = QtWidgets.QPushButton(AGTRasterExtentDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 6, 2, 1, 1)
        self.rastercomboBox = QtWidgets.QComboBox(AGTRasterExtentDialog)
        self.rastercomboBox.setObjectName("rastercomboBox")
        self.gridLayout.addWidget(self.rastercomboBox, 0, 1, 1, 2)
        self.checkBox_zeroExtent = QtWidgets.QCheckBox(AGTRasterExtentDialog)
        self.checkBox_zeroExtent.setObjectName("checkBox_zeroExtent")
        self.gridLayout.addWidget(self.checkBox_zeroExtent, 5, 2, 1, 1)
        self.spinBox_kernelLimit = QtWidgets.QSpinBox(AGTRasterExtentDialog)
        self.spinBox_kernelLimit.setMaximum(2000)
        self.spinBox_kernelLimit.setProperty("value", 3)
        self.spinBox_kernelLimit.setObjectName("spinBox_kernelLimit")
        self.gridLayout.addWidget(self.spinBox_kernelLimit, 3, 2, 1, 1)

        self.retranslateUi(AGTRasterExtentDialog)
        QtCore.QMetaObject.connectSlotsByName(AGTRasterExtentDialog)

    def retranslateUi(self, AGTRasterExtentDialog):
        _translate = QtCore.QCoreApplication.translate
        AGTRasterExtentDialog.setWindowTitle(_translate("AGTRasterExtentDialog", "Cropping raster extent"))
        self.outputLabel.setText(_translate("AGTRasterExtentDialog", "Raster output"))
        self.label.setText(_translate("AGTRasterExtentDialog", "Select raster layer"))
        self.min_value_label.setText(_translate("AGTRasterExtentDialog", "Cropping widness"))
        self.ButtonBrowseRaster.setText(_translate("AGTRasterExtentDialog", "Browse"))
        self.runButton.setText(_translate("AGTRasterExtentDialog", "Run"))
        self.checkBox_zeroExtent.setText(_translate("AGTRasterExtentDialog", "0 as dummy"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AGTRasterExtentDialog = QtWidgets.QDialog()
    ui = Ui_AGTRasterExtentDialog()
    ui.setupUi(AGTRasterExtentDialog)
    AGTRasterExtentDialog.show()
    sys.exit(app.exec_())
