# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Pump2_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1006, 724)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gb_Input = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gb_Input.sizePolicy().hasHeightForWidth())
        self.gb_Input.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.gb_Input.setFont(font)
        self.gb_Input.setObjectName("gb_Input")
        self.gridLayout = QtWidgets.QGridLayout(self.gb_Input)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_PHigh = QtWidgets.QLabel(self.gb_Input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_PHigh.sizePolicy().hasHeightForWidth())
        self.lbl_PHigh.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lbl_PHigh.setFont(font)
        self.lbl_PHigh.setObjectName("lbl_PHigh")
        self.gridLayout.addWidget(self.lbl_PHigh, 0, 0, 1, 1)
        self.btn_Calculate = QtWidgets.QPushButton(self.gb_Input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Calculate.sizePolicy().hasHeightForWidth())
        self.btn_Calculate.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_Calculate.setFont(font)
        self.btn_Calculate.setObjectName("btn_Calculate")
        self.gridLayout.addWidget(self.btn_Calculate, 1, 1, 1, 1)
        self.le_PHigh = QtWidgets.QLineEdit(self.gb_Input)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_PHigh.sizePolicy().hasHeightForWidth())
        self.le_PHigh.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_PHigh.setFont(font)
        self.le_PHigh.setText("")
        self.le_PHigh.setClearButtonEnabled(True)
        self.le_PHigh.setObjectName("le_PHigh")
        self.gridLayout.addWidget(self.le_PHigh, 0, 1, 1, 2)
        self.verticalLayout_2.addWidget(self.gb_Input)
        self.gb_Output = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gb_Output.sizePolicy().hasHeightForWidth())
        self.gb_Output.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.gb_Output.setFont(font)
        self.gb_Output.setObjectName("gb_Output")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gb_Output)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.le_P2 = QtWidgets.QLineEdit(self.gb_Output)
        self.le_P2.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_P2.setFont(font)
        self.le_P2.setObjectName("le_P2")
        self.gridLayout_2.addWidget(self.le_P2, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gb_Output)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.gb_Output)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gb_Output)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gb_Output)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.le_p5 = QtWidgets.QLineEdit(self.gb_Output)
        self.le_p5.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_p5.setFont(font)
        self.le_p5.setObjectName("le_p5")
        self.gridLayout_2.addWidget(self.le_p5, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gb_Output)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.le_P1 = QtWidgets.QLineEdit(self.gb_Output)
        self.le_P1.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_P1.setFont(font)
        self.le_P1.setObjectName("le_P1")
        self.gridLayout_2.addWidget(self.le_P1, 0, 1, 1, 3)
        self.le_P3 = QtWidgets.QLineEdit(self.gb_Output)
        self.le_P3.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_P3.setFont(font)
        self.le_P3.setObjectName("le_P3")
        self.gridLayout_2.addWidget(self.le_P3, 2, 1, 1, 3)
        self.le_P4 = QtWidgets.QLineEdit(self.gb_Output)
        self.le_P4.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.le_P4.setFont(font)
        self.le_P4.setObjectName("le_P4")
        self.gridLayout_2.addWidget(self.le_P4, 3, 1, 1, 3)
        self.verticalLayout_2.addWidget(self.gb_Output)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.gb_Input.setTitle(_translate("Form", "Input"))
        self.lbl_PHigh.setText(_translate("Form", "Filename"))
        self.btn_Calculate.setText(_translate("Form", "Read File and Calculate"))
        self.le_PHigh.setPlaceholderText(_translate("Form", "Find file path"))
        self.gb_Output.setTitle(_translate("Form", "Output"))
        self.label_5.setText(_translate("Form", "Flow Units"))
        self.label_15.setText(_translate("Form", "Head Units"))
        self.label_7.setText(_translate("Form", "Efficiency Coefficients"))
        self.label_9.setText(_translate("Form", "Head Coefficients"))
        self.label_2.setText(_translate("Form", "Pump Name"))