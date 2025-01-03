import sqlite3 as sql #use sql
from os import path #save files to paths
from random import choice, randint #make random decisions e.g. for randomised ids
import re as regex #match passwords
from datetime import date, datetime #to get current date and time
from icecream import ic # type: ignore #testing
from string import ascii_letters #holds a list os all letters
import bcrypt as bcp # type: ignore
from icecream import ic
connecter = sql.connect('labify.db')
with connecter:
    cursor = connecter.cursor()


def com(): #To be added to every sql command which updates/deletes/creates values
    connecter.commit()
    
#Creating the neccesary tables
cursor.execute("CREATE TABLE IF NOT EXISTS Users (UserID TEXT PRIMARY KEY, Password BLOB, DateOfSetup TEXT, Admin INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS Equipment (EquipmentName TEXT PRIMARY KEY, CountOfEquipment INTEGER, CountOfInUseEquipment INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS DefaultExperiments(ExperimentName TEXT PRIMARY KEY, Equipment TEXT, MinsTaken INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS LiveExperiments (ExperimentID TEXT PRIMARY KEY, ExperimentName Text, Equipment TEXT, Active INTEGER, UserID Text)")
com()





#doc
def convertlisttostring(li) -> str: #This exists to let us store equipment as a string rather then a list in the sql table
    return f'{li}'[1: -1]

def convertstringtoli(string) -> list: #doc
    if len(string == 0):
        return []
    else:
        return string.split(',')

def convertminstohoursmins(mins): #doc
    hours = 0
    while mins >= 60:
        hours += 1
        mins -= 60
    if hours > 0:
        return f'{hours}H{mins}M'
    else:
        return f'{mins}M'
            
#format timeinout
'''
def total_time(timein, timeout) -> str:

    #format is HH:MM
    left = int(timein[0:2]) + int(timeout[0:2])
    right = int(timein[3:5]) + int(timeout[3:5])
    if right >= 60:
        left += 1
        right -= 60
    if left < 10: #prevents wrong length of string, by adding in an extra 0 if neccesary
        left = f"0{left}"
    if right < 10:
        right = f"0{right}"
    return f"{left}:{right}"
'''

def getPassword(id) -> str:#doc
    if checkExistsInUsers(id) == True:
        values = cursor.execute(f"SELECT Password FROM Users WHERE UserID='{id}'")
        values = values.fetchone()
        return values[0]
    else:
        return 'INVALID'

def passwordvalidate(password):#doc
     if regex.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password) == None:
         return False
     else:
         return True

def hashpassword(password):#doc
    password = password.encode('utf-8')
    salt = bcp.gensalt()
    return bcp.hashpw(password, salt)

def comparepasswordtohash(password, hashedpassword):#doc
    password = password.encode('utf-8')
    print(password, hashedpassword)
    if isinstance(hashedpassword, str) and hashedpassword.startswith("b'") and hashedpassword.endswith("'"):
        hashedpassword = hashedpassword[2:-1].encode('latin1')  
    return bcp.checkpw(password, hashedpassword)    



def idgen() -> str:  #doc
    #generate random 5 digit number
    id = randint(1000000, 9999999)
    while f"{id}" not in getAllUsers() and f"{id}" not in getAllDefaultExperiments and f"{id}" not in getAllEquipment:
        id = randint(1000000, 9999999)
    return str(id)




def createUser(username, password, admin): #doc
    conversiondictforadmin = {
        'yes': 1,
        'no': 0
    }
    if admin in ['yes', 'Yes', 'no', 'No']:
        admin = conversiondictforadmin[admin.lower()]
    else:
        return False
    if not regex.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
        print("Password is not valid")
        return False
    elif admin not in [1,0]:
        print(f'Admin should be 1,0 instead it was: {admin}')
    if checkExistsInUsers(username):
        print("Duplicate Error")
        return False
    password = hashpassword(password)
    cursor.execute (f"INSERT INTO Users VALUES (?, ?, ?, ?)", (username, password, date.today(), admin))
    com()
    print(f"User Created: {username}")
    return username

def searchUserByID(id):#doc
    values = cursor.execute(f"SELECT * FROM Users WHERE UserID = '{id}'")
    values = values.fetchone()
    if values == None:
        print("User does not exist")
        return [0,0,0,0]
    else:
        print(f"User is {values}")
        return values


#doc
def checkExistsInUsers(id) -> bool: 
    values = cursor.execute(f"SELECT UserID FROM Users WHERE UserID='{id}'")
    values = values.fetchall()
    if values == [] or values == None:
        return False
    else:
        return True

#doc  
def getInfoFromUsers(id) -> list: 
    if checkExistsInUsers(id) == False:
        return [0]
    values = cursor.execute(f"SELECT * FROM Users WHERE UserID = '{id}'")
    values = values.fetchone()
    return list(values)

#doc
def getAllUsers() -> list:
    values = cursor.execute(f"SELECT UserID FROM Users")
    values = values.fetchall()
    if values in [[], None]:
        print("No users in database")
        return ['None']
    else:
        return values

#doc
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

#doc
def updateUserName(id, newid) -> bool: #This function never used by gui, but instead by admins via commandline
    if checkExistsInUsers(id) == False:
        print("Error: User not found in DB")
        return False
    else:
        if checkExistsInUsers(newid):
            print('duplicate error')
            return False
        cursor.execute(f"UPDATE Users SET UserID = '{newid}' WHERE UserID = '{id}'")
        com()
        print(f"User {newid} has had id changed from {id} -> {newid}")
        return True


#doc
def deleteUserFromUsers(id) -> bool: #doc
    if checkExistsInUsers(id) == False:
        print("Error: User not found in DB")
        return False
    else:
        cursor.execute(f"DELETE FROM Users WHERE UserID = '{id}'")
        com()
        return True
    
#end of Users functions
#start of SignIO functiosn

'''
def signIn(user):
    #cursor.execute("CREATE TABLE IF NOT EXISTS SignIO (UserID TEXT PRIMARY KEY, Date TEXT, SignInTime TEXT, SignOutTime TEXT, TotalTime TEXT)")
    if checkExistsInUsers(user) == False:
        return False
    currenttime = datetime.now()
    currentdate = datetime.date()
    cursor.execute("INSERT INTO SignIO Values(?,?,?,?,?)", (user, currentdate, currenttime, 0, 0))
    com()

def signOut(user):
    if checkExistsInUsers(user) == False:
        return False
    else:
        if
'''
    

#end of SignIO functions
#start of Equipment functions

def checkEquipmentExists(Name) -> bool:#doc
    values = cursor.execute(f"SELECT EquipmentName FROM Equipment WHERE EquipmentName = '{Name}' ")
    values = values.fetchall()
    if values in [[], None]:
        return False
    else:
        return True

def checkEquipmentUsable(Name) -> bool:#doc
    if checkEquipmentExists(Name) == False:
        print("Equipment was not found")
        return False
    #cursor.execute("CREATE TABLE IF NOT EXISTS Equipment (EquipmentName TEXT PRIMARY KEY, CountOfEquipment INTERGER, CountOfInUseEquipment INTERGER)")
    values = cursor.execute(f"SELECT CountOfEquipment, CountOfInUseEquipment FROM Equipment WHERE EquipmentName = '{Name}'")
    values = values.fetchone()
    if values[0] == values[1]:
        print("All equipment is in use")
        return False
    else:
        return True

def createNewEquipment(Name, Count) -> bool:#doc
    if checkEquipmentExists(Name) == True:
        print("Equipment already exists")
        return False
    else:
        cursor.execute("INSERT INTO Equipment Values (?, ?, ?)", (Name, Count, 0))
        com()
        return True

def getEquipmentValues(Name):#doc
    if checkEquipmentExists(Name) == False:
        return [None,None, 0]
    values = cursor.execute(f"SELECT * FROM Equipment WHERE EquipmentName = '{Name}'")
    values = values.fetchone()
    return values


def incrementEquipment(Name) -> bool:#doc
    if checkEquipmentUsable(Name) == False:
        print("Equipment Not useable")
        return False
    else:
        values = getEquipmentValues(Name)
        count = values[2] + 1
        cursor.execute(f"UPDATE Equipment SET CountOfInUseEquipment = {count} WHERE EquipmentName = '{Name}'")
        com()
        return True

#ic(incrementEquipment('Gloves'))

def decrementEquipment(Name) -> bool:#doc
    values = getEquipmentValues(Name)
    count = values[2] - 1
    if count < 0:
        ic("Count Can NOT go below 0")
        return False
    cursor.execute(f"UPDATE Equipment SET CountOfInUseEquipment = {count} WHERE EquipmentName = '{Name}'")
    com()
    return True

def deleteEquipment(Name) -> bool:#doc
    if checkEquipmentExists(Name) == False:
        ic("CANT BE DELETED, DOES NOT EXIST")
        return False
    cursor.execute(f"DELETE FROM Equipment WHERE EquipmentName = '{Name}'")
    com()
    return True

def getAllEquipment():#doc
    values = cursor.execute("SELECT EquipmentName FROM Equipment")
    values = values.fetchall()
    for i in range(len(values)):
        values[i] = str(values[i][0])
    return values
#equipment functions ends
#defaultExperiments functions start

def checkDefaultExperimentExists(Name) -> bool: #doc
    values = cursor.execute(f"SELECT ExperimentName FROM DefaultExperiments WHERE ExperimentName = '{Name}'")
    values = values.fetchone()
    print(values)
    return values != None


def createDefaultExperiment(Name, Equipment, TimeTaken): #doc
    if checkDefaultExperimentExists(Name) == True:
        print("Already exists")
        return False
    else:
        cursor.execute(f"INSERT INTO DefaultExperiments Values(?, ?, ?)", (Name, Equipment, TimeTaken))
        com()
        return True


def deleteDefaultExperiment(Name): #doc
    if checkDefaultExperimentExists(Name) == False:
        print("Experiment Not Found")
        return False
    cursor.execute(f"DELETE FROM DefaultExperiments WHERE ExperimentName = '{Name}'")
    com()
    print("Default Experiment Deleted")
    return True

def getAllDefaultExperiments() -> list: #doc
    values = cursor.execute(f"SELECT ExperimentName FROM DefaultExperiments")
    values = values.fetchall()
    if values == []:
        return ['None']
    else:
        return values
    
def getDefaultExperimentValues(Name): #doc
    if Name[0] == "'":
        Name = Name[1: -1] #name had 'name ' around it so this fixes it? 
    defaultValues = cursor.execute(f"SELECT * FROM DefaultExperiments WHERE ExperimentName = '{Name}'")
    defaultValues = defaultValues.fetchone()
    return defaultValues
#end of defaultexperiments
#start of liveexperiments

def checkExperimentExistsByName(Name): #doc
    values = cursor.execute(f"SELECT ExperimentName FROM LiveExperiments WHERE ExperimentName = '{Name}'")
    values = values.fetchone()
    if values == []:
        print("Value not found")
        return False
    else:
        print("Value Found")
        return True
    
def getAllLiveExperiments() -> list: #doc
    values = cursor.execute(f"SELECT ExperimentName FROM LiveExperiments WHERE (Active= 1)")
    values = values.fetchall()
    if values == []:
        return ['None']
    else:
        return values

def checkExperimentExistsByID(ID): #doc
    values = cursor.execute(f"SELECT ExperimentID FROM LiveExperiments WHERE ExperimentID = '{ID}'")
    values = values.fetchone()
    if values == []:
        print("Value not found")
        return False
    else:
        print("Value Found")
        return True

def createExperimentID() -> str: #doc
    ID = ''
    for i in range(0, 12):
        ID = f"{ID}{choice(ascii_letters)}"
    if checkExperimentExistsByID(ID) == True:
       return createExperimentID()
    return ID


def createLiveExperimentFromDefault(NameOfDefault, User):
    print('createLiveExperimentFromDefault was ran')
    if checkDefaultExperimentExists(NameOfDefault) == False:
        return False
    defaultValues = cursor.execute(f"SELECT * FROM DefaultExperiments WHERE ExperimentName = '{NameOfDefault}'")
    defaultValues = defaultValues.fetchone()
    Equipment = defaultValues[1].split(',')
    print(Equipment)
    Equipment = str(Equipment)
    for obj in Equipment:
        increment = incrementEquipment(obj)
        if checkEquipmentUsable(obj) == False:
            ic("Equipment Not Usable")
            return False
        if not increment:
            ic("Error incrementing equipment")
            return False
        
    ID = createExperimentID()
    cursor.execute(f"INSERT INTO LiveExperiments Values (?, ?, ?, ?, ?)", (ID, NameOfDefault, Equipment, True, User))
    com()
    return True



def createLiveExperimentFromNew(NameofExperiment, Equipment, User):
    #("CREATE TABLE IF NOT EXISTS LiveExperiments (ExperimentID TEXT PRIMARY KEY, ExperimentName Text, Equipment TEXT, Active INTERGER, UserID TEXT)")
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

    ic(NameofExperiment, Equipment, True, User)
    ID = createExperimentID()
    cursor.execute(f"INSERT INTO LiveExperiments Values (?, ?, ?, ?, ?)", (ID, NameofExperiment, Equipment, True, User))
    com()
    return True

def endExperimentByID(ID):
    if checkExperimentExistsByID(ID) == False:
        print("Experiment Not Found")
        return False
    values = cursor.execute(f"SELECT Equipment FROM LiveExperiments WHERE ExperimentID = '{ID}'")
    values = values.fetchone()
    if values != None:
        for obj in values:
            decrement = decrementEquipment(obj)
            if decrement == False:
                print("Error Decrementing Equipment")
                return False
    cursor.execute(f"UPDATE LiveExperiments SET Active = 0 WHERE ExperimentID = '{ID}'")
    com()
    return True

def getIDOfLiveFromName(Name):
    values = cursor.execute(f"SELECT ExperimentID FROM LiveExperiments WHERE ExperimentName = '{Name}'")
    values = values.fetchone()
    if values == None:
        print("Experiment Not Found")
        return 0
    return values[0]

def getLiveExperimentValuesByID(ID):
    if checkExperimentExistsByID(ID) == False:
        ic("Experiment Not Found")
        return [None, None, None, None, None]
    return cursor.execute(f"SELECT * FROM LiveExperiments WHERE ExperimentID = '{ID}'").fetchone()
    
def getLiveExperimentValuesByName(Name):
    ID = getIDOfLiveFromName(Name)
    if ID == 0:
        ic("Experiment Not Found")
        return [None, None, None, None, None]
    return getLiveExperimentValuesByID(ID)



'''
#Creating the neccesary tables
cursor.execute("CREATE TABLE IF NOT EXISTS Users (UserID TEXT PRIMARY KEY, Password TEXT, DateOfSetup TEXT, Admin INTERGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS Equipment (EquipmentName TEXT PRIMARY KEY, CountOfEquipment INTERGER, CountOfInUseEquipment INTERGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS DefaultExperiments(ExperimentName TEXT PRIMARY KEY, Equipment TEXT, MinsTaken INTERGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS LiveExperiments (ExperimentID TEXT PRIMARY KEY, ExperimentName Text, Equipment TEXT, Active INTERGER, UserID TEXT)")
com()
'''

''''Troubleshooting functions'''

def viewEverythingInEachTable():#doc
    ic(cursor.execute("SELECT * FROM Users").fetchall())
    ic(cursor.execute("SELECT * FROM Equipment").fetchall())
    ic(cursor.execute("SELECT * FROM DefaultExperiments").fetchall())
    ic(cursor.execute("SELECT * FROM LiveExperiments").fetchall())

#doc
def resetAllTables():  #DO NOT USE UNLESS RESETTING EVERYTHING
    cursor.execute('DROP TABLE Users')
    cursor.execute('DROP TABLE Equipment')
    cursor.execute('DROP TABLE DefaultExperiments')
    cursor.execute('DROP TABLE LiveExperiments')
    com()
    ic('All tables deleted')

''' Spade: 4, Cart: 2, Sponge: 5'''
'''Deleted 50C, 50D,  54C, 56B, 56C, all 57, 59A'''
