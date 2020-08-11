# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_RasterDestripeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AGTRasterDestripeDialog(object):
    def setupUi(self, AGTRasterDestripeDialog):
        AGTRasterDestripeDialog.setObjectName("AGTRasterDestripeDialog")
        AGTRasterDestripeDialog.resize(357, 243)
        self.gridLayout = QtWidgets.QGridLayout(AGTRasterDestripeDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.outputFilename = QtWidgets.QLineEdit(AGTRasterDestripeDialog)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setObjectName("outputFilename")
        self.gridLayout.addWidget(self.outputFilename, 1, 1, 1, 1)
        self.outputLabel = QtWidgets.QLabel(AGTRasterDestripeDialog)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 1, 0, 1, 1)
        self.rastercomboBox = QtWidgets.QComboBox(AGTRasterDestripeDialog)
        self.rastercomboBox.setObjectName("rastercomboBox")
        self.gridLayout.addWidget(self.rastercomboBox, 0, 1, 1, 2)
        self.min_value_label = QtWidgets.QLabel(AGTRasterDestripeDialog)
        self.min_value_label.setObjectName("min_value_label")
        self.gridLayout.addWidget(self.min_value_label, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(AGTRasterDestripeDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.ButtonBrowseRaster = QtWidgets.QPushButton(AGTRasterDestripeDialog)
        self.ButtonBrowseRaster.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ButtonBrowseRaster.setObjectName("ButtonBrowseRaster")
        self.gridLayout.addWidget(self.ButtonBrowseRaster, 1, 2, 1, 1)
        self.runButton = QtWidgets.QPushButton(AGTRasterDestripeDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 7, 2, 1, 1)
        self.max_value_label = QtWidgets.QLabel(AGTRasterDestripeDialog)
        self.max_value_label.setObjectName("max_value_label")
        self.gridLayout.addWidget(self.max_value_label, 5, 0, 1, 1)
        self.spinBox_rotation = QtWidgets.QSpinBox(AGTRasterDestripeDialog)
        self.spinBox_rotation.setMinimum(-360)
        self.spinBox_rotation.setMaximum(360)
        self.spinBox_rotation.setProperty("value", -45)
        self.spinBox_rotation.setObjectName("spinBox_rotation")
        self.gridLayout.addWidget(self.spinBox_rotation, 6, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(AGTRasterDestripeDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.spinBox_freqcut = QtWidgets.QSpinBox(AGTRasterDestripeDialog)
        self.spinBox_freqcut.setMaximum(50000)
        self.spinBox_freqcut.setProperty("value", 200)
        self.spinBox_freqcut.setObjectName("spinBox_freqcut")
        self.gridLayout.addWidget(self.spinBox_freqcut, 5, 2, 1, 1)
        self.spinBox_widness = QtWidgets.QSpinBox(AGTRasterDestripeDialog)
        self.spinBox_widness.setProperty("value", 3)
        self.spinBox_widness.setObjectName("spinBox_widness")
        self.gridLayout.addWidget(self.spinBox_widness, 3, 2, 1, 1)

        self.retranslateUi(AGTRasterDestripeDialog)
        QtCore.QMetaObject.connectSlotsByName(AGTRasterDestripeDialog)

    def retranslateUi(self, AGTRasterDestripeDialog):
        _translate = QtCore.QCoreApplication.translate
        AGTRasterDestripeDialog.setWindowTitle(_translate("AGTRasterDestripeDialog", "Raster destripping filtering"))
        self.outputLabel.setText(_translate("AGTRasterDestripeDialog", "Raster output"))
        self.min_value_label.setText(_translate("AGTRasterDestripeDialog", "Largeur"))
        self.label.setText(_translate("AGTRasterDestripeDialog", "Select raster layer"))
        self.ButtonBrowseRaster.setText(_translate("AGTRasterDestripeDialog", "Browse"))
        self.runButton.setText(_translate("AGTRasterDestripeDialog", "Run"))
        self.max_value_label.setText(_translate("AGTRasterDestripeDialog", "Fréquence de coupure"))
        self.label_2.setText(_translate("AGTRasterDestripeDialog", "Angle"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AGTRasterDestripeDialog = QtWidgets.QDialog()
    ui = Ui_AGTRasterDestripeDialog()
    ui.setupUi(AGTRasterDestripeDialog)
    AGTRasterDestripeDialog.show()
    sys.exit(app.exec_())
