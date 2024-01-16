from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QWidget
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QFile, QTextStream
import sys
import os

sys.path.insert(0, './gui') #import _ui.py files
from mainscreen_ui import Ui_MainWindow
from login_ui import Ui_Form
from register_ui import Ui_Form as SignUp_Ui_Form

from login import logowanie, rejestracja
from classes import Artist, Songs, Plyty, Admin, songs_to_album
from default_base import db, conn

global CurrentUser

def toggle_stylesheet(style):
        # get the QApplication instance,  or crash if not set
        app = QApplication.instance()
        if app is None:
            raise RuntimeError("No Qt Application found.")
        style_paths = ["./gui/light_layout.qss", "./gui/dark_layout.qss"]
        file = QFile(style_paths[style])
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
        self.admin_loaded = False
        #layout style change
        self.ui.theme_combo.currentTextChanged.connect(lambda: toggle_stylesheet(self.ui.theme_combo.currentIndex()))
        #language change
        self.ui.language_combo.currentIndexChanged.connect(lambda: self.change_language(self.ui.language_combo.currentIndex()))
        self.ui.trans = QtCore.QTranslator(self)
        self.ui.retranslateUi(self)
        
    def change_language(self, language):
        languages = ['./locale/main_en', './locale/main_pl']
        self.ui.trans.load(languages[language])
        QtWidgets.QApplication.instance().installTranslator(self.ui.trans)
        self.ui.retranslateUi(self)

    def admin_access(self):
        if not self.admin_loaded:
            if CurrentUser.is_admin:
                self.ui.addmin.show()
                self.ui.addmin_2.show()
                self.admin_combo_fill()
                self.admin_loaded = True
    
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
        for i in reversed(range(self.ui.ostatnio_dodane.count())): 
            self.ui.ostatnio_dodane.itemAt(i).widget().setParent(None)
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
        for i in reversed(range(self.ui.gridLayout_4.count())): 
            self.ui.gridLayout_4.itemAt(i).widget().setParent(None)
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
        for i in reversed(range(self.ui.gridLayout_2.count())): 
            self.ui.gridLayout_2.itemAt(i).widget().setParent(None)
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
        for i in reversed(range(self.ui.gridLayout_3.count())): 
            self.ui.gridLayout_3.itemAt(i).widget().setParent(None)
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
        for i in reversed(range(self.ui.song_search_container.count())): 
            self.ui.song_search_container.itemAt(i).widget().setParent(None)
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
        for i in reversed(range(self.ui.gridLayout_5.count())): 
            self.ui.gridLayout_5.itemAt(i).widget().setParent(None)
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
        for i in reversed(range(self.ui.search_artist.count())): 
            self.ui.search_artist.itemAt(i).widget().setParent(None)
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

    def admin_combo_fill(self):
        #załadować id albumów do album_id_field, song_album_field
        db.execute("SELECT album_id, title FROM plyty")
        get_albums = db.fetchall()
        for album_id, title in get_albums:
            self.ui.album_id_field.addItem(title, userData=album_id)
            self.ui.song_album_field.addItem(title, userData=album_id)
        #załadować z bazy listę stylów muzyki z indeksami do genre_field, song_genre_field
        db.execute("SELECT id_genre, title FROM genre")
        get_genres = db.fetchall()
        for id_genre, title in get_genres:
            self.ui.genre_field.addItem(title, userData=id_genre)
            self.ui.song_genre_field.addItem(title, userData=id_genre)
        #załadować id piosenek do song_id_field
        db.execute("SELECT song_id, title FROM utwory")
        get_songs = db.fetchall()
        for song_id, title in get_songs:
            self.ui.song_id_field.addItem(title, userData=song_id)
        #załadować id arystów do artist_id_field, song_artist_field
        db.execute("SELECT artist_id, pseudonim FROM tworcy")
        get_artists = db.fetchall()
        for artist_id, pseudonim in get_artists:
            self.ui.artist_id_field.addItem(pseudonim, userData=artist_id)
            self.ui.song_artist_field.addItem(pseudonim, userData=artist_id)
        #załadować id adminów do admin_id_field
        db.execute("SELECT user_id, username FROM users WHERE is_admin = 1")
        get_admins = db.fetchall()
        for user_id, username in get_admins:
            self.ui.admin_id_field.addItem(username, userData=user_id)
        #załadować id uzerów do user_id_field
        db.execute("SELECT user_id, username FROM users WHERE is_admin = 0")
        get_users = db.fetchall()
        for user_id, username in get_users:
            self.ui.user_id_field.addItem(username, userData=user_id)


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
    def on_addmin_toggled(self):#dane do edytowania
        self.ui.stackedWidget.setCurrentIndex(3)
        #dane do edytowania albumów
        def on_album_id_field_option_change(index):
            if index != 0:
                query = "SELECT title, description, genre FROM plyty WHERE album_id = ?"
                db.execute(query, (self.ui.album_id_field.itemData(index, Qt.UserRole),))
                result = db.fetchone()
                self.ui.title_field.setText(result['title'])
                self.ui.description_field.setText(result['description'])
                self.ui.genre_field.setCurrentIndex(self.ui.genre_field.findData(result['genre'], Qt.UserRole))
            else:
                self.ui.title_field.setText("")
                self.ui.description_field.setText("")
                self.ui.genre_field.setCurrentIndex(0)
        self.ui.album_id_field.currentIndexChanged.connect(lambda: on_album_id_field_option_change(self.ui.album_id_field.currentIndex()))
        #dane do edytowania twórców
        def on_artist_id_field_option_change(index):
            if index != 0:
                query = "SELECT pseudonim, description FROM tworcy WHERE artist_id = ?"
                db.execute(query, (self.ui.artist_id_field.itemData(index, Qt.UserRole),))
                result = db.fetchone()
                self.ui.artist_pseudonim_field.setText(result['pseudonim'])
                self.ui.artist_description_field.setText(result['description'])
            else:
                self.ui.artist_pseudonim_field.setText("")
                self.ui.artist_description_field.setText("")
        self.ui.artist_id_field.currentIndexChanged.connect(lambda: on_artist_id_field_option_change(self.ui.artist_id_field.currentIndex()))
        #dane do edytowania utworów
        def on_song_id_field_option_change(index):
            if index != 0:
                query = "SELECT title, genre, artist, album, status FROM utwory WHERE song_id = ?"
                db.execute(query, (self.ui.song_id_field.itemData(index, Qt.UserRole),))
                result = db.fetchone()
                self.ui.song_title_field.setText(result['title'])
                self.ui.song_genre_field.setCurrentIndex(self.ui.song_genre_field.findData(result['genre'], Qt.UserRole))
                self.ui.song_artist_field.setCurrentIndex(self.ui.song_artist_field.findData(result['artist'], Qt.UserRole))
                self.ui.song_album_field.setCurrentIndex(self.ui.song_album_field.findData(result['album'], Qt.UserRole))
                if result['status'] == "Published":
                    self.ui.is_published.setChecked(True)
                else:
                    self.ui.is_published.setChecked(False)
            else:
                self.ui.song_title_field.setText("")
                self.ui.song_genre_field.setCurrentIndex(0)
                self.ui.song_artist_field.setCurrentIndex(0)
                self.ui.song_album_field.setCurrentIndex(0)
        self.ui.song_id_field.currentIndexChanged.connect(lambda: on_song_id_field_option_change(self.ui.song_id_field.currentIndex()))

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
    @pyqtSlot()
    def on_album_add_btn_clicked(self):
        title = self.ui.title_field.text()
        description = self.ui.description_field.toPlainText()
        genre = self.ui.genre_field.itemData(self.ui.genre_field.currentIndex(), Qt.UserRole)
        album = Plyty(title, description, genre)
        album.create()
    def on_album_edit_btn_clicked(self):
        id_albumu = self.ui.album_id_field.itemData(self.ui.album_id_field.currentIndex(), Qt.UserRole)
        title = self.ui.title_field.text()
        description = self.ui.description_field.toPlainText()
        genre = self.ui.genre_field.itemData(self.ui.genre_field.currentIndex(), Qt.UserRole)
        album = Plyty(title, description, genre, id_albumu)
        album.update()
    def on_album_dlt_btn_clicked(self):
        id_albumu = self.ui.album_id_field.itemData(self.ui.album_id_field.currentIndex(), Qt.UserRole)
        query = "DELETE FROM plyty WHERE album_id = ?"
        db.execute(query, (id_albumu,))
        conn.commit()
    @pyqtSlot()
    def on_artist_add_clicked(self):
        name = self.ui.artist_pseudonim_field.text()
        description = self.ui.artist_description_field.toPlainText()
        artist = Artist(name, description)
        artist.create()
    def on_artist_edit_clicked(self):
        id_artist = self.ui.artist_id_field.itemData(self.ui.artist_id_field.currentIndex(), Qt.UserRole)
        name = self.ui.artist_pseudonim_field.text()
        description = self.ui.artist_description_field.toPlainText()
        artist = Artist(name, description, id_artist)
        artist.update()
    def on_artist_delete_clicked(self):
        id_artist = self.ui.artist_id_field.itemData(self.ui.artist_id_field.currentIndex(), Qt.UserRole)
        query = "DELETE FROM tworcy WHERE artist_id = ?"
        db.execute(query, (id_artist,))
        conn.commit()
    @pyqtSlot()
    def on_song_add_clicked(self):
        title = self.ui.song_title_field.text()
        genre = self.ui.song_genre_field.itemData(self.ui.song_genre_field.currentIndex(), Qt.UserRole)
        artist = self.ui.song_artist_field.itemData(self.ui.song_artist_field.currentIndex(), Qt.UserRole)
        album = self.ui.song_album_field.itemData(self.ui.song_album_field.currentIndex(), Qt.UserRole)
        if self.ui.is_published.isChecked():
            status = "Published"
        else:
            status = "Unpublished"
        song = Songs(title, genre, artist, album, status)
        song.create() #relacja tworzy się automatycznie w klasie
        if artist and album:#jeżeli twórca i album są podane, to wszystkie piosenki w albumie będą należały do niego
            songs_to_album(album, artist)
    def on_song_edit_clicked(self):
        id_utworu = self.ui.song_id_field.itemData(self.ui.song_id_field.currentIndex(), Qt.UserRole)
        title = self.ui.song_title_field.text()
        genre = self.ui.song_genre_field.itemData(self.ui.song_genre_field.currentIndex(), Qt.UserRole)
        artist = self.ui.song_artist_field.itemData(self.ui.song_artist_field.currentIndex(), Qt.UserRole)
        album = self.ui.song_album_field.itemData(self.ui.song_album_field.currentIndex(), Qt.UserRole)
        if self.ui.is_published.isChecked():
            status = "Published"
        else:
            status = "Unpublished"
        song = Songs(title, genre, artist, album, status, id_utworu)
        song.update()
    def on_song_delete_clicked(self):
        id_utworu = self.ui.song_id_field.itemData(self.ui.song_id_field.currentIndex(), Qt.UserRole)
        query = "DELETE FROM utwory WHERE song_id = ?"
        db.execute(query, (id_utworu,))
        conn.commit()

    def on_resign_btn_clicked(self):#make confirmation
        zastepca = self.ui.user_id_field.itemData(self.ui.user_id_field.currentIndex(), Qt.UserRole)    
        CurrentUser.resignation(zastepca)
    def on_awans_btn_clicked(self):
        nowy_admin = self.ui.user_id_field.itemData(self.ui.user_id_field.currentIndex(), Qt.UserRole)
        CurrentUser.awans(nowy_admin)
    def on_fire_btn_clicked(self):
        zwolniony = self.ui.admin_id_field.itemData(self.ui.admin_id_field.currentIndex(), Qt.UserRole)
        CurrentUser.delete_other_admin(zwolniony)

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
            window.admin_access()
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

        login_window.show()
        sys.exit(app.exec_())
        #conn.close() przy zamykaniu applikacji
    #wykrzaczacz    
    else:
        exit(1)