import PySimpleGUI as sg
def mainwindow():
    layout = [
        [sg.text("Labify")]
    ]
    window = sg.window("Labify", layout)
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

mainwindow()
