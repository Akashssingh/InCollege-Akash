# API Information for InCollege
import os
from sqlite3.dbapi2 import connect
import login
import random
import sqlite3
import options


def studentAccountsAPI():
    userCount = 0
    # Checking to see if file named "studentAccounts.txt" exists
    # If file does exits continue, if not do nothing
    if(os.path.isfile('studentAccounts.txt')):
        # Opening file
        file = open('studentAccounts.txt', 'r')
        lineCount = 1
        username = ""
        password = ""
        #usercount = 0
        for line in file:
            if(lineCount == 1):
                username = line.rstrip()
            if(lineCount == 2):
                password = line.rstrip()
            if(lineCount == 3):
                lineCount = 1
                # print("Username: ", username, "Password: ", password)
                # Checking # of users is less than 11
                userCount = 0
                for i in login.cursor.execute('SELECT * FROM users'):
                    userCount += 1

                # print('Number of Users', userCount)

                count = 1
                emails = 1
                ads = 1
                sms = 1
                lang = 1  # 1 is English 0 is Spanish
                empty = "Profile not yet completed, please go to 'edit profile' to fill in these sections"
                empty2 = ""
                membership = "Standard"

                if(login.passwordCheck(password) and login.usernameCheck(username) and userCount < 11):
                    login.cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (empty2, empty2, username, password,
                                                                                                                    emails, ads, sms, lang, empty, empty, empty, empty, empty, empty, empty2, empty2, empty2, empty2, empty2, membership, empty2, empty2))
                    login.conn.commit()

                continue

            lineCount += 1
        file.close()
        return userCount
    else:
        return -1


def jobsAPI():
    # Checking to see if file named "studentAccounts.txt" exists
    # If file does exits continue, if not do nothing
    if(os.path.isfile('newJobs.txt')):
        # Opening file
        file = open('newJobs.txt', 'r')
        # Creating Variable to keep track of number of Jobs
        jobCount = 0
        # Counting Already Jobs that are in the database
        for i in login.cursor.execute('SELECT * FROM jobs'):
            jobCount += 1
        # Creating List to Store Raw Job Info
        job = []
        # Looping through newJobs.txt
        for line in file:
            # Making sure there aren't more than 10 jobs in Database
            if(jobCount < 11):
                # If line isn't end of job add line to list
                if(line.rstrip() != "====="):
                    job.append(line.rstrip())
                else:
                    # Once it reaches end of job
                    # Increasing Job Count
                    jobCount += 1
                    # Finding Index of End of Description
                    descEnd = job.index("&&&")
                    # First Index always title
                    title = job[0]
                    # Slicing List for only description lines
                    descList = job[1:descEnd]
                    # Converting list into string
                    description = "".join(descList)
                    # Getting Employer Info
                    employer = job[len(job) - 3]
                    # Getting Location Info
                    location = job[len(job) - 2]
                    # Getting Salary Info
                    salary = job[len(job) - 1]

                    # Creating Random ID
                    tableID = str(random.randint(1, 10000))
                    uniqueID = False
                    while uniqueID == False:
                        # Searching Table for ID
                        cursor.execute(
                            'SELECT * from jobs WHERE id=?', (tableID,))
                        # Returning Selection
                        idList = cursor.fetchall()
                        # If Cursor found any rows with ID
                        if len(idList) > 0:
                            # Generate another ID
                            tableID = random.randint(1, 10000)
                        else:
                            # End Loop
                            uniqueID = True
                    # Inserting Job into Job Database Table
                    options.cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', (tableID, "",
                                                                                         "", title, description, employer, location, salary))
                    options.conn.commit()

                    job.clear()
                    continue
        file.close()
        return jobCount
    else:
        # Returns -1 if there is no file
        return -1


def trainingAPI():
    # Checking to see if file named "newTraining.txt" exists
    # If file does exits continue, if not do nothing
    if(os.path.isfile('newTraining.txt')):
        # Opening file
        file = open('newTraining.txt', 'r')
        for line in file:
            programTitle = line.rstrip()
            options.trainingList.append(programTitle)

        totalTrainingPrograms = len(options.trainingList)
        file.close()
        return totalTrainingPrograms
    else:
        return -1


def myCollegeJobsAPI():
    if(os.path.isfile('MyCollege_jobs.txt')):
        os.remove("MyCollege_jobs.txt")
    # Create New file MyCollege_jobs.txt
    file = open("MyCollege_jobs.txt", "x")
    # Getting all jobs from Database
    options.cursor.execute(
        "SELECT title, description, employer, location, salary FROM jobs")
    # Writing Jobs to file
    jobTuple = options.cursor.fetchall()
    # print(jobTuple)
    jobCount = 0
    for i in jobTuple:
        print(i)
        for j in i:
            file.write(j+"\n")
        file.write("=====\n")
        jobCount += 1
    options.conn.commit()
    # Closing File
    file.close()
    # Returning Number of Jobs
    return jobCount


def myCollegeProfilesAPI():
    if(os.path.isfile('MyCollege_profiles.txt')):
        os.remove("MyCollege_profiles.txt")
    # Create New file MyCollege_profiles.txt
    file = open("MyCollege_profiles.txt", "x")
    # Getting all users from Database
    options.cursor.execute(
        "SELECT title, major, university, information, experiance, education FROM users")
    # Writing Users to file
    userTuple = options.cursor.fetchall()
    # print(userTuple)
    userCount = 0
    for i in userTuple:
        print(i)
        for j in i:
            file.write(j+"\n")
        file.write("=====\n")
        userCount += 1
    options.conn.commit()
    # Closing File
    file.close()
    # Returning Number of Users
    return userCount

##############################################################################################################
# Epic 10 - Akash Singh
##############################################################################################################


def myCollegeUsersAPI():
    if(os.path.isfile('MyCollege_users.txt')):
        os.remove('MyCollege_users.txt')

    # Create new file : MyCollege_users.txt
    file = open('MyCollege_users.txt', 'x')

    # Getting all usernames from database and the membership types
    options.cursor.execute('SELECT username, membership FROM users')

    userTuple = options.cursor.fetchall()
    userCount = 0

    for i in userTuple:
        print(i)
        for j in i:
            file.write(j + " ")
        file.write("\n")
        userCount += 1

    # Close file
    file.close()

    return userCount


def appliedJobsAPI():
    if (os.path.isfile('MyCollege_appliedJobs.txt')):
        os.remove('MyCollege_appliedJobs.txt')

    # Create new file : MyCollege_appliedJobs.txt
    file = open('MyCollege_appliedJobs.txt', 'x')

    # Getting all job_id and applied users and paragraph
    options.cursor.execute(
        'SELECT job_id, applied_username, paragraph FROM apps')

    job = options.cursor.fetchall()
    jobCount = 0

    for i in job:
        print(i)
        options.cursor.execute('SELECT title FROM jobs WHERE id=?', i)
        title = options.cursor.fetchall()
        file.write(title + "\n")
        for j in i[1:]:
            file.write(j + "\n")
        file.write("=====\n")
        jobCount += 1

    # Close file
    file.close()

    return jobCount


def savedJobsAPI():
    if (os.path.isfile('MyCollege_savedJobs.txt')):
        os.remove('MyCollege_savedJobs.txt')

    # Create new file : MyCollege_appliedJobs.txt
    file = open('MyCollege_savedJobs.txt', 'x')

    options.cursor.execute('SELECT username FROM users')
    users = options.cursor.fetchall()
    userCount = 0

    for i in users:
        file.write(db2Cleaner(str(i)) + "\n")
        options.cursor.execute(
            'SELECT savedJobs FROM users WHERE username=?', i)
        jobsTuple = options.cursor.fetchone()
        jobsStr = jobsTuple[0]
        jobs = jobsStr.split(',')
        for job in jobs:
            if(job == ''):
                continue
            options.cursor.execute('SELECT title FROM jobs WHERE id=?', job)
            title = options.cursor.fetchall()
            file.write(title + "\n")
        file.write("=====\n")
        userCount += 1

    file.close()

    return userCount


def myCollegeTraining():
    if (os.path.isfile('MyCollege_training.txt')):
        os.remove('MyCollege_training.txt')

        # Create new file : MyCollege_training.txt
    file = open('MyCollege_training.txt', 'x')
    options.cursor.execute('SELECT username FROM users')
    users = options.cursor.fetchall()
    userCount = 0

    for i in users:
        file.write(db2Cleaner(str(i)) + "\n")
        for j in options.trainingList:
            file.write(j + "\n")
        file.write("=====\n")
        userCount += 1

    file.close()

    return userCount


def db2Cleaner(str):
    str2 = ""
    for i in range(2, len(str)-3):
        str2 = str2 + str[i]
    return str2
