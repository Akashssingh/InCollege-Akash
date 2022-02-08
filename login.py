import sqlite3
import user
import api
# Creating Database File
conn = sqlite3.connect('users.db')
# Creating SQLite Cursor Global Variable
cursor = conn.cursor()
# Creating User Table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
            (firstName text, lastName text, username text, password text, emailStatus int, adStatus int, smsStatus int, language int, title text, major text, university text, information text, experiance text, education text, pendingReqs text, pendingSentReqs text, friends text, appliedJobs text, savedJobs text, membership text, masterList text, completedCourses text)''')

# Creating Job Table
cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
            (id text, postedBy_firstname text, postedBy_lastName text, title text, description text, employer text, location text, salary text)''')

# Creating Application Table
cursor.execute('''CREATE TABLE IF NOT EXISTS apps
            (job_id text, applied_username text, gradDate text, startDate text, paragraph text)''')

# Creating Messages Table
cursor.execute('''CREATE TABLE IF NOT EXISTS messages
            (to_user text, from_user text, message text)''')


def deleteRecords():
    cursor.execute('DROP TABLE users')
    cursor.execute('DROP TABLE jobs')
    cursor.execute('DROP TABLE apps')
    cursor.execute('DROP TABLE messages')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
            (firstName text, lastName text, username text, password text, emailStatus int, adStatus int, smsStatus int, language int, title text, major text, university text, information text, experiance text, education text, pendingReqs text, pendingSentReqs text, friends text, appliedJobs text, savedJobs text, membership text, masterList text, completedCourses text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
            (id text, postedBy_firstname text, postedBy_lastName text, title text, description text, employer text, location text, salary text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS apps
            (job_id text, applied_username text, gradDate text, startDate text, paragraph text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
            (to_user text, from_user text, message text)''')

# Username Validation Function - Checks for uniqueness


def usernameCheck(username):
    valid = True
    count = 0
    t = (username,)

    for i in cursor.execute('SELECT * FROM users WHERE username=?', t):
        count = count + 1

    if count == 0:
        valid = True
    else:
        valid = False
        print("Sorry, your username has already been taken. Please Try Again.")

    return valid

# Password Validation Function


def passwordCheck(password):
    # Password Requirements
    overallStatus = False
    hasCapitalLetter = False
    hasSpecialCharacter = False
    hasOneDigit = False
    # If Password Lengths are Wrong
    if(len(password) < 8):
        overallStatus = False
        return overallStatus
    if(len(password) > 13):
        overallStatus = False
        return overallStatus
    # Loop through each character of the string to see if it passes all test cases
    for char in password:
        if char.isupper():  # Checking for Capital
            hasCapitalLetter = True
        if char.isalnum() == False:  # Checking for Special Character
            hasSpecialCharacter = True
        if char.isdigit():  # Checking for Digits
            hasOneDigit = True

    if hasCapitalLetter == True and hasSpecialCharacter == True and hasOneDigit == True:
        overallStatus = True

    return overallStatus


# Inserting a User Into Database

def insertUser(firstName, lastName, username, password):
    count = 1
    emails = 1
    ads = 1
    sms = 1
    lang = 1  # 1 is English 0 is Spanish
    empty = "Profile not yet completed, please go to 'edit profile' to fill in these sections"
    empty2 = ""
    print("Membership Preference: ")
    ch = 0
    while(True):
        print("1. Standard")
        print("2. Plus")
        ch = int(input("Your Choice: "))
        if(ch == 1):
            membership = "Standard"
            break
        if(ch == 2):
            print("Welcome to Plus")
            print("You are to be billed monthly")
            cc = input("Enter CC ")
            address = input("Enter Address")
            print("Membership: Plus.")
            membership = "Plus"
            break

    for i in cursor.execute('SELECT * FROM users'):
        count = count + 1

    if(passwordCheck(password) and usernameCheck(username) and count < 10):
        cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (firstName, lastName, username, password,
                                                                                              emails, ads, sms, lang, empty, empty, empty, empty, empty, empty, empty2, empty2, empty2, empty2, empty2, membership, empty2, empty2))
        conn.commit()
        api.myCollegeProfilesAPI()
        print('User Added!')
        temp = loginUser(username, password)
        return temp  # flag
    if(count > 11):
        print("All permitted accounts have been created, please come back later")
        return 0  # flag
    # Used for Displaying Rows in Database
    # for row in cursor.execute('SELECT * FROM users'):
    #     print(row)

# Logging In A User


def loginUser(username, password):
    cursor.execute(
        'SELECT * FROM users WHERE username=? AND password=?', (username, password,))
    if(cursor.fetchone()):
        print()  # formatting
        print('You have successfully logged in!')
        print()  # formatting
        return username  # flag
    else:
        print('Incorrect username / password, please try again.')
        return 0  # flag



def insertUserTesting(firstName, lastName, username, password, x = 1):
    count = 1
    emails = 1
    ads = 1
    sms = 1
    lang = 1  # 1 is English 0 is Spanish
    empty = "Profile not yet completed, please go to 'edit profile' to fill in these sections"
    empty2 = ""
    print("Membership Preference: ")
    ch = 0
    while(True):
        print("1. Standard")
        print("2. Plus")
        #ch = int(input("Your Choice: "))
        if(x == 1):
            membership = "Standard"
            break

    for i in cursor.execute('SELECT * FROM users'):
        count = count + 1

    if(passwordCheck(password) and usernameCheck(username) and count < 10):
        cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (firstName, lastName, username, password,
                                                                                              emails, ads, sms, lang, empty, empty, empty, empty, empty, empty, empty2, empty2, empty2, empty2, empty2, membership, empty2, empty2))
        conn.commit()
        api.myCollegeProfilesAPI()
        print('User Added!')
        temp = loginUser(username, password)
        return temp  # flag
    if(count > 11):
        print("All permitted accounts have been created, please come back later")
        return 0  # flag
    # Used for Displaying Rows in Database
    # for row in cursor.execute('SELECT * FROM users'):
    #     print(row)

# Logging In A User


def loginUser(username, password):
    cursor.execute(
        'SELECT * FROM users WHERE username=? AND password=?', (username, password,))
    if(cursor.fetchone()):
        print()  # formatting
        print('You have successfully logged in!')
        print()  # formatting
        return username  # flag
    else:
        print('Incorrect username / password, please try again.')
        return 0  # flag