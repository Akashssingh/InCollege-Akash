import notifs
import profile
import guestControls
import user
import options
from notifs import newFriend, newJob
import sys
import login
import friend
from sqlite3.dbapi2 import OperationalError
import sqlite3
import courses
import notifs
import api
# Team Minnesota
# Developers: Siddhant Raman, Tyler Smith
# Epic 3

# API Calls
api.studentAccountsAPI()
api.jobsAPI()
api.trainingAPI()
api.myCollegeJobsAPI()
api.myCollegeProfilesAPI()
api.myCollegeUsersAPI()
api.appliedJobsAPI()
api.savedJobsAPI()
api.myCollegeTraining()

x = 0  # this is the option that the user picks from the main menu
loggedIn = 0  # keeps track of user status
lang = 1  # keeps track of the language
currentUser = "Temp"

print('Welcome to InCollege!')
print()

while x != 19:

    if loggedIn == 1:
        hold = notifs.notifyMessage(currentUser)
        print("The following jobs that you have applied to have been removed")
        print(notifs.beenRemoved(currentUser))
        print("You have: " + str(hold) + " messages")
    if loggedIn == 0:
        print('STUDENT SUCCESS STORY: Tom was a senior in college, about to graduate. He was about to enter the \'real world\' and his soft skills were lacking.')
        print('Tom wasn\'t sure how to build his network of connections. He decided to join InCollege and meet new people. With the help of ')
        print('InCollege, Tom was able to connect with other college students who had strong soft skills and learn from them. He was also able to')
        print('learn about new job listings in his dream location that led to a promised job following graduation!\n')
        print('Find out why you should join InCollege! To see more, type 0.')

        print()
        print('Account Services:')
        print('1. Login')
        print('2. Create an Account')
    else:
        print("Current User: ", currentUser)
        name = newFriend(currentUser)
        print("We have ", name, " in the system. Try adding them to your network!")
        jobs = newJob(currentUser)
        print("We have ", jobs, " job in the system. Try applying to your profile!")

        print('Your language is set to:')
        if lang == 1:
            print("English")
        else:
            print("Spanish")
        print('Account Services:')
        print('1. Login (You are logged in.)')
        print('1. Create an Account (You are logged in.)')

    print()

    print('The following services are offered:')
    if loggedIn == 0:
        print(
            '3. Search for Jobs (Service unavailable. Please log in to use this service.)')
    else:
        print('3. Search for Jobs')
    print('4. Search for People (Send Friend Request)')
    print('5. Learn New Skills')

    if loggedIn == 0:
        print('6. Connect with People (Service unavailable. Please log in to use this service.)')
    else:
        print('6. Connect with People')

    if loggedIn == 0:
        print('7. Post a Job (Service unavailable. Please log in to use this service.)')
    else:
        print('7. Post a Job')
    if loggedIn == 0:
        print('8. Help (Service unavailable. Please log in to use this service.)')
    else:
        print('8. Help')

    print("9. Useful Links")
    print("10. inCollege Links")

    if loggedIn == 0:
        print('11. Profiles (Service unavailable. Please log in to use this service.)')
    else:
        print('11. Profiles')

    if loggedIn == 1:
        print('12. Show My Network')

    if loggedIn == 1:
        if friend.pending_count(currentUser) > 0:
            print('13. Pending sent/received friend requests (You have (' +
                  str(friend.pending_count(currentUser)) + ') pending friend requests!!)')
        else:
            print('13. Pending sent/received friend requests')

    if loggedIn == 1:
        print('14. Applied Jobs')
    if loggedIn == 1:
        print('15. Saved Jobs')
    if loggedIn == 1:
        print('16. Delete a Job Posting')
    if loggedIn == 1:
        print('17. Messages')

    if loggedIn == 1:
        print('18. Plus')
    if loggedIn == 1:
        print('19. Incollege Learning')

    print()
    print('20. Exit')
    print()

    option = input("Please enter a main menu option or enter 20 to exit: ")
    print()

    if(option == '0'):
        x = 0
        print('Video is now playing.')
        print()
        # give user the option to return to the main menu
        print('Would you like to return to the main menu?')
        leave = input(
            'Please enter a "y" to return to the main menu or enter a "n" to exit the program: ')  # y or n

        if(leave == 'n'):
            sys.exit()  # will exit the program

        print()  # formatting

    if(option == '1'):
        temp = options.loginFunc(loggedIn)
        if temp != 1 and temp != 0:
            x = 0
            currentUser = temp
            show = options.showNotAppliedJobs(currentUser)
            if (show == 0):

                print("Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")
        if temp != 0:
            loggedIn = 1

    if (option == '2'):
        temp = options.signup(loggedIn)
        if temp != 1 and temp != 0:
            x = 0
            currentUser = temp
        if temp != 0:
            loggedIn = 1

    if (option == '3'):
        x = 3
        if (loggedIn == 1):
            if options.job_search(currentUser) == False:
                continue  # call job search function
            print()
        else:
            print("Log in to use this feature")

    if (option == '4'):
        if (loggedIn == 1):
            x = 4
            options.find_people(currentUser)
            print()
        else:
            print("Log in to use this feature")

    if (option == '5'):
        x = 5
        options.learn_skills()  # call learn function
        print()
    if(option == '6'):
        if (loggedIn == 0):
            print('You are not logged in.')
            print()
        else:
            x = 6
            options.connect_people(currentUser)  # Call Connect Function
        print()

    if (option == '7'):
        if(loggedIn == 0):
            print('You are not logged in.')
            print()
        else:
            x = 7
            title = input('Enter job title: ')
            description = input('Enter job description: ')
            employer = input('Enter name of employer: ')
            location = input('Enter job location: ')
            salary = input('Enter job salary: ')
            options.postJob(title, description, employer, location, salary)
            print()
    if(option == '8'):
        print()
        if(loggedIn == 0):
            print("You are not logged in.")
        else:
            x = 8
            firstName = input("Enter your first name: ")
            lastName = input("Enter last name: ")
            options.help_page(firstName, lastName)
    if(option == '9'):
        print()
        x = 9
        options.useful_link(loggedIn)
    if(option == '10'):
        x = 11
        options.imp_link(currentUser)
        if currentUser != "Temp":
            x = 10
            lang = guestControls.getLang(currentUser)
    if(option == '11'):
        if loggedIn == 1:
            x = 11
            options.profilePage(currentUser)
        else:
            print("Log in to use this feature")
    if(option == '12'):
        if loggedIn == 1:
            x = 12
            options.showMyNetwork(currentUser)
        else:
            print("Log in to use this feature")
    if(option == '13'):
        if loggedIn == 1:
            x = 13
            friend.pendingDisplay(currentUser)
        else:
            print("Log in to use this feature")
    if(option == '14'):
        if loggedIn == 1:
            x = 14
            applied = options.showAppliedJobs(currentUser)
            show = options.showNotAppliedJobs(currentUser)
        else:
            print("Log in to use this feature")
    if(option == '15'):
        if loggedIn == 1:
            x = 15
            print('Saved Jobs')
        else:
            print("Log in to use this feature")

    if(option == '16'):
        if loggedIn == 1:
            x = 16
            options.getJobPostings(currentUser)
        else:
            print("Log in to use this feature")

    if(option == '17'):
        if loggedIn == 1:
            x = 17
            options.seeInbox(currentUser)
        else:
            print("Log in to use this feature")
    if(option == '18'):
        print()
        if loggedIn != 1:
            print("Log in to use feature")
        else:
            options.plus(currentUser)
    if(option == '19'):
        print()
        if loggedIn != 1:
            print("Log in to use feature")
        else:
            options.selectCourse(currentUser)

    if (option == '20'):
        x = 19
        print('Have a great day!')
        # this is will exit the program
    if (int(option) < 0 or int(option) > 19):
        print("Please Make a Valid Choice\n")
