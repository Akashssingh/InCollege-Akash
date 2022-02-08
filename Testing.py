#Testing File
#Team Minnesota

import pytest
import main
import profile
import options
import guestControls
import login
import user
import friend
import sqlite3
import builtins

# Creating Database File
conn = sqlite3.connect('users.db')
# Creating SQLite Cursor Global Variable
cursor = conn.cursor()
# # Creating User Table
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
#             (firstName text, lastName text, username text, password text, emailStatus int, adStatus int, smsStatus int, language int, title text, major text, university text, information text, experiance text, education text, pendingReqs text, pendingSentReqs text, friends text, appliedJobs text, savedJobs text)''')

# # Creating Job Table
# cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
#             (id text, postedBy_firstname text, postedBy_lastName text, title text, description text, employer text, location text, salary text)''')

# # Creating Application Table
# cursor.execute('''CREATE TABLE IF NOT EXISTS apps
#             (job_id text, applied_username text, gradDate text, startDate text, paragraph text)''')

# # Creating Messages Table
# cursor.execute('''CREATE TABLE IF NOT EXISTS messages
#             (to_user text, from_user text, message text)''')

def test_started():
    result = login.deleteRecords()
    if result:
        assert False
    else:
        assert True
   

#Epic 1 -----------------------------------------------------------------------------------

#Setups an initial value for testing purposes
def test_setup():
    input_values = [1, 2]
    
    def mock_input(s):
        return input_values.pop(0)
    
    login.input = mock_input  
    result = login.insertUser("", "", "user1", "Password1!")

#This test cases uses a known good username
def test_userNameClean():
    
    result = login.usernameCheck("user2")
    if(result):
        assert True
    else:
        assert False
        
#This test cases uses a known bad username
def test_userNameDirty():
    
    result = login.usernameCheck("user1")
    if(result):
        assert False
    else:
        assert True
        
#Tests a knows good password
def test_pwClean():
    result = login.passwordCheck("Password1!")
    if(result):
        assert True
    else:
        assert False
        
#Tests a known bad password
def test_pwDirty():
    result1 = login.passwordCheck("Password1")
    result2 = login.passwordCheck("Password")
    result3 = login.passwordCheck("password")
    result4 = login.passwordCheck("Password!")
    result5 = login.passwordCheck("password1")
    result6 = login.passwordCheck("password!")
    if(result1 and result2 and result3 and result4 and result5 and result6):
        assert False
    else:
        assert True

#tests adding a known not present user
def test_addUserClean():
    input_values = [1, 2]
    
    def mock_input(s):
        return input_values.pop(0)
    
    login.input = mock_input 
    result = login.insertUser("", "", "User3","P@ssword1")
    if result:
        assert True
    else:
        assert False
        
#tests adding a known present user
def test_addUserDirty():
    input_values = [1, 2]
    
    def mock_input(s):
        return input_values.pop(0)
    
    login.input = mock_input 
    result = login.insertUser("", "", "User3","P@ssword1")
    if result:
        assert False
    else:
        assert True

#fills the db and then tests if an additional member past the allowed 10 can be added
def test_isTooMany():
    login.deleteRecords()
    un = "User"
    un2 = ""
    pw = "P@ssword1"
    
    input_values = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
    
    def mock_input(s):
        return input_values.pop(0)
    
    login.input = mock_input 

    for i in range(0,10):
        un2 = un + str(i)
        temp = login.insertUser("Test","Test",un2, pw)

    temp = login.insertUser("Test","Test","User11","P@ssword1")
    if temp:
        assert False
    else:
        assert True
        
#tests logging into a known good account
def test_loginClean():
    input_values = [1, 2]
    
    def mock_input(s):
        return input_values.pop(0)
    
    login.input = mock_input 
    result = login.loginUser("User4", "P@ssword1")
    if result:
        assert True
    else:
        assert False
        
#tests logging in with both a bad username and password
def test_loginDirty():

    input_values = [1, 2, 1, 2]
    
    def mock_input(s):
        return input_values.pop(0)
    
    login.input = mock_input 
    result1 = login.loginUser("User4", "P@ssword")
    result2 = login.loginUser("Use4", "P@ssword1")
    if result1 or result2:
        assert False
    else:
        assert True
        
 #Epic 2 -----------------------------------------------------------------------------------
# updated for Epic 6 which increased job listings to 10
def test_postJob():
    title = "Python Tester"
    description = "Testing Python Files"
    employer = "USF"
    location = "Florida"
    salary = "80000"
    input_values = ['Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe', 'Jane', 'Doe']

    def mock_input(s):
        return input_values.pop(0)
    
    options.input = mock_input
    
    result1 = options.postJob(title, description, employer, location, salary)
    result2 = options.postJob(title, description, employer, location, salary)
    result3 = options.postJob(title, description, employer, location, salary)
    result4 = options.postJob(title, description, employer, location, salary)
    result5 = options.postJob(title, description, employer, location, salary)
    result6 = options.postJob(title, description, employer, location, salary)
    result7 = options.postJob(title, description, employer, location, salary)
    result8 = options.postJob(title, description, employer, location, salary)
    result9 = options.postJob(title, description, employer, location, salary)
    result10 = options.postJob(title, description, employer, location, salary)
    result11 = options.postJob(title, description, employer, location, salary)

    if(result1 and result2 and result3 and result4 and result5 and result6 and result7 and result8 and result9 and result10 and result11):
        assert True
    else:
        assert False
        

#tests help page with a known unique existing person and adding another person with unique name
def test_help_page():
    login.deleteRecords()
    #creates the user so we have have an existing unique user.
    login.insertUser("Firstname", "Lastname", "User7", "Password1!")
    result = options.help_page("Firstname", "Lastname")
    result2 = options.help_page("FirstName", "LastName")
    if result and not result2:
        assert True
    else:
        assert False

def test_connect_people():
    result = options.connect_people("UserA")
    if result:
        assert False
    else:
        assert True
        
#Epic 3 -----------------------------------------------------------------------------------
def test_importantLinks():
    login.deleteRecords()

    input_values = [1, 2, 3, 4, 6, 7, 8, 10]
    
    def mock_input(s):
        return input_values.pop(0)
    
    options.input = mock_input
    result = options.imp_link(True)

    if result:
        assert False
    else:
        assert True

def test_languageOption():
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i

    login.insertUser('test', 'user', 'tester', 'Test123!')
    
    input_values = [9, 10]
    
    def mock_input(s):
        return input_values.pop(0)
    
    options.input = mock_input
    result = options.imp_link('tester')

    if result:
        assert False
    else:
        assert True 

def test_guestControl():
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser('test1', 'user1', 'tester1', 'Test123!')
    conn.commit()
    input_values = [1, 2, 3, 4, 5]
    
    def mock_input(s):
        return input_values.pop(0)

    guestControls.input = mock_input
    result = guestControls.guestOption('tester1')

    if result:
        assert False
    else:
        assert True

def test_usefulLinks():
    input_values = [1, 1, 2, 3, 4, 5, 6, 7, 8, 2, 3, 4, 5]

    def mock_input(s):
        return input_values.pop(0)

    options.input = mock_input
    result = options.useful_link(1)

    if result:
        assert False
    else:
        assert True
        
#Epic 4 -----------------------------------------------------------------------------------

#testing creation of title for profile
def testing_profileTitle():
    login.deleteRecords()
    
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser('test', 'user', 'tester1', 'Test123!')

    input_values = ['Tester Student 1']
    
    def mock_input(s):
        return input_values.pop(0)
    
    profile.input = mock_input
    result = profile.editTitle('tester1')

    if result:
        assert True
    else:
        assert False

#testing titlecase for major and university
def testing_titlecase():
    result1 = profile.sanatize('coMPUTER sCIENCe')
    result2 = profile.sanatize('uniVERsity Of sOUTH FLorida')
    if result1 == 'Computer Science' and result2 == 'University Of South Florida':
        assert True
    else:
        assert False
        
#testing creation of text for about section
def testing_aboutSection():
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser('test', 'user', 'tester2', 'Test123!')


    input_values = ['This is test about.']
    
    def mock_input(s):
        return input_values.pop(0)
    
    profile.input = mock_input
    result = profile.editInfo('tester2')

    if result:
        assert True
    else:
        assert False

#testing entering job information on profile, up to three jobs
def testing_experience():
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser('test', 'user', 'tester3', 'Test123!')

    input_values = ['This is job experience 1.', 'This is job experience 2.', 'This is job experience 3.']
    
    def mock_input(s):
        return input_values.pop(0)
    
    profile.input = mock_input
    result = profile.editExp('tester3')

    if result:
        assert True
    else:
        assert False

#testing creation of education information on profile
def testing_education():
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    login.insertUser('test', 'user', 'tester4', 'Test123!')

    input_values = ['University of South Florida', 'BS', '2017-2021']
    
    def mock_input(s):
        return input_values.pop(0)
    
    profile.input = mock_input
    result = profile.editEdu('tester4')

    if result:
        assert True
    else:
        assert False
    
def test_send_friend():
    values = [1, 2, 1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    login.insertUser('John', 'Doe', 'John', 'Test123!')
    conn.commit()
    login.insertUser('Serena', 'Rampersad', 'serena', 'Serena123!')
    conn.commit()
    
    input_values = ['serena', 2]
    
    def mock_inputs(s):
        return input_values.pop(0)
    
    friend.input = mock_inputs
    
    result=friend.send_friendReq('John')
    if result:
        assert False
    else:
        assert True

def test_receive():
    values = [1, 2, 1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    login.insertUser('John', 'Doe', 'John', 'Test123!')
    conn.commit()
    login.insertUser('Serena', 'Rampersad', 'serena', 'Serena123!')
    conn.commit()
    
    input_values = ['serena', 2]
    
    def mock_inputs(s):
        return input_values.pop(0)
    
    friend.input = mock_inputs
    friend.send_friendReq('John')
    result=friend.accept_friend_req('serena', 'John')
    if result:
        assert True
    else:
        assert False

#Epic 5 -----------------------------------------------------------------------------------------

def test_list():
    login.deleteRecords()
    
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")
    cursor.execute('SELECT friends FROM users WHERE username=?', ("UserA",))
    u2data = cursor.fetchall()
    strUdata = profile.dbCleaner(str(u2data))
    if strUdata == "":
        assert True
    else:
        assert False

def test_remove():
    login.deleteRecords()
    
    values = [1, 2, 1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")
    conn.commit()
    login.insertUser("UserB", "UserB", "UserB", "P@ssword1")
    conn.commit()
    updateStr ="UserB"
    currentUser = "UserA"

    cursor.execute('UPDATE users SET friends=? WHERE username=?', (updateStr, currentUser,))
    conn.commit()
    updateStr ="UserA"
    currentUser = "UserB"
    cursor.execute('UPDATE users SET friends=? WHERE username=?', (updateStr, currentUser,))
    conn.commit()

    options.removeFriend("UserA","UserB")
    
    cursor.execute('SELECT friends FROM users WHERE username=?', ("UserB",))
    u2data = cursor.fetchall()
    strUdata = profile.dbCleaner(str(u2data))
    print(strUdata)
    if strUdata != "UserA":
        assert True
    else:
        assert False
        
def test_network():
    login.deleteRecords()
    
    values = [1, 2, 1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")
    conn.commit()
    login.insertUser("UserB", "UserB", "UserB", "P@ssword1")
    conn.commit()
    
    input_value=['UserB']
    
    def mock_input(s):
        return input_value.pop(0)
    friend.input = mock_input
    
    friend.send_friendReq("UserA") 
    friend.accept_friend_req("UserB", "UserA")
    
    cursor.execute('SELECT friends FROM users WHERE username=?', ("UserA",))
    u2data = cursor.fetchall()
    strUdata = profile.dbCleaner(str(u2data))
    print()
    print(strUdata)
    if strUdata == ",UserB,":
        assert True
    else:
        assert False
        
def test_search():
    login.deleteRecords()
    
    values = [1, 2, 1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")
    conn.commit()
    login.insertUser("UserB", "UserB", "UserB", "P@ssword1")
    conn.commit()

    input_value = ['4']

    def mock_input(s):
        return input_value.pop(0)
        
    friend.input = mock_input
    result = friend.search_people("UserA")

    if result:
        assert False
    else:
        assert True


def test_display():
    login.deleteRecords()
    
    values = [1, 2, 1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")
    conn.commit()
    login.insertUser("UserB", "UserB", "UserB", "P@ssword1")
    conn.commit()

    input_value = ['3']

    def mock_input(s):
        return input_value.pop(0)
        
    friend.input = mock_input
    result = friend.pendingDisplay("UserA")

    if result:
        assert False
    else:
        assert True

#Epic 6 -------------------------------------------------------------------------------------------------
def test_ReApply():
    login.deleteRecords()
    
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")    

    cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', ("3","firstName",
                                                                   "lastName", "title", "description", "employer", "location", "salary"))
    conn.commit()
    cursor.execute('SELECT id FROM jobs')
    data = cursor.fetchone()
    temp = data[0]
    print('TEMP ' + temp)
    if temp == "3":
        assert True
    else:
        assert False

def test_BuildList():
    login.deleteRecords()
    
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")    

    cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', ("3","firstName",
                                                                   "lastName", "title", "description", "employer", "location", "salary"))
    conn.commit()

    cursor.execute('SELECT id FROM jobs')
    data = cursor.fetchone()
    temp = data[0]

    if temp:
        assert True
    else:
        assert False


def test_del_job():
    login.deleteRecords()
    
    values = [1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")

    cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', ("3", "firstName",
                                                                 "lastName", "title", "description", "employer",
                                                                 "location", "salary"))
    conn.commit()
    cursor.execute('SELECT id FROM jobs')
    data = cursor.fetchone()
    temp = data[0]

    result = options.removeJob(temp)

    if result:
        assert False
    else:
        assert True

def test_searchJob():
    login.deleteRecords()
    
    values = [1, 2, 1, 2]
    
    def mock_i(s):
        return values.pop(0)
    
    login.input = mock_i
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")

    cursor.execute('INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?)', ("3", "firstName",
                                                                 "lastName", "title", "description", "employer",
                                                                 "location", "salary"))
    conn.commit()
    login.insertUser("UserB", "UserB", "UserB", "P@ssword1")
    conn.commit()
    input_values = [0]
    
    def mock_input(s):
        return input_values.pop(0)
    
    options.input = mock_input
    
    result = options.job_search("UserB")

    if result:
        assert False
    else:
        assert True

# Epic 7 -------------------------------------------------------------------------

#tests the plus feature
def test_Plus():
    login.deleteRecords()
    input_values = [1, 1]
    def mock_input(s):
        return input_values.pop(0)
    login.input = mock_input
    login.insertUser("UserA", "UserA", "UserA", "P@ssword1")
    conn.commit()
    login.insertUser("UserB", "UserB", "UserB", "P@ssword1")
    conn.commit()
    
    input_v = [1, 2, 3, 3, 3, 1, 2, 3, 3, 3]
    def mock_i(s):
        return input_v.pop(0)
    options.input = mock_i
    
    result = options.Plus("UserA")
    result2 = options.Plus("UserB")

    if result and result2:
        assert False
    else:
        assert True
        