import PySimpleGUI as sg # type: ignore #the gui library
from serverside import * #import all functions from serverside.py
from datetime import date #to get the current date and time
from icecream import ic # type: ignore #testing
sg.theme('DarkGrey') #

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
signedInUser = 'Dan' # change this to blank string '' before deploying
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
    window = sg.Window('Labify', layout)
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
            equipment = str(f"'{convertlisttostring(equipment)}'")
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
    #ExperimentID TEXT PRIMARY KEY, ExperimentName Text, Equipment TEXT, Active INTERGER, UserID TEXT)

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


def equipmentManagementWindow():
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
            chooseSignInWhenReOpening(signedInUser)

def viewEquipmentWindow():
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

def singleEquipmentWindow(Name):
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
    

def createEquipmentWindow():
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
            if createNewEquipment(name, count):
                sg.Popup(f'Equipment {name} created, total: {count}')
            else:
                sg.Popup(f'Error {name} could not be created')
            window.Close()
            equipmentManagementWindow()
        elif event == 'Cancel':
            window.Close()
            equipmentManagementWindow()


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
            chooseSignInWhenReOpening(signedInUser)

def viewUsersWindow():
    users = getAllUsers()

    for i in range(len(users)):
        users[i] = str(users[i])
    
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
            window.Close()
            manageUsersWindow()
        elif event == 'Cancel':
            window.Close()
            manageUsersWindow()   


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
            window.Close()
            manageUsersWindow()


#this starts both programs, no need to run 'serverside.py'



def start():
    if getAllUsers() == []:
        createUserWindow()
    else:
        chooseSignInWhenReOpening(signedInUser)


start()


#startExperimentFromDefaultWindow()
#startExperimentFromNewWindow()
#singleLiveExperimentWindow()
#viewLiveExperimentsWindow()