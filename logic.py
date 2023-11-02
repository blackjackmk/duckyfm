import sqlite3
import hashlib

from classes import Artist

#database connect
conn = sqlite3.connect("duckybase.db") #if don't exist - create
db = conn.cursor()

#logowanie
def logowanie(login, password):
    query = "SELECT username, user_id, is_admin, haslo FROM users WHERE username = ?"
    db.execute(query, (login,))
    result = db.fetchone()
    hash = hashlib.sha256()
    hash.update(password.encode())
    szyfred = hash.hexdigest()  #zaszyfrowane hasło
    if szyfred == result[3]:
        print("login success")
    else:
        print("login error")

#tworzenie twórcy
def create_artist(name, description):
    artist = Artist(name, description)
    artist.create()

#edytowanie twórcy
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

# Zmieniamy opis
#edit_artist(1, opis="Nowy opis")

#usunięcie twórcy
def delete_artist(id):
    query = "DELETE FROM tworcy WHERE artist_id = ?"
    db.execute(query, (id,))
    conn.commit()

db.close()