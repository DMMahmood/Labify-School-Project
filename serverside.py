import sqlite3 as sql
from os import path
from main import *
connecter = sql.connect('labify.db')
with connecter:
    cursor = connecter.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Users (UserID TEXT PRIMARY KEY, Password TEXT, DateOfSetup TEXT, Admin INTERGER)") 
cursor.execute("CREATE TABLE IF NOT EXISTS Experiments (ExperimentID TEXT PRIMARY KEY, Equipment TEXT, Date TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS SignIO (UserID TEXT PRIMARY KEY, Date TEXT, SignInTime TEXT, SignOutTime TEXT, TotalTime TEXT)")


def createUser(password, admin):
    username = userIDGen()
    if not regex.fullmatch(r'[A-Za-z0-9]{8,}', password) or admin not in [0, 1, '0', '1']:
        print("RegexError, Serverside")
        return -1
    username = str(userIDGen())
    cursor.execute (f"INSERT INTO Users VALUES (?, ?, ?, ?)", (username, str(password), today(), int(admin)))
    print(f"User Created: {username}")
    return username

def checkExistsInUsers(id):
    values = cursor.execute(f"SELECT UserID FROM Users WHERE UserID='{id}'")
    values = values.fetchall()
    if values == '':
        return False
    else:
        return True
    
def searchUserByID(id):
    values = cursor.execute(f"SELECT * FROM Users WHERE UserID = '{id}'")
    values = values.fetchone()
    if values == None:
        print("User does not exist")
        return False
    else:
        print(f"User is {values}")
        return values
    
def findAllUsers():
    values = cursor.execute(f'SELECT * FROM Users')
    values = values.fetchall()
    if values == []:
        print("No users in database")
    else:
        for val in values:
            print(val)
        return values

def checkUserAdmin(id):
    if checkExistsInUsers(id):
        user = searchUserByID(id)
        if user[3] == 1:
            return True
        else:
            return False
    else:
        print("User does not exist")
        return False
    
createUser("ADMIN1234", 1)
searchUserByID("ADMIN")
findAllUsers()