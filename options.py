import sqlite3
from sqlite3.dbapi2 import Cursor
import login
import guestControls
import profile
import friend
import courses
import notifs
import random
import api

# Creating Database File
conn = sqlite3.connect('users.db')
# Creating SQLite Cursor Global Variable
cursor = conn.cursor()


def loginFunc(val):
    if(val == 1):
        print('You are already logged in.')
        print()
        return 1
    else:
        #x = 1
        run = True
        train = ""
        while run:
            train = input(
                "Would you like to access the training mode? Enter Y/N: ")
            if(train.lower() == 'y') or (train.lower() == 'n'):
                run = False
            else:
                print("\nInvalid Input. Please enter a valid input (Y/N).\n")

        if(train.lower() == 'y'):
            training()

        userUsername = input('Enter your Username: ')
        userPassword = input('Enter your Password: ')
        # Change this to be the username so it cyan be saved in main for later use
        return login.loginUser(userUsername, userPassword)


def signup(val):
    if(val == 1):
        print('You are already logged in.')
        print()
        return 1
    else:
        x = 2
        # call create account function
        firstName = input('Enter your first name: ')
        lastName = input('Enter your last name: ')
        userUsername = input('Enter a Username ')
        userPassword = input('Enter a Password ')
        loggedIn = login.insertUser(
            firstName, lastName, userUsername, userPassword)

        print('LOGGEDIN IS ' + str(loggedIn))
        return loggedIn
        print()

# post job function


def postJob(title, description, employer, location, salary):
    # check how many jobs are already posted
    count = 1
    for i in cursor.execute('SELECT * FROM jobs'):
        count = count + 1
    if(count > 10):
        print()
        print(
            'The maximum number of job postings has been reached. Please try again later.')
    else:
        print()
        # get first name of user
        firstName = input('Please enter your first name: ')
        # get last name of user
        lastName = input('Please enter your last name: ')
        print()
        # Creating Random ID
        tableID = str(random.randint(1, 10000))
        uniqueID = False
        while uniqueID == False:
            # Searching Table for ID
            cursor.execute('SELECT * from jobs WHERE id=?', (tableID,))
            # Returning Selection
            idList = cursor.fetchall()
            # If Cursor found any rows with ID
            if len(idList) > 0:
                # Generate another ID1

                tableID = random.randint(1, 10000)
            else:
                # End Loop
                uniqueID = True
        # Inserting Job into Job Database Table
        cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', (tableID, firstName,
                                                                     lastName, title, description, employer, location, salary))
        conn.commit()
        # Updating MyCollege_jobs.txt
        api.myCollegeJobsAPI()
        print('The job has been posted. It is currently unavailable to be displayed.')
        print()
    return True
# Help Function


def help_page(first, last):
    cursor.execute('SELECT * FROM users ')

    cursor.execute(
        'SELECT * FROM users WHERE firstName=? AND lastName=?', (first, last))
    if(cursor.fetchone()):
        print("They are a part of the InCollege system")
        return 1
    else:
        print("They are not yet a part of the InCollege system yet")
        return 0

# job search function

# Option 3 - Search for Jobs - Chase Rogalski 10/21/20


def job_search(username):
    appliedTo = notifs.howManyJobs(username)
    hold = str(appliedTo)
    print("You have applied to: " + hold + " jobs")
    print("The following jobs that you have applied for are no longer avalible:")
    tempList = notifs.beenRemoved(username)
    for i in range(0, len(tempList)):
        print(tempList[i])
    while(True):
        print('Job Listings:')
        # Cursor selects jobs table
        cursor.execute('SELECT * FROM jobs ')
        # listOfJobs contains list of tuples
        listOfJobs = cursor.fetchall()

        count = 1
        # Listing All Jobs in Jobs Table
        for job in listOfJobs:
            print(count, "-", job[3])
            count += 1

        #print('To learn more, please enter listing number or 0 to return to Main Menu: ')
        choice = input(
            'To learn more, please enter listing number or 0 to return to Main Menu: ')
        # Validating the Choice Input
        if (int(choice) > 0 and int(choice) <= count):
            userChoice = int(choice)
            # Job Info Output
            print('Title:', listOfJobs[1 - userChoice][3])
            print('Description:', listOfJobs[1 - userChoice][4])
            print('Employer:', listOfJobs[1 - userChoice][5])
            print('Location:', listOfJobs[1 - userChoice][6])
            print(f'Salary: ${listOfJobs[1 - userChoice][7]}')
            print('Contact Info:',
                  listOfJobs[1 - userChoice][1], listOfJobs[1 - userChoice][2])

            print(
                'To Apply - Enter 1 / To Save the Job - Enter 2 / To Return to Job Listings - Enter 0')
            jobChoice = input()
            # Returns to Job Listings
            if(jobChoice == '0'):
                continue
            if(jobChoice == '1'):
                # Apply Job Function
                # Check if User already Applied
                cursor.execute(
                    'SELECT appliedJobs FROM users WHERE username=?', (username,))
                appliedJobsTuple = cursor.fetchone()
                # Retrives String
                jobsString = appliedJobsTuple[0]
                # Checks to see if String Contains the Job ID
                if(jobsString.find(str(listOfJobs[1 - userChoice][0])) != -1):
                    print('Sorry, you already applied for the job.')
                    continue

                # Adding Job ID to String
                jobsString = jobsString + "," + \
                    str(listOfJobs[1 - userChoice][0])
                # If its the first Job, then removing first comma
                if jobsString[0] == ',':
                    jobsString = jobsString[1:]
                # Updating the Database

                # ------------------------------------------- grab/insert applicant information
                gradDate = input("Please enter your graduation date: ")
                startDate = input("Please enter your preferred start date: ")
                paragraph = input(
                    "Please tell us why you are good fit for this job: ")

                cursor.execute('INSERT INTO apps VALUES(?,?,?,?,?)', (
                    listOfJobs[1 - userChoice][0], username, gradDate, startDate, paragraph))

                # -------------------------------------------

                cursor.execute(
                    'UPDATE users SET appliedJobs=? WHERE username=?', (jobsString, username,))

                cursor.execute(
                    'UPDATE users SET masterList=? WHERE username=?', (jobsString, username,))
                # Saving Database
                conn.commit()

                print('Applied!')

                continue
            if(jobChoice == '2'):
                # Save Job Function
                # Check if User already Applied
                cursor.execute(
                    'SELECT savedJobs FROM users WHERE username=?', (username,))
                savedJobsTuple = cursor.fetchone()
                # Retrives String
                savedJobsString = savedJobsTuple[0]
                # Checks to see if String Contains the Job ID
                if(savedJobsString.find(str(listOfJobs[1 - userChoice][0])) != -1):
                    print('Sorry, you already saved the job')
                    continue

                # Adding Job ID to String
                savedJobsString = savedJobsString + "," + \
                    str(listOfJobs[1 - userChoice][0])
                # If its the first Job, then removing first comma
                if savedJobsString[0] == ',':
                    savedJobsString = savedJobsString[1:]
                # Updating the Database
                cursor.execute(
                    'UPDATE users SET savedJobs=? WHERE username=?', (savedJobsString, username,))
                # Saving to Databse
                conn.commit()

                print('Saved!')
                continue
            else:
                print('Please Enter A Valid Number')
                continue
        else:
            return False

    # print('This feature is under construction. Come back later!')

# Removing Job Function = Chase Rogalski 10/22/20


def removeJob(jobID):
    notifs.updateMaster(jobID)
    # Iterates through Every Row in Database
    for row in cursor.execute('SELECT username,appliedJobs,savedJobs FROM users'):
        # row[0] - username row[1] - appliedJobs row[2] - savedJobs
        appliedJobsString = ''
        savedJobsString = ''
        if(row[1].find(jobID) != -1):
            print('Found in Applied Jobs')
            # Found Job ID
            appliedJobsString = row[1]
            # Removing JobID and Comma from Applied Jobs
            if(row[1].find(',')):
                savedJobsString = savedJobsString.replace((','+jobID), '')
            else:
                savedJobsString = savedJobsString.replace(jobID, '')

            # Updating AppliedJobs Cell for Row in Database
            cursor.execute(
                'UPDATE users SET appliedJobs=? WHERE username=?', (appliedJobsString, row[0],))
            # Saving Database
            conn.commit()

        if(row[2].find(jobID) != -1):
            print('Found in Saved Jobs')
            # Found Job ID
            savedJobsString = row[2]

            # Removing JobID and Comma from Saved Jobs
            if(row[2].find(',')):
                savedJobsString = savedJobsString.replace((','+jobID), '')
            else:
                savedJobsString = savedJobsString.replace(jobID, '')

            # Updating savedJobs Cell for Row in Database
            cursor.execute(
                'UPDATE users SET savedJobs=? WHERE username=?', (savedJobsString, row[0],))
            # Saving Database
            conn.commit()

    # Removing Job from Job Table Database
    cursor.execute('DELETE FROM jobs WHERE id=?', (jobID,))
    # Removing Job ID from User's Saved & Applied Job
    conn.commit()
    # Removing from apps table
    cursor.execute('DELETE FROM apps WHERE job_id=?', (jobID,))
    conn.commit()

    # Updating MyCollege_jobs.txt
    api.myCollegeJobsAPI()


def getJobPostings(username):  # get jobs posted by current user
    firstname = input('Please enter your first name: ')
    lastname = input('Please enter your last name: ')
    cursor.execute('SELECT id, title FROM jobs WHERE postedBy_firstname=? AND postedBy_lastname=?',
                   (firstname, lastname,))  # get all current job listings
    jobs = cursor.fetchall()  # grabs all results
    option = -1
    while(not (int(option) == 0)):
        count = 1
        print()
        print('Jobs Posted By You')
        for j in jobs:
            print(str(count) + '. ' + j[1])
            count = count + 1

        option = input(
            'Enter the number of the posting to delete or enter 0 to return to main menu: ')

        if(int(option) > count):
            print('Invalid choice.')
        elif (not (int(option) == 0)):
            id = jobs[int(option) - 1][0]
            # print(id)
            removeJob(id)
    print()

# find people function


def find_people(currentUser):
    friend.search_people(currentUser)


# Connect People Function


def connect_people(currentUser):
    print('This feature is under construction. Come back later!')

# Useful Link


def useful_link(val):
    ch = 0
    while(ch != 5):
        print("1.General")
        print("2.Browse InCollege")
        print("3.Business Solutions")
        print("4.Directories")
        print("5.Exit Section\n")
        ch = int(input("Your Choice:"))
        if(ch == 1):
            ch1 = 0
            while(ch1 != 8):
                print("\n1.Sign Up")
                print("2.Help Center")
                print("3.About")
                print("4.Press")
                print("5.Blog")
                print("6.Careers")
                print("7.Developers")
                print("8.Exit Section\n")
                ch1 = int(input("Your Choice"))
                if(ch1 == 1):
                    signup(val)
                elif(ch1 == 2):
                    print("We're here to help")
                elif(ch1 == 3):
                    print("In College: Welcome to In College,the world's largest college student network with many users in many countries and territories worldwide")
                elif(ch1 == 4):
                    print(
                        "In College Pressroom: Stay on top of the latest news, updates, and reports")
                elif(ch1 == 5):
                    print("Under Construction")
                elif(ch1 == 6):
                    print("Under Construction")
                elif(ch1 == 7):
                    print("Under Construction")
                elif(ch1 == 8):
                    print("Bye!")
                    break
                else:
                    print("Invalid Selection")
        elif(ch == 2):
            print("Under Construction")
        elif(ch == 3):
            print("Under Construction")
        elif(ch == 4):
            print("Under Construction")
        elif(ch == 5):
            print("Bye!")
            break


def print_data(file):
    ofile = open(file, "r")
    data = ofile.readlines()
    for line in data:
        print(line)


def imp_link(currentUser):
    print()
    ch = 0
    while(ch != 10):
        print("1.A Copyright Notice")
        print("2.About")
        print("3.Accessibility")
        print("4.User Agreement")
        print("5.Privacy Policy (ONLY WORKS WHEN LOGGED IN)")
        print("6.Cookie Policy")
        print("7.Copyright Policy")
        print("8.Brand Policy")
        print("9.Change language (ONLY WORKS WHEN LOGGED IN")
        print("10.Exit")
        ch = int(input("Your Choice: "))
        if(ch == 1):
            print_data("copyright_notice.txt")
        elif(ch == 2):
            print("In College: Welcome to In College,the world's largest college student network with many users in many countries and territories worldwide")
        elif(ch == 3):
            print_data("accessibility.txt")
        elif(ch == 4):
            print_data("user_agreement.txt")
        elif(ch == 5) and currentUser != "Temp":
            guestControls.guestOption(currentUser)
        elif(ch == 6):
            print_data("cookie_policy.txt")
        elif(ch == 7):
            print_data("copyright_policytxt.txt")
        elif(ch == 8):
            print_data("brand_policy.txt")
        elif(ch == 9) and currentUser != "Temp":
            guestControls.flipLang(currentUser)
        elif(ch == 10):
            ch = 10
        else:
            print("Invalid input")


def learn_skills():
    y = 0
    while y != 6:
        print()
        print('These are the skills offered:')
        print('1. Java')
        print('2. MySQL')
        print('3. Agile')
        print('4. C++')
        print('5. Python')
        print('To return to the main menu, enter 6.')
        print()
        value = input('Please select a skill 1-5 or enter 6 to exit: ')
        print()

        if (value == '1'):
            y = 1
            print('You selected Java. This skill is under construction. Come back later!')

        if (value == '2'):
            y = 2
            print(
                'You selected MySQL. This skill is under construction. Come back later!')

        if (value == '3'):
            y = 3
            print(
                'You selected Agile. This skill is under construction. Come back later!')

        if (value == '4'):
            y = 4
            print('You selected C++. This skill is under construction. Come back later!')

        if (value == '5'):
            y = 5
            print(
                'You selected Python. This skill is under construction. Come back later!')

        if (value == '6'):
            y = 6


def profilePage(currentUser):
    isDefault = profile.checkDefault(currentUser)
    if isDefault:
        print("Your profile hasn't been updated yet!")
    run = True
    while run:
        print("1. View Current Profile")
        print("2. Edit Current Profile")
        print("3. Exit")

        x = input()

        if x == "1":
            profile.viewProfile(currentUser)
        elif x == "2":
            profile.editProfile(currentUser)
        elif x == "3":
            run = False
        else:
            print("Invalid input")

#################################### Show My Network Option ####################################
# Chase Rogalski
# Function will show list of available friends
# Will allow user to remove friends as well
################################################################################################


def showMyNetwork(currentUser):
    print('Your Network: ')
    # Finds Username's friends from SQL database
    cursor.execute(
        'SELECT friends FROM users WHERE username=?', (currentUser,))
    # Retrieves the cell of friends for user - returns a tuple
    cursorData = cursor.fetchone()
    # Splits index 0 (where the friends data is) into a list
    listOfFriends = cursorData[0].split(',')

    if len(listOfFriends) > 0:
        # Itterates through list and outputs to user
        for friend in listOfFriends:
            print(friend)

        print('Would you like to remove a friend? Y or N')
        userInput = input()

        if userInput.lower() == 'y':
            print('Please Enter Name you would like to Remove: ')
            userInput = input()
            removeFriend(userInput, currentUser)
            removeFriend(currentUser, userInput)
        else:
            return False
    else:
        print('You have no friends :(')
        return False


#################################### Remove Friend Function ####################################
# Chase Rogalski
# Function will remove friend1 from friend2's friends list
# Used with showMyNetwork Function
################################################################################################
def removeFriend(friend1, friend2):
    print('Removing Friend')
    # Finds Username's friends from SQL database
    cursor.execute('SELECT friends FROM users WHERE username=?', (friend2,))
    # Retrieves the cell of friends for user - returns a tuple
    cursorData = cursor.fetchone()
    # Splits index 0 (where the friends data is) into a list
    friend2ListOfFriends = cursorData[0].split(',')
    try:
        friend2ListOfFriends.remove(friend1)
    except ValueError:
        pass  # do nothing!
    friend2ListOfFriendsString = ""

    for friend in friend2ListOfFriends:
        friend2ListOfFriendsString = friend2ListOfFriendsString + friend + ","
    # Removes Semi Colon for Formatting
    friend2ListOfFriendsString = friend2ListOfFriendsString[:-1]
    if len(friend2ListOfFriendsString) == 0:
        friend2ListOfFriendsString = None
    # Saving back friend2ListOfFriends to Database
    cursor.execute('UPDATE users SET friends=? WHERE username=?',
                   (friend2ListOfFriendsString, friend2,))
    conn.commit()
    return len(friend2ListOfFriends)


def showAppliedJobs(username):  # will print a list of the jobs the student has applied for
    print('------- Jobs You Have Applied For -------')
    cursor.execute(
        'SELECT appliedJobs FROM users WHERE username=?', (username,))
    cursorData = cursor.fetchone()  # grabs all results
    jobs = cursorData[0].split(',')  # breaks them up into list

    count = 1
    for job in jobs:
        cursor.execute('SELECT title FROM jobs WHERE id=?', (job,))
        title = cursor.fetchone()

        if(title):
            titles = title[0].split(',')
        else:
            titles = []

        for t in titles:
            print(str(count) + '. ' + t)

        count = count + 1  # to create a numbered list

    print()
    return count


# will print a list of the jobs the student has not applied for
def showNotAppliedJobs(username):
    print('------- Jobs You Have Not Applied For -------')
    cursor.execute('SELECT id FROM jobs')  # get all current job listings
    ids_list = cursor.fetchall()  # grabs all results
    cursor.execute('SELECT appliedJobs FROM users WHERE username=?',
                   (username,))  # get jobs user has applied to
    apps_list = cursor.fetchone()  # grabs all results
    apps = apps_list[0].split(',')  # breaks them up into list

    if(apps_list):
        apps = apps_list[0].split(',')
    else:
        apps = []

    found = False

    count = 1
    for i in ids_list:
        # print(a)
        found = False
        for a in apps:
            # print(i[0])

            if a == i[0]:
                # print(i[0])
                found = True  # the student has already applied
        #print('a:' + a + 'found: ' + str(found))
        if (not found):  # the student has not applied yet
            cursor.execute('SELECT title FROM jobs WHERE id=?',
                           (i[0],))  # get all current job listings
            title = cursor.fetchone()
            titles = title[0].split(',')
            for t in titles:
                print(str(count), '. ', t)
                count = count + 1
    return count


def printReceivedMessages(currentUser):
    cursor.execute('SELECT * FROM messages WHERE to_user=?', (currentUser,))
    messages = cursor.fetchall()  # grabs all messages to current user
    count = 0
    for message in reversed(messages):
        count = count + 1
        print(str(count) + '. FROM: ' +
              message[1] + ', MESSAGE: ' + message[2])

    return count
    print()


def seeInbox(currentUser):  # will allow user to see received messages, allow user to send messages
    print()
    option = ''
    while option != '3':
        print()
        print('Received Messages: ')
        printReceivedMessages(currentUser)
        print()
        print('Options:')
        print('1. Reply to a Message')
        print('2. Send a New Message')
        print('3. Return to Main Menu')
        option = input('Selected option: ')

        if option == '1':
            print()
            messageReceived = ''

            while messageReceived != 'exit':
                count = printReceivedMessages(currentUser)
                messageReceived = input(
                    'Which message would you like to reply to? Enter the message number, or enter "exit" to return to inbox: ')

                if messageReceived != 'exit':
                    if int(messageReceived) < 1 or int(messageReceived) > count:  # invalid choice
                        print('Invalid Choice.')
                        print()
                    else:  # correct choice
                        response = input(
                            'Please type your response to the selected message: ')
                        cursor.execute(
                            'SELECT * FROM messages WHERE to_user=?', (currentUser,))
                        messages = cursor.fetchall()  # grabs all messages to current user
                        to_user = int(count) - int(messageReceived)
                        cursor.execute("INSERT INTO messages VALUES (?,?,?)",
                                       (messages[int(to_user)][1], currentUser, response))
                        conn.commit()
                        print('Reply sent!')
                        print()

        if option == '2':
            friend = ''

            while friend != 'exit':
                print()
                print('Your Network: ')
                # Finds Username's friends from SQL database
                cursor.execute(
                    'SELECT friends FROM users WHERE username=?', (currentUser,))
                # Retrieves the cell of friends for user - returns a tuple
                cursorData = cursor.fetchone()
                # Splits index 0 (where the friends data is) into a list
                listOfFriends = cursorData[0].split(',')

                if len(listOfFriends) > 0:  # if there are friends to print
                   # Iterates through list and outputs to user
                    for friend in listOfFriends:
                        print(friend)

                friend = input(
                    'Please enter the username of the friend you want to message, or enter "exit" to return to inbox: ')

                cursor.execute(
                    'SELECT membership FROM users WHERE username=?', (currentUser,))
                memberstat = cursor.fetchone()
                if (memberstat == 'Plus'):
                    flag = True
                if friend != 'exit':
                    flag = False  # True if friend is found in network
                    for person in listOfFriends:
                        if friend == person:
                            flag = True

                    if not flag:
                        print('That person is not in your network.')
                        print()
                    else:
                        message = input('Please type your message: ')
                        print()
                        cursor.execute(
                            "INSERT INTO messages VALUES (?,?,?)", (friend, currentUser, message))
                        conn.commit()
                        print('Message sent!')
                        print()

    print()


def Plus(currentUser):
    ch = 0
    cursor.execute(
        'SELECT membership FROM users WHERE username=?', (currentUser,))
    memberstat = cursor.fetchone()
    while(ch != 3):
        print("1. Get Plus")
        print("2. Remove Plus")
        print("3. Exit")
        ch = int(input("Your Choice: "))

        if(ch == 1):
            if(memberstat == 'Plus'):
                print("You own a Plus Membership")
                break
            else:
                print("Welcome to Plus")
                print("You are to be billed monthly")
                cc = input("Enter CC ")
                address = input("Enter Address")
                print("Membership Upgraded.")
                memberstat = 'Plus'
                cursor.execute(
                    'UPDATE users SET membership=? WHERE username=?', ('Plus', currentUser,))

        if(ch == 2):
            if(memberstat == 'Standard'):
                print("You own a Standard Membership")
            else:
                print("Welcome to Standard")
                memberstat = 'Standard'
                cursor.execute(
                    'UPDATE users SET membership=? WHERE username=?', ('Standard', currentUser,))
    if(memberstat == 'Plus'):
        print("Plus Features")
        ch = 0
        while(ch != 3):
            print("1. View Students in the System")
            print("2. Send Message to Student")
            print("3. Exit")
            ch = int(input("Your Choice: "))
            cursor.execute('SELECT username FROM users')
            data = cursor.fetchall()

            if(ch == 1):
                for i in range(len(data)):
                    print(i+1, '\t', data[i])
            if(ch == 2):
                friend = input(
                    "Enter username you want to send a message to: ")
                if friend in data:
                    message = input('Please type your message: ')
                    print()
                    cursor.execute(
                        "INSERT INTO messages VALUES (?,?,?)", (friend, currentUser, message))
                    conn.commit()
                    print('Message sent!')
                    print()

                else:
                    print("User doesn't exist")

###################################################################################################################
# Epic 9 - Training Functionality - Akash Singh
###################################################################################################################

trainingList = ["Training and Education","IT Help Desk","Bustiness Analysis and Strategy","Security"]
def training():
    run = True
    while run:
        print("\nHere is a list of training topics\n")
        for i in range(1,len(trainingList) + 1):
            print(i,"-",trainingList[i-1])
        print(len(trainingList) + 1,"- Exit\n")
        print("Please choose a valid option from 1 to",len(trainingList),"or enter",len(trainingList) + 1,"to exit this menu:",end=" ")
        x = input()

        if(x == "1"):
            trainAndEdu()
        elif(x == "2"):
            itHelp()
        elif(x == "3"):
            BusAnalStrat()
            break
        elif(x == "4"):
            secure()
        elif(int(x) > 4 and int(x) < len(trainingList) + 1):
            print("\n Coming Soon!")
        elif(x == str(len(trainingList) + 1)):
            print('Leaving Training...')
            run = False
        else:
            print("\nInvalid Input. Please try again.")


def trainAndEdu():
    run = True
    while run:
        print("\nHere are your training and education options: \n"
              "1. Resume\n"
              "2. Interview\n"
              "3. Job Search\n"
              "4. Networking\n"
              "5. Exit\n")
        x = input(
            "Please enter a valid option from 1 to 4 or enter 5 to exit this menu: ")

        if (x == "1"):
            print("\nUnder Construction. Please come back later.")
        elif (x == "2"):
            print("\nUnder Construction. Please come back later.")
        elif (x == "3"):
            print("\nUnder Construction. Please come back later.")
        elif (x == "4"):
            print("\nUnder Construction. Please come back later.")
        elif (x == "5"):
            run = False
        else:
            print("\nInvalid Input. Please try again.")


def itHelp():
    print("\nComing soon!")
    return True


def secure():
    print("\nComing soon!")
    return True


def BusAnalStrat():
    print("\nHere are lists of some trending courses - \n"
          "1. How to use In College learning\n"
          "2. Train the trainer\n"
          "3. Gamification of learning\n\n"
          "Not seeing what you’re looking for? Sign in to see all 7,609 results!\n")
    x = input("Please enter any valid input from 1 - 3 to sign in!")
    return False


# Epic 9

def selectCourse(currentUser):
    run = True
    while run:
        courses.loadCourses()
        x = courses.alreadyTaken(currentUser)
        print("The following courses have been taken already:")
        for i in range(0, len(x)):
            print(x[i])
        print("Type the number of the course you want to take, press 6 to exit")
        userIn = input()
        if userIn != "6":
            courses.takeCourse(userIn, currentUser)
        else:
            run = False



def postJobTest(title, description, employer, location, salary):
    # check how many jobs are already posted
    count = 1
    for i in cursor.execute('SELECT * FROM jobs'):
        count = count + 1
    if(count > 10):
        print()
        print(
            'The maximum number of job postings has been reached. Please try again later.')
    else:
        print()
        # get first name of user
        firstName = "fn"
        # get last name of user
        lastName = "ln"
        print()
        # Creating Random ID
        tableID = str(random.randint(1, 10000))
        uniqueID = False
        while uniqueID == False:
            # Searching Table for ID
            cursor.execute('SELECT * from jobs WHERE id=?', (tableID,))
            # Returning Selection
            idList = cursor.fetchall()
            # If Cursor found any rows with ID
            if len(idList) > 0:
                # Generate another ID1

                tableID = random.randint(1, 10000)
            else:
                # End Loop
                uniqueID = True
        # Inserting Job into Job Database Table
        cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', (tableID, firstName,
                                                                     lastName, title, description, employer, location, salary))
        conn.commit()
        # Updating MyCollege_jobs.txt
        api.myCollegeJobsAPI()
        print('The job has been posted. It is currently unavailable to be displayed.')
        print()
    return True
# Help Function