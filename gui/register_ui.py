# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\gui\register.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 366)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.back_btn = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.back_btn.sizePolicy().hasHeightForWidth())
        self.back_btn.setSizePolicy(sizePolicy)
        self.back_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icomoon/cross.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back_btn.setIcon(icon)
        self.back_btn.setObjectName("back_btn")
        self.horizontalLayout.addWidget(self.back_btn)
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.name = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        self.name.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom: 2px solid black;\n"
"color: black;\n"
"padding-bottom:7px;")
        self.name.setText("")
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.surname = QtWidgets.QLineEdit(Form)
        self.surname.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom: 2px solid black;\n"
"color: black;\n"
"padding-bottom:7px;")
        self.surname.setText("")
        self.surname.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.surname.setObjectName("surname")
        self.verticalLayout.addWidget(self.surname)
        self.login = QtWidgets.QLineEdit(Form)
        self.login.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom: 2px solid black;\n"
"color: black;\n"
"padding-bottom:7px;")
        self.login.setText("")
        self.login.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.login.setObjectName("login")
        self.verticalLayout.addWidget(self.login)
        self.email = QtWidgets.QLineEdit(Form)
        self.email.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom: 2px solid black;\n"
"color: black;\n"
"padding-bottom:7px;")
        self.email.setText("")
        self.email.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.email.setObjectName("email")
        self.verticalLayout.addWidget(self.email)
        self.password = QtWidgets.QLineEdit(Form)
        self.password.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom: 2px solid black;\n"
"color: black;\n"
"padding-bottom:7px;")
        self.password.setText("")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.verticalLayout.addWidget(self.password)
        self.password_repeat = QtWidgets.QLineEdit(Form)
        self.password_repeat.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom: 2px solid black;\n"
"color: black;\n"
"padding-bottom:7px;")
        self.password_repeat.setText("")
        self.password_repeat.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_repeat.setObjectName("password_repeat")
        self.verticalLayout.addWidget(self.password_repeat)
        self.error = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setItalic(True)
        self.error.setFont(font)
        self.error.setStyleSheet("color: red;")
        self.error.setText("")
        self.error.setObjectName("error")
        self.verticalLayout.addWidget(self.error)
        self.register_btn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.register_btn.setFont(font)
        self.register_btn.setStyleSheet("border-radius: 5px;\n"
"border: 1px solid black;")
        self.register_btn.setObjectName("register_btn")
        self.verticalLayout.addWidget(self.register_btn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "DuckyFM - Login"))
        self.label.setText(_translate("Form", "Register"))
        self.name.setPlaceholderText(_translate("Form", "Name"))
        self.surname.setPlaceholderText(_translate("Form", "Surname"))
        self.login.setPlaceholderText(_translate("Form", "Login"))
        self.email.setPlaceholderText(_translate("Form", "Email"))
        self.password.setPlaceholderText(_translate("Form", "Password"))
        self.password_repeat.setPlaceholderText(_translate("Form", "Repeat password"))
        self.register_btn.setText(_translate("Form", "Create User"))
import resource_rc
