artist_table = '''CREATE TABLE tworcy ( 
    artist_id INT IDENTITY PRIMARY KEY, 
    pseudonim NVARCHAR (50), 
    description NVARCHAR (255) )'''
utwory_table = '''CREATE TABLE utwory (
    song_id    INT IDENTITY PRIMARY KEY,
    title      NVARCHAR (30),
    genre      INT   REFERENCES genre (id_genre) ON UPDATE CASCADE,
    artist     INT   REFERENCES tworcy (artist_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    album      INT   REFERENCES plyty (album_id) ON DELETE NO ACTION ON UPDATE NO ACTION,
    status     NVARCHAR(12) DEFAULT 'Published',
    created_at DATE
)'''

plyty_table = '''CREATE TABLE plyty (
    album_id    INT IDENTITY PRIMARY KEY,
    title       NVARCHAR (30),
    description NVARCHAR (60),
    genre       INT   REFERENCES genre (id_genre) ON UPDATE CASCADE
)'''
users_table = '''CREATE TABLE users (
    user_id INT IDENTITY PRIMARY KEY, 
    username NVARCHAR (30), 
    name NVARCHAR (60), 
    surname NVARCHAR (80), 
    email NVARCHAR (40),
    adress NVARCHAR (250), 
    is_admin INT DEFAULT (0), 
    haslo NVARCHAR(500) NOT NULL);'''
genre = '''CREATE TABLE genre (
    id_genre INT IDENTITY PRIMARY KEY,
    title    NVARCHAR(10)    NOT NULL
                     UNIQUE
);'''
wykonawcy_utwory = '''CREATE TABLE wykonawcy_utwory (
    connect_id   INT IDENTITY PRIMARY KEY,
    id_wykonawcy        INT REFERENCES tworcy (artist_id) ON DELETE CASCADE,
    id_utworu           INT REFERENCES utwory (song_id) 
);'''
ulubione_utwory = '''CREATE TABLE ulubione_utwory (
    connect_id   INT IDENTITY PRIMARY KEY,
    id_usera       INT REFERENCES users (user_id) ON DELETE CASCADE,
    id_utworu           INT REFERENCES utwory (song_id) 
);'''
ulubione_plyty = '''CREATE TABLE ulubione_plyty (
    connect_id   INT IDENTITY PRIMARY KEY,
    id_usera        INT REFERENCES users (user_id) ON DELETE CASCADE,
    id_album          INT REFERENCES plyty (album_id) 
);'''

import pypyodbc as odbc
from credential import db_login, db_pass, db_name, server_name

conn = odbc.connect(
  SERVER = server_name,
  DATABASE = db_name,
  UID = db_login,
  PWD = db_pass,
  DRIVER='{ODBC Driver 18 for SQL Server}',
  Trusted_Connection="no"
)

db = conn.cursor()



try:
    db.execute("SELECT * FROM users")
except odbc.ProgrammingError:
    #raise Exception("Brak tabeli users")
    db.execute(artist_table)
    db.execute(users_table)
    db.execute(genre)
    db.execute(plyty_table)
    db.execute(utwory_table)
    db.execute(wykonawcy_utwory)
    db.execute(ulubione_utwory)
    db.execute(ulubione_plyty)
    conn.commit()