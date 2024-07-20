from sqlite3 import *
from random import randint
import re
'''
tables: users, experiments, checkin/out
columns: users: id, password, admin
         experiment: description, location
         check in and out: id, timein, timeout, totaltime(calculated at timeout else assume 0)

format for timeinandout:
  timein: HH:MM, timeout: HH:MM, totaltime: HH:MM

format for variables:
id: str -> 7 digit number, followed by U for user, E for experiment, C for checkin/out
password: str, 
admin: int, 
description: str, 
location: str, 
timein: str, 
timeout: str, 
totaltime: str
'''

#connecting to db
conn = connect('database.db')
c = conn.cursor()

def starter():
    global conn
    global c
    conn = connect('database.db')
    c = conn.cursor()
    create_tables()


def create_tables(): #call at runtime(add to main but do not loop)
    c.execute('CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, password TEXT, admin INTERGER)') #admin: 0 = false, 1 = true
    c.execute('CREATE TABLE IF NOT EXISTS experiments (id TEXT PRIMARY KEY, description TEXT, location TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS checkinout (id TEXT PRIMARY KEY, timein TEXT, timeout TEXT, totaltime TEXT)') #totaltime is calculated at timeout, else assume 0
    conn.commit()


def add_user(password, admin):
    checkvars({"password": password,
              "admin": admin})
    c.execute('INSERT INTO users VALUES (?,?,?)', (f"{idgen()}U", password, admin))
    conn.commit()

def add_experiment(description, location):
    checkvars({
        "description": description,
        "location": location
    })
    c.execute('INSERT INTO experiments VALUES (?,?,?)', (f"{idgen()}E", description, location))
    conn.commit()

def add_checkin(timein):
    checkvars({
        "timein": timein
    })
    c.execute('INSERT INTO checkinout VALUES (?,?,?,?)', (f"{idgen()}C", timein, '', 0))
    conn.commit()

def add_checkout(id, timeout):
    checkvars({
        "id": f"{id}",
        "timeout": timeout
    })
    #get timein, calculate totaltime, add to database
    c.execute('SELECT timein FROM checkinout WHERE id=?', (id,))
    timein = c.fetchone()[0]
    totaltime = total_time(timein, timeout)
    c.execute('UPDATE checkinout SET timeout=?, totaltime=? WHERE id=?', (timeout, totaltime, id))
    conn.commit()

#functions to read from database
def get_user(id):
    id = f"{id}U"
    checkvars({
        "id": id
    })
    c.execute('SELECT * FROM users WHERE id=?', (id,))
    return c.fetchone()

def get_experiment(id):
    id = f"{id}E"
    checkvars({
        "id": id
    })
    c.execute('SELECT * FROM experiments WHERE id=?', (id,))
    return c.fetchone()

def get_checkin(id):
    id = f"{id}C"
    checkvars({
        "id": id
    })
    c.execute('SELECT * FROM checkinout WHERE id=?', (id,))
    return c.fetchone()

def get_all_users():
    c.execute('SELECT * FROM users')
    return c.fetchall()

def get_all_experiments():
    c.execute('SELECT * FROM experiments')
    return c.fetchall()

def get_all_checkin():
    c.execute('SELECT * FROM checkinout')
    return c.fetchall()

#functions to update database
def update_user(id, password, admin):
    id = f"{id}U"
    checkvars({
        "id": f"{id}",
        "password": password,
        "admin": admin
    })
    c.execute('UPDATE users SET password=?, admin=? WHERE id=?', (password, admin, id))
    conn.commit()

def update_experiment(id, description, location):
    id = f"{id}E"
    checkvars({
        "id": id,
        "description": description,
        "location": location
    })
    c.execute('UPDATE experiments SET description=?, location=? WHERE id=?', (description, location, id))
    conn.commit()

def update_checkinout(id, timein, timeout):
    id = f"{id}C"
    checkvars({
        "id": id,
        "timein": timein,
        "timeout": timeout
    })
    totaltime = totaltime(timein, timeout)
    c.execute('UPDATE checkinout SET timein=?, timeout=?, totaltime=? WHERE id=?', (timein, timeout, totaltime, id))
    conn.commit()

#functions to delete from database
def delete_user(id):
    id = f"{id}U"
    checkvars({
        "id": id
    })
    c.execute('DELETE FROM users WHERE id=?', (id,))
    conn.commit()

def delete_experiment(id):
    id = f"{id}E"
    checkvars({
        "id": id
    })
    c.execute('DELETE FROM experiments WHERE id=?', (id,))
    conn.commit()

def delete_checkin(id):
    id = f"{id}C"
    checkvars({
        "id": id
    })
    c.execute('DELETE FROM checkinout WHERE id=?', (id,))
    conn.commit()

def delete_all_users():
    c.execute('DELETE FROM users')
    conn.commit()

def delete_all_experiments():
    c.execute('DELETE FROM experiments')
    conn.commit()

def delete_all_checkin():
    c.execute('DELETE FROM checkinout')
    conn.commit()

def delete_all_tables():
    c.execute('DROP TABLE users')
    c.execute('DROP TABLE experiments')
    c.execute('DROP TABLE checkinout')
    conn.commit()

def close():
    conn.close()
