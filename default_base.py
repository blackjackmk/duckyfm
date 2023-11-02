artist_table = '''CREATE TABLE tworcy (
    artist_id   INTEGER   PRIMARY KEY AUTOINCREMENT,
    pseudonim   TEXT (25),
    description TEXT (50) );'''
utwory_table = '''CREATE TABLE utwory (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT (30), 
    link TEXT, 
    artist INTEGER, 
    album INTEGER, 
    status TEXT DEFAULT Published, 
    created_at DATE);'''
plyty_table = '''CREATE TABLE plyty (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT (30),
    description TEXT (60),
    link TEXT,
    artist REFERENCES tworcy (artist_id) ON DELETE CASCADE ON UPDATE CASCADE);'''
users_table = '''CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
    username TEXT (30), 
    name TEXT (60), 
    surname TEXT (80), 
    adress TEXT, 
    is_admin INTEGER (1) DEFAULT (0), 
    haslo TEXT NOT NULL);'''