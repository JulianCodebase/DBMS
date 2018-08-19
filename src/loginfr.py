# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'temp\loginfr.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QDialog,QMessageBox, QFormLayout, QLineEdit,QPushButton,QHBoxLayout
from databaseframe import Call_UI
import apprcc2_rc
import sys

class Ui_login_dlg(object):
    def setupUi(self, login_dlg):
        login_dlg.setObjectName("login_dlg")
        login_dlg.resize(548, 384)
        login_dlg.setMaximumSize(548, 384)
        login_dlg.setMinimumSize(548,384)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r".\rcc\blue.ico"))
        login_dlg.setWindowIcon(icon)
        login_dlg.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(login_dlg)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        pixmap = QtGui.QPixmap(r'.\rcc\doru.jpg')
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(pixmap.scaled(login_dlg.size())))
        login_dlg.setPalette(palette)
        login_dlg.setAutoFillBackground(True)

        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(140, 200, 140, 30)
        self.horizontalLayout.setObjectName(
            "horizontalLayout")
        self.username_lb = QtWidgets.QLabel(login_dlg)
        self.username_lb.setObjectName("username_lb")
        self.horizontalLayout.addWidget(self.username_lb)
        self.lineEdit = QtWidgets.QLineEdit(login_dlg)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(140, -1, 140, 30)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.password_lb = QtWidgets.QLabel(login_dlg)
        self.password_lb.setObjectName("password_lb")
        self.horizontalLayout_2.addWidget(self.password_lb)
        self.lineEdit_2 = QtWidgets.QLineEdit(login_dlg)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        # self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(150, -1, 180, 10)
        # self.horizontalLayout_4.setContentsMargins(180, -1, 180, 10)
        self.horizontalLayout_3.setSpacing(80)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.login_btn = QtWidgets.QPushButton(login_dlg)
        self.horizontalLayout_3.addWidget(self.login_btn)
        self.exit_btn = QtWidgets.QPushButton(login_dlg)
        self.horizontalLayout_3.addWidget(self.exit_btn)
        self.exit_btn.clicked.connect(self.register)
        # self.horizontalLayout_4.addWidget(self.exit_btn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        # self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.login_btn.setStyleSheet("color: white; background-color: rgb(25, 80, 199);")
        self.exit_btn.setStyleSheet("color: white; background-color: rgb(25, 80, 199)")
        self.login_btn.setMinimumSize(100, 10)
        self.exit_btn.setMinimumSize(100, 10)
        # self.exit_btn.hide()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.retranslateUi(login_dlg)
        QtCore.QMetaObject.connectSlotsByName(login_dlg)

    def retranslateUi(self, login_dlg):
        _translate = QtCore.QCoreApplication.translate
        login_dlg.setWindowTitle(_translate("login_dlg", "登录"))
        self.username_lb.setText(_translate("login_dlg", "用户名:"))
        self.password_lb.setText(_translate("login_dlg", "密  码:"))
        self.login_btn.setText(_translate("login_dlg", "登录"))
        self.exit_btn.setText(_translate("login_dlg", "注册"))

    def register(self):
        def confirmMessage():
            if password_LE.text() != confirm_LE.text():
                QMessageBox.warning(dlg,'错误','两次密码输入不一致', QMessageBox.Ok)
            elif password_LE.text() and confirm_LE.text():
                if username_LE.text() not in self.users:
                    f = open(r'D:\PySubjects\database3\table\users\usernames.txt', 'a', encoding = 'utf8')
                    f.write(username_LE.text() +' '+ password_LE.text()+'\n')
                    f.close()
                    QMessageBox.information(dlg,'信息','注册成功', QMessageBox.Ok)
                    self.updateusers()
                    dlg.close()
                else:
                    QMessageBox.warning(dlg,'错误','该用户已存在', QMessageBox.Ok)

        dlg = QDialog(self)
        dlg.setWindowTitle('注册')
        formlayout = QFormLayout()
        username_LE = QLineEdit()
        formlayout.addRow('用户名', username_LE)
        password_LE = QLineEdit()
        password_LE.setEchoMode(QtWidgets.QLineEdit.Password)
        formlayout.addRow('密  码', password_LE)
        confirm_LE = QLineEdit()
        confirm_LE.setEchoMode(QtWidgets.QLineEdit.Password)
        formlayout.addRow('确认密码', confirm_LE)
        confirm_btn = QPushButton('注册')
        confirm_btn.clicked.connect(confirmMessage)
        confirm_btn.setStyleSheet("color: white; background-color: rgb(25, 80, 199);")
        cancel_btn = QPushButton('取消')
        cancel_btn.clicked.connect(dlg.close)
        cancel_btn.setStyleSheet("color: white; background-color: rgb(25, 80, 199);")
        horizontalLayout = QHBoxLayout()
        horizontalLayout.addWidget(confirm_btn)
        horizontalLayout.addWidget(cancel_btn)
        horizontalLayout.setSpacing(30)
        formlayout.addRow(horizontalLayout)
        dlg.setLayout(formlayout)
        dlg.setFixedSize(250,150)
        dlg.setModal(True)
        dlg.show()

class Call_LoginUI(Ui_login_dlg, QDialog):
    def __init__(self, parent = None):
        super(Call_LoginUI, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def updateusers(self):
        f = open(sys.path[0] + r'\table\users\usernames.txt','r',encoding = 'utf8')
        lines = f.readlines()
        f.close()
        self.users = {}.fromkeys([i.split()[0] for i in lines], '')
        for i in lines:
            items = i.split()
            self.users[items[0]] = items[-1]

    def initUI(self):
        self.login_btn.clicked.connect(self.submit)
        self.updateusers()

    def submit(self):
        input_username = self.lineEdit.text()
        if input_username not in self.users:
            QMessageBox.warning(self, "错误","用户名不存在！",QMessageBox.Ok)
            self.lineEdit.setFocus()
        elif self.lineEdit_2.text() == self.users[input_username]:
            self.hide()
            self.ui = Call_UI(username = self.lineEdit.text(), loginfr = self)
            self.ui.show()
        else:
            QMessageBox.warning(self, "错误","密码错误！",QMessageBox.Ok)
            self.lineEdit_2.setFocus()

app = QApplication(sys.argv)
loginfr = Call_LoginUI()
loginfr.show()
sys.exit(app.exec_())

# jpeg=QtGui.QPixmap(self)
# jpeg.load("./bk2.png")
# pixmap = QtGui.QPixmap()
# palette = QtGui.QPalette(self)
# palette.setBrush(self.backgroundRole(), QtGui.QBrush(pixmap))
# self.widget.setPalette(palette);
# self.widget.setAutoFillBackground(True)

