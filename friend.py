import sqlite3
import login
import user
import profile
# Creating Database File
conn = sqlite3.connect('users.db')
# Creating SQLite Cursor Global Variable
cursor = conn.cursor()

#function that search for people. It is called in option 4 of main.
#This function search for people by input parameter
def search_people(currentUser):
    run = True
    while run:
        print("You may search people in the system by either university name, major or last name.")
        print("1. University")
        print("2. Major")
        print("3. Last Name")
        print("4. Exit")
        opt = input("Search results will be displayed as -> firstname lastname (username)."
                    "Please enter respective number from given options: ")
        if(opt == "4"):
            run = False
            break

        if(opt != "1" and opt != "2" and opt != "3" and opt != "4"):
            print("\nNot a Valid choice. Please enter valid number or enter 4 to return to main menu.\n")

        result = print_search_result(opt, currentUser)
        if result:
            send_friendReq(currentUser)



# prints the search result according to user input
def print_search_result(x, currentUser):
    run = True
    while run:
        if(x == "1"):
            uname = input("Enter University Name: ")
            cursor.execute('SELECT university FROM users WHERE university=?', (uname,))
            check = cursor.fetchall()
            for k in check:
                if k[0] == uname:
                    cursor.execute('SELECT*FROM users WHERE university=?', (uname,))
                    data = cursor.fetchall()
                    for i in data:
                        if currentUser == i[2]:
                            continue
                        print(i[0] + " " + i[1] + " (" + i[2] + ")")
                    print()
                    return True
            else:
                print("There are no users enrolled in entered university.")
                return False
        elif(x == "2"):
            maj = input("Enter Major: ")
            cursor.execute('SELECT major FROM users WHERE major=?', (maj,))
            check = cursor.fetchall()
            for k in check:
                if k[0] == maj:
                    cursor.execute('SELECT*FROM users WHERE major=?', (maj,))
                    data = cursor.fetchall()
                    for i in data:
                        if currentUser == i[2]:
                            continue
                        print(i[0] + " " + i[1] + " (" + i[2] + ")")
                    print()
                    return True
            else:
                print("There are no users enrolled in entered major.")
                return False
        elif(x == "3"):
            lname = input("Enter last name: ")
            cursor.execute('SELECT lastName FROM users WHERE lastName=?', (lname,))
            check = cursor.fetchall()
            for k in check:
                if k[0] == lname:
                    cursor.execute('SELECT*FROM users WHERE lastName=?', (lname,))
                    data = cursor.fetchall()
                    for i in data:
                        if currentUser == i[2]:
                            continue
                        print(i[0] + " " + i[1] + " (" + i[2] + ")")
                    print()
                    return True
            else:
                print("There are no users with the entered lastname.")
                return False

        else:
            run = False

#sends friend request
def send_friendReq(currentUser):
    run = True
    while run:
        x = input("Enter the username of the person you would like to send friend request:")

        cursor.execute('SELECT friends FROM users WHERE username=?', (currentUser,))
        dataCheck = cursor.fetchone()
        dataCheckstr = db2Cleaner(str(dataCheck))
        tempChecklist = [dataCheckstr]
        friendCheck = convert(tempChecklist)
        if x in friendCheck:
            print("You are already friend with this user.")
            run = False
            return run

        cursor.execute('SELECT username FROM users WHERE username=?',(x,))
        data = cursor.fetchone()
        if data is None:
            print("No such username exist in user directory")
            return False
        elif x in data:
            cursor.execute('SELECT pendingSentReqs FROM users WHERE username=?', (currentUser,))
            data = cursor.fetchone()
            datastr = db2Cleaner(str(data))
            templist = [datastr]
            sentReqs = convert(templist)
            if x in sentReqs:
                print("You have already sent a friend request to this person.")
                run = False
            else:
                cursor.execute('SELECT pendingReqs FROM users WHERE username=?', (x,))
                data = cursor.fetchone()
                data2 = str(data)
                data2 = db2Cleaner(data2)
                str1 = ","
                data2 += (currentUser + str1)

                cursor.execute('SELECT pendingSentReqs FROM users WHERE username=?', (currentUser,))
                data = cursor.fetchone()
                data3 = str(data)
                data3 = db2Cleaner(data3)
                data3 += (x + str1)

                cursor.execute("UPDATE users SET pendingReqs=? WHERE username=?", (data2,x,))
                conn.commit()
                cursor.execute("UPDATE users SET pendingSentReqs=? WHERE username=?", (data3,currentUser,))
                conn.commit()
                print("\nYour request is sent.\n")
                run = False
        else:
            print("The username is not found. Please check if it's correct")
            run = False
            return run

#Displays the pending menu and has underlying other functionalities
def pendingDisplay(currentUser):
    run = True
    while run:
        print("Please choose from following options:")
        print("1. Sent friend requests")
        print("2. Pending friend requests")
        x = input("3. Exit")

        if (x == "1"):
            cursor.execute('SELECT pendingSentReqs FROM users WHERE username=?', (currentUser,))
            data = cursor.fetchone()
            datastr = db2Cleaner(str(data))
            templist = [datastr]
            sentReqs = convert(templist)

            if len(sentReqs) == 1:
                print("There are no sent friend requests pending at the moment")
                run = False
            elif len(sentReqs) > 1:
                print("Following are pending friend requests sent by you.")
                print()

                for i in sentReqs:
                    cursor.execute('SELECT*FROM users where username =?', (i,))
                    dataloop = cursor.fetchone()
                    if dataloop is not None:
                        print(dataloop[0] + " " + dataloop[1] + " (" + dataloop[2] + ")")
                print()
                inpt = input("Would you like to cancel a friend request sent by you? Please enter Y or N :")
                if (inpt.lower() == "y"):
                    inpt2 = input("Enter the username: ")
                    cancel_sent_req(currentUser, inpt2)
                    run = False
                else:
                    run = False
        elif(x == "2"):
            cursor.execute('SELECT pendingReqs FROM users WHERE username=?', (currentUser,))
            data2 = cursor.fetchone()
            data2str = db2Cleaner(str(data2))
            temp2list = [data2str]
            pendReqs = convert(temp2list)

            if len(pendReqs) == 1:
                print("There are no pending friend requests at the moment")
                run = False
            elif len(pendReqs) > 1:
                print("Following are pending friend requests for you:")
                print()
                for i in pendReqs:
                    cursor.execute('SELECT*FROM users where username =?', (i,))
                    dataL = cursor.fetchone()
                    if dataL is not None:
                        print(dataL[0] + " " + dataL[1] + " (" + dataL[2] + ")")
                print()
                inpt3 = input("Would you like to accept/deny a friend request? Enter Y or N: ")
                if (inpt3.lower() == "y"):
                    pendUname = input("Enter the username of person you would like to accept/deny as friend: ")
                    if pendUname not in pendReqs:
                        print("This user is not in your pending requests list. Please enter valid username: ")
                        run = False
                    else:
                        print("Choose from below options: ")
                        print("1.Accept")
                        print("2.Deny")
                        print("3.Exit")
                        inpt4 = input()

                        if(inpt4 == "1"):
                            accept_friend_req(currentUser, pendUname)
                            run = False
                        elif(inpt4 == "2"):
                            cancel_friend_req(currentUser, pendUname)
                            run = False
                        else:
                            run = False
        else:
            return False

# cancels the sent request before it is accepted by the recipient
def cancel_sent_req (currentUser, cancelUser):
    cursor.execute('SELECT pendingSentReqs FROM users WHERE username=?', (currentUser,))
    data = cursor.fetchone()
    datastr = db2Cleaner(str(data))
    templist = [datastr]
    sentReqs = convert(templist)

    if(cancelUser not in sentReqs):
        print("You have not sent a friend request to this user. Enter valid username.")
        return 1
    else:
        sentReqs.remove(cancelUser)
        if ("" in sentReqs):
            sentReqs.remove("")

        updateStr = ""
        for i in sentReqs:
            updateStr += (i + ",")
        cursor.execute('UPDATE users SET pendingSentReqs=? WHERE username=?', (updateStr, currentUser,))
        conn.commit()

        cursor.execute('SELECT pendingReqs FROM users WHERE username=?', (cancelUser,))
        data2 = cursor.fetchone()
        data2str = db2Cleaner(str(data2))
        temp2list = [data2str]
        pendReqs = convert(temp2list)
        pendReqs.remove(currentUser)
        if ("" in pendReqs):
            pendReqs.remove("")
        update2Str = ""
        for i in pendReqs:
            update2Str += (i + ",")
        cursor.execute('UPDATE users SET pendingReqs=? WHERE username=?', (update2Str, cancelUser,))
        conn.commit()
        print("The friend request has been successfully withdrawn")
        return 1

# Denies the friend request.
def cancel_friend_req(currentUser, pendUser):
    cursor.execute('SELECT pendingReqs FROM users WHERE username=?', (currentUser,))
    data = cursor.fetchone()
    datastr = db2Cleaner(str(data))
    templist = [datastr]
    pendReqs = convert(templist)
    pendReqs.remove(pendUser)
    if ("" in pendReqs):
        pendReqs.remove("")
    updateStr = ""
    for i in pendReqs:
        updateStr += (i + ",")
    cursor.execute('UPDATE users SET pendingReqs=? WHERE username=?', (updateStr, currentUser,))
    conn.commit()

    cursor.execute('SELECT pendingSentReqs FROM users WHERE username=?', (pendUser,))
    data2 = cursor.fetchone()
    data2str = db2Cleaner(str(data2))
    temp2list = [data2str]
    pendSentReqs = convert(temp2list)
    pendSentReqs.remove(currentUser)
    if ("" in pendSentReqs):
        pendSentReqs.remove("")
    update2Str = ""
    for i in pendSentReqs:
        update2Str += (i + ",")
    cursor.execute('UPDATE users SET pendingSentReqs=? WHERE username=?', (update2Str, pendUser,))
    conn.commit()

    print("The friend request from this user was denied.")
    print()
    return 1

#accepts the friend request
def accept_friend_req(currentUser, penduser):
    cursor.execute('SELECT friends FROM users WHERE username=?', (currentUser,))
    data = cursor.fetchone()
    datastr = db2Cleaner(str(data))
    templist = [datastr]
    friendList = convert(templist)
    friendList.append(penduser)
    if ("" in friendList):
        friendList.remove("")
    updateStr = ""
    for i in friendList:
        updateStr += (i + ",")

    cursor.execute('SELECT friends FROM users WHERE username=?', (penduser,))
    data2 = cursor.fetchone()
    data2str = db2Cleaner(str(data2))
    temp2list = [data2str]
    friend2List = convert(temp2list)
    friend2List.append(currentUser)
    update2Str = ""
    for i in friend2List:
        update2Str += (i + ",")

    cursor.execute('UPDATE users SET friends=? WHERE username=?', (updateStr, currentUser,))
    conn.commit()
    cursor.execute('UPDATE users SET friends=? WHERE username=?', (update2Str, penduser,))
    conn.commit()

    cursor.execute('SELECT pendingReqs FROM users WHERE username=?', (currentUser,))
    data3 = cursor.fetchone()
    data3str = db2Cleaner(str(data3))
    temp3list = [data3str]
    pendReqs = convert(temp3list)
    pendReqs.remove(penduser)
    if ("" in pendReqs):
        pendReqs.remove("")
    update3Str = ""
    for i in pendReqs:
        update3Str += (i + "")
    cursor.execute('UPDATE users SET pendingReqs=? WHERE username=?', (update3Str, currentUser,))
    conn.commit()

    cursor.execute('SELECT pendingSentReqs FROM users WHERE username=?', (penduser,))
    data4 = cursor.fetchone()
    data4str = db2Cleaner(str(data4))
    temp4list = [data4str]
    pendSentReqs = convert(temp4list)
    pendSentReqs.remove(currentUser)
    if("" in pendSentReqs):
        pendSentReqs.remove("")
    update4Str = ""
    for i in pendSentReqs:
        update4Str += (i + ",")
    cursor.execute('UPDATE users SET pendingSentReqs=? WHERE username=?', (update4Str, penduser,))
    conn.commit()
    print("The friend request from this user was accepted.")
    print()
    return 1

# Used display alert message on main menu if there are any pending friend requests
def pending_count(currentUser):
    cursor.execute('SELECT pendingReqs FROM users WHERE username=?', (currentUser,))
    data = cursor.fetchone()
    datastr = db2Cleaner(str(data))
    #if datastr == "":
       # return 0
    templist = [datastr]
    pendReqs = convert(templist)
    if ("" in pendReqs):
        pendReqs.remove("")
    return len(pendReqs)

#converts string into list of words that were inside string by comma delimiting
def convert(lst):
    return (lst[0].split(","))

#Cleans the from db
def db2Cleaner(str):
    str2 = ""
    for i in range(2, len(str)-3):
        str2 = str2 + str[i]
    return str2








