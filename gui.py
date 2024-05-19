import PySimpleGUI as sg
from main import *
from random import randint
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

def signInWindow():
    layout = [
        [sg.T('Welcome User')],
        [sg.T('ID'), sg.Input(key='_ID')],
        [sg.T('Password'), sg.Input(key='_Password')],
        [sg.B('Sign in', key='_SignIn'), sg.Cancel()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
#signInWindow()
def signUpWindow():
    layout = [
        [sg.T('Name'), sg.Input('')],
        [sg.T('Password'), sg.Input('', password_char='*')],
        [sg.B('Sign Up'), sg.Cancel()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
#SignUpWindow()
def mainAdminWindow(User):
    layout = [
        [sg.T(f'Welcome ADMIN {User}, todays date is {today()})')],
        [sg.B('Manage Users'), sg.B('Manage Experiments'), sg.B('Manage Equipment')],
        [sg.B('Sign Out'), [sg.B('User View')], sg.Cancel()]
    ]
    window = sg.Window('Labify', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

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
        [sg.T('Name'), sg.Input()],
        [sg.T('Password'), sg.Input(password_char='*')],
        [sg.B('Admin')]
    ]
    