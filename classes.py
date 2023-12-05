import datetime
from default_base import db, conn
from login import CurrentUser

class Artist:
    def __init__(self, pseudonim, opis, id=None): # is always executed when the class is being initiated
        self.pseudonim = pseudonim
        self.opis = opis
        self.id = id

    #tworzenie
    def create(self):
        query = "INSERT INTO tworcy ('pseudonim', 'description') VALUES (?, ?)"
        db.execute(query, (self.pseudonim, self.opis))
        conn.commit()
        self.id = db.lastrowid

    #edytowanie
    def update(self):
        query = "UPDATE tworcy SET 'pseudonim' = ?, 'description' = ? WHERE artist_id = ?"
        db.execute(query, (self.pseudonim, self.opis, self.id))
        conn.commit()

class Songs:
    def __init__(self, title=None, genre=None, artist=None, album=None, status="Published", id=None): # is always executed when the class is being initiated
        self.title = title
        self.genre = genre
        self.artist = artist
        self.album = album
        self.status = status
        self.id = id

    #tworzenie relacji twórca-utwór
    def song_singer_connect(self):
        query = "INSERT INTO wykonawcy_utwory (id_wykonawcy, id_utworu) VALUES (?, ?)"
        db.execute(query, (self.artist, self.id))
        conn.commit()

    #tworzenie
    def create(self):
        query = "INSERT INTO utwory ('title', 'genre', 'artist', 'album', 'created_at') VALUES (?, ?, ?, ?, ?)"
        teraz = datetime.datetime.now()
        createtime = teraz.strftime("%Y-%m-%d %H:%M:%S")
        db.execute(query, (self.title, self.genre, self.artist, self.album, createtime))
        conn.commit()
        self.id = db.lastrowid
        query = "INSERT INTO wykonawcy_utwory (id_wykonawcy, id_utworu) VALUES (?, ?)"
        db.execute(query, (self.artist, self.id))
        conn.commit()

    #edytowanie
    def update(self):
        query = "UPDATE utwory SET 'title' = ?, 'genre' = ?, 'artist' = ?, 'album' = ?, 'status' = ? WHERE song_id = ?"
        db.execute(query, (self.title, self.genre, self.artist, self.album, self.status, self.id))
        query2 = "UPDATE wykonawcy_utwory SET 'id_wykonawcy' = ?, 'id_utworu' = ?)"
        db.execute(query2, (self.artist, self.id))
        conn.commit()

class Plyty:
    def __init__(self, title, description, genre, id=None):
        self.title = title
        self.description = description
        self.genre = genre
        self.id = id

    #tworzenie
    def create(self):
        query = "INSERT INTO plyty ('title', 'description', 'genre', 'artist') VALUES (?, ?, ?, ?)"
        db.execute(query, (self.title, self.description, self.genre))
        conn.commit()
        self.id = db.lastrowid

    #edytowanie
    def update(self):
        query = "UPDATE plyty SET 'title' = ?, 'description' = ?, 'genre' = ? WHERE album_id = ?"
        db.execute(query, (self.title, self.description, self.genre, self.id))
        conn.commit()

class User:
    def __init__(self, username, is_admin, id=None):
        self.username = username
        self.is_admin = False
        self.id = id

    owned_albums = {}
    liked_songs = {}

def only_admin(func):
    def wrapper(*args, **kwargs):
        if not isinstance(CurrentUser, Admin):#gdy nie jest objektem klasy
            raise PermissionError("Brak dostępu. Zaloguj się jako admin.")
        return func(*args, **kwargs)
    return wrapper

class Admin(User):
    def __init__(self, username, is_admin):
        super().__init__(username, True)

    def awans(self, new_admin_id):
        query = "UPDATE users SET 'is_admin' = 1 WHERE user_id = ?"
        db.execute(query, (new_admin_id,))
        conn.commit()

    def delete_other_admin(self, admin_to_fire):
        #tylko admin może usunąć innego admina
        db.execute("SELECT * FROM users WHERE is_admin = 1 ORDER BY user_id ASC")
        results = db.fetchone()
        if results[0] == admin_to_fire:
            #nie można usunąć pierwszego admina
            return False
        else:
            query = "UPDATE users SET 'is_admin' = 0 WHERE user_id = ?"
            db.execute(query, (admin_to_fire,))
        

    def resignation(self):
        #moze sam zrezygnowac, ale uwaga: musi wskazac kogos innego z listy
        zastepca = input("Podaj id swojego zastępcy: ")
        #check is user exist
        db.execute('SELECT COUNT(*) AS user_count FROM users WHERE user_id = ?', (zastepca,))
        result = db.fetchone()

        if result[0] > 0:
            #exist
            query = "UPDATE users SET 'is_admin' = 1 WHERE user_id = ?"
            db.execute(query, (zastepca,))
            query = "UPDATE users SET 'is_admin' = 0 WHERE user_id = ?"
            db.execute(query, (self.id,))
        else:
            #doesn't exist
            print("Taki id nie istnieje")
        conn.commit()


    
    