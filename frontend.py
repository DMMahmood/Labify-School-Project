from main import *
#text based ui
from re import fullmatch
def mainUI():
    print(f'Welcome to the Lab System, the date is {today()} and the time is {timeCurrent()}')
    print("Lab System \n 1. User menu \n 2. Experiment menu \n 3. SignIO \n 4. Refresh \n 5. Settings(TBC) \n 6. Progress(TBC) \n 7. Exit")
    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Invalid choice")
        mainUI()
    if choice == 1:
        UserMenu()
    elif choice == 2:
        ExperimentMenu()
    elif choice == 3:
        SignIO()
    elif choice == 4:
        mainUI()
    elif choice == 5:
        Settings()
    elif choice == 6:
        Progress()
    elif choice == 7 or -1:
        exit()
    else:
        print('>invalid choice')

while __name__ == '__main__':
    mainUI()

def UserMenu():
    suboptions = '1. Search user \n 2. Add user \n 3. Delete user \n 4. Back'
    print(suboptions)
    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Invalid choice")
        UserMenu()
    if choice == 1:
        searchUser()
    elif choice == 2:
        addUser()
    elif choice == 3:
        deletingUser()5
    elif choice == 4:
        mainUI()
    else: 
        print('Invalid choice')

def ExperimentMenu():
    suboptions = '1. Search experiment \n 2. Add experiment \n 3. Delete experiment \n 4. Back'
    print(suboptions)
    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Invalid choice")
        ExperimentMenu()
    if choice == 1:
        searchExperiment()
    elif choice == 2:
        addExperiment()
    elif choice == 3:
        deleteExperiment()
    elif choice == 4:
        mainUI()
    else: 
        print('Invalid choice')

def SignIO():
    suboptions = '1. Sign in \n 2. Sign out \n 3. Back'
    print(suboptions)
    try:
        choice = int(input("Enter choice: "))
    except ValueError:
        print("Invalid choice")
        SignIO()
    if choice == 1:
        signIn()
    elif choice == 2:
        signOut()
    elif choice == 3:
        mainUI()
    else:
        print('Invalid choice')


def Settings():
    print('TBC')

def Progress():
    print('TBC')


def searchUser():
    print("Searching for User \n")
    try:
        userID = str(input("Please enter the User's id: ")).lower()
    except ValueError:
        print('ValueError')
    if fullmatch("^[A-Z]{4}[0-9]{3}$", userID) != None:
        user = searchUserID(userID)
        print(user)
    else:
        print(-1)

def addUser():
    print('Creating new User \n')
    try:
        password = str(input('Password: '))
        admin = int(input('Admin (0 for no, 1 for yes: )'))
    except ValueError:
        print("ValueError")
    if fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password) == None or admin not in [0, 1]:
        return -1
    else:
        print(f'New user ID: {createUser(password, admin)}')

def searchExperiment():
    print()