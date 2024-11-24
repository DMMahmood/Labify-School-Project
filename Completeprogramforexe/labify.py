import PySimpleGUI as sg # type: ignore #the gui library
from icecream import ic # type: ignore #testing
import sqlite3 as sql #use sql
from os import path #save files to paths
from random import choice, randint #make random decisions e.g. for randomised ids
import re as regex #match passwords
from datetime import date, datetime #to get current date and time
from string import ascii_letters #holds a list os all letters
import bcrypt as bcp # type: ignore
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
     if regex.match(r'[0-9]{7}[UEC]', password) == None:
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


font = ('Arial', '16')
sg.set_options(font=font)
sg.theme('DarkGrey') 


signedInUser = '' # change this to blank string '' before deploying
adminStatus = True #change this to None before deploying
exec(open("serverside.py").read())
def chooseSignInWhenReOpening(ID = ''):
    global signedInUser
    if checkExistsInUsers(ID) == False:
        signedInUser = ''
        signInWindow()
    if checkUserAdmin(ID):
        adminStatus = True
        mainAdminWindow(ID)
    else:
        adminStatus = False
        mainUserWindow(ID)




def signInWindow(): #documented
    global adminStatus, signedInUser
    layout = [
        [sg.T('Welcome User')],
        [sg.T('ID'), sg.Input(key='_ID')],
        [sg.T('Password'), sg.Input(key='_Password', password_char='*')],
        [sg.B('Sign in', key='_SignIn'), sg.Cancel()]
    ]
    window = sg.Window('Labify', layout, icon='mainlogo.png', titlebar_icon='mainlogo.png')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            sg.Popup('Goodbye', auto_close_duration=5)
            exit()
        elif event == '_SignIn':
            ID = values['_ID']
            inppassword = values['_Password']
            userExists = checkExistsInUsers(ID)
            if userExists == False:
                sg.Popup('User does not exist')
                window.Close()
                signInWindow()
            realpassword = getPassword(ID)
            if comparepasswordtohash(inppassword, realpassword):
                adminStatus = checkUserAdmin(ID)
                signedInUser = ID
                if adminStatus == True:
                    window.Close()
                    mainAdminWindow(ID)
                else:
                    window.Close()
                    mainUserWindow(ID)
            else:
                sg.Popup(f'Incorrect password')
                window.Close()
                signInWindow()


def signUpWindow(): #documented
    layout = [
        [sg.T('Name'), sg.Input('', key='_Name')],
        [sg.T('Password'), sg.Input('', password_char='*', key='_Password')],
        [sg.T('Admin'), sg.DropDown(['No', 'Yes'], default_value=['No'], readonly=True)],
        [sg.B('Sign Up'), sg.Cancel()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            sg.Popup('goodbye')
            exit()
        else:
            username, password, admin = values['_Name'], values['_Password'], values['_Admin']
            if passwordvalidate(password) == False:
                sg.Popup('Password Invalid')
            elif checkExistsInUsers(username):
                sg.Popup('User already exists')

            else:
                if admin == 'Yes':
                    admin = True
                    createUser(username, password, admin)
                else:
                    admin = False
                    createUser(username, password, admin)
                global signedInUser
                signedInUser = username
                window.Close()
                chooseSignInWhenReOpening()

            window.Close()
            signUpWindow()


def mainAdminWindow(ID): #documented
    layout = [
        [sg.T(f'Welcome ADMIN {ID}, todays date is {date.today()}')],
        [sg.B('Manage Users'), sg.B('Manage Live'), sg.B('Manage Default'), sg.B('Manage Equipment')],
        [sg.B('Sign Out'), [sg.B('User View')], sg.Exit()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event == 'Sign Out':
            window.Close()
            signInWindow()
        elif event == 'Manage Users':
            window.Close()
            manageUsersWindow()
        elif event == 'Manage Live':
            window.Close()
            liveExperimentsManagementWindow()
        elif event == 'Manage Default':
            window.Close()
            defaultExperimentsManagementWindow()
        elif event == 'Manage Equipment':
            window.Close()
            equipmentManagementWindow()
        elif event == 'User View':
            window.Close()
            mainUserWindow(signedInUser)



def mainUserWindow(ID = ''): #documented
    layout = [ 
        [sg.T(f'Welcome USER {signedInUser}, {date.today()}')],
        [sg.B('Experiments')],
        [sg.B('My Info'), sg.B('Sign Out')] #mismatched event names
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Sign Out': # if user closes window or signs out
            exit() #event mismatched
        elif event == 'Experiments':
            window.Close()
            liveExperimentsManagementWindow()
        elif event == 'My Info':
            window.Close()
            personalInfo = getInfoFromUsers(ID)
            sg.Popup(f'Name: {personalInfo[0]}, Joined {personalInfo[2]}')
            mainUserWindow()


def liveExperimentsManagementWindow(): #documented
    layout = [
        [sg.B('Start Default'), sg.B('Start New')],
        [sg.B('View Live'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event == 'Start Default':
            startExperimentFromDefaultWindow()
        elif event == 'Start New':
            startExperimentFromNewWindow()
        elif event == 'View Live':
            viewLiveExperimentsWindow()
        elif event == 'Cancel':
            chooseSignInWhenReOpening(signedInUser)
            

'''DefaultExperiments(ExperimentName TEXT PRIMARY KEY, Equipment TEXT, MinsTaken INTERGER)")
LiveExperiments (ExperimentID TEXT PRIMARY KEY, ExperimentName Text, Equipment TEXT, Active BOOLEAN, UserID TEXT))")'''

def genEquipmentCheckBoxes(): #documented
    equipment = getAllEquipment()
    checkboxs = []
    for i in range(len(equipment)):
        checkboxs.append(sg.Checkbox(text= equipment[i], key=f'_{equipment[i]}'))
    return checkboxs


def startExperimentFromDefaultWindow(): #doc
    defaultExperiments = getAllDefaultExperiments()
    for i in range(len(defaultExperiments)):
        defaultExperiments[i] = str(defaultExperiments[i])[2:-3]
    column = [
    [sg.B(str(defaultExperiments[i]))] for i in range(len(defaultExperiments))]
    layout = [
        [sg.Column(column, scrollable=True,  vertical_scroll_only= True)], #Creates a vertical scroll of all experiments
        [sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event == 'Cancel':
            window.Close()
            liveExperimentsManagementWindow()
        elif event not in ['Exit', 'Cancel']:
            values = getDefaultExperimentValues(event)
            sg.Popup(f'The Equipment that will be used is \n {values[1]}')
            if createLiveExperimentFromDefault(values[0], signedInUser):
                sg.Popup('Experiment succesfully created')
            else:
                sg.Popup('Error, Experiment could not be started')
            window.Close()
            liveExperimentsManagementWindow()

def startExperimentFromNewWindow(): #doc
    #default experiments: need the name, equipment needed, time taken
    #need to get all equipment in a list as checkboxes
    equipmentcheckboxes = genEquipmentCheckBoxes()
    layout = [
        [sg.T('Create new default experiment')],
        [sg.T('Name: '), sg.Input(default_text='', key='_Name')],
        [equipmentcheckboxes],
        [sg.B('Create'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event == 'Create':
            name = str(values['_Name'])
            equipment = []
            for key in values:
                if key not in ['_Name', 'Cancel'] and values[key] == True:
                    equipment.append(key[1:])
            equipment = str(f"{convertlisttostring(equipment)}")
            ic(equipment)
            if name == '':
                sg.Popup('Name can not be blank')
            elif createLiveExperimentFromNew(name, equipment, signedInUser):
                sg.Popup('Experiment created succesfully')
            else:
                sg.Popup('There was an error in execution')
            window.close()
            chooseSignInWhenReOpening(signedInUser)
        elif event == 'Cancel':
            window.Close()
            liveExperimentsManagementWindow()
 
def singleLiveExperimentWindow(vals):#doc
    equipment = vals[2]
    equipment = equipment.split(',')
    if len(equipment) > 1: #formatting the list of elements
        equipment[0] = equipment[0][3: -3]
        for i in range(1, len(equipment)):
            equipment[i] = equipment[i][4: len(equipment[i]) - 3]
    elif len(equipment) == 1:
        equipment = equipment[3: -3]
    
    layout = [
        [sg.T(f'Name {vals[1]}'), sg.T(f'Started by {vals[4]}')],
        [sg.T(f'Equipment {", ".join(equipment)}')],
        [sg.B('Finish'), sg.B('Cancel')]
    ]
        
    ic(equipment)
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event == 'Finish':
            endExperimentByID(vals[0])
            sg.Popup('Experiment has been ended')
            window.Close()
            liveExperimentsManagementWindow()
        elif event == 'Cancel':
            window.Close()
            liveExperimentsManagementWindow()


def viewLiveExperimentsWindow(): #doc
    liveExperiments = getAllLiveExperiments()
    columnLayout = [sg.B(f'{str(liveExperiments[i])[2: -3]}') for i in range(len(liveExperiments))]
    for i in range(len(columnLayout)): columnLayout[i] = [columnLayout[i]]
    layout = [
        [sg.Column(columnLayout)], #Creates a vertical scroll of all experiments
        [sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event not in ['Exit', 'Cancel']:
            print(event)
            values = getLiveExperimentValuesByName(event)
            window.Close()
            singleLiveExperimentWindow(values)
        elif event == 'Cancel':
            window.Close()
            liveExperimentsManagementWindow()

            
            

'''Default experiment windows and subwindows'''

def defaultExperimentsManagementWindow(): #documented
    layout = [
        [sg.T('Defaults')], 
        [sg.B('Create'), sg.B('Delete'), sg.B('Edit')],
        [sg.B('View'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            break
        elif event == 'Create':
            window.close()
            createDefaultWindow()
        elif event == 'Delete':
            window.close()
            deleteDefaultWindow()
        elif event == 'Edit':
            window.close()
            editDefaultWindow()
        elif event == 'View':
            window.Close()
            viewDefaultExperimentsWindow()
        elif event == 'Cancel':
            window.Close()
            chooseSignInWhenReOpening(signedInUser)


def createDefaultWindow(): #documented
    #default experiments: need the name, equipment needed, time taken
    #need to get all equipment in a list as checkboxes
    equipmentcheckboxes = genEquipmentCheckBoxes()
    layout = [
        [sg.T('Create new default experiment')],
        [sg.T('Name: '), sg.Input(key='_Name')],
        [equipmentcheckboxes],
        [sg.T('Time Taken (mins)'), sg.I(key='_TimeTaken')],
        [sg.B('Create'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event == 'Create':
            name = str(values['_Name'])
            try:
                timetaken = int(values['_TimeTaken'])
            except ValueError:
                sg.Popup('Time not valid')
                window.Close()
                createDefaultWindow()
            if checkDefaultExperimentExists(name):
                sg.Popup(f'{name} Already exists')
                window.Close()
                createDefaultWindow()
            else:
                equipment = []
                for key in values.keys():
                    if key not in ['_Name', '_TimeTaken', 'Cancel'] and values[key] == True:
                        equipment.append(key[1:])
                equipment = convertlisttostring(equipment)
                createDefaultExperiment(name, equipment, timetaken)
                sg.Popup('Experiment created succesfully')
                window.close()
                defaultExperimentsManagementWindow()
        elif event == 'Cancel':
            window.Close()
            defaultExperimentsManagementWindow()


def viewDefaultExperimentsWindow(): #documented
    defaultexperiments = getAllDefaultExperiments()
    for i in range(len(defaultexperiments)):
        defaultexperiments[i] = [sg.B(str(f'{defaultexperiments[i]}')[1: -2])]
    
    layout = [
        [sg.T('Experiments:')],
        [defaultexperiments],
        [sg.B('Close')]
        ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event not in ['Close', 'Exit', sg.WIN_CLOSED]:
            experiment = list(getDefaultExperimentValues(event))
            timetaken = convertminstohoursmins(int(experiment[2]))
            sg.Popup(f'Experiment: {experiment[0]} \nEquipment: {experiment[1]} \nTime taken: {timetaken}')
        elif event == 'Close':
            window.Close()
            defaultExperimentsManagementWindow()
 

def deleteDefaultWindow(): #documented
    layout = [
        [sg.T('Experiment Name')],
        [sg.I(key='_Experiment')],
        [sg.B('Delete'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            window.Close()
            chooseSignInWhenReOpening(signedInUser)
        elif event == 'Delete':
            experiment = values['_Experiment']
            if checkDefaultExperimentExists(experiment) == False:
                sg.Popup(f'Experiment: {experiment} does not exist')
                window.Close()
                deleteDefaultWindow()
            else:
                deleteDefaultExperiment(experiment)
                sg.Popup('Succesfully deleted experiment')
                window.Close()
                defaultExperimentsManagementWindow()
        elif event == 'Cancel':
            window.Close()
            defaultExperimentsManagementWindow()

def editDefaultWindow(): #documented
    equipmentcheckboxes = genEquipmentCheckBoxes()
    layout = [
        [sg.T('Experiment Name'), sg.I('', key='_Experiment')],
        [sg.T('Time Taken'), sg.I('', key='_TimeTaken')],
        [sg.T('Equipment Used')],
        [equipmentcheckboxes],
        [sg.B('Update'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event == 'Update':
            experiment, timetaken = values['_Experiment'], values['_TimeTaken']
            if checkDefaultExperimentExists(experiment) == False:
                sg.Popup(f'Experiment: {experiment} does not exist')
                window.Close()
                deleteDefaultWindow()
            else:
                equipment = []
                for key in values.keys():
                    if key not in ['_Name', '_TimeTaken', 'Cancel', 'Update', '_Experiment'] and values[key] == True:
                        equipment.append(key[1:])
                equipment = convertlisttostring(equipment)
                deleteDefaultExperiment(experiment)
                createDefaultExperiment(experiment, equipment, timetaken)
                window.Close()
                defaultExperimentsManagementWindow()
        elif event == 'Cancel':
            window.Close()
            defaultExperimentsManagementWindow()


'''Default experiment window ends'''


def equipmentManagementWindow():#doc
    layout = [
    [sg.B('View'), sg.B('Create')],
    [ sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event == 'View':
            viewEquipmentWindow()
        elif event == 'Create':
            createEquipmentWindow()
        elif event == 'Cancel':
            window.Close()
            equipmentManagementWindow()

def viewEquipmentWindow():#doc
    #[sg.B(str(defaultExperiments[i])[2: -3])] for i in range(len(defaultExperiments))]
    equipment = getAllEquipment()

    if len(equipment) == 0: #error message implementation for empty equipment list
        sg.Popup('There is no equipment')
        window.Close()
        equipmentManagementWindow()

    equipmentButtons = [
        [sg.B(str(equipment[i]))] for i in range(len(equipment))
    ]

    layout = [
        equipmentButtons, 
        [sg.B('Cancel')]
        ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event in equipment:
            singleEquipmentWindow(event)
        elif event == 'Cancel':
            window.Close()
            equipmentManagementWindow()

def singleEquipmentWindow(Name):#doc
    equipment = getEquipmentValues(Name) #Name, Count of total, Count of in use
    layout = [
        [sg.T(f'{equipment[0]} Total: {equipment[1]} In Use: {equipment[2]}')],
        [sg.B('Increment'), sg.B('Decrement'), sg.B('Delete'), sg.B('Cancel')]
            ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event == 'Increment':
            if equipment[2] == equipment[1]:
                sg.Popup('Limit reached')
                window.Close()
                viewEquipmentWindow()
            elif incrementEquipment(equipment[0]) == True:
                sg.Popup(f'Equipment {equipment[0]} incremented')
                window.Close()
                viewEquipmentWindow()
            else:
                sg.Popup(f'Equipment could not be incremented')
                window.Close()
                viewEquipmentWindow()
        elif event == 'Decrement':
            if equipment[2] == 0:
                sg.Popup('Limit reached')
            elif decrementEquipment(equipment[0]) == True:
                sg.Popup(f'Equipment {equipment[0]} decremented')
            else:
                sg.Popup(f'Equipment could not be decremented')
            window.Close()
            viewEquipmentWindow()
        elif event == 'Delete':
            if deleteEquipment(equipment[0]):
                sg.Popup(f'Equipment {equipment[0]} deleted')
            else:
                sg.Popup(f'Equipment {equipment[0]} could not be deleted')
            window.Close()
            viewEquipmentWindow()
        elif event == 'Cancel':
            window.Close()
            viewEquipmentWindow()
    

def createEquipmentWindow(): #doc
    layout = [
        [sg.T('Name'), sg.I(default_text='', key='_Name')],
        [sg.T('Count'), sg.I(default_text='', key='_Count')],
        [sg.B('Submit'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event == 'Submit':
            name, count = values['_Name'], values['_Count']
            try:
                count = int(count)
            except TypeError:
                sg.Popup('Count is invalid')
                window.Close()
                equipmentManagementWindow()
            if count < 0:
                sg.Popup(f'Equipemnt count {count} is invalid')
            elif createNewEquipment(name, count):
                sg.Popup(f'Equipment {name} created, total: {count}')
            else:
                sg.Popup(f'Error {name} could not be created')
            window.Close()
            equipmentManagementWindow()
        elif event == 'Cancel':
            window.Close()
            equipmentManagementWindow()


def manageUsersWindow(): #doc
    layout = [
        [sg.T('Users'), sg.B('Delete'), sg.B('Create')],
        [sg.B('Update'), sg.B('View'), sg.Cancel()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event == 'Delete':
            window.Close()
            deleteUserWindow()
        elif event == 'Create':
            window.Close()
            createUserWindow()
        elif event == 'Update':
            window.Close()
            updateUserWindow()
        elif event == 'View':
            window.Close()
            viewUsersWindow()
        elif event == 'Cancel':
            window.Close()
            chooseSignInWhenReOpening(signedInUser)

def viewUsersWindow(): #doc
    users = getAllUsers()
    ic(users)
    for i in range(len(users)):
        users[i] = str(users[i])[2: -3]
    
    ic(users)

    layout = [
        [sg.T('Users:')],
        [sg.T(f'{", ".join(users)}')],
        [sg.B('Close')]
        ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event == 'Close':
            window.Close()
            manageUsersWindow()

        

def deleteUserWindow():#doc
    layout = [
        [sg.T('Name'), sg.Input('', key='_Name')],
        [sg.B('Submit'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event == 'Submit':
            name = values['_Name']
            if name == signedInUser:
                sg.Popup('Warning: You can not try and delete yourself', title='Labify', auto_close_duration=5, auto_close=True)
                window.Close()
                exit()
            if checkExistsInUsers(name) == False:
                sg.Popup(f'User {name} Does not exist')
                window.Close()
                manageUsersWindow()
            else:
                deleteUserFromUsers(name)
                sg.Popup(f'User {name} deleted')
            window.Close()
            manageUsersWindow()
        elif event ==  'Cancel':
            window.Close()
            manageUsersWindow()

def updateUserWindow():#doc
    layout = [
        [sg.T('Name'), sg.Input('', key='_Name')],
        [sg.B('Submit'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event == 'Submit':
            name = values['_Name']
            if checkExistsInUsers(name) == False:
                sg.Popup(f'User {name} Does Not Exist')
                window.Close()
                manageUsersWindow()
            else:
                window.Close()
                nameUpdateUserWindow(name)
        elif event == 'Cancel':
            window.Close()
            manageUsersWindow()

def nameUpdateUserWindow(name):#doc
    #format for values: userid, password, dateofcreation, admin status
    values = searchUserByID(name)
    if values[3] == 1:
        defaultvalueforadmin = 'Yes'
    else:
        defaultvalueforadmin = 'No'
    layout = [
        [sg.T(f'Currently editing: {name}, leave boxes blank for no change')],
        [sg.T(f'Password'), sg.Input(default_text='New Password', key = '_NewPassword')],
        [sg.T(f'Current admin status is {bool(values[3])}'), sg.DD(['Yes', 'No'], default_value=defaultvalueforadmin, key='_Admin')],
        [sg.B('Submit'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            exit()
        elif event == 'Submit':
            if values['_NewPassword'] not in ['', None, 'New Password']:
                values[1] = values['_NewPassword']
                if len(values[1]) < 8:
                    sg.Popup('INVALID PASSWORD')
                    window.Close()
                    manageUsersWindow()

            deleteUserFromUsers(name)
            createUser(name, values[1], values['_Admin'])
            window.Close()
            manageUsersWindow()
        elif event == 'Cancel':
            window.Close()
            manageUsersWindow()   


def createUserWindow():#doc
    layout = [
        [sg.T('Name'), sg.Input(key='_Name')],
        [sg.T('Password'), sg.Input(password_char='*', key= '_Password')],
        [sg.T('Admin'), sg.DD(['Yes', 'No'], default_value='No', key='_Admin')],
        [sg.B('Submit'), sg.Cancel()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            exit()
        elif event == 'Cancel':
            window.close()
            manageUsersWindow()
        elif event == 'Submit':
            print(values)
            Name = values['_Name']
            Password = values['_Password']
            Admin = values['_Admin']
            ID = createUser(Name, Password, Admin)
            if ID == False:
                sg.Popup('Error please try again')
            else:
                if Admin == 1:
                    sg.Popup(f"Your unique id is {ID}, you are an admin")
                else:
                    sg.Popup(f"Your unique id is {ID}")
            window.Close()
            manageUsersWindow()


#this starts both programs, no need to run 'serverside.py'


#deleted: 53B, 53C
def start():#doc
    if getAllUsers() == []:
        createUserWindow()
    else:
        chooseSignInWhenReOpening(signedInUser)

start()