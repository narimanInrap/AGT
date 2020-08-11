# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_RasterHistoDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AGTRasterHistoDialog(object):
    def setupUi(self, AGTRasterHistoDialog):
        AGTRasterHistoDialog.setObjectName("AGTRasterHistoDialog")
        AGTRasterHistoDialog.resize(497, 263)
        self.gridLayout = QtWidgets.QGridLayout(AGTRasterHistoDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.outputLabel = QtWidgets.QLabel(AGTRasterHistoDialog)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 1, 0, 1, 1)
        self.outputFilename = QtWidgets.QLineEdit(AGTRasterHistoDialog)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setObjectName("outputFilename")
        self.gridLayout.addWidget(self.outputFilename, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(AGTRasterHistoDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.ButtonBrowseRaster = QtWidgets.QPushButton(AGTRasterHistoDialog)
        self.ButtonBrowseRaster.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ButtonBrowseRaster.setObjectName("ButtonBrowseRaster")
        self.gridLayout.addWidget(self.ButtonBrowseRaster, 1, 2, 1, 1)
        self.runButton = QtWidgets.QPushButton(AGTRasterHistoDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 5, 2, 1, 1)
        self.rastercomboBox = QtWidgets.QComboBox(AGTRasterHistoDialog)
        self.rastercomboBox.setObjectName("rastercomboBox")
        self.gridLayout.addWidget(self.rastercomboBox, 0, 1, 1, 2)
        self.unitName = QtWidgets.QLineEdit(AGTRasterHistoDialog)
        self.unitName.setObjectName("unitName")
        self.gridLayout.addWidget(self.unitName, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(AGTRasterHistoDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(AGTRasterHistoDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.spinBox_fontSize = QtWidgets.QSpinBox(AGTRasterHistoDialog)
        self.spinBox_fontSize.setProperty("value", 10)
        self.spinBox_fontSize.setObjectName("spinBox_fontSize")
        self.gridLayout.addWidget(self.spinBox_fontSize, 3, 1, 1, 1)
        self.checkHisto = QtWidgets.QCheckBox(AGTRasterHistoDialog)
        self.checkHisto.setChecked(True)
        self.checkHisto.setObjectName("checkHisto")
        self.gridLayout.addWidget(self.checkHisto, 4, 1, 1, 1)

        self.retranslateUi(AGTRasterHistoDialog)
        QtCore.QMetaObject.connectSlotsByName(AGTRasterHistoDialog)

    def retranslateUi(self, AGTRasterHistoDialog):
        _translate = QtCore.QCoreApplication.translate
        AGTRasterHistoDialog.setWindowTitle(_translate("AGTRasterHistoDialog", "Histogramme"))
        self.outputLabel.setText(_translate("AGTRasterHistoDialog", "Save histogram"))
        self.label.setText(_translate("AGTRasterHistoDialog", "Select raster layer"))
        self.ButtonBrowseRaster.setText(_translate("AGTRasterHistoDialog", "Browse"))
        self.runButton.setText(_translate("AGTRasterHistoDialog", "Run"))
        self.label_2.setText(_translate("AGTRasterHistoDialog", "Unité"))
        self.label_3.setText(_translate("AGTRasterHistoDialog", "FontSize"))
        self.checkHisto.setText(_translate("AGTRasterHistoDialog", "Histogramme"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AGTRasterHistoDialog = QtWidgets.QDialog()
    ui = Ui_AGTRasterHistoDialog()
    ui.setupUi(AGTRasterHistoDialog)
    AGTRasterHistoDialog.show()
    sys.exit(app.exec_())
