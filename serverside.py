import sqlite3 as sql
from os import path
from main import *
from random import choice
from string import ascii_letters
connecter = sql.connect('labify.db')
with connecter:
    cursor = connecter.cursor()
def com(): #To be added to every sql command which updates/deletes/creates values
    connecter.commit()
# Creating the neccesary tables
cursor.execute("CREATE TABLE IF NOT EXISTS Users (UserID TEXT PRIMARY KEY, Password TEXT, DateOfSetup TEXT, Admin INTERGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS Equipment (EquipmentName TEXT PRIMARY KEY, CountOfEquipment INTERGER, CountOfInUseEquipment INTERGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS DefaultExperiments(ExperimentName TEXT PRIMARY KEY, Equipment TEXT, MinsTaken INTERGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS LiveExperiments (ExperimentID TEXT PRIMARY KEY, ExperimentName Text, Equipment TEXT, Active INTERGER, UserID TEXT)") #0 = false, 1 = true
cursor.execute("CREATE TABLE IF NOT EXISTS SignIO (UserID TEXT PRIMARY KEY, Date TEXT, SignInTime TEXT, SignOutTime TEXT, TotalTime TEXT)")
com()
#Start of User functions
def createUser(password, admin):
    username = userIDGen()
    if not regex.fullmatch(r'[A-Za-z0-9]{8,}', password) or admin not in [0, 1, '0', '1']:
        print("RegexError, Serverside")
        return False
    if checkExistsInUsers(id):
        print("Duplicate Error")
        return False
    username = str(userIDGen())
    cursor.execute (f"INSERT INTO Users VALUES (?, ?, ?, ?)", (username, str(password), today(), int(admin)))
    print(f"User Created: {username}")
    com()
    return username

def checkExistsInUsers(id) -> bool:
    values = cursor.execute(f"SELECT UserID FROM Users WHERE UserID='{id}'")
    values = values.fetchall()
    if values == []:
        return False
    else:
        return True

def searchUserByID(id):
    values = cursor.execute(f"SELECT * FROM Users WHERE UserID = '{id}'")
    values = values.fetchone()
    if values == None:
        print("User does not exist")
        return [0,0,0,0]
    else:
        print(f"User is {values}")
        return values

def findAllUsers() -> list:
    values = cursor.execute(f'SELECT * FROM Users')
    values = values.fetchall()
    if values == []:
        print("No users in database")
        return ['None']
    else:
        for val in values:
            print(val)
        return values

def checkUserAdmin(id) -> bool:
    if checkExistsInUsers(id):
        user = searchUserByID(id)
        if user[3] == 1:
            return True
        else:
            return False
    else:
        print("User does not exist")
        return False


def updateUserName(id, newid) -> bool: #Must be done by admin
    if checkExistsInUsers(id) == False:
        print("Error: User not found in DB")
        return False
    else:
        cursor.execute(f"UPDATE Users SET UserID = '{newid}' WHERE UserID = '{id}'")
        com()
        print(f"User {newid} has had id changed from {id} -> {newid}")
        return True

def deleteUserFromUsers(id) -> bool:
    if checkExistsInUsers(id) == False:
        print("Error: User not found in DB")
        return False
    else:
        cursor.execute(f"DELETE FROM Users WHERE UserID = '{id}'")
        com()
        return True
#end of Users functions
#start of Equipment functions

def checkEquipmentExists(Name) -> bool:
    values = cursor.execute(f"SELECT EquipmentName FROM Equipment WHERE EquipmentName = '{Name}' ")
    values = values.fetchall()
    if values == []:
        print("Equipment does not exist")
        return False
    else:
        return True

def checkEquipmentUsable(Name) -> bool:
    if checkEquipmentExists(Name) == False:
        print("Equipment was not found")
        return False
    values = cursor.execute(f"SELECT (CountOfEquipment, CountOfInUseEquipment) FROM Equipment WHERE Equipment = '{Name}")
    values = values.fetchone()
    if values[0] == values[1]:
        print("All equipment is in use")
        return False
    else:
        return True

def createNewEquipment(Name, Count) -> bool:
    if checkEquipmentExists(Name) == False:
        print("Equipment already exists")
        return False
    else:
        cursor.execute("INSERT INTO Equipment Values (?, ?, ?)", (Name, Count, 0))
        com()
        return True

def getEquipmentValues(Name):
    if checkEquipmentExists(Name) == False:
        return [None,None, 0, 0]
    values = cursor.execute(f"SELECT * FROM Equipment WHERE Equipment = '{Name}'")
    values = values.fetchone()
    return values

def incrementEquipment(Name) -> bool:
    if checkEquipmentUsable(Name) == False:
        print("Equipment Not useable")
        return False
    else:
        values = getEquipmentValues(Name)
        count = values[2] + 1
        cursor.execute(f"UPDATE Equipment SET CountOfInUseEquipment = {count} WHERE EquipmentName = '{Name}")
        com()
        return True

def decrementEquipment(Name) -> bool:
    if checkEquipmentUsable(Name) == False:
        print("Equipment Not useable")
        return False
    else:
        values = getEquipmentValues(Name)
        count = values[2] - 1
        if count < 0:
            print("Count Can NOT go below 0")
            return False
        cursor.execute(f"UPDATE Equipment SET CountOfInUseEquipment = {count} WHERE EquipmentName = '{Name}")
        com()
        return True

def deleteEquipment(Name) -> bool:
    if checkEquipmentExists(Name) == False:
        print("CANT BE DELETED, DOES NOT EXIST")
        return False
    cursor.execute(f"DELETE FROM Experiments WHERE Name = '{Name}'")
    com()
    return True

#equipment functions ends
#defaultExperiments functions start

def checkDefaultExperimentExists(Name) -> bool:
    values = cursor.execute(f"SELECT ExperimentName FROM DefaultExperiments WHERE ExperimentName = '{Name}'")
    values = values.fetchone()
    if values == []:
        print("Value not found")
        return False
    else:
        print("Value Found")
        return True

def createDefaultExperiment(Name, Equipment, TimeTaken) :
    if checkDefaultExperimentExists(Name) == True:
        print("Already exists")
        return False
    else:
        cursor.execute(f"INSERT INTO DefaultExperiments Values(?, ?, ?)", (Name, Equipment, TimeTaken))
        com()
        print("Default Experiment added")
        return True


def removeDefaultExperiment(Name):
    if checkDefaultExperimentExists(Name) == False:
        print("Experiment Not Found")
        return False
    cursor.execute(f"DELETE FROM DefaultExperiments WHERE Name = '{Name}'")
    com()
    print("Default Experiment Deleted")
    return True

#end of defaultexperiments
#start of liveexperiments

def checkExperimentExistsByName(Name):
    values = cursor.execute(f"SELECT ExperimentName FROM LiveExperiments WHERE ExperimentName = '{Name}'")
    values = values.fetchone()
    if values == []:
        print("Value not found")
        return False
    else:
        print("Value Found")
        return True

def checkExperimentExistsByID(ID):
    values = cursor.execute(f"SELECT ExperimentID FROM LiveExperiments WHERE ExperimentID = '{ID}'")
    values = values.fetchone()
    if values == []:
        print("Value not found")
        return False
    else:
        print("Value Found")
        return True

def createExperimentID() -> str:
    ID = ''
    for i in range(0, 12):
        ID = "f{ID}{choice(ascii_letters)}"
    if checkExperimentExistsByID(ID) == True:
        createExperimentID()
    return ID

'''cursor.execute("CREATE TABLE IF NOT EXISTS DefaultExperiments(ExperimentName TEXT PRIMARY KEY, Equipment TEXT, MinsTaken INTERGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS LiveExperiments (ExperimentID TEXT PRIMARY KEY, ExperimentName Text, Equipment TEXT, Active BOOLEAN, UserID TEXT))")'''
def createLiveExperimentFromDefault(NameOfDefault, User):
    if checkDefaultExperimentExists(NameOfDefault) == False:
        print("Default Experiment Not Found")
        return False
    defaultValues = cursor.execute(f"SELECT * FROM DefaultExperiments WHERE ExperimentName = '{NameOfDefault}'")
    defaultValues = defaultValues.fetchone()
    Equipment = defaultValues[1].split(',')
    for obj in Equipment:
        increment = incrementEquipment(obj)
        if checkEquipmentUsable(obj) == False:
            print("Equipment Not Usable")
            return False
        if incrementEquipment(obj) == False:
            print("Error incrementing equipment")
            return False
    ID = createExperimentID()
    cursor.execute(f"INSERT INTO LiveExperiments Values (?, ?, ?, ?, ?)", (ID, NameOfDefault, Equipment, True, User))
    com()
    return True

def createLiveExperimentFromNew(NameofExperiment, Equipment, User):
    if checkDefaultExperimentExists(NameofExperiment) == True:
        print("Default Experiment Already Exists")
        return False
    for obj in Equipment:
        if checkEquipmentUsable(obj) == False:
            print("Equipment Not Usable")
            return False
        if incrementEquipment(obj) == False:
            print("Error incrementing equipment")
            return False
    ID = createExperimentID()
    cursor.execute(f"INSERT INTO LiveExperiments Values (?, ?, ?, ?, ?)", (ID, NameofExperiment, Equipment, True, User))
    com()
    return True

def removeLiveExperimentByID(ID):
    if checkExperimentExistsByID(ID) == False:
        print("Experiment Not Found")
        return False
    values = cursor.execute(f"SELECT Equipment FROM LiveExperiments WHERE ExperimentID = '{ID}'")
    values = values.fetchone()
    for obj in values:
        decrement = decrementEquipment(obj)
        if decrement == False:
            print("Error Decrementing Equipment")
            return False
    cursor.execute(f"DELETE FROM LiveExperiments WHERE ExperimentID = '{ID}'")
    com()
    return

def getIDOfLiveFromName(Name):
    values = cursor.execute(f"SELECT ExperimentID FROM LiveExperiments WHERE ExperimentName = '{Name}'")
    values = values.fetchone()
    if values == []:
        print("Experiment Not Found")
        return 0
    return values[0]

def getLiveExperimentValuesByID(ID):
    if checkExperimentExistsByID(ID) == False:
        print("Experiment Not Found")
        return [None, None, None, None, None]
    values = cursor.execute(f"SELECT * FROM LiveExperiments WHERE ExperimentID = '{ID}'")
    values = values.fetchone()
    return values

def getLiveExperimentValuesByName(Name):
    ID = getIDOfLiveFromName(Name)
    if ID == 0:
        print("Experiment Not Found")
        return [None, None, None, None, None]
    return getLiveExperimentValuesByID(ID)

