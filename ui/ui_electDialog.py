# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_electDialog.ui'
#
# Created: Mon Oct 02 14:59:12 2017
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_AGTElectDialogBase(object):
    def setupUi(self, AGTElectDialogBase):
        AGTElectDialogBase.setObjectName(_fromUtf8("AGTElectDialogBase"))
        AGTElectDialogBase.resize(337, 442)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AGTElectDialogBase.sizePolicy().hasHeightForWidth())
        AGTElectDialogBase.setSizePolicy(sizePolicy)
        AGTElectDialogBase.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.gridLayout = QtGui.QGridLayout(AGTElectDialogBase)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QtGui.QWidget(AGTElectDialogBase)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setEnabled(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.inFileLine = QtGui.QLineEdit(self.widget)
        self.inFileLine.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.inFileLine.setObjectName(_fromUtf8("inFileLine"))
        self.horizontalLayout_4.addWidget(self.inFileLine)
        self.ButtonBrowse = QtGui.QPushButton(self.widget)
        self.ButtonBrowse.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ButtonBrowse.setObjectName(_fromUtf8("ButtonBrowse"))
        self.horizontalLayout_4.addWidget(self.ButtonBrowse)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.widget_2 = QtGui.QWidget(AGTElectDialogBase)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.progressBar = QtGui.QProgressBar(self.widget_2)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout.addWidget(self.progressBar)
        self.allProcess_button = QtGui.QPushButton(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allProcess_button.sizePolicy().hasHeightForWidth())
        self.allProcess_button.setSizePolicy(sizePolicy)
        self.allProcess_button.setObjectName(_fromUtf8("allProcess_button"))
        self.horizontalLayout.addWidget(self.allProcess_button)
        self.gridLayout.addWidget(self.widget_2, 4, 0, 1, 1)
        self.gBox_filter = QtGui.QGroupBox(AGTElectDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gBox_filter.sizePolicy().hasHeightForWidth())
        self.gBox_filter.setSizePolicy(sizePolicy)
        self.gBox_filter.setTitle(_fromUtf8(""))
        self.gBox_filter.setObjectName(_fromUtf8("gBox_filter"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gBox_filter)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.spinBox_maskR = QtGui.QSpinBox(self.gBox_filter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_maskR.sizePolicy().hasHeightForWidth())
        self.spinBox_maskR.setSizePolicy(sizePolicy)
        self.spinBox_maskR.setSuffix(_fromUtf8(""))
        self.spinBox_maskR.setPrefix(_fromUtf8(""))
        self.spinBox_maskR.setMinimum(3)
        self.spinBox_maskR.setMaximum(15)
        self.spinBox_maskR.setSingleStep(2)
        self.spinBox_maskR.setProperty("value", 3)
        self.spinBox_maskR.setObjectName(_fromUtf8("spinBox_maskR"))
        self.gridLayout_3.addWidget(self.spinBox_maskR, 2, 2, 1, 1)
        self.spinBox_mvp = QtGui.QSpinBox(self.gBox_filter)
        self.spinBox_mvp.setSuffix(_fromUtf8(""))
        self.spinBox_mvp.setPrefix(_fromUtf8(""))
        self.spinBox_mvp.setMaximum(100)
        self.spinBox_mvp.setProperty("value", 30)
        self.spinBox_mvp.setObjectName(_fromUtf8("spinBox_mvp"))
        self.gridLayout_3.addWidget(self.spinBox_mvp, 1, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.gBox_filter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 2)
        self.checkBox_filt = QtGui.QCheckBox(self.gBox_filter)
        self.checkBox_filt.setObjectName(_fromUtf8("checkBox_filt"))
        self.gridLayout_3.addWidget(self.checkBox_filt, 0, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.gBox_filter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_3.addWidget(self.label_5, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.gBox_filter, 2, 0, 1, 1)
        self.gBox_Output = QtGui.QGroupBox(AGTElectDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gBox_Output.sizePolicy().hasHeightForWidth())
        self.gBox_Output.setSizePolicy(sizePolicy)
        self.gBox_Output.setObjectName(_fromUtf8("gBox_Output"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gBox_Output)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.outputLabel = QtGui.QLabel(self.gBox_Output)
        self.outputLabel.setObjectName(_fromUtf8("outputLabel"))
        self.gridLayout_2.addWidget(self.outputLabel, 0, 0, 1, 1)
        self.outputFilename = QtGui.QLineEdit(self.gBox_Output)
        self.outputFilename.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.outputFilename.setObjectName(_fromUtf8("outputFilename"))
        self.gridLayout_2.addWidget(self.outputFilename, 0, 1, 1, 2)
        self.label_enconding = QtGui.QLabel(self.gBox_Output)
        self.label_enconding.setObjectName(_fromUtf8("label_enconding"))
        self.gridLayout_2.addWidget(self.label_enconding, 1, 0, 1, 2)
        self.datFilechkbox = QtGui.QCheckBox(self.gBox_Output)
        self.datFilechkbox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.datFilechkbox.setObjectName(_fromUtf8("datFilechkbox"))
        self.gridLayout_2.addWidget(self.datFilechkbox, 2, 0, 1, 3)
        self.comboEncoding = QtGui.QComboBox(self.gBox_Output)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboEncoding.sizePolicy().hasHeightForWidth())
        self.comboEncoding.setSizePolicy(sizePolicy)
        self.comboEncoding.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.comboEncoding.setObjectName(_fromUtf8("comboEncoding"))
        self.gridLayout_2.addWidget(self.comboEncoding, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.gBox_Output, 1, 0, 1, 1)
        self.checkBox_geo = QtGui.QCheckBox(AGTElectDialogBase)
        self.checkBox_geo.setEnabled(True)
        self.checkBox_geo.setObjectName(_fromUtf8("checkBox_geo"))
        self.gridLayout.addWidget(self.checkBox_geo, 3, 0, 1, 1)

        self.retranslateUi(AGTElectDialogBase)
        QtCore.QMetaObject.connectSlotsByName(AGTElectDialogBase)

    def retranslateUi(self, AGTElectDialogBase):
        AGTElectDialogBase.setWindowTitle(_translate("AGTElectDialogBase", "RM15/RM85 processing", None))
        self.label.setText(_translate("AGTElectDialogBase", "Raw data (.dat)", None))
        self.ButtonBrowse.setText(_translate("AGTElectDialogBase", "browse", None))
        self.allProcess_button.setText(_translate("AGTElectDialogBase", "run", None))
        self.label_4.setText(_translate("AGTElectDialogBase", "Median value percentage %   ", None))
        self.checkBox_filt.setText(_translate("AGTElectDialogBase", "Median filter", None))
        self.label_5.setText(_translate("AGTElectDialogBase", "Kernel size      ", None))
        self.gBox_Output.setTitle(_translate("AGTElectDialogBase", "Output files", None))
        self.outputLabel.setText(_translate("AGTElectDialogBase", "Project name", None))
        self.label_enconding.setText(_translate("AGTElectDialogBase", "Character encoding", None))
        self.datFilechkbox.setText(_translate("AGTElectDialogBase", "Export also as .DAT", None))
        self.checkBox_geo.setText(_translate("AGTElectDialogBase", "Georeferencing", None))

