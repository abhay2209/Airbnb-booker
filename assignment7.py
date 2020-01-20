import pyodbc
import sys
import datetime

conn = pyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=cypress.csil.sfu.ca;Trusted_Connection=yes; autocommit=True')

cur = conn.cursor()

choose_option=3
while choose_option!='0':
    print('Press 1 if you want to search Listings and book too\n')
    print('Press 2 if you want to review a listing\n')
    print('Press 0 if you want to end')
    choose_option=input("Your option\n")
    if choose_option=='1':
        print('We start from searching for a listing')
        minimum_price = int(input('What is the minimum price you are looking for? \n')or "0")
        maximum_price =int(input('what is the maximum price you want?\n') or "2000")
        start_date =input('Whats is teh start date? YYYY-MM-DD\n')
        end_date=input('What is the end date? YYYY-MM-DD \n')
        start=datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end=datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        number_of_bedrooms=int(input('How many bedrooms are you looking for?')or"1")
        SQLquery="""SELECT DISTINCT id,name,number_of_bedrooms,LEFT(description,25),MAX(price) FROM Listings,Calendar WHERE number_of_bedrooms = ? AND id=listing_id AND (date >= ? AND date <= ? )AND  id NOT IN  (SELECT listing_id FROM Calendar WHERE (date >= ? AND date <= ?) AND (price > ? OR price < ? OR available = 0)) GROUP BY id,name,LEFT(description,25),number_of_bedrooms ;"""

        cur.execute(SQLquery,number_of_bedrooms,start,end,start,end,maximum_price,minimum_price)
        records=cur.fetchall()
        while len(records)==0:
            print("\n No listing for requested filter,Please try again \n")
            minimum_price = int(input('What is the minimum price you are looking for? \n')or "0")
            maximum_price =int(input('what is the maximum price you want?\n') or "2000")
            start_date =input('Whats is teh start date? YYYY-MM-DD\n')
            end_date=input('What is the end date? YYYY-MM-DD \n')
            start=datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end=datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            number_of_bedrooms=int(input('How many bedrooms are you looking for?')or"1")
            SQLquery="""SELECT DISTINCT id,name,number_of_bedrooms,LEFT(description,25),MAX(price) FROM Listings,Calendar WHERE number_of_bedrooms>= ? AND id=listing_id AND (date >= ? AND date <= ? )AND  id NOT IN  (SELECT listing_id FROM Calendar WHERE (date >= ? AND date <= ?) AND (price > ? OR price < ? OR available = 0)) GROUP BY id,name,LEFT(description,25),number_of_bedrooms ;"""

            cur.execute(SQLquery,number_of_bedrooms,start,end,start,end,maximum_price,minimum_price)
            records=cur.fetchall()
        
        for row in records:
            print("id= ", row[0])
            print("Name= ", row[1])
            print("Number of bedrooms are= ",row[2])
            print("description= ",row[3])
            print("price=",row[4])
        print('\n A booking will be made for your selected start and end date for which you searched listings for. \n')
        print('Listing will be available again for the next user on the END DATE of the previous user\n')
        listing_to_book =  int(input(' Please enter listings you want to book\n'))
        user_name= (input('Enter the name for whome booking has to be made\n'))
        guest_number=int(input('Enter the number of guests\n'))

        checkQuery= "SELECT MAX(id), COUNT(id) FROM Bookings;"
        cur.execute(checkQuery)
        checkResults=cur.fetchone()
        bid=(checkResults[0])
        if checkResults[1]==0:
            bid=int(1)
        else:
            bid=bid+1

        # Now as we have all our info, lets insert into table
        finalQuery="INSERT INTO Bookings (id,listing_id,guest_name,stay_from,stay_to,number_of_guests) VALUES(?,?,?,?,?,?)"
        Values=[bid,listing_to_book,user_name,start,end,guest_number]
        cur.execute(finalQuery,Values)
        
    elif choose_option=='2':
        name=input("Please enter your name\n")
        reviewQuery="SELECT * FROM Bookings WHERE guest_name=?"
        cur.execute(reviewQuery,name)
        qRecords=cur.fetchall()
        while len(qRecords)==0:
            print('No data exists by that name, Please try again/n')
            name=input("Please enter your name\n")
            reviewQuery="SELECT * FROM Bookings WHERE guest_name=?"
            cur.execute(reviewQuery,name)
            qRecords=cur.fetchall()
        
        for qrow in qRecords:
            print('id',qrow[0])
            print('listing_id',qrow[1])
            print('guest_name',qrow[2])
            print('stay_from',qrow[3])
            print('stay_to',qrow[4])
            print('number_of_guests',qrow[5])
        rListing=int(input('\nEnter listing you want to review\n'))
        review_listing=input('Please review your query\n')

        checkQuery2="SELECT MAX(id),COUNT(id) FROM Reviews;"
        cur.execute(checkQuery2)
        checkResults2=cur.fetchone()
        rid=(checkResults2[0])
        if checkResults2[1]==0:
            rid=int(1)
        else:
            rid=rid+1

        
    
        insertReview="INSERT INTO Reviews (id,listing_id,comments,guest_name) Values(?,?,?,?);"
        cur.execute(insertReview,rid,rListing,review_listing,name)
        print('Succefully added if date was before stay to')


conn.commit()

conn.close()
