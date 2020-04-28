from requests import post
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QFileDialog, QLabel
import sys, os
import webbrowser


class MainForm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(351, 220)
        Form.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.login = QtWidgets.QLineEdit(Form)
        self.login.setGeometry(QtCore.QRect(40, 90, 271, 21))
        self.login.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.login.setObjectName("login")
        self.passw = QtWidgets.QLineEdit(Form)
        self.passw.setGeometry(QtCore.QRect(40, 120, 271, 20))
        self.passw.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.passw.setObjectName("pass")
        self.auth = QtWidgets.QLabel(Form)
        self.auth.setGeometry(QtCore.QRect(40, 20, 161, 31))
        self.auth.setStyleSheet("color: rgb(255, 255, 255);")
        self.auth.setObjectName("auth")
        self.login_btn = QtWidgets.QPushButton(Form)
        self.login_btn.setGeometry(QtCore.QRect(40, 150, 71, 21))
        self.login_btn.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.login_btn.setObjectName("pushButton")
        self.web = QtWidgets.QPushButton(Form)
        self.web.setGeometry(QtCore.QRect(240, 150, 71, 21))
        self.web.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.web.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(40, 60, 271, 20))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.login.setText(_translate("Form", "login"))
        self.passw.setText(_translate("Form", "password"))
        self.auth.setText(_translate("Form",
                                     "<html><head/><body><p><span style=\" font-size:18pt;\">Authentication</span></p></body></html>"))
        self.login_btn.setText(_translate("Form", "sing in"))
        self.web.setText(_translate("Form", "registration"))
        self.lineEdit.setText(_translate("Form", "url"))


class MainWindow(QMainWindow, MainForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        QMainWindow.setFixedSize(self, 350, 200)
        self.web.clicked.connect(self.gotowebsite)
        self.login_btn.clicked.connect(self.login_confirm)

    def gotowebsite(self):
        webbrowser.open(self.lineEdit.text() + '/register', new=2)  # url сайта

    def login_confirm(self):
        login_text = self.login.text()
        passw_text = self.passw.text()
        url = self.lineEdit.text()
        try:
            data = post(url + '/api/login', json={
                'email': login_text,
                'password': passw_text
            }).json()
            if 'message' in data:
                if data['message'] == 'Wrong password':
                    self.passw.setText('Try Again')
                elif 'not found' in data['message']:
                    self.login.setText('Try Again')
            else:
                self.launch_game(data)
        except Exception:
            self.lineEdit.setText('Try Again')

    def launch_game(self, data):
        print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
