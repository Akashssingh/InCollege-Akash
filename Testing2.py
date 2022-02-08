# Testing File
# Team Minnesota

import pytest
import main
import profile
import options
import guestControls
import login
import user
import notifs
import friend
import courses
import api
import sqlite3
import builtins
import random

# Creating Database File
conn = sqlite3.connect('users.db')
# Creating SQLite Cursor Global Variable
cursor = conn.cursor()


def test_started():
    result = login.deleteRecords()
    if result:
        assert False
    else:
        assert True

# Epic 8 -------------------------------------------------------------------------


def test_remind_finishProfile():
    login.deleteRecords()

    values = [1, 2]

    def mock_i(s):
        return values.pop(0)

    login.input = mock_i

    login.insertUser("Jane", "Doe", "jane", "P@ssword1")
    conn.commit()

    result = profile.checkDefault('jane')

    if result:
        assert True
    else:
        assert False

# def test_notif_messages():


def test_job_notifs():

    cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', ("3", "Jane",
                                                                 "Doe", "title", "description", "employer", "location", "salary"))
    conn.commit()

    cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', ("4", "Jane",
                                                                 "Doe", "title", "description", "employer", "location", "salary"))
    conn.commit()

    result = notifs.howManyJobs('jane')

    if result == 1:
        assert True
    else:
        assert False

# def test_job_deletionNotifs():


# Chase Rogalski
def test_showNotAppliedJobs():
    numberofJobs = 10
    # Adding # of New Jobs to Database
    firstName = "test_firstName"
    lastName = "test_lastName"
    description = "test_description"
    employer = "test_employer"
    location = "test_location"
    salary = "test_salary"
    for i in range(1, numberofJobs + 1):
        title = "testJob" + str(i)
        tableID = "100" + str(i)
        cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', (tableID, firstName,
                                                                     lastName, title, description, employer, location, salary))
    # Picking Random Number of Applied Jobs
    numberofApplied = random.randint(1, numberofJobs - 1)
    # Creating List of Applied Job Titles
    appliedJobs = []
    for i in range(1, numberofApplied + 1):
        jobTitle = "testJob" + str(i)
        appliedJobs.append(jobTitle)
    # Finding Difference from Total Jobs and Number of Apllied Jobs
    print('Number of Applied Jobs Tested: ', numberofApplied)
    diff = 10 - numberofApplied

    # Joining List into comma-separated string
    appliedJobsString = ",".join(appliedJobs)
    # Adding New User to SQL Database
    firstName = "test"
    lastName = "showNotAppliedJobs"
    username = "usershowNotAppliedJobs"
    password = "Password5%"
    emails = 1
    ads = 1
    sms = 1
    lang = 1
    empty = ''
    membership = 1
    friend = "friend2,"
    cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (firstName, lastName, username, password,
                                                                                              emails, ads, sms, lang, empty, empty, empty, empty, empty, empty, empty, empty, empty, appliedJobsString, empty, membership, empty, empty))
    conn.commit()

    # Calling Function
    result = options.showNotAppliedJobs("usershowNotAppliedJobs")

    # Removing Jobs
    for i in range(1, numberofJobs + 1):
        jobTitle = "testJob" + str(i)
        cursor.execute('DELETE FROM jobs WHERE title=?', (jobTitle,))
        conn.commit()
    # Removing User
        cursor.execute('DELETE FROM users WHERE username=?', (username,))
        conn.commit()
    #  If Function Matches Job Difference, Assert True otherwise Assert False
    print("Result: ", result)
    print("Actual Difference: ", diff)

    # Testing if Student hasn't applied for a Job
    cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (firstName, lastName, "test_NoApply", password,
                                                                                              emails, ads, sms, lang, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, membership, empty, empty))
    conn.commit()
    nonAppliedJobs = options.showNotAppliedJobs("test_NoApply")

    # Removing User
    cursor.execute('DELETE FROM users WHERE username=?', ("test_NoApply",))
    conn.commit()

    assert result == diff


# Chase Rogalsk
def test_newFriend():
    # Inserting UserA
    userAfirstName = "test"
    userAlastName = "newFried"
    userAusername = "userA"
    userApassword = "Password5%"
    emails = 1
    ads = 1
    sms = 1
    lang = 1
    empty = ''
    membership = 1
    cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (userAfirstName, userAlastName, userAusername,
                                                                                              userApassword, emails, ads, sms, lang, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, membership, empty, empty))
    conn.commit()

    # Inserting UserB
    userBfirstName = "test"
    userBlastName = "newFried"
    userBusername = "userB"
    userBpassword = "Password5%"
    cursor.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (userBfirstName, userBlastName, userBusername,
                                                                                              userBpassword, emails, ads, sms, lang, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, empty, membership, empty, empty))
    conn.commit()
    friendName = notifs.newFriend(userAusername)

    # Removing Users
    cursor.execute('DELETE FROM users WHERE username=?', (userAusername,))
    conn.commit()
    cursor.execute('DELETE FROM users WHERE username=?', (userBusername,))
    conn.commit()
    print("userBusername: ", userBusername)
    print("friendName: ", friendName[0])

    assert userBusername == friendName[0]


# Epic 9 -------------------------------------------------------------------------


def testTraining():  # good
    input_values = ['5']

    def mock_input(s):
        return input_values.pop(0)

    options.input = mock_input
    result = options.training()

    if result:
        assert False
    else:
        assert True


def test_trainAndEdu():  # good
    input_values = ['1', '2', '3', '4', '5']

    def mock_input(s):
        return input_values.pop(0)

    options.input = mock_input
    result = options.trainAndEdu()

    if result:
        assert False
    else:
        assert True


def test_ITHelp_Security():  # good
    result1 = options.itHelp()
    result2 = options.secure()

    if result1 and result2:
        assert True
    else:
        assert False


def test_BusStrat():  # good
    input_values = [1]

    def mock_input(s):
        return input_values.pop(0)

    options.input = mock_input
    result = options.BusAnalStrat()

    if not result:
        assert True
    else:
        assert False


def test_havetook():
    login.insertUser("Jane", "Doe", "jane", "P@ssword1")
    conn.commit()

    result = courses.haveTook(1, "jane")

    if result:
        assert False
    else:
        assert True


def test_takecourse():
    login.insertUser("Jane", "Doe", "jane", "P@ssword1")
    conn.commit()

    result = courses.takeCourse(3, "jane")

    if result:
        assert False
    else:
        assert True
# Epic 10


def test_userop():
    val = api.myCollegeJobsAPI()
    if (val >= 0):
        assert True
    else:
        assert False


def test_usertrain():
    val = api.myCollegeTraining()
    if (val >= 0):
        assert True
    else:
        assert False


def test_appliedjob():
    val = api.appliedJobsAPI()
    if (val >= 0):
        assert True
    else:
        assert False


def test_savedjob():
    val = api.savedJobsAPI()
    if (val >= 0):
        assert True
    else:
        assert False



#Tyler Smith Epic 10

def test_studentAPI():
   #Wipe the db to a fresh state
    login.deleteRecords()
    username = "jane"
    password = "P@ssword1"

    #Create new entry
    #login.insertUserTesting("Jane", "Doe", "jane", "P@ssword1")
    
    #Creates a file
    file = open('studentAccounts.txt', 'a')
    file.write("jane\n")
    file.write("P@ssword1\n")
    file.write("=====\n")
    file.close

    #Check that file opened
    x = api.studentAccountsAPI()
    if x == -1:
        assert False

    #Checks that file's data is valid    
    cursor.execute('SELECT firstName FROM users WHERE username=? AND password=?', (username, password,))
    dataCheck = cursor.fetchone()
    dataCheckstr = friend.db2Cleaner(str(dataCheck))
    
    if dataCheckstr == "":
        assert True
    else:
        assert False

    


def test_newJobsAPI():

    title = "teacher"
    description = "test"
    employer = "test"
    location = "test"
    salary = "test"

    #Create new entry
    options.postJobTest(title, description, employer, location, salary)
    
    #Creates a file
    file = open('newJobs.txt', 'a')
    file.write("teacher\ntest1\ntest2\n")
    file.write("&&&\n")
    file.write("test\ntest\ntest\n====\n")
    file.close

    #Check that file opened
    x = api.jobsAPI()
    if x == -1:
        assert False

    #Checks that file's data is valid    
    cursor.execute('SELECT title FROM jobs WHERE description=? AND salary=?', (description, salary,))
    dataCheck = cursor.fetchone()
    dataCheckstr = friend.db2Cleaner(str(dataCheck))
    
    if dataCheckstr == "teacher":
        assert True
    else:
        assert False


def test_TrainingAPI():    
    #Creates a file
    file = open('newTraining.txt', 'a')
    
    file.close

    #Check that file opened
    x = api.trainingAPI()
    if x == -1:
        assert False
    
    if x == len(options.trainingList):
        assert True
    else:
        assert False


def test_myCollegeJobsAPI():
    x = api.myCollegeJobsAPI

    if x == 1:
        assert False
    else:
        assert True

def test_myCollegeProfilesAPI():
    x = api.myCollegeProfilesAPI

    if x == 1:
        assert False
    else:
        assert True