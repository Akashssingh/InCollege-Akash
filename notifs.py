import sqlite3
import friend
import profile
# Creating Database File
conn = sqlite3.connect('users.db')
# Creating SQLite Cursor Global Variable
cursor = conn.cursor()

# Returns the number of jobs a student has applied to


def howManyJobs(currentUser):
    cursor.execute(
        'SELECT appliedJobs FROM users WHERE username=?', (currentUser,))
    cursorData = cursor.fetchone()
    # Splits jobs into List
    listOfJobs = cursorData[0].split(',')
    return len(listOfJobs)


#Returns a list of all the jobs that have been removed that the user has applied to
def beenRemoved(currentUser):
    cursor.execute('SELECT appliedJobs FROM users WHERE username=?', (currentUser,))
    cursorData = cursor.fetchone()
    # Splits jobs into List
    alpha = cursorData[0].split(',')
    #print(alpha)
    cursor.execute('SELECT masterList FROM users WHERE username=?', (currentUser,))
    cursorData = cursor.fetchone()
    bravo = cursorData[0].split(',')    
    
    return bravo[0]

#Returns a list of all the jobs that have been removed that the user has applied to
def updateMaster(jobID):
    #Get the name of the removed job
    cursor.execute('SELECT title FROM jobs WHERE id=?', (jobID,))
    cursorData = cursor.fetchone()
    jobName = str(cursorData)
    jobName = friend.db2Cleaner(jobName) #changed from dbCleaner2 to db2Cleaner
    
    #Add to every user who's applied to the job
    cursor.execute('SELECT appliedJobs FROM users')
    cursorData = list(cursor.fetchall())
    appliedList = []
    for i in range(0, len(cursorData)):
        appliedList.append(str(cursorData[i]))
    
    subStringList = [] 
    jobString = str(jobID)
    #Gives a list of the index of all users who applied to the removed job
    for i in range(0, len(appliedList)):
        x = appliedList[i].find(jobString)
        if x == -1:
            pass
        #elif appliedList[i][x-1] != ",":
            #print("Secondary check")
            #break
        else:
            subStringList.append(i)
    #Build list of all usernames by index
    cursor.execute('SELECT username FROM users')
    cursorData = cursor.fetchall()
    userNameList= []
    for i in range(0, len(cursorData)):
        userNameList.append(str(cursorData[i]))
    #update master list to have the removed jobs for each user based on index
    for i in range(0, len(subStringList)): 
        hold = friend.db2Cleaner(userNameList[subStringList[i]]) #changed from dbCleaner2 to db2Cleaner
        
        cursor.execute('SELECT masterList FROM users WHERE username=?', (hold,))
        cursorData = cursor.fetchone()
        masterList = str(cursorData)
        masterList = friend.db2Cleaner(masterList) #changed from dbCleaner2 to db2Cleaner
        
        masterList = masterList + "," + jobName  
        cursor.execute('UPDATE users SET masterList=? WHERE username=?',(masterList,hold,))
        conn.commit()



#Updates the job list for a user
def updateJobList(currentUser):
    cursor.execute('SELECT id FROM jobs')
    cursorData = cursor.fetchall()
    # Splits jobs into List
    alpha = []
    hold = cursorData
    for i in range(0,len(hold)):
        alpha.append(hold[i])     
    bravo = []
    for i in range(0, len(alpha)):
        bravo.append(profile.dbCleaner2(str(alpha[i])))
    cursor.execute('SELECT masterList FROM users WHERE username=?', (currentUser,))
    cursorData = cursor.fetchone()
    master = cursorData[0].split(',')
    #print(master[0])
    comp = list(set(bravo).intersection(set(master)))
    #print(comp)
    clean = []
    for i in range (0, len(comp)):
        clean.append(str(comp[i]))
    clean = ",".join(clean)
    cursor.execute("UPDATE users SET appliedJobs=? WHERE username=?",(clean,currentUser,))
    conn.commit()

#tells the user if they have a message
def notifyMessage(currentUser):
    cursor.execute('SELECT * FROM messages WHERE to_user=?', (currentUser,))
    messages = cursor.fetchall()
    count = len(messages)
    return count



def newFriend(currentUser):
    cursor.execute(
        'SELECT username FROM users')
    cursorData = cursor.fetchone()
    if cursorData is None:
        return 0
    alpha = cursorData[0].split(',')
    cursor.execute(
        'SELECT friends FROM users WHERE username=?', (currentUser,))
    cursorData = cursor.fetchone()
    bravo = cursorData[0].split(',')

    comp = list(set(alpha).difference(set(bravo)))

    if len(comp) == 0:
        return "None"
    return comp


def newJob(currentUser):
    print()
    cursor.execute(
        'SELECT appliedJobs FROM users WHERE username=?', (currentUser,))
    cursorData = cursor.fetchone()
    if cursorData is None:
        return 0
    # Splits jobs into List
    alpha = cursorData[0].split(',')
    cursor.execute(
        'SELECT title FROM jobs')
    cursorData = cursor.fetchone()
    bravo = cursorData[0].split(',')

    comp = list(set(alpha).difference(set(bravo)))
    if len(comp) == 0:
        return 0
    return comp
