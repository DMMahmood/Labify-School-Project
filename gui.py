import PySimpleGUI as sg
from main import *
from serverside import *
from random import randint
import matplotlib as mpl
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
exec(open("serverside.py").read())

def signInWindow():
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
            break
        elif event == '_SignIn':
            ID = values['_ID']
            password = values['_Password']
            userExists = checkExistsInUsers(ID)
            if userExists == False:
                sg.popup('User does not exist')
                signInWindow()
            realpassword = getPassword(ID)
            if realpassword == password:
                adminStatus = AdminCheck(ID, password)
                if adminStatus == True:
                    window.Close()
                    mainAdminWindow(ID)
                else:
                    window.Close()
                    mainUserWindow(ID)
            else:
                sg.popup(f'Incorrect password')

def mainAdminWindow(ID):
    layout = [
        [sg.T(f'Welcome ADMIN {ID}, todays date is {today()})')],
        [sg.B('Manage Users'), sg.B('Manage Experiments'), sg.B('Manage Equipment')],
        [sg.B('Sign Out'), [sg.B('User View')], sg.Exit()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
            break
        elif event == 'Sign Out':
            window.Close()
            signInWindow()
        elif event == 'Manage Users':
            window.Close()
            mainUserWindow(ID)
        elif event == 'Manage Experiments':
            defaultExperimentWindow()
        elif event == 'Manage Equipment':
            equipmentManagementWindow()

def defaultExperimentWindow()
    layout = [
        [sg.T('Default Experiments')]
        [sg.B('Create'), sg.B('Delete'), sg.B('Edit')]
    ]
    window = sg.Window('Labify', layout)



def equipmentManagementWindow():
    pass




def mainUserWindow(User):
    layout = [ 
        [sg.T(f'Welcome USER {User}, {today()}')],
        [sg.T('Experiments'), sg.B('Create'), sg.B('Delete')],
        [sg.B('My Info'), sg.B('Sign Out')]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break


def manageUsersWindow(User):
    layout = [
        [sg.T('Users'), sg.B('Delete'), sg.B('Create')],
        [sg.T('Update'), sg.B('Export'), sg.Cancel()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break


def manageExperimentsWindow(User):
    layout = [
        [sg.T('Defaults'), sg.B('Create'), sg.B('Delete')],
        [sg.T('Live'), sg.B('Edit'), sg.B('Delete'), sg.B('Create')]
    ]

def createUserWindow():
    layout = [
        [sg.T('Name'), sg.Input(key='_Name')],
        [sg.T('Password'), sg.Input(key='_Password', password_char='*')],
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
            Name = values['_Name']
            Password = values['_Password']
            Admin = convertTo01(values['_Admin'])
            ID = createUser(Password, Admin)
            if ID == False:
                sg.Popup('Error please try again')
            else:
                if Admin == 1:
                    sg.Popup(f"Your unique id is {ID}, you are an admin")
                else:
                    sg.Popup(f"Your unique id is {ID}")
        
createUserWindow()

