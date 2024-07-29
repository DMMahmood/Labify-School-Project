import PySimpleGUI as sg
from serverside import *
from random import randint
from datetime import date
from icecream import ic
sg.theme('DarkGrey')

'''
Windows i need:
sign in 
signout
signup
main admin window
main non admin window
-admin- 
manage users
manage experiments
create user
delete user
-main user-
create experiment
delete experiment
create experiment template
delete experiment template
'''
'''
testing admin data:
username: liqp214
password: TestPassword1
'''
signedInUser = 'Daniyal'
exec(open("serverside.py").read())
def chooseSignInWhenReOpening(ID = ''):
    global signedInUser
    if checkExistsInUsers(ID) == False:
        signedInUser = ''
        signInWindow()
    if checkUserAdmin(ID):
        mainAdminWindow(ID)
    else:
        mainUserWindow(ID)
def signInWindow():
    global adminStatus, signedInUser
    layout = [
        [sg.T('Welcome User')],
        [sg.T('ID'), sg.Input(key='_ID')],
        [sg.T('Password'), sg.Input(key='_Password', password_char='*')],
        [sg.B('Sign in', key='_SignIn'), sg.Cancel()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            sg.Popup('Goodbye', auto_close_duration=5)
            exit()
        elif event == '_SignIn':
            ID = values['_ID']
            inppassword = hashpassword(values['_Password'])
            userExists = checkExistsInUsers(ID)
            if userExists == False:
                sg.Popup('User does not exist')
                signInWindow()
            realpassword = getPassword(ID)
            if realpassword == inppassword:
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
                exit()


def signUpWindow():
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
            break
        else:
            password, admin = values['_Password'], values['_Admin']
            if admin == 'Yes':
                admin = True
            else:
                admin = False
            createUser(password, admin)


def mainAdminWindow(ID):
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
            experimentsManagementWindow()
        elif event == 'Manage Default':
            window.Close()
            manageExperimentsWindow()
        elif event == 'Manage Equipment':
            window.Close()
            equipmentManagementWindow()



def mainUserWindow(ID = ''):
    layout = [ 
        [sg.T(f'Welcome USER {signedInUser}, {date.today()}')],
        [sg.T('Experiments'), sg.B('Create'), sg.B('Delete')],
        [sg.B('My Info'), sg.B('Sign Out')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break


def experimentsManagementWindow():
    layout = [
        [sg.B('Start Default'), sg.B('Start New')],
        [sg.B('View Live'), sg.B('Exit')]
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
            

'''DefaultExperiments(ExperimentName TEXT PRIMARY KEY, Equipment TEXT, MinsTaken INTERGER)")
LiveExperiments (ExperimentID TEXT PRIMARY KEY, ExperimentName Text, Equipment TEXT, Active BOOLEAN, UserID TEXT))")'''

def genEquipmentCheckBoxes():
    equipment = getAllEquipment()
    checkboxs = []
    for i in range(len(equipment)):
        checkboxs.append(sg.Checkbox(text= equipment[i], key=f'_{equipment[i]}'))
    return checkboxs


def startExperimentFromDefaultWindow():
    defaultExperiments = getAllDefaultExperiments()
    column = [
    [sg.B(defaultExperiments[i])] for i in range(len(defaultExperiments))]
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
            experimentsManagementWindow()
        elif event in defaultExperiments:
            ic('Meow')
            #Need to validate for the experiment e.g. checks experiment is possible
            values = getDefaultExperimentValues(event)
            sg.Popup(f'The Equipment that will be used is \n {values[1]}')
            if createLiveExperimentFromDefault(values[0], signedInUser):
                sg.Popup('Experiment succesfully created')
            else:
                sg.Popup('Error, Experiment could not be started')
        window.Close()
        experimentsManagementWindow()

    
def startExperimentFromNewWindow():
    #default experiments: need the name, equipment needed, time taken
    #need to get all equipment in a list as checkboxes
    equipmentcheckboxes = genEquipmentCheckBoxes()
    layout = [
        [sg.T('Create new default experiment')],
        [sg.T('Name: '), sg.Input(default_text='', key='_Name')],
        [equipmentcheckboxes],
        [sg.B('Create'), sg.Exit()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event == 'Create':
            name = str(values['_Name'])
            equipment = []
            for key in values.keys():
                if key not in ['_Name', 'Cancel'] and values[key] == True:
                    equipment.append(key[1:])
            equipment = convertlisttostring(equipment)
            createLiveExperimentFromNew(name, equipment, signedInUser)
            sg.Popup('Experiment created succesfully')
            window.close()
            chooseSignInWhenReOpening(signedInUser)
        elif event == 'Cancel':
            window.Close()
            experimentsManagementWindow()

def singleLiveExperimentWindow(values):
    #ExperimentID TEXT PRIMARY KEY, ExperimentName Text, Equipment TEXT, Active INTERGER, UserID TEXT)
    layout = [
        [sg.T(f'Name {values[1]}'), sg.T(f'Started by {values[4]}')],
        [sg.T(f'Equipment {values[2]}')],
        [sg.B('Finish'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event == 'Finish':
            endExperimentByID(values[0])
            sg.Popup('Experiment has been ended')
            window.Close()
            manageExperimentsWindow()
        elif event == 'Cancel':
            window.Close()
            manageExperimentsWindow()


def viewLiveExperimentsWindow():
    liveExperiments = getAllLiveExperiments()
    ic(liveExperiments)
    columnLayout = [sg.B(liveExperiments[i]) for i in range(len(liveExperiments))]
    for i in range(len(columnLayout)): columnLayout[i] = [columnLayout[i]]
    ic(columnLayout)
    

    layout = [
        [sg.Column(columnLayout)], #Creates a vertical scroll of all experiments
        [sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            exit()
        elif event in liveExperiments:
            values = getLiveExperimentValuesByName(event)
            window.Close()
            singleLiveExperimentWindow(values)
        elif event == 'Cancel':
            window.Close()
            manageExperimentsWindow()

            
            

'''Default experiment windows and subwindows'''

def defaultExperimentWindow():
    layout = [
        [sg.T('Defaults')], 
        [sg.B('Create'), sg.B('Delete'), sg.B('Edit')]
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
        elif event == 'Cancel':
            window.Close()
            chooseSignInWhenReOpening()


def createDefaultWindow():
    #default experiments: need the name, equipment needed, time taken
    #need to get all equipment in a list as checkboxes
    equipmentcheckboxes = genEquipmentCheckBoxes()
    layout = [
        [sg.T('Create new default experiment')],
        [sg.T('Name: '), sg.Input(key='_Name')],
        [equipmentcheckboxes],
        [sg.T('Time Taken (mins)'), sg.I(key='_TimeTaken')],
        [sg.B('Create'), sg.Exit()]
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
                defaultExperimentWindow()
        elif event == 'Cancel':
            window.Close()
            defaultExperimentWindow()


def viewDefaultExperimentsWindow():
    defaultexperiments = getAllDefaultExperiments()
    for i in range(len(defaultexperiments)):
        defaultexperiments[i] = [sg.T(str(f'{defaultexperiments[i]}')[1: -2])]
    
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
        elif event == 'Close':
            window.Close()
            defaultExperimentWindow()
     

def deleteDefaultWindow():
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
                defaultExperimentWindow()
        elif event == 'Cancel':
            window.Close()
            defaultExperimentWindow()

def editDefaultWindow():
    equipmentcheckboxes = genEquipmentCheckBoxes()
    layout = [
        [sg.T('Experiment Name'), sg.I('', key='_Experiment')],
        [sg.T('Time Taken'), sg.I('', key='_TimeTaken')],
        [sg.T('EquipmentUsed')],
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
                convertlisttostring(equipmentcheckboxes)
                deleteDefaultExperiment(experiment)
                createDefaultExperiment(experiment, equipmentcheckboxes, timetaken)
        elif event == 'Cancel':
            window.Close()
            defaultExperimentWindow()


'''Default experiment window ends'''


def equipmentManagementWindow():
    pass #to be made


def manageUsersWindow(): #to be continued
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
            chooseSignInWhenReOpening()

def viewUsersWindow():
    users = getAllUsers()
    for i in range(len(users)):
        users[i] = str(users[i][0])
    
    layout = [
        [sg.T('Users:')],
        [sg.T(f'{users}')],
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

        

def deleteUserWindow():
    layout = [
        [sg.T('Name'), sg.Input('', key='_Name')],
        [sg.B('Submit'), sg.B('Cancel')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
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

            #this works
            window.Close()
            manageUsersWindow()

def updateUserWindow():
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

def nameUpdateUserWindow(name):
    #format for values: userid, password, dateofcreation, admin status
    values = searchUserByID(name)
    if values[3] == 1:
        defaultvalueforadmin = 'Yes'
    else:
        defaultvalueforadmin = 'No'
    layout = [
        [sg.T(f'currently editing: {name}, leave boxes blank for no change')],
        [sg.T(f'Current password is {values[1]}'), sg.Input(default_text='New Password', key = '_NewPassword')],
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
            deleteUserFromUsers(name)
            createUser(name, values[1], values['_Admin'])
        elif event == 'Cancel':
            window.Close()
            manageUsersWindow()   

        

def manageExperimentsWindow(): 
    layout = [
        [sg.T('Defaults'), sg.B('Create'), sg.B('Delete')],
        [sg.T('Live'), sg.B('Edit'), sg.B('Delete'), sg.B('Create')]
    ]

def createUserWindow():
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
            break
        elif event == 'Cancel':
            window.close()
            break
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

editDefaultWindow()