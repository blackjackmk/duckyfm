import hashlib

from default_base import db, conn
from classes import User, Admin

CurrentUser = None

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
        if result[2] == 0:
            CurrentUser = User(result[0], False, result[1])
        else:
            CurrentUser = Admin(result[0], result[1])
    else:
        print("login error")

#register_user

while(CurrentUser == None):
    login = input("Podaj login: ")
    password = input("Podaj haslo: ")
    logowanie(login, password)

