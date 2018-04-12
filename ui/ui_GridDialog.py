# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_GridDialog.ui'
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

class Ui_AGTGridDialog(object):
    def setupUi(self, AGTGridDialog):
        AGTGridDialog.setObjectName(_fromUtf8("AGTGridDialog"))
        AGTGridDialog.resize(373, 217)
        self.gridLayout_2 = QtGui.QGridLayout(AGTGridDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLabel = QtGui.QLabel(AGTGridDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.gridLabel.setFont(font)
        self.gridLabel.setText(_fromUtf8(""))
        self.gridLabel.setObjectName(_fromUtf8("gridLabel"))
        self.gridLayout_2.addWidget(self.gridLabel, 0, 0, 1, 1)
        self.widget_2 = QtGui.QWidget(AGTGridDialog)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout = QtGui.QGridLayout(self.widget_2)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.widget_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.widget_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.nameSpin = QtGui.QSpinBox(self.widget_2)
        self.nameSpin.setObjectName(_fromUtf8("nameSpin"))
        self.gridLayout.addWidget(self.nameSpin, 1, 1, 1, 1)
        self.xSpin = QtGui.QDoubleSpinBox(self.widget_2)
        self.xSpin.setObjectName(_fromUtf8("xSpin"))
        self.gridLayout.addWidget(self.xSpin, 2, 1, 1, 1)
        self.ySpin = QtGui.QDoubleSpinBox(self.widget_2)
        self.ySpin.setObjectName(_fromUtf8("ySpin"))
        self.gridLayout.addWidget(self.ySpin, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 1)
        self.widget = QtGui.QWidget(AGTGridDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.runButton = QtGui.QPushButton(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runButton.sizePolicy().hasHeightForWidth())
        self.runButton.setSizePolicy(sizePolicy)
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.horizontalLayout.addWidget(self.runButton)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addWidget(self.widget, 2, 0, 1, 1)

        self.retranslateUi(AGTGridDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AGTGridDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AGTGridDialog)

    def retranslateUi(self, AGTGridDialog):
        AGTGridDialog.setWindowTitle(_translate("AGTGridDialog", "Grid Dialog", None))
        self.label_2.setText(_translate("AGTGridDialog", "Grid\'s first point X coordinate", None))
        self.label.setText(_translate("AGTGridDialog", "Grid\'s name (number)", None))
        self.label_3.setText(_translate("AGTGridDialog", "Grid\'s first point Y coordinate", None))
        self.runButton.setText(_translate("AGTGridDialog", "Apply", None))

