#main code
import sqlite3 as sql
import re as regex
from random import randint
from datetime import date, datetime
connecter = sql.connect('lab.db')
#Creating basic database strucuture: to start we need to build up the structure
cursor = connecter.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS Users (UserID TEXT PRIMARY KEY, Password TEXT, DateOfSetup TEXT, Admin TEXT)") #Admin 1 == yes 0 == No
cursor.execute("CREATE TABLE IF NOT EXISTS Experiments (ExperimentID TEXT PRIMARY KEY, Equipment TEXT, Date TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS SignIO (Date TEXT, UserID TEXT PRIMARY KEY, SignInTime TEXT, SignOutTime TEXT, TotalTime TEXT)")
'''
Formats for Data:
ADMIN: 1 == yes, 0 == No (can be used to add more levels later)
UserID: Random 4 Digits followed by 3 chars chosen by user
ExperimentID: 10 random letters
Password: len >= 8, must contain >=1 digits e.g: 1234567890
Dates: ISO STANDERD FORMAT (YYYY-MM-DD)
'''
def randomLetter(count):
    out = ''
    letters = 'abcdefghijklmnopqrstuvwxyz'
    for i in range(count):
        out = f'{out}{letters[randint(1, len(letters) - 1)]}'
    return out
def randomNumber(count):
    out = ''
    for i in range(count):
        out = f'{out}{randint(1,9)}'
    return out

def userIDGen():
    ID = f'{randomLetter(4)}{randomNumber(3)}'
    return ID

def experimentIDGen(start):
    ID = f'{randomLetter(10)}'
    return ID

def today():
    return str(date.today().isoformat())

def createUser(password, admin):
    username = userIDGen()
    if regex.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password) == False or admin not in [0, 1]:
        return -1
    cursor.execute(f'INSERT INTO Users VALUES ({username}, {password}, {today()}), {int(admin)}') 
    return username
    
def createExperiment(equipment):
    cursor.execute(f'INSERT INTO Users VALUES ({experimentIDGen()}, {equipment}, {today()})')
    
def showAllUsers():
    rows =  cursor.execute(f'SELECT UserID, Password, DateOfSetup, Admin FROM Users') #Selects values from this table
    return rows.fetchall() #returns all rows

def searchUserID(ID):
    row = cursor.execute(f'SELECT * FROM Users WHERE UserID = "{ID}"') #finds where the id matches
    if row == '':
        return -1
    else:
        return row.fetchone() #returns the first row
    
def searchExperimentID(ID):
    row = cursor.execute(f'SELECT * FROM Experiments WHERE ExperimentID = "{ID}"')
    if row == '':
        return -1
    else: 
        return row.fetchone()

    
def searchUserAdmin(admin):
    row = cursor.execute(f'SELECT * FROM Users WHERE Admin = "{int(admin)}"')
    if row == '':
        return -1
    else:
        return row.fetchone()

    
def searchExperimentDate(date):
    row = cursor.execute(f'SELECT * FROM Experiments WHERE Date == {date}')
    if row == '':
        return -1
    else:
        return row.fetchone()
    

def deleteUser(admin, ID):
    if int(admin) != 1:
        return -1
    cursor.execute(f"DELETE FROM Users WHERE UserID = {ID}")

def deleteExperiment(admin, ID):
    if int(admin) != 1:
        return -1
    cursor.execute(f"DELETE FROM Experiments WHERE ExperimentID = {ID}")


'''
Defining Signing in and out:
sign in: Time taken of day
sign out: time taken of day, 
totalDailyTime = time total in day
'''
def timeCurrent():
    return str(datetime.now().isoformat())[-15: -7] #formats time to be returned as HH:MM:SS

def timeDifference(timein, timeout):
    hoursdiff = int(timeout[0:2]) - int(timein[0:2])
    minsdiff = int(timeout[3:5]) - int(timein[3:5])
    if minsdiff < 0:
        minsdiff += 60
        hoursdiff -= 1
    minsdiff, hoursdiff = str(abs(minsdiff)), str(abs(hoursdiff))
    if len(minsdiff) == 1:
        minsdiff = f'0{minsdiff}'
    elif len(minsdiff) == 0:
        minsdiff = '00'
    if len(hoursdiff) == 1:
        hoursdiff = f'0{hoursdiff}'
    elif len(hoursdiff) == 0:
        hoursdiff = '00'
    return f'{hoursdiff}:{minsdiff}'

def SignIn(UserID): 
    cursor.execute(f"INSERT INTO SignIO VALUES(?,?,?,?,?)", (today(), UserID, timeCurrent(), '0', '0')) #need to implement second part


def SignOut(UserID):
    row = cursor.execute(f'SELECT SignInTime FROM SignIO WHERE (UserID = {UserID} AND Date = {today()})')
    timein = row.fetchone()
    currentTime = timeCurrent()
    totaltime = timeDifference(timein, currentTime)
    cursor.execute(f'UPDATE SignIO SET SignOutTime = {currentTime}, TotalTime = {totaltime} WHERE (UserID = {UserID} AND Date = {today()})')

'''
Testing is as follows:
- Use IC library for outputs
- Confirm all fits intentional output
'''

from icecream import ic
ic(today())

