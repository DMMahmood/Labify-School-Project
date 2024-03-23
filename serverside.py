import sqlite3 as sql
from os import path
from main import *
connecter = sql.connect('labify.db')
with connecter:
    cursor = connecter.cursor()
def com(): #To be added to every sql command which updates/deletes/creates values
    connecter.commit()
#Creating the neccesary tables
cursor.execute("CREATE TABLE IF NOT EXISTS Users (UserID TEXT PRIMARY KEY, Password TEXT, DateOfSetup TEXT, Admin INTERGER)") 
cursor.execute("CREATE TABLE IF NOT EXISTS Equipment (EquipmentName TEXT PRIMARY KEY, CountOfEquipment INTERGER, CountOfInUseEquipment INTERGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS DefaultExperiments(ExperimentName TEXT PRIMARY KEY, Equipment TEXT, MinsTaken INTERGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS LiveExperiments (ExperimentID TEXT PRIMARY KEY, Equipment TEXT, Date TEXT)")
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

def checkExistsInUsers(id):
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
    

def updateUserName(id, newid): #Must be done by admin
    if checkExistsInUsers(id) == False:
        print("Error: User not found in DB")
        return False
    else:
        cursor.execute(f"UPDATE Users SET UserID = '{newid}' WHERE UserID = '{id}'")
        com()
        print(f"User {newid} has had id changed from {id} -> {newid}")
        return True

def deleteUserFromUsers(id):
    if checkExistsInUsers(id) == False:
        print("Error: User not found in DB")
        return False
    else:
        cursor.execute(f"DELETE FROM Users WHERE UserID = '{id}'")
        com()
        return True
#end of Users functions
#start of Equipment functions
     
def checkEquipmentExists(Name):
    values = cursor.execute(f"SELECT EquipmentName FROM Equipment WHERE EquipmentName = '{Name}' ")
    values = values.fetchall()
    if values == []:
        print("Equipment does not exist")
        return False
    else:
        return True
    
def checkEquipmentUsable(Name):
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
    
def createNewEquipment(Name, Count):
    if checkEquipmentExists(Name) == False:
        print("Equipment already exists")
        return False
    else:
        cursor.execute("INSERT INTO Equipment Values (?, ?, ?)", (Name, Count, 0))
        com()
        return True
    
def getEquipmentValues(Name):
    if checkEquipmentExists(Name) == False:
        return False
    values = cursor.execute(f"SELECT * FROM Equipment WHERE Equipment = '{Name}'")
    values = values.fetchone()
    return values

def incrementEquipment(Name):
    if checkEquipmentUsable(Name) == False:
        print("Equipment Not useable")
        return False
    else:
        values = getEquipmentValues()
        count = values[2] + 1
        cursor.excecute(f"UPDATE Equipment SET CountOfInUseEquipment = {count} WHERE EquipmentName = '{Name}")
        com()
        return True

def decrementEquipment(Name):
    if checkEquipmentUsable(Name) == False:
        print("Equipment Not useable")
        return False
    else:
        values = getEquipmentValues()
        count = values[2] - 1 
        if count < 0:
            print("Count Can NOT go below 0")
            return False
        cursor.excecute(f"UPDATE Equipment SET CountOfInUseEquipment = {count} WHERE EquipmentName = '{Name}")
        com()
        return True

def deleteEquipment(Name):
    if checkEquipmentExists(Name) == False:
        print("CANT BE DELETED, DOES NOT EXIST")
        return False
    cursor.execute(f"DELETE FROM Experiments WHERE Name = '{Name}'")
    com()
    return True

#equipment functions ends
#defaultExperiments functions start

def checkDefaultExperimentExists(Name):
    values = cursor.execute(f"SELECT ExperimentName FROM DefaultExperiments WHERE ExperimentName = '{Name}'")
    values = values.fetchone()
    if values == []:
        print("Value not found")
        return False
    else:
        print("Value Found")
        return True
    
def createDefaultExperiment(Name, Equipment, TimeTaken) -> True:
    if checkDefaultExperimentExists(Name) == True:
        print("Already exists")
        return False
    Equipment = Equipment.split(',')
    for Name in Equipment:
        if checkEquipmentExists(Name) == False:
            print("Eqiupment not available")
            return False
    print(f"New experiment is: {Name}, {Equipment}, {TimeTaken}")
    cursor.execute(f"INSERT INTO DefaultExperiments Values (?,?,?)", (Name, Equipment, TimeTaken))
    com()
    return True
    
def deleteDefaultExperiment(Name):
    if checkDefaultExperimentExists(Name) == False:
        print("experiment does not exist")
        return False
    cursor.execute(f"DELETE FROM DefaultExperiments WHERE ExperimentName = '{Name}'")
    com()
    return True

def updateDefaultExperimentTimeTaken(Name, NewTimeTaken):
    if checkDefaultExperimentExists(Name) == False:
        print("Experiment does not exist")
        return False
    cursor.execute(f"UPDATE SET MinsTaken = {NewTimeTaken} WHERE ExperimentName = '{Name}'")
    com()
    return True
    
#end of default experiment
#start of live experiment 

def checkLiveExperimentExists(Name) -> bool:
    values = cursor.execute(f"SELECT * FROM LiveExperiments WHERE ExperimentName = '{Name}'")
    values = values.fetchone()
    if values == []:
        print("Experiment not found")
        return False
    print("Experiment Found")
    return True
    
def createLiveExperiment(Name):