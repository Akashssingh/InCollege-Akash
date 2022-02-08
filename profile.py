import sqlite3
# Creating Database File
conn = sqlite3.connect('users.db')
# Creating SQLite Cursor Global Variable
cursor = conn.cursor()
import friend
#Formats words in a string to all start with an uppercase letter and end in lowercase
def sanatize(str):
    str2 = ""
    for i in range(0, len(str)):
        if i == 0:
            str2 = str2 + str[i].upper()
        elif str2[i-1] == " ":
            str2 = str2 + str[i].upper()
        else:
            str2 = str2 + str[i].lower()
    return str2
#Provides the user option screen to edit their profile
def editProfile(currentUser):
    run = True
    while run:
        print("What would you like to edit?")
        print("1. Edit Title")
        print("2. Edit Major")
        print("3. Edit University Name")
        print("4. Edit Personal Info")
        print("5. Edit Experiance")
        print("6. Edit Education")
        print("7. Exit")

        x = input()

        if x == "1":
            editTitle(currentUser)
        elif x == "2":
            editMajor(currentUser)
        elif x == "3":
            editUni(currentUser)
        elif x == "4":
            editInfo(currentUser)
        elif x == "5":
            editExp(currentUser)
        elif x == "6":
            editEdu(currentUser)
        elif x == "7":
            run = False
        else:
            print("Invalid Input")

#displays profile
def viewProfile(currentUser):
    run = True
    while run:
        print("Whose profile you would like to see? Please select appropriate option.")
        print("1. See my profile")
        print("2. See a friend's profile")
        print("3. Exit")
        x = input()

        if(x == "1"):
            cursor.execute('SELECT * FROM users WHERE username=?', (currentUser,))
            data = cursor.fetchone()
            print(data[0],data[1])
            print("Title -> ",data[8])
            print("Major -> ",data[9])
            print("University -> ",data[10])
            print("About -> ",data[11])
            print("Experience (below): \n",data[12])
            print("Education (below): \n",data[13])
            print()
        elif(x == "2"):
            print("Friends:")
            # Finds Current User Friends
            cursor.execute('SELECT friends FROM users WHERE username=?', (currentUser,))
            cursorData = cursor.fetchone()
            # Splits Friends into List
            listOfFriends = cursorData[0].split(',')
            # print('Length of Friends', len(listOfFriends))
            if(len(listOfFriends) == 1):
                print('You have no friends :(')
                return False
            # Prints out List of Friends
            for friend in listOfFriends:
                print(friend)
            print("Please select the friend whose profile you would like to see. Enter Friends Username: ")
            friendName = input()

            # While loop waiting for correct username
            while friendName not in listOfFriends:
                print("Please input valid username from list")
                friendName = input()
            # Gets Friends Profile Information
            cursor.execute('SELECT * FROM users WHERE username=?', (friendName,))
            data2 = cursor.fetchone()
            print(data2[0], data2[1])
            print("Title -> ", data2[8])
            print("Major -> ", data2[9])
            print("University -> ", data2[10])
            print("About -> ", data2[11])
            print("Experience (below): \n", data2[12])
            print("Education (below): \n", data2[13])
            print()

        elif(x == "3"):
            run = False


#Edits the Title    
def editTitle(currentUser):
    cursor.execute('SELECT title FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    convert = str(data)
    print("Current Title:")
    print(dbCleaner(convert))
    #print("Input your new title below:")
    x = input("Input your new title below:")

    cursor.execute("UPDATE users SET title=? WHERE username=?",(x,currentUser,))
    conn.commit()
    print("The title has been updated")
    return 1

#Edits the Major
def editMajor(currentUser):
    cursor.execute('SELECT major FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    convert = str(data)
    print("Current major:")
    print(dbCleaner(convert))
    print("Input your new major below:")
    x = input()
    x =sanatize(x) 

    cursor.execute("UPDATE users SET major=? WHERE username=?",(x,currentUser,))
    conn.commit()
    print("The major has been updated")
    return 1

#Edits the University
def editUni(currentUser):
    cursor.execute('SELECT university FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    convert = str(data)
    print("Current university:")
    print(dbCleaner(convert))
    print("Input your new university below:")
    x = input()
    x =sanatize(x)

    cursor.execute("UPDATE users SET university=? WHERE username=?",(x,currentUser,))
    conn.commit()
    print("The university has been updated")
    return 1

#Edits the Information
def editInfo(currentUser):
    cursor.execute('SELECT information FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    convert = str(data)
    print("Current information:")
    print(dbCleaner(convert))
    #print("Input your new information below:")
    x = input("Input your new information below:")

    cursor.execute("UPDATE users SET information=? WHERE username=?",(x,currentUser,))
    conn.commit()
    print("The information has been updated")
    return 1

#Edits the experience
def editExp(currentUser):
    cursor.execute('SELECT experiance FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    convert = str(data)
    print("Current experience:")
    print(dbCleaner(convert))
    print("Input up to 3 jobs below. If you have less than 3 you can simply type N/A:")
    
    #print("Job 1:")
    x = input("Job 1:")
    x = x + "\n"

    #print("Job 2:")
    y = input("Job 2:")
    x = x + y + "\n"

    #print("Job 3:")
    y = input("Job 3:")
    x = x + y + "\n"

    cursor.execute("UPDATE users SET experiance=? WHERE username=?",(x,currentUser,))
    conn.commit()
    print("The experience has been updated")
    return 1

#Edits the Education
def editEdu(currentUser):
    cursor.execute('SELECT education FROM users WHERE username=?',(currentUser,))
    data = cursor.fetchall()

    convert = str(data)
    print("Current education:")
    print(dbCleaner(convert))
    #print("Input your schoool name below:")
    x = input("Input your schoool name:")
    x = sanatize(x)
    x = x + "\n"

    #print("Input your degree:")
    y = input("Input your degree:")
    x = x + y + "\n"

    #print("Input your years attended:")
    y = input("Input your years attended:")
    x = x + y + "\n"

    cursor.execute("UPDATE users SET education=? WHERE username=?",(x,currentUser,))
    conn.commit()
    print("The education has been updated")
    return 1

#Formats text read from the database to not include [("")] surrounding it
def dbCleaner(str):
    str2 = ""
    for i in range(3, len(str)-4):
        str2 = str2 + str[i]
    return str2

#Returns true if the profile has not been edited yet.
def checkDefault(currentUser):
    cursor.execute('SELECT title FROM users WHERE username=?', (currentUser,))
    cursorData = cursor.fetchone()
    convert = str(cursorData)
    #convert = dbCleaner(convert)
    
    str2 = ""
    for i in range(2, len(convert)-3):
        str2 = str2 + convert[i]
    
    
    badString = "Profile not yet completed, please go to 'edit profile' to fill in these sections"
    print("convert: " + str2)
    if badString == str2:
        return True
    else:
        return False