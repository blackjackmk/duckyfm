import hashlib
import re

from default_base import db, conn
from classes import User, Admin

global CurrentUser
CurrentUser = None
#logowanie
def logowanie(login, password):
    query = "SELECT username, user_id, is_admin, haslo FROM users WHERE username = ?"
    db.execute(query, (login,))
    result = db.fetchone()
    hash = hashlib.sha256()
    hash.update(password.encode())
    global CurrentUser
    szyfred = hash.hexdigest()  #zaszyfrowane hasło
    if szyfred == result['haslo']:
        if result['is_admin'] == 0:
            CurrentUser = User(result['username'], False, result['user_id']) #zwykły użytkownik
        else:
            CurrentUser = Admin(result['username'], True,  result['user_id']) #użytkownik z uprawnieniami admina
        return CurrentUser
    else:
        return None

def rejestracja(username, name, surname, email, haslo, haslo2):
    #sprawdzamy wszystkie warunki
    regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
    if (re.match(regex, email) == False):
        print("Podaj poprawny email")
        return False
    if (haslo != haslo2):
        print("Hasła nie zgadzają się")
        return False
    #pierwszy zarejestrowany uzytkownik staje sie administratorem systemu
    db.execute("SELECT * FROM users")
    results = db.fetchone()
    if results is None:
        is_admin = 1
    else:
        is_admin = 0
    #sprawdzamy czu user o takim username istnieje
    db.execute("SELECT * FROM users WHERE username = ?", username)
    results = db.fetchone()
    if results is None:
        pass
    else:
        raise Exception("Taki user już istnieje")
    #wpisujemy użytkownika w bazie
    query = "INSERT INTO users (username, name, surname, email, is_admin, haslo) VALUES (?, ?, ?, ?, ?, ?)"
    hash = hashlib.sha256()
    hash.update(haslo.encode())
    haslo_zaszyfrowane = hash.hexdigest()
    db.execute(query, (username, name, surname, email, is_admin, haslo_zaszyfrowane))
    conn.commit()

#rejestracja("testman", "Tester", "Maksym", "credentials@s.pm.pl", "test123", "test123")

while (CurrentUser == None):
    login = input("Podaj login: ")
    password = input("Podaj haslo: ")
    logowanie(login, password)

