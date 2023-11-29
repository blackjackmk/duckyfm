import hashlib

from classes import Artist, Songs, Plyty
from classes import only_admin
from default_base import db, conn

#tworzenie twórcy
@only_admin
def create_artist(name, description):
    artist = Artist(name, description)
    artist.create()

#edytowanie twórcy
@only_admin
def edit_artist(id, **args):
    #tworzymy object z istniejącego artysty
    query = "SELECT * FROM tworcy WHERE artist_id = ?"
    db.execute(query, (id,))
    result = db.fetchone()
    artist = Artist(result[1], result[2], result[0])
    #zmieniamy potrzebne pola objektu
    # Definiujemy listę pól, które chcemy zaktualizować.
    fields_to_update = []

    # Pobieramy wartości pól do zmiany z argumentów funkcji.
    for field, value in args.items():
        # Dodajemy pole do listy pól do aktualizacji.
        fields_to_update.append(field)

    # Aktualizujemy pola w obiekcie artysty.
    for field in fields_to_update:
        artist.__setattr__(field, value)
    #zapisujemy zmiany
    artist.update()

# Zmieniamy opis (musimy podać jaki argument zmienić)
#edit_artist(1, opis="Nowy opis")

#usunięcie twórcy
@only_admin
def delete_artist(id):
    query = "DELETE FROM tworcy WHERE artist_id = ?"
    db.execute(query, (id,))
    conn.commit()

#tworzenie relacji twórca-utwór (gdy są więcej niż jeden)
@only_admin
def song_singer_connect(singer_id,song_id):
    query = "INSERT INTO wykonawcy_utwory (id_wykonawcy, id_utworu) VALUES (?, ?)"
    db.execute(query, (singer_id, song_id))
    conn.commit()

#tworzenie utworu
@only_admin
def create_song(title, genre, artist, album=None):
    song = Songs(title, genre, artist, album)
    song.create()

#edytowanie utworu
@only_admin
def edit_song(id, **args):
    query = "SELECT * FROM utwory WHERE song_id = ?"
    db.execute(query, (id,))
    result = db.fetchone()
    song = Songs(result[1], result[2], result[3], result[4], result[5], result[0])
    fields_to_update = []

    for field, value in args.items():
        fields_to_update.append(field)

    for field in fields_to_update:
        song.__setattr__(field, value)
    song.update()

#usunięcie utworu
@only_admin
def delete_song(id):
    query = "DELETE FROM utwory WHERE song_id = ?"
    db.execute(query, (id,))
    conn.commit()

#tworzenie plyty
@only_admin
def create_album(title, description, genre, artist):
    album = Plyty(title, description, genre, artist)
    album.create()

#edytowanie plyty
@only_admin
def edit_album(id, **args):
    query = "SELECT * FROM plyty WHERE album_id = ?"
    db.execute(query, (id,))
    result = db.fetchone()
    album = Plyty(result[1], result[2], result[3], result[4], result[0])
    fields_to_update = []

    for field, value in args.items():
        fields_to_update.append(field)

    for field in fields_to_update:
        album.__setattr__(field, value)
    album.update()
    
#przypisanie utworów do płyt
@only_admin
def songs_to_album(album_id, songs, singer_id = None): #songs to set z id utworów
    #jeżeli twórca jest podany, to wszystkie piosenki w albumie będą należały do niego
    #dla każdego utworu zmienić pole 'album' na album_id
    for song in songs:
        s = Songs(None,None,singer_id,album_id,None,song)
        s.update()

#usunięcie plyty
@only_admin
def delete_album(id):
    query = "DELETE FROM plyty WHERE album_id = ?"
    db.execute(query, (id,))
    conn.commit()

db.close()