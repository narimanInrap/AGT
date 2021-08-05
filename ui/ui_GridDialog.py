# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_GridDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AGTGridDialog(object):
    def setupUi(self, AGTGridDialog):
        AGTGridDialog.setObjectName("AGTGridDialog")
        AGTGridDialog.resize(373, 217)
        self.gridLayout_2 = QtWidgets.QGridLayout(AGTGridDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLabel = QtWidgets.QLabel(AGTGridDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.gridLabel.setFont(font)
        self.gridLabel.setText("")
        self.gridLabel.setObjectName("gridLabel")
        self.gridLayout_2.addWidget(self.gridLabel, 0, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(AGTGridDialog)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.nameSpin = QtWidgets.QSpinBox(self.widget_2)
        self.nameSpin.setObjectName("nameSpin")
        self.gridLayout.addWidget(self.nameSpin, 1, 1, 1, 1)
        self.xSpin = QtWidgets.QDoubleSpinBox(self.widget_2)
        self.xSpin.setObjectName("xSpin")
        self.gridLayout.addWidget(self.xSpin, 2, 1, 1, 1)
        self.ySpin = QtWidgets.QDoubleSpinBox(self.widget_2)
        self.ySpin.setObjectName("ySpin")
        self.gridLayout.addWidget(self.ySpin, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 1)
        self.widget = QtWidgets.QWidget(AGTGridDialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.runButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setObjectName("runButton")
        self.horizontalLayout.addWidget(self.runButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addWidget(self.widget, 2, 0, 1, 1)

        self.retranslateUi(AGTGridDialog)
        self.buttonBox.rejected.connect(AGTGridDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AGTGridDialog)

    def retranslateUi(self, AGTGridDialog):
        _translate = QtCore.QCoreApplication.translate
        AGTGridDialog.setWindowTitle(_translate("AGTGridDialog", "Grid Dialog"))
        self.label_2.setText(_translate("AGTGridDialog", "Grid\'s first point X coordinate"))
        self.label.setText(_translate("AGTGridDialog", "Grid\'s name (number)"))
        self.label_3.setText(_translate("AGTGridDialog", "Grid\'s first point Y coordinate"))
        self.runButton.setText(_translate("AGTGridDialog", "Apply"))

