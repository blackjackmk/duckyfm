from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QFile, QTextStream
import sys
import os

sys.path.insert(0, './gui') #import _ui.py files

from mainscreen_ui import Ui_MainWindow
from login_ui import Ui_Form
from register_ui import Ui_Form as SignUp_Ui_Form

from login import logowanie, rejestracja

global CurrentUser

def toggle_stylesheet(style):
        # get the QApplication instance,  or crash if not set
        app = QApplication.instance()
        if app is None:
            raise RuntimeError("No Qt Application found.")
        if style == "Light":
            path = "./gui/light_layout.qss"
        else:
            path = "./gui/dark_layout.qss"
        file = QFile(path)
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

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
        #layout style change
        self.ui.theme_combo.currentTextChanged.connect(lambda: toggle_stylesheet(self.ui.theme_combo.currentText()))
        
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
        latest = ["Pierwszy", "Drugi", "Trzeci", "Czwarty", "Piąty", "Szósty"]
        n = 0
        for r in range(2): #row
            for c in range(3): #col
                self.ui.new_album = QtWidgets.QPushButton(self.ui.home_page)
                font = QtGui.QFont()
                font.setPointSize(14)
                self.ui.icon8 = QtGui.QIcon()
                self.ui.icon8.addPixmap(QtGui.QPixmap(":/icon/icomoon/radio-checked2.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.ui.new_album.setFont(font)
                self.ui.new_album.setStyleSheet("")
                self.ui.new_album.setIcon(self.ui.icon8)
                self.ui.new_album.setIconSize(QtCore.QSize(30, 30))
                self.ui.new_album.setObjectName("new_album")
                self.ui.ostatnio_dodane.addWidget(self.ui.new_album, r, c, 1, 1)
                self.ui.new_album.setText(latest[n])
                n += 1

    def discover_fill(self):
        for r in range(3): #row
            for c in range(5): #col
                self.ui.song_card = QtWidgets.QWidget(self.ui.home_container)
                self.ui.song_card.setObjectName("song_card")
                self.ui.verticalLayout_7 = QtWidgets.QVBoxLayout(self.ui.song_card)
                self.ui.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
                self.ui.verticalLayout_7.setSpacing(0)
                self.ui.verticalLayout_7.setObjectName("verticalLayout_7")
                self.ui.img = QtWidgets.QLabel(self.ui.song_card)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.img.sizePolicy().hasHeightForWidth())
                self.ui.img.setSizePolicy(sizePolicy)
                self.ui.img.setText("")
                self.ui.img.setPixmap(QtGui.QPixmap(":/icon/icomoon/play3.svg"))
                self.ui.img.setScaledContents(False)
                self.ui.img.setAlignment(QtCore.Qt.AlignCenter)
                self.ui.img.setObjectName("img")
                self.ui.verticalLayout_7.addWidget(self.ui.img)
                self.ui.song_title = QtWidgets.QLabel(self.ui.song_card)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.song_title.sizePolicy().hasHeightForWidth())
                self.ui.song_title.setSizePolicy(sizePolicy)
                font = QtGui.QFont()
                font.setPointSize(12)
                self.ui.song_title.setFont(font)
                self.ui.song_title.setObjectName("song_title")
                self.ui.verticalLayout_7.addWidget(self.ui.song_title)
                self.ui.artist = QtWidgets.QLabel(self.ui.song_card)
                font = QtGui.QFont()
                font.setPointSize(10)
                self.ui.artist.setFont(font)
                self.ui.artist.setObjectName("artist_2")
                self.ui.verticalLayout_7.addWidget(self.ui.artist)
                self.ui.song_title.setText("Cinema City")
                self.ui.artist.setText("Gibbs")
                self.ui.gridLayout_4.addWidget(self.ui.song_card, r, c, 1, 1)

    def library_fill(self):
        for r in range(3): #row
            for c in range(4): #col
                self.ui.library_card = QtWidgets.QFrame(self.ui.library_container)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.library_card.sizePolicy().hasHeightForWidth())
                self.ui.library_card.setSizePolicy(sizePolicy)
                self.ui.library_card.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.ui.library_card.setFrameShadow(QtWidgets.QFrame.Raised)
                self.ui.library_card.setObjectName("library_card")
                self.ui.verticalLayout_23 = QtWidgets.QVBoxLayout(self.ui.library_card)
                self.ui.verticalLayout_23.setObjectName("verticalLayout_23")
                self.ui.library_card_img = QtWidgets.QLabel(self.ui.library_card)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.library_card_img.sizePolicy().hasHeightForWidth())
                self.ui.library_card_img.setSizePolicy(sizePolicy)
                self.ui.library_card_img.setText("")
                self.ui.library_card_img.setPixmap(QtGui.QPixmap(":/icon/icomoon/radio-unchecked.svg"))
                self.ui.library_card_img.setScaledContents(False)
                self.ui.library_card_img.setAlignment(QtCore.Qt.AlignCenter)
                self.ui.library_card_img.setObjectName("library_card_img")
                self.ui.verticalLayout_23.addWidget(self.ui.library_card_img)
                self.ui.library_card_title = QtWidgets.QLabel(self.ui.library_card)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.library_card_title.sizePolicy().hasHeightForWidth())
                self.ui.library_card_title.setSizePolicy(sizePolicy)
                self.ui.library_card_title.setObjectName("library_card_title")
                self.ui.verticalLayout_23.addWidget(self.ui.library_card_title)
                self.ui.library_card_autor = QtWidgets.QLabel(self.ui.library_card)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.library_card_autor.sizePolicy().hasHeightForWidth())
                self.ui.library_card_autor.setSizePolicy(sizePolicy)
                self.ui.library_card_autor.setObjectName("library_card_autor")
                self.ui.verticalLayout_23.addWidget(self.ui.library_card_autor)
                self.ui.gridLayout_2.addWidget(self.ui.library_card, r, c, 1, 1)
                self.ui.library_card_title.setText("Album")
                self.ui.library_card_autor.setText("Artist")

    def liked_fill(self):
        for r in range(3): #row
            for c in range(4): #col
                self.ui.liked_card = QtWidgets.QFrame(self.ui.liked_container)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.liked_card.sizePolicy().hasHeightForWidth())
                self.ui.liked_card.setSizePolicy(sizePolicy)
                self.ui.liked_card.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.ui.liked_card.setFrameShadow(QtWidgets.QFrame.Raised)
                self.ui.liked_card.setObjectName("liked_card")
                self.ui.verticalLayout_31 = QtWidgets.QVBoxLayout(self.ui.liked_card)
                self.ui.verticalLayout_31.setObjectName("verticalLayout_31")
                self.ui.liked_card_img = QtWidgets.QLabel(self.ui.liked_card)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.liked_card_img.sizePolicy().hasHeightForWidth())
                self.ui.liked_card_img.setSizePolicy(sizePolicy)
                self.ui.liked_card_img.setText("")
                self.ui.liked_card_img.setPixmap(QtGui.QPixmap(":/icon/icomoon/heart.svg"))
                self.ui.liked_card_img.setScaledContents(False)
                self.ui.liked_card_img.setAlignment(QtCore.Qt.AlignCenter)
                self.ui.liked_card_img.setObjectName("liked_card_img")
                self.ui.verticalLayout_31.addWidget(self.ui.liked_card_img)
                self.ui.liked_card_title = QtWidgets.QLabel(self.ui.liked_card)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.liked_card_title.sizePolicy().hasHeightForWidth())
                self.ui.liked_card_title.setSizePolicy(sizePolicy)
                font = QtGui.QFont()
                font.setPointSize(12)
                self.ui.liked_card_title.setFont(font)
                self.ui.liked_card_title.setObjectName("liked_card_title")
                self.ui.verticalLayout_31.addWidget(self.ui.liked_card_title)
                self.ui.liked_card_autor = QtWidgets.QLabel(self.ui.liked_card)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.liked_card_autor.sizePolicy().hasHeightForWidth())
                self.ui.liked_card_autor.setSizePolicy(sizePolicy)
                self.ui.liked_card_autor.setObjectName("liked_card_autor")
                self.ui.verticalLayout_31.addWidget(self.ui.liked_card_autor)
                self.ui.gridLayout_3.addWidget(self.ui.liked_card, r, c, 1, 1)
                self.ui.liked_card_title.setText("Album")
                self.ui.liked_card_autor.setText("Artist")

    def search_songs_fill(self, search_text):
        for l in range(2):
            self.ui.search_song_info = QtWidgets.QWidget(self.ui.scrollAreaWidgetContents_4)
            self.ui.search_song_info.setObjectName("search_song_info")
            self.ui.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.ui.search_song_info)
            self.ui.horizontalLayout_4.setObjectName("horizontalLayout_4")
            self.ui.song_logo = QtWidgets.QLabel(self.ui.search_song_info)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.ui.song_logo.sizePolicy().hasHeightForWidth())
            self.ui.song_logo.setSizePolicy(sizePolicy)
            self.ui.song_logo.setText("")
            self.ui.song_logo.setPixmap(QtGui.QPixmap(":/icon/icomoon/music.svg"))
            self.ui.song_logo.setScaledContents(False)
            self.ui.song_logo.setAlignment(QtCore.Qt.AlignCenter)
            self.ui.song_logo.setObjectName("song_logo")
            self.ui.horizontalLayout_4.addWidget(self.ui.song_logo)
            self.ui.info = QtWidgets.QWidget(self.ui.search_song_info)
            self.ui.info.setObjectName("info")
            self.ui.verticalLayout_18 = QtWidgets.QVBoxLayout(self.ui.info)
            self.ui.verticalLayout_18.setObjectName("verticalLayout_18")
            self.ui.song_title = QtWidgets.QLabel(self.ui.info)
            font = QtGui.QFont()
            font.setPointSize(15)
            self.ui.song_title.setFont(font)
            self.ui.song_title.setObjectName("song_title")
            self.ui.verticalLayout_18.addWidget(self.ui.song_title)
            self.ui.song_autor = QtWidgets.QLabel(self.ui.info)
            font = QtGui.QFont()
            font.setPointSize(12)
            self.ui.song_autor.setFont(font)
            self.ui.song_autor.setObjectName("song_autor")
            self.ui.verticalLayout_18.addWidget(self.ui.song_autor)
            self.ui.horizontalLayout_4.addWidget(self.ui.info)
            self.ui.song_search_container.addWidget(self.ui.search_song_info)
            self.ui.song_title.setText(search_text)
            self.ui.song_autor.setText("Autor")
    
    def search_albums_fill(self, search_text):
        for r in range(3): #row
            for c in range(5): #col
                self.ui.song_card_find = QtWidgets.QWidget(self.ui.albums_search_container)
                self.ui.song_card_find.setObjectName("song_card_find")
                self.ui.verticalLayout_19 = QtWidgets.QVBoxLayout(self.ui.song_card_find)
                self.ui.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
                self.ui.verticalLayout_19.setSpacing(0)
                self.ui.verticalLayout_19.setObjectName("verticalLayout_19")
                self.ui.img = QtWidgets.QLabel(self.ui.song_card_find)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.img.sizePolicy().hasHeightForWidth())
                self.ui.img.setSizePolicy(sizePolicy)
                self.ui.img.setText("")
                self.ui.img.setPixmap(QtGui.QPixmap(":/icon/icomoon/play3.svg"))
                self.ui.img.setScaledContents(False)
                self.ui.img.setAlignment(QtCore.Qt.AlignCenter)
                self.ui.img.setObjectName("img")
                self.ui.verticalLayout_19.addWidget(self.ui.img)
                self.ui.song_title = QtWidgets.QLabel(self.ui.song_card_find)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.ui.song_title.sizePolicy().hasHeightForWidth())
                self.ui.song_title.setSizePolicy(sizePolicy)
                font = QtGui.QFont()
                font.setPointSize(12)
                self.ui.song_title.setFont(font)
                self.ui.song_title.setObjectName("song_title")
                self.ui.verticalLayout_19.addWidget(self.ui.song_title)
                self.ui.artist = QtWidgets.QLabel(self.ui.song_card_find)
                font = QtGui.QFont()
                font.setPointSize(10)
                self.ui.artist.setFont(font)
                self.ui.artist.setObjectName("artist")
                self.ui.verticalLayout_19.addWidget(self.ui.artist)
                self.ui.song_title.setText(search_text)
                self.ui.artist.setText("Gibbs")
                self.ui.gridLayout_5.addWidget(self.ui.song_card_find, r, c, 1, 1)
    
    def search_artist_fill(self, search_text):
        for r in range(2): #row
            for c in range(3): #col
                self.ui.search_singer = QtWidgets.QPushButton(self.ui.scrollAreaWidgetContents_4)
                font = QtGui.QFont()
                font.setPointSize(14)
                self.ui.search_singer.setFont(font)
                self.ui.search_singer.setStyleSheet("")
                self.ui.search_singer.setIcon(self.ui.icon8)
                self.ui.search_singer.setIconSize(QtCore.QSize(30, 30))
                self.ui.search_singer.setObjectName("search_singer")
                self.ui.search_singer.setText("Radiohead")
                self.ui.search_artist.addWidget(self.ui.search_singer, r, c, 1, 1)


    #funkcje do przycisków sidebaru
    #oba przyciski są połączone, więc wystarczy zaprogramować tylko jeden
    def on_home_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ostatnio_dodane_fill()
        self.discover_fill()
    def on_library_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.library_fill()
    def on_liked_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.liked_fill()
    def on_addmin_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_search_button_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        search_text = self.ui.search_line.text().strip()
        if search_text:
            self.ui.stackedWidget.setCurrentIndex(4)
            self.search_songs_fill(search_text)
            self.search_albums_fill(search_text)
            self.search_artist_fill(search_text)

    def on_profile_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.login.setText(CurrentUser.username)
        self.ui.name.setText(CurrentUser.name)
        self.ui.surname.setText(CurrentUser.surname)
        self.ui.email.setText(CurrentUser.email)
        self.ui.addres.setPlainText(CurrentUser.adress)

    def on_profile_save_btn_clicked(self):
        CurrentUser.username = self.ui.login.text()
        CurrentUser.name = self.ui.name.text()
        CurrentUser.surname = self.ui.surname.text()
        CurrentUser.email = self.ui.email.text()
        CurrentUser.adress = self.ui.addres.toPlainText()
        CurrentUser.update_user_info()

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

        #stylesheet connect
        file = QFile("./gui/light_layout.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

        login_window.successful_login.connect(window.show)
        login_window.successful_login.connect(window.show_admin)
        login_window.show()
        sys.exit(app.exec_())
    
    #wykrzaczacz    
    else:
        exit(1)