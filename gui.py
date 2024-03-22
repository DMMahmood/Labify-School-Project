import PySimpleGUI as sg
from main import *
from random import randint
sg.theme('DarkGrey')

'''
Button key layout is as follows
sg.input('Text', key= 'Upper')
sg.Button('Confirm', key= 'Confirm')
layout = ['LayoutName']
'''
layouts = {
    'StartLayout' : [
        [sg.Text('Welcome'), sg.Text(str(today()))],
        [sg.Text('User: '), sg.Input(key= '_User')], 
        [sg.Text('Password: '), sg.Input(key= '_Password', password_char= '*')],
        [sg.Button('Confirm', key= '_Confirm'), sg.Button('Close', key= '_Close')]
    ],
    'MainLayout' : [
        [sg.Text('Welcome', text_color='Red'), sg.T(today())],
        [sg.Button('Experiments', key= '_Experiments'), sg.Button('Labs', key= '_Labs')],
        [sg.Button('View Info', key= '_ViewInfo', disabled= True, disabled_button_color='Grey'), sg.Button('Settings', key= '_Settings', disabled= True, disabled_button_color='Grey')],
        [sg.Button('Close', key='_Close')]
    ],
    
     'AdminMainLayout' : [
        [sg.Text('Welcome ADMIN', text_color='Red'), sg.Text(today())],
        [sg.Button('Experiments', key= '_Experiments'), sg.Button('Labs', key= '_Labs')],
        [sg.Button('View Info', key= '_ViewInfo'), sg.Button('Settings', key= '_Settings')],
        [sg.Button('Close', key='_Close')]
    ],

    }

def StartWindow():
    startWindow = sg.Window('Welcome', layout= layouts['StartLayout'], no_titlebar= True)
    while True:
        event, values = startWindow.read()
        if event in (sg.WIN_CLOSED, 'Exit', '_Close'):
            startWindow.close()
            break
        elif event == '_Confirm':
            user, password = values['_User'], values['_Password']
            x = searchUserID(user)
            if x == None:
                sg.popup('Incorrect Information', no_titlebar= True)
                startWindow.close()
                StartWindow()
            elif x[1] == password:
                admin = AdminCheck(user)
                if admin == True:
                    admin = '1'
                else:
                    admin = '0'
                MainWindow(startWindow, user, admin)
            else:
                startWindow.close()
                StartWindow()
        else:
            startWindow.close()
            break



def MainWindow(prevWindow, user, admin):
    prevWindow.close() #alawys close previous window
    if admin == '1':
        mainWindow = sg.Window('Main', layout= layouts['AdminMainLayout'], no_titlebar= True)
    else:
        mainWindow = sg.Window('Main', layout= layouts['MainLayout'], no_titlebar= True)
    while True:
        event, values = mainWindow.read()
       
        
        
def ExperimentsWindow(prevWindow, User, admin):
    prevWindow.close()
    adminExperimentLayout = [
        [sg.Text('Experiments'), sg.Text(str(today()))],
        [sg.Button('New', key='_NewExp'), sg.Button('Edit', key= '_Edit')],
        [sg.Button('Delete', key='_Delete'), sg.Button('View', key= '_View')],
        [sg.Button('Close', key= '_close')]
    ]
    ExperimentLayout = [
        [sg.Text('Experiments'), sg.Text(str(today()))],
        [sg.Button('New', key='_NewExp'), sg.Button('View', key='_View')],
        [sg.Button('Close', '_Close')]
    ]
    if admin == '1':
        experimentsWindow = sg.Window('Experiments', layout= adminExperimentLayout, no_titlebar= True)
    else:
        experimentsWindow = sg.Window('Experiments', layout= ExperimentLayout, no_titlebar= True)
        event, values = experimentsWindow.read()
    
        if event in (sg.WIN_CLOSED, 'Exit', '_Close'):
            MainWindow(experimentsWindow())
        elif event == 'New':
            newPersonLayout = [
                [sg.Text('New experiment'), sg.Text(timeCurrent())],
                [sg.Text('Info'), sg.Input('')],
                [sg.Button('Confirm'), sg.Button('Cancel')]
            ]




def LabsWindow(prevWindow, User, Admin):
    prevWindow.close()
    labsLayout = [
        [sg.Text('Labs'), sg.Text(str(today()))],
        [sg.button('New', key='_NewLab'), ]
    ]

def SettingsWindow():
    pass

def ViewInfoWindow():
    pass


StartWindow()

