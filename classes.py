import datetime
from default_base import db, conn

class Artist:
    def __init__(self, pseudonim, opis, id=None): # is always executed when the class is being initiated
        self.pseudonim = pseudonim
        self.opis = opis
        self.id = id

    #tworzenie
    def create(self):
        query = "INSERT INTO tworcy (pseudonim, description) VALUES (?, ?)"
        db.execute(query, (self.pseudonim, self.opis))
        conn.commit()

    #edytowanie
    def update(self):
        query = "UPDATE tworcy SET pseudonim = ?, description = ? WHERE artist_id = ?"
        db.execute(query, (self.pseudonim, self.opis, self.id))
        conn.commit()

class Songs:
    def __init__(self, title, genre, artist, album, status, id=None): # is always executed when the class is being initiated
        self.title = title
        self.genre = genre
        self.artist = artist
        self.album = album
        self.status = status
        self.id = id

    #tworzenie
    def create(self):
        query = "INSERT INTO utwory (title, genre, artist, album, created_at) VALUES (?, ?, ?, ?, ?)"
        teraz = datetime.datetime.now()
        createtime = teraz.strftime("%Y-%m-%d %H:%M:%S")
        db.execute(query, (self.title, self.genre, self.artist, self.album, createtime))
        conn.commit()
        db.execute("SELECT IDENT_CURRENT('utwory')")
        self.id = db.fetchone()[0]
        query = "INSERT INTO wykonawcy_utwory (id_wykonawcy, id_utworu) VALUES (?, ?)"
        db.execute(query, (self.artist, self.id))
        conn.commit()

    #edytowanie
    def update(self):
        query = "UPDATE utwory SET title = ?, genre = ?, artist = ?, album = ?, status = ? WHERE song_id = ?"
        db.execute(query, (self.title, self.genre, self.artist, self.album, self.status, self.id))
        query2 = "UPDATE wykonawcy_utwory SET id_wykonawcy = ? WHERE id_utworu = ?"
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
        query = "INSERT INTO plyty (title, description, genre) VALUES (?, ?, ?)"
        db.execute(query, (self.title, self.description, self.genre))
        conn.commit()

    #edytowanie
    def update(self):
        query = "UPDATE plyty SET title = ?, description = ?, genre = ? WHERE album_id = ?"
        db.execute(query, (self.title, self.description, self.genre, self.id))
        conn.commit()

#tworzenie relacji twórca-utwór (gdy są więcej niż jeden)
def song_singer_connect(singer_id,song_id):
    query = "INSERT INTO wykonawcy_utwory (id_wykonawcy, id_utworu) VALUES (?, ?)"
    db.execute(query, (singer_id, song_id))
    conn.commit()

#przypisanie utworów do płyt
def songs_to_album(album_id, singer_id):
    #jeżeli twórca jest podany, to wszystkie piosenki w albumie będą należały do niego
    query = "SELECT song_id FROM utwory WHERE album = ?"
    db.execute(query, (album_id,))
    songs_in_album = db.fetchall()
    #dla każdego utworu zmienić pole 'artist' na singer_id
    for song in songs_in_album:
        query2 = "UPDATE utwory SET artist = ? WHERE song_id = ?"
        db.execute(query2, (singer_id, song['song_id']))
        conn.commit()
        query3 = "UPDATE wykonawcy_utwory SET id_wykonawcy = ? WHERE id_utworu = ?"
        db.execute(query3, (singer_id, song['song_id']))
        conn.commit()

class User:
    def __init__(self, username, is_admin, id):
        self.username = username
        self.is_admin = is_admin
        self.id = id
        self.get_liked_albums()
        self.get_liked_songs()
        self.get_personal_info()


    def get_personal_info(self):
        query = "SELECT name, surname, email, adress FROM users WHERE user_id = ?"
        db.execute(query, (self.id,))
        result = db.fetchone()
        self.name = result['name']
        self.surname = result['surname']
        self.email = result['email']
        self.adress = result['adress']
    
    def get_liked_albums(self):
        self.liked_albums = []
        query = "SELECT ulubione_plyty.id_album, plyty.title, plyty.description FROM ulubione_plyty INNER JOIN plyty ON ulubione_plyty.id_album = plyty.album_id WHERE ulubione_plyty.id_usera = ?"
        db.execute(query, (self.id,))
        rows = db.fetchall()
        for row in rows:
            self.liked_albums.append({"album_id":row['id_album'], "title":row['title'], "description":row['description']})
    def like_album(self, album_id, album_title, album_description):
        liked_album = {"album_id":album_id, "title":album_title, "description":album_description}
        if liked_album in self.liked_albums:
            pass
        else:
            self.liked_albums.append(liked_album)
            query = "INSERT INTO ulubione_plyty (id_usera, id_album) VALUES (?, ?)"
            db.execute(query, (self.id, liked_album['album_id']))
            db.commit()
    def dislike_album(self, album_id):
        index_to_remove = next((index for index, album in enumerate(self.liked_albums) if album["album_id"] == album_id), None)
        if index_to_remove is not None:
            del self.liked_albums[index_to_remove]
            query = "DELETE FROM ulubione_plyty WHERE id_usera = ? AND id_album = ?"
            db.execute(query, (self.id, album_id))
            db.commit()

    def get_liked_songs(self):
        self.liked_songs = []
        query = "SELECT ulubione_utwory.id_utworu, utwory.title, tworcy.pseudonim, genre.title AS genre FROM ulubione_utwory INNER JOIN utwory ON ulubione_utwory.id_utworu = utwory.song_id INNER JOIN tworcy ON utwory.artist = tworcy.artist_id INNER JOIN genre ON utwory.genre = genre.id_genre WHERE ulubione_utwory.id_usera = ?"
        db.execute(query, (self.id,))
        rows = db.fetchall()
        for row in rows:
            self.liked_songs.append({"song_id":row['id_utworu'], "title":row['title'], "artist":row['pseudonim'], "genre":row['genre']})      
    def like_song(self, song_id, song_title, song_artist, song_genre):
        liked_song = {"song_id":song_id, "title":song_title, "artist":song_artist, "genre":song_genre}
        if liked_song in self.liked_songs:
            pass
        else:
            self.liked_songs.append(liked_song)
            query = "INSERT INTO ulubione_utwory (id_usera, id_utworu) VALUES (?, ?)"
            db.execute(query, (self.id, liked_song['song_id']))
            db.commit()
    def dislike_song(self, song_id):
        index_to_remove = next((index for index, song in enumerate(self.liked_songs) if song["song_id"] == song_id), None)
        if index_to_remove is not None:
            del self.liked_songs[index_to_remove]
            query = "DELETE FROM ulubione_utwory WHERE id_usera = ? AND id_utworu = ?"
            db.execute(query, (self.id, song_id))
            db.commit()
    
    def update_user_info(self):
        query = "UPDATE users SET username = ?, name = ?, surname = ?, email = ?, adress = ? WHERE user_id = ?"
        db.execute(query, (self.username, self.name, self.surname, self.email, self.adress, self.id))
        conn.commit()

class Admin(User):
    def __init__(self, username, is_admin, id):
        super().__init__(username, is_admin, id)
        
    def awans(self, new_admin_id):
        query = "UPDATE users SET is_admin = 1 WHERE user_id = ?"
        db.execute(query, (new_admin_id,))
        conn.commit()

    def delete_other_admin(self, admin_to_fire):
        #tylko admin może usunąć innego admina
        db.execute("SELECT user_id FROM users WHERE is_admin = 1 ORDER BY user_id ASC")
        results = db.fetchone()
        if results[0] == admin_to_fire:
            #nie można usunąć pierwszego admina
            return False
        else:
            query = "UPDATE users SET is_admin = 0 WHERE user_id = ?"
            db.execute(query, (admin_to_fire,))
        conn.commit()
        
    def resignation(self, zastepca):
        #moze sam zrezygnowac, ale uwaga: musi wskazac kogos innego z listy
        query = "UPDATE users SET is_admin = 1 WHERE user_id = ?"
        db.execute(query, (zastepca,))
        query = "UPDATE users SET is_admin = 0 WHERE user_id = ?"
        db.execute(query, (self.id,))
        conn.commit()


    
    