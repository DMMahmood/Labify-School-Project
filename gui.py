import PySimpleGUI as sg
sg.theme('DarkPurple6')
layout = [
    [sg.Text("Welcome to pakistan UWU <3"), sg.Button('UWU ONI CHAN')], 
    [sg.Text("Skibidi fornitie chicago detroit  toilet chungus ballsack 42069 i just licked my own hair")]
]
window = sg.Window('Balls', layout)

while True:
    event, values = window.read()
    print(event, values)
    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?') == 'Yes':
        exit()
    elif event == sg.Exit:
        exit()
window.close()