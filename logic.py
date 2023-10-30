import sqlite3
import hashlib

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
    szyfred = hash.hexdigest()#zaszyfrowane hasło
    if szyfred == result[3]:
        print("login success")
    else:
        print("login error")

#logowanie('kaczor','pass')
#conn.commit()
db.close()