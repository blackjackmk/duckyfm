from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
import sys
import os

sys.path.insert(0, './gui') #import _ui.py files

from mainscreen_ui import Ui_MainWindow
from login_ui import Ui_Form
from register_ui import Ui_Form as SignUp_Ui_Form

from login import logowanie, rejestracja

global CurrentUser

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
    
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #sidebar
        self.ui.sidebar_full.hide()
        self.ui.stackedWidget.setCurrentIndex(0) #home window
        self.ui.home.setChecked(True)
        #hide admin
        self.ui.addmin.hide()
        self.ui.addmin_2.hide()
        
    def show_admin(self):
        if CurrentUser.is_admin:
            self.ui.addmin.show()
            self.ui.addmin_2.show() 
    
    #może zrobić to enum'em
    #[home, library, liked, admin, search, user]

    def on_stackedWidget_currentChanged(self, index): #przy zmianie okna
        btn_list = self.ui.sidebar_icon.findChildren(QPushButton)
        btn_list.pop(0)
        full_btn_list = self.ui.sidebar_full.findChildren(QPushButton)
        full_btn_list.pop(0)
        btn_list.extend(full_btn_list)
        
        for btn in btn_list:
            if index not in range(0, 3): #jeżeli strona wyszukiwania, konta lub kosza to odznaczamy przyciski sidebaru
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)


    def ostatnio_dodane_fill(self):
        for r in range(2): #row
            for c in range(3): #col
                self.ui.new_album = QtWidgets.QPushButton(self.ui.home_page)
                font = QtGui.QFont()
                font.setPointSize(14)
                icon8 = QtGui.QIcon()
                icon8.addPixmap(QtGui.QPixmap(":/icon/icomoon/radio-checked2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.new_album.setFont(font)
                self.ui.new_album.setStyleSheet("")
                self.ui.new_album.setIcon(icon8)
                self.ui.new_album.setIconSize(QtCore.QSize(30, 30))
                self.ui.new_album.setObjectName("new_album")
                self.ui.ostatnio_dodane.addWidget(self.ui.new_album, r, c, 1, 1)
                self.ui.new_album.setText("City of Stars")
    #funkcje do przycisków sidebaru
    #oba przyciski są połączone, więc wystarczy zaprogramować tylko jeden
    def on_home_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ostatnio_dodane_fill()
    def on_library_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_liked_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def on_addmin_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_search_button_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        search_text = self.ui.search_line.text().strip()
        if search_text:
            self.ui.stackedWidget.setCurrentIndex(4)

    def on_profile_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)


class LoginScreen(QDialog):
    successful_login = pyqtSignal()
    def __init__(self):
        super(LoginScreen, self).__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def on_login_btn_clicked(self):
        self.ui.error.setText("")
        username = self.ui.login.text() 
        password = self.ui.password.text()
        global CurrentUser
        CurrentUser = logowanie(username, password)
        if CurrentUser:
            self.successful_login.emit()
            self.close()
        else:
            self.ui.error.setText("Login error")

    def on_register_btn_clicked(self):
        register_window.show()
        self.close()

class RegisterScreen(QDialog):

    def __init__(self):
        super(RegisterScreen, self).__init__()
        
        self.ui = SignUp_Ui_Form()
        self.ui.setupUi(self)

    def on_register_btn_clicked(self):
        self.ui.error.setText("")
        username = self.ui.login.text()
        name = self.ui.name.text()
        surname = self.ui.surname.text()
        email = self.ui.email.text()
        haslo = self.ui.password.text()
        haslo2 = self.ui.password_repeat.text()
        try:
            rejestracja(username, name, surname, email, haslo, haslo2)
            #!udana rejestracja - pop up window
            login_window.show()
            self.close()
        except ValueError as e:
            self.ui.error.setText(str(e))

    def on_back_btn_clicked(self):
        login_window.show()
        self.close()

if __name__ == "__main__":
    if os.path.isfile("dzika_szyszka.jpg"):
        app = QApplication(sys.argv)

        login_window = LoginScreen()
        register_window = RegisterScreen()
        window = MainWindow()

        
        login_window.successful_login.connect(window.show)
        login_window.successful_login.connect(window.show_admin)
        login_window.show()
        sys.exit(app.exec_())
    
    #wykrzaczacz    
    else:
        exit(1)