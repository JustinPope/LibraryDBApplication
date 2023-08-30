import sqlite3
import random
conn = sqlite3.connect('library.db')

choice = input("What would you like to do? (enter the corresponding number)\n"
               "1: Find an item in the library\n"
               "2: Borrow an item from the library\n"
               "3: Return a borrowed item\n"
               "4: Donate an item to the library\n"
               "5: Find an event in the library\n"
               "6: Register for an event in the libary\n"
               "7: Volunteer for the library\n"
               "8: Ask for help from a librarian\n"
               "Q: Quit program and close database\n\n")

cursor = conn.cursor()
print("\nOpened database successfully \n")

with conn:
    cur = conn.cursor()

    if choice == "1":
        findItem = input("What is the name of the item you are looking for?\n")
        myItemQuery = "SELECT * FROM catalogue WHERE itemName=:myItem"
        cur.execute(myItemQuery,{"myItem":findItem})
        item = cur.fetchall()
        if item:
            print("Here are the details for your item, " + findItem + ": \n")
        else:
            print("We do not have any item called " + findItem + "\n")
        for row in item:
            print("Item ID: " + str(row[0]) +  
                  "\nItem Type: " + row[2] + 
                  "\nItem Currently in Catalogue: " + row[3])
        print("\n")

    elif choice == "2":
        findItem = input("What is the item ID of the item you would like to borrow?\n")
        findUser = input("What is your customer ID?\n")
        myLoanQuery = "SELECT * FROM catalogue WHERE itemID=:myItem"
        newLoanQuery = "INSERT INTO loans(itemID, custID, loanDate, dueDate) VALUES (:myItemID, :myID, :curDate, :dueDate)"
        cur.execute(myLoanQuery, {"myItem":findItem})
        item = cur.fetchall()
        if item: 
            for row in item:
                loan = input("The item you requested is " + row[1] + ", would you like to borrow this item? (Y/N)\n")
                if loan == "Y":
                    currentDate = "2023-08-04"
                    itemDueDate = "2023-08-18"
                    cur.execute(newLoanQuery, {"myItemID":findItem, "myID":findUser, "curDate":currentDate, "dueDate":itemDueDate})
                    conn.commit()
                    print("You have successfully loaned " + row[1] + ", please return it before " + itemDueDate)
                else:
                    print("A new loan will not be created\n")
        else:
            print("Sorry, we do not have any item in our catalogue with that item ID\n")

    elif choice == "3": 
        findUser = input("What is your customer ID?\n")
        findItem = input("What is the item ID of the item you would like to return?\n")
        myReturnQuery = "SELECT * FROM loans WHERE custID=:myID AND itemID=:myItem"
        removeFromLoansQuery = "DELETE FROM loans WHERE custID=:myID AND itemID=:myItem"
        cur.execute(myReturnQuery, {"myID":findUser, "myItem":findItem})
        toReturn = cur.fetchall()
        if toReturn:
            for row in toReturn:
                response = input("Would you like to return the item with item ID " + str(row[1]) + "? (Y/N)\n")
                if response == "Y":
                    cur.execute(removeFromLoansQuery, {"myID":findUser, "myItem":findItem})
                    conn.commit()
                    print("You have successfully returned the item with item ID " + str(row[1]) + ", thank you!")
                else:
                    print("Your item will not be returned\n")
        else:
            print("You do not currently have this item loaned under your customer ID\n")
    
    elif choice == "4":
        toDonate = input("What is the name of the item you would like to donate?\n")
        generateItemID = random.randint(100000,999999)
        toDonateType = input("What is the type of the item you are donating? (eg. Print Book, CD, etc.)\n")
        curItem = "Y"
        donateQuery = "INSERT INTO catalogue(itemID, itemName, itemType, current) VALUES (:ID, :name, :type, :curYN)"
        cur.execute(donateQuery, {"ID":generateItemID, "name":toDonate, "type":toDonateType, "curYN":curItem})
        conn.commit()
        print("Your copy of " + toDonate + " has been donated, thank you!")


    elif choice == "5":
        findEvent = input("What is the name of the event you are looking for?\n")
        myEventQuery = "SELECT * FROM events JOIN bookedin ON events.eventID == bookedin.eventID WHERE eventName=:myEvent"
        cur.execute(myEventQuery,{"myEvent":findEvent})
        event = cur.fetchall()
        if event:
            print("Here are the details for your event, " + findEvent + ": \n")
        else: 
            print("We do not have any event scheduled called " + findEvent + "\n")
        for row in event:
            print("Event ID: " + str(row[0]) +  
                  "\nEvent Date: " + str(row[2]) + 
                  "\nNum Attendees: " + str(row[3]) + 
                  "\nIntended Audience: " + row[4] + 
                  "\nRoom Number: " + str(row[6]))
        print("\n")

    elif choice == "6":
        #Register for an event in the library
        findEventToRegister = input("What is the event you would like to register for?\n")
        myEventToRegisterQuery = "SELECT * FROM events JOIN bookedin ON events.eventID == bookedin.eventID JOIN rooms ON rooms.roomNumber == bookedin.roomNumber WHERE eventName=:myEvent"
        cur.execute(myEventToRegisterQuery,{"myEvent":findEventToRegister})
        event = cur.fetchall()
        if event:
            print("An event has been identified with the specified name, checking if there is an available slot")
        else:
            print("The event you have specified does not exist")
        for row in event:
            if (row[3] + 1) <= row[8]:
                print("There is an available slot for you to attend the event and you have now been registered. Please enjoy the " + str(row[1]) +"!\n")
                updateAttendeesQuery = "UPDATE events SET numAttendees = numAttendees + 1 WHERE eventName =:myEvent"
                cur.execute(updateAttendeesQuery,{"myEvent":findEventToRegister})
                conn.commit()
            else:
                print("The event has reached its capacity of " + str(row[8]) + "\n")

    elif choice =="7":
        #Adding a new employee
        print("Thank you for choosing to volunteer! You will be registered as an employee within our database.")
        findEmployeesFirstName = input("What is your first name?\n")
        findEmployeesLastName = input("What is your last name?\n")
        myEmployeeQuery = "SELECT * FROM employee WHERE employeeID=:myEvent"
        myEmployeeCreateQuery = "INSERT INTO employee(employeeID, firstName, lastName, salary) VALUES (:myEmployeeID, :myFirstName, :myLastName, :mySalary)"
        while True:
            generateEmployeeID = random.randint(1000,9999)
            cur.execute(myEmployeeQuery,{"myEvent":generateEmployeeID})
            event = cur.fetchall()
            if not event:
                cur.execute(myEmployeeCreateQuery, {"myEmployeeID":generateEmployeeID, "myFirstName":findEmployeesFirstName, "myLastName":findEmployeesLastName, "mySalary":0})
                conn.commit()
                print("You have been registered as a volunteer within our database with employeeID: " + str(generateEmployeeID) +"\n")
                break


    elif choice == "8":
        print("Please contact us at 604-555-1234 to reach a librarian, or email us at libraryhelp@reallibrary.com\n")
        
    elif choice == "Q":
        print("Closing database...\n")

    else: 
        print("Invalid choice\n")

if conn:
    conn.close()
    print("Closed database successfully")
