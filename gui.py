import PySimpleGUI as sg
from main import *
from serverside import *
from random import randint
import matplotlib as mpl
sg.theme('DarkGrey')
'''
Windows i need:
sign in  done
signout done 
signup done
main admin window done 
main non admin window done
-admin- 
manage users - Submenus: create, delete, update
manage experiments - Submenus: create, delete, update
create user done
delete user done
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
     'AdminMainLayout' : [
        [sg.Text('Welcome ADMIN', text_color='Red'), sg.Text(today())],
        [sg.Button('Experiments', key= '_Experiments'), sg.Button('Labs', key= '_Labs')],
        [sg.Button('View Info', key= '_ViewInfo'), sg.Button('Settings', key= '_Settings')],
        [sg.Button('Close', key='_Close')]
    ],
    'ExperimentsLayout' : [
        [sg.Text('Experiments'), sg.Text(str(today()))],
        [sg.Button('New', key='_NewExp'), sg.Button('Edit', key= '_Edit')],
        [sg.Button('Delete', key='_Delete'), sg.Button('View', key= '_View')],
        [sg.Button('Close', key= '_close')]
    ],
    'LabsLayout' : [
        [sg.Text('Labs'), sg.Text(str(today()))],
        [sg.button('New', key='_NewLab'), ]
    ],
    'SettingsLayout' : [
        [sg.Text('Settings'), sg.Text(str(today()))],
        [sg.Button('Change Password', key= '_ChangePass'), sg.Button('Change User', key= '_ChangeUser')],
        [sg.Button('Close', key= '_Close')]
    ]
}


def StartWindow():
    startWindow = sg.Window('Welcome', layout= layouts['StartLayout'], no_titlebar= True)
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

def defaultExperimentWindow():
    layout = [
        [sg.T('Default Experiments')], 
        [sg.B('Create'), sg.B('Delete'), sg.B('Edit')]
    ]
    window = sg.Window('Labify', layout)
    pass

def getCheckBoxes(values) -> list:
    boxes = []
    for value in values:
        boxes.append([sg.Checkbox(str(value), default=False, id=f'_{value}')])
    return boxes

def createDefaultExperimentWindow():
    allequipment = getAllEquipment()
    for i in range (0, len(allequipment)):
        allequipment[i] = [str(allequipment[i]), 0]
    #essentially need to check if each equipment is possiblle by having a dynamic layout whihc adaptsto the changing ammoint of equipment needed
    layout = [
        [sg.T('Name'), sg.InputText('', key='_Name')],
        [sg.T('Time (mins)'), sg.InputText('', key='_Time')],
        [sg.T('Equipment')],
        getCheckBoxes(getAllEquipment()),
        [sg.B('Confirm'), sg.B('Cancel')]
        ]

    window = sg.Window('labify', layout)
    event, values = window.read()
    while True:
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Confirm':
            equipment = []
            Name = values['_Name']
            if checkDefaultExperimentExists(Name):
                sg.Popup('Default already exists')
                window.close()
                defaultExperimentWindow()
            for each in allequipment:
                if values[f'_{each}'] == True:
                    equipment.append(each)
            try:
                time = int(values['_Time'])
                if 0 > time or time > 1200:
                    sg.Popup('Time not valid')    
            except ValueError:
                sg.Popup('Time not valid')
                
            
            createDefaultExperiment(Name, str(equipment), time)



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

signInWindow()