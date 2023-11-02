import sqlite3

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
