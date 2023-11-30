artist_table = '''CREATE TABLE tworcy (
    artist_id   INTEGER   PRIMARY KEY AUTOINCREMENT,
    pseudonim   TEXT (25),
    description TEXT (50) );'''
utwory_table = '''CREATE TABLE utwory (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT (30), 
    genre TEXT, 
    artist INTEGER, 
    album INTEGER, 
    status TEXT DEFAULT Published, 
    created_at DATE);'''
plyty_table = '''CREATE TABLE plyty (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT (30),
    description TEXT (60),
    genre TEXT,
    artist REFERENCES tworcy (artist_id) ON DELETE CASCADE ON UPDATE CASCADE);'''
users_table = '''CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
    username TEXT (30), 
    name TEXT (60), 
    surname TEXT (80), 
    email TEXT (40),
    adress TEXT, 
    is_admin INTEGER (1) DEFAULT (0), 
    haslo TEXT NOT NULL);'''
connect_table = '''CREATE TABLE wykonawcy_utwory (
    connect_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_wykonawcy         REFERENCES tworcy (artist_id) ON DELETE CASCADE,
    id_utworu            REFERENCES utwory (song_id) 
);'''

import sqlite3

#database connect
conn = sqlite3.connect("duckybase.db") #if don't exist - create 
db = conn.cursor()

try:
    db.execute("SELECT * FROM users") # pozwala sprawdzić czy istnieją tabele, czy stworzona pusta baza
except sqlite3.OperationalError:
    #print("Nie ma takiej tabeli")
    #tworzymy wszystkie tabele
    db.execute(artist_table)
    db.execute(utwory_table)
    db.execute(plyty_table)
    db.execute(users_table)
    db.execute(connect_table)
    #możemy równierz wypełnić ich tutaj domyślnymi wartościami