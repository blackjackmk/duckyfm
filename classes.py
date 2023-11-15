import sqlite3
import datetime

#database connect
conn = sqlite3.connect("duckybase.db") #if don't exist - create
db = conn.cursor()

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
    def __init__(self, title=None, link=None, artist=None, album=None, status="Published", id=None): # is always executed when the class is being initiated
        self.title = title
        self.link = link
        self.artist = artist
        self.album = album
        self.status = status
        self.id = id

    #tworzenie
    def create(self):
        query = "INSERT INTO utwory ('title', 'link', 'artist', 'album', 'created_at') VALUES (?, ?, ?, ?, ?)"
        teraz = datetime.datetime.now()
        createtime = teraz.strftime("%Y-%m-%d %H:%M:%S")
        db.execute(query, (self.title, self.link, self.artist, self.album, createtime))
        conn.commit()
        self.id = db.lastrowid

    #edytowanie
    def update(self):
        query = "UPDATE utwory SET 'title' = ?, 'link' = ?, 'artist' = ?, 'album' = ?, 'status' = ? WHERE song_id = ?"
        db.execute(query, (self.title, self.link, self.artist, self.album, self.status, self.id))
        conn.commit()

class Plyty:
    def __init__(self, title, description, link, artist, id=None):
        self.title = title
        self.description = description
        self.link = link
        self.artist = artist
        self.id = id

    #tworzenie
    def create(self):
        query = "INSERT INTO plyty ('title', 'description', 'link', 'artist') VALUES (?, ?, ?, ?)"
        db.execute(query, (self.title, self.description, self.link, self.artist))
        conn.commit()
        self.id = db.lastrowid

    #edytowanie
    def update(self):
        query = "UPDATE plyty SET 'title' = ?, 'description' = ?, 'link' = ?, 'artist' = ? WHERE album_id = ?"
        db.execute(query, (self.title, self.description, self.link, self.artist, self.id))
        conn.commit()