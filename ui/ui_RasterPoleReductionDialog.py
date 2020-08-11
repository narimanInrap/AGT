# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_RasterPoleReductionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AGTRasterPoleReductionDialog(object):
    def setupUi(self, AGTRasterPoleReductionDialog):
        AGTRasterPoleReductionDialog.setObjectName("AGTRasterPoleReductionDialog")
        AGTRasterPoleReductionDialog.resize(451, 210)
        self.gridLayout = QtWidgets.QGridLayout(AGTRasterPoleReductionDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.outputLabel = QtWidgets.QLabel(AGTRasterPoleReductionDialog)
        self.outputLabel.setObjectName("outputLabel")
        self.gridLayout.addWidget(self.outputLabel, 1, 0, 1, 1)
        self.outputFilename = QtWidgets.QLineEdit(AGTRasterPoleReductionDialog)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setObjectName("outputFilename")
        self.gridLayout.addWidget(self.outputFilename, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(AGTRasterPoleReductionDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.ButtonBrowseRaster = QtWidgets.QPushButton(AGTRasterPoleReductionDialog)
        self.ButtonBrowseRaster.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ButtonBrowseRaster.setObjectName("ButtonBrowseRaster")
        self.gridLayout.addWidget(self.ButtonBrowseRaster, 1, 2, 1, 1)
        self.runButton = QtWidgets.QPushButton(AGTRasterPoleReductionDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.runButton.setObjectName("runButton")
        self.gridLayout.addWidget(self.runButton, 5, 2, 1, 1)
        self.rastercomboBox = QtWidgets.QComboBox(AGTRasterPoleReductionDialog)
        self.rastercomboBox.setObjectName("rastercomboBox")
        self.gridLayout.addWidget(self.rastercomboBox, 0, 1, 1, 2)
        self.groupBox_5 = QtWidgets.QGroupBox(AGTRasterPoleReductionDialog)
        self.groupBox_5.setObjectName("groupBox_5")
        self.doubleSpinBox_inclinaison = QtWidgets.QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_inclinaison.setGeometry(QtCore.QRect(230, 20, 62, 22))
        self.doubleSpinBox_inclinaison.setMaximum(90.0)
        self.doubleSpinBox_inclinaison.setProperty("value", 65.0)
        self.doubleSpinBox_inclinaison.setObjectName("doubleSpinBox_inclinaison")
        self.doubleSpinBox_alpha = QtWidgets.QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_alpha.setGeometry(QtCore.QRect(230, 50, 62, 22))
        self.doubleSpinBox_alpha.setObjectName("doubleSpinBox_alpha")
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 71, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_5)
        self.label_7.setGeometry(QtCore.QRect(20, 50, 71, 16))
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.groupBox_5, 3, 0, 1, 3)

        self.retranslateUi(AGTRasterPoleReductionDialog)
        QtCore.QMetaObject.connectSlotsByName(AGTRasterPoleReductionDialog)

    def retranslateUi(self, AGTRasterPoleReductionDialog):
        _translate = QtCore.QCoreApplication.translate
        AGTRasterPoleReductionDialog.setWindowTitle(_translate("AGTRasterPoleReductionDialog", "PoleReduction"))
        self.outputLabel.setText(_translate("AGTRasterPoleReductionDialog", "Raster output"))
        self.label.setText(_translate("AGTRasterPoleReductionDialog", "Select raster layer"))
        self.ButtonBrowseRaster.setText(_translate("AGTRasterPoleReductionDialog", "Browse"))
        self.runButton.setText(_translate("AGTRasterPoleReductionDialog", "Run"))
        self.groupBox_5.setTitle(_translate("AGTRasterPoleReductionDialog", "Field characteristics"))
        self.label_6.setText(_translate("AGTRasterPoleReductionDialog", "Inclinaison"))
        self.label_7.setText(_translate("AGTRasterPoleReductionDialog", "Angle alpha"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AGTRasterPoleReductionDialog = QtWidgets.QDialog()
    ui = Ui_AGTRasterPoleReductionDialog()
    ui.setupUi(AGTRasterPoleReductionDialog)
    AGTRasterPoleReductionDialog.show()
    sys.exit(app.exec_())
