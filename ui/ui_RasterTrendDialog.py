# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_RasterTrendDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AGTRasterTrendDialog(object):
    def setupUi(self, AGTRasterTrendDialog):
        AGTRasterTrendDialog.setObjectName("AGTRasterTrendDialog")
        AGTRasterTrendDialog.resize(356, 295)
        self.gridLayout = QtWidgets.QGridLayout(AGTRasterTrendDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.outputLabel = QtWidgets.QLabel(AGTRasterTrendDialog)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 1, 0, 1, 1)
        self.outputFilename = QtWidgets.QLineEdit(AGTRasterTrendDialog)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setObjectName("outputFilename")
        self.gridLayout.addWidget(self.outputFilename, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(AGTRasterTrendDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.min_value_label = QtWidgets.QLabel(AGTRasterTrendDialog)
        self.min_value_label.setObjectName("min_value_label")
        self.gridLayout.addWidget(self.min_value_label, 3, 0, 1, 1)
        self.ButtonBrowseRaster = QtWidgets.QPushButton(AGTRasterTrendDialog)
        self.ButtonBrowseRaster.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ButtonBrowseRaster.setObjectName("ButtonBrowseRaster")
        self.gridLayout.addWidget(self.ButtonBrowseRaster, 1, 2, 1, 1)
        self.runButton = QtWidgets.QPushButton(AGTRasterTrendDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 7, 2, 1, 1)
        self.spinBox_kernelTrend = QtWidgets.QSpinBox(AGTRasterTrendDialog)
        self.spinBox_kernelTrend.setMaximum(2000)
        self.spinBox_kernelTrend.setProperty("value", 3)
        self.spinBox_kernelTrend.setObjectName("spinBox_kernelTrend")
        self.gridLayout.addWidget(self.spinBox_kernelTrend, 3, 2, 1, 1)
        self.rastercomboBox = QtWidgets.QComboBox(AGTRasterTrendDialog)
        self.rastercomboBox.setObjectName("rastercomboBox")
        self.gridLayout.addWidget(self.rastercomboBox, 0, 1, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(AGTRasterTrendDialog)
        self.groupBox.setObjectName("groupBox")
        self.radioButton_comp_local = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_comp_local.setGeometry(QtCore.QRect(110, 30, 95, 20))
        self.radioButton_comp_local.setObjectName("radioButton_comp_local")
        self.radioButton_comp_regional = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_comp_regional.setGeometry(QtCore.QRect(230, 30, 95, 20))
        self.radioButton_comp_regional.setChecked(True)
        self.radioButton_comp_regional.setObjectName("radioButton_comp_regional")
        self.gridLayout.addWidget(self.groupBox, 5, 0, 1, 3)
        self.groupBox_2 = QtWidgets.QGroupBox(AGTRasterTrendDialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.radioButton_method_relative = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_method_relative.setGeometry(QtCore.QRect(110, 30, 95, 20))
        self.radioButton_method_relative.setObjectName("radioButton_method_relative")
        self.radioButton_method_absolue = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_method_absolue.setGeometry(QtCore.QRect(230, 30, 95, 20))
        self.radioButton_method_absolue.setChecked(True)
        self.radioButton_method_absolue.setObjectName("radioButton_method_absolue")
        self.gridLayout.addWidget(self.groupBox_2, 4, 0, 1, 3)

        self.retranslateUi(AGTRasterTrendDialog)
        QtCore.QMetaObject.connectSlotsByName(AGTRasterTrendDialog)

    def retranslateUi(self, AGTRasterTrendDialog):
        _translate = QtCore.QCoreApplication.translate
        AGTRasterTrendDialog.setWindowTitle(_translate("AGTRasterTrendDialog", "Trend Removal"))
        self.outputLabel.setText(_translate("AGTRasterTrendDialog", "Raster output"))
        self.label.setText(_translate("AGTRasterTrendDialog", "Select raster layer"))
        self.min_value_label.setText(_translate("AGTRasterTrendDialog", "Kernel size (pixel)"))
        self.ButtonBrowseRaster.setText(_translate("AGTRasterTrendDialog", "Browse"))
        self.runButton.setText(_translate("AGTRasterTrendDialog", "Run"))
        self.groupBox.setTitle(_translate("AGTRasterTrendDialog", "Composante"))
        self.radioButton_comp_local.setText(_translate("AGTRasterTrendDialog", "Local"))
        self.radioButton_comp_regional.setText(_translate("AGTRasterTrendDialog", "Régional"))
        self.groupBox_2.setTitle(_translate("AGTRasterTrendDialog", "Method"))
        self.radioButton_method_relative.setText(_translate("AGTRasterTrendDialog", "Relative"))
        self.radioButton_method_absolue.setText(_translate("AGTRasterTrendDialog", "Asolue"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AGTRasterTrendDialog = QtWidgets.QDialog()
    ui = Ui_AGTRasterTrendDialog()
    ui.setupUi(AGTRasterTrendDialog)
    AGTRasterTrendDialog.show()
    sys.exit(app.exec_())
