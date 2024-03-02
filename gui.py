import PySimpleGUI as sg
from main import *
from random import randint
sg.theme('DarkGrey')


layout = [
    [sg.Text(quoteCurrent()), sg.Text(f'{timeCurrent()}')], 
    [sg.Button('Sign IO', key='SignIO'), sg.Button('Labs', key='Labs'), sg.Button('Experiments', key='Experiments')],
    [sg.Button('Settings', key='Settings'), sg.Button('Tracking')]
]
window = sg.Window('LabiDB', layout, resizable= False, size=(720, 600))

while True:
    event, values = window()
    if ((event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?') == 'Yes') or event == sg.Exit() or event == window.Close():
        exit()
    elif event in ['SignIO', 'Labs', 'Experiments', 'Settings', 'Tracking']:
        print(event)
    
    else:
        break

