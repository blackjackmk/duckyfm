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
def edit_artist(id):
    #tworzymy object z istniejącego artysty
    query = "SELECT * FROM tworcy WHERE artist_id = ?"
    db.execute(query, (id,))
    result = db.fetchone()
    artist = Artist(result[2], result[1])
    artist.id = result[0]
    #zmieniamy potrzebne dane
    ##artist.pseudonim = "Nowe imie"
    #zapisujemy zmiany
    artist.update()

#usunięcie twórcy
def delete_artist(id):
    query = "DELETE FROM tworcy WHERE artist_id = ?"
    db.execute(query, (id,))
    conn.commit()

db.close()