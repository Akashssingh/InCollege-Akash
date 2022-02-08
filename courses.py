import sqlite3

# Creating Database File
conn = sqlite3.connect('users.db')
# Creating SQLite Cursor Global Variable
cursor = conn.cursor()


def loadCourses():
    x = []

    print("The following courses are offered:")
    print("1. How to use In College learning")
    print("2. Train the trainer")
    print("3. Gamification of learning")
    print("4. Understanding the Architectural Design Process")
    print("5. Project Management Simplified")
    print()

# Returns a list of the courses that a given user has already taken


def alreadyTaken(currentUser):
    x = []
    cursor.execute(
        'SELECT completedCourses FROM users WHERE username=?', (currentUser,))
    cursorData = cursor.fetchone()
    x = cursorData[0].split(',')
    return x


def haveTook(classID, currentUser):
    x = alreadyTaken(currentUser)
    for i in range(0, len(x)):
        if classID == str(x[i]):
            return True
    return False


def takeCourse(userIn, currentUser, inputTest=0):
    x = alreadyTaken(currentUser)
    reTake = ""
    result = ""
    if inputTest != 0:  # this condition is used for testing purposes so that testers don't need to provide input
        print()
    elif haveTook(userIn, currentUser):
        print("You have already taken this course, would you like to retake it? (y/n)")
        retake = input()
        while (reTake != "y" and reTake != "n"):
            print("Bad input, try again")
            reTake = input()
    if reTake != "n":
        print("You have now completed this training")
        # Update the db here
        for i in range(0, len(x)):
            result = result + x[i] + ","
        cursor.execute(
            "UPDATE users SET completedCourses=? WHERE username=?", (result, currentUser,))
        conn.commit()
    else:
        print("Course cancled")
    return result
