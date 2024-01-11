from classes import Artist, Songs, Plyty
from default_base import db, conn

#usunięcie twórcy
def delete_artist(id):
    query = "DELETE FROM tworcy WHERE artist_id = ?"
    db.execute(query, (id,))
    conn.commit()

#tworzenie relacji twórca-utwór (gdy są więcej niż jeden)
def song_singer_connect(singer_id,song_id):
    query = "INSERT INTO wykonawcy_utwory (id_wykonawcy, id_utworu) VALUES (?, ?)"
    db.execute(query, (singer_id, song_id))
    conn.commit()

#tworzenie utworu
def create_song(title, genre, artist, album=None):
    song = Songs(title, genre, artist, album)
    song.create() #relacja tworzy się automatycznie w klasie

#edytowanie utworu
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
def delete_song(id):
    query = "DELETE FROM utwory WHERE song_id = ?"
    db.execute(query, (id,))
    conn.commit()
   
#przypisanie utworów do płyt
def songs_to_album(album_id, songs, singer_id = None): #songs to set z id utworów
    #jeżeli twórca jest podany, to wszystkie piosenki w albumie będą należały do niego
    #dla każdego utworu zmienić pole 'album' na album_id
    for song in songs:
        s = Songs(None,None,singer_id,album_id,None,song)
        s.update()
