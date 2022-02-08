#Epic 3
#Written by: Tyler Smith
#Team Minnesota
#Provides the options for guest controls
import sqlite3
import functools

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

def guestOption(currentUser):
    run = True
    while run:
        print("Guest Controls:")
        print()
        print("1.Toggle Email Setting")
        print("2.Toggle SMS Setting")
        print("3.Toggle Targeted Ads Setting")
        print("4.Toggle Language Settings")
        print("5.Exit")

        x = int(input('Option: '))

        if x == 1:
            flipEmail(currentUser)
        elif x == 2:
            flipSMS(currentUser)
        elif x == 3:
            flipAds(currentUser)
        elif x == 4:
            flipLang(currentUser)
        elif x == 5:
            run = False
        else:
            print("Invalid input, try again!")


#General logic for how these functions work
#Retreives needed data based on username
#Flips respective values in the DB
def flipEmail(currentUser):
    cursor.execute('SELECT emailStatus FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    #Converts the raw data into a usable int
    clean = functools.reduce(lambda sub, ele: sub * 10 + ele, data[0])
    if clean == 1:
        clean = 0
    else:
        clean = 1

    #Updating DB
    cursor.execute("UPDATE users SET emailStatus=? WHERE username=?",(clean,currentUser,))
    conn.commit()
    print("Email setting has been toggled")
    return clean

def flipAds(currentUser):
    cursor.execute('SELECT adStatus FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    #Converts the raw data into a usable int
    clean = functools.reduce(lambda sub, ele: sub * 10 + ele, data[0])
    if clean == 1:
        clean = 0
    else:
        clean = 1

    #Updating DB
    cursor.execute("UPDATE users SET adStatus=? WHERE username=?",(clean,currentUser,))
    conn.commit()
    print("Targeted Ads setting has been toggled")
    return clean

def flipSMS(currentUser):
    cursor.execute('SELECT smsStatus FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    #Converts the raw data into a usable int
    clean = functools.reduce(lambda sub, ele: sub * 10 + ele, data[0])
    if clean == 1:
        clean = 0
    else:
        clean = 1

    #Updating DB
    cursor.execute("UPDATE users SET smsStatus=? WHERE username=?",(clean,currentUser,))
    conn.commit()
    print("SMS setting has been toggled")
    return clean

def flipLang(currentUser):
    cursor.execute('SELECT language FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    #Converts the raw data into a usable int
    clean = functools.reduce(lambda sub, ele: sub * 10 + ele, data[0])
    if clean == 1:
        clean = 0
    else:
        clean = 1

    #Updating DB
    cursor.execute('UPDATE users SET language=? WHERE username=?',(clean,currentUser,))
    conn.commit()
    print("Language setting has been toggled")
    return clean

def getLang(currentUser):
    cursor.execute('SELECT language FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    #Converts the raw data into a usable int
    clean = functools.reduce(lambda sub, ele: sub * 10 + ele, data[0])
    return clean
