import PySimpleGUI as sg
from main import *
from random import randint

sg.theme('DarkPurple6')
layout = [
    [sg.Text('Labify', size=(30, 1), justification='center', font=("Helvetica", 25))],
    [sg.Button('Users', key= 'Users'), sg.Button('Experiments', key= 'Experiments')], 
    [sg.Button('SignIO', key= 'SignIO'), sg.Button('Options', key= 'Options')]
]
window = sg.Window('Labify', layout, location = (0,0), size= (720, 480), resizable = False, finalize=True)

def ConfirmAdminWindow():
    layout = [
        [sg.Text('Enter an admin ID and password to continue')], 
        [sg.Text('Admin ID'), sg.InputText(key= 'AdminID')],
        [sg.Text('Password'), sg.InputText(key= 'AdminPassword')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]
    window = sg.Window('Admin Confirmation', layout, location = (0,0), size= (720, 480), resizable = False, finalize=True)
    event, values = window()
    if event == 'Submit':
        if adminCheck(values['AdminID'], values['AdminPassword']):
            return True
        else:
            return False
    elif event == 'Cancel':
        window.close()
        main()

def ExperimentsWindow():
    layout = [
        [sg.Text('Experiments')],
        [sg.Button('Live', key= 'Live'), sg.Button('Past', key= 'Past')],
        [sg.Button('New', key= 'New'), sg.Button('Edit', key= 'Edit')]
    ]
    window = sg.Window(title= 'Experiments', size=(720, 480), finalize= True, resizable= False)
    event, values = window(layout= layout)
    if ((event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?') == 'Yes') or event == window.close() or sg.Exit() or event == 'Exit':
        window.Close()
        main()


def UserWindow():
    layout = [ 
        [sg.Text('Users', size=(30, 1), justification='center', font=("Helvetica", 25))], 
        [sg.Button('Create User', key='CreateUser'), sg.Button('Show All Users', key= 'ShowUsers'), sg.Button('Search User', key= 'SearchUser')] 
        ] 

    
    window = sg.Window('Users', layout= layout, location = (0,0), size= (720, 480), resizable = False, finalize=True)
    event, values = window.read()
    if ((event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?') == 'Yes') or event == window.close() or sg.Exit() or event == 'Exit':
        exit()



def main():
    event, values = window.read()
    print(event, values)
    if ((event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?') == 'Yes') or event == window.close() or sg.Exit() or event == 'Exit':
        exit()
    else:
        if event == 'Users':
            UserWindow()
        elif event == 'Experiments':
            ExperimentWindow()
        elif event == 'SignIO':
            SignIOWindow()
        elif event == 'Options':
            OptionsWindow()
        else:
            pass



while __name__ == '__main__':
    main()

