#Program Name: BooksDatabase
#Author: Hayden Decker
#Date of Release: 12/3/21
#This program is used to create a database used to store book, customer, and publisher information.
#In addition this program will print and read data from .txt files into the database.
import sqlite3
import csv

conn = sqlite3.connect('books.db') #Conn object is made. It creates the books.db database.
cursor = conn.cursor() #Cursor object is made.

def main():
    customersTable = """ CREATE TABLE Customers (
                            custID integer PRIMARY KEY NOT NULL, 
                            Name text,
                            Address text,
                            Age integer,
                            Income float,
                            LoginID text,
                            Password text) """ #This sql command creates the customers table with custID as it's primary key.
    publishersTable = """ CREATE TABLE Publishers (
                            PublisherID text PRIMARY KEY NOT NULL,
                            Name text,
                            Address text,
                            Discount integer) """ #This sql command creates the publishers table with PublisherID as it's primary key.
    booksTable = """ CREATE TABLE Books (
                        isbn integer PRIMARY KEY NOT NULL,
                        title text,
                        author text,
                        qty_in_stock integer,
                        price float,
                        cost float,
                        year integer,
                        PublisherID integer,
                        FOREIGN KEY (PublisherID) REFERENCES
                            Publishers(PublisherID)) """ #This sql command creates the books table with isbn as it's primary key and PublisherID as a foreign key.
    ordersTable = """ CREATE TABLE Orders (
                        ordernum integer PRIMARY KEY NOT NULL,
                        custID integer,
                        Cardnum integer,
                        Cardmonth integer,
                        Cardyear integer,
                        Orderdate text,
                        Shipdate text,
                        FOREIGN KEY (custID) REFERENCES
                            Customers(custID)) """ #This sql command creates the orders table with ordernum as it's primary key and custID as it's foreign key.
    orderListTable = """ CREATE TABLE OrderList (
                            ordernum integer NOT NULL,
                            isbn integer NOT NULL,
                            Quantity integer,
                            FOREIGN KEY (ordernum) REFERENCES
                                Orders(ordernum),
                            FOREIGN KEY (isbn) REFERENCES
                                Books(isbn),
                            PRIMARY KEY (ordernum, isbn)) """ #ordernum and isbn are a composite primary key since neither are unique on their own.
                                                              #This table is an association table so composite key fields are also foreign keys.

    customersFile = "Customers.txt" #These string variables are used in the insertData function to read data from each file.
    publishersFile = "Publishers.txt"
    booksFile =  "Books.txt"
    ordersFile = "Orders.txt"
    orderListFile = "OrderList.txt"

    customersSQL = """INSERT INTO Customers (custID, Name, Address, Age, Income, LoginID, Password)
                            VALUES(?,?,?,?,?,?,?)
                            """ #Each table has an insert sql command which populates each table with data. This command is used in the insertData function.
    publishersSQL = """INSERT INTO Publishers (PublisherID, Name, Address, Discount)
                            VALUES(?,?,?,?)"""
    booksSQL = """INSERT INTO Books (isbn, title, author, qty_in_stock, price, cost, year, PublisherID)
                            VALUES(?,?,?,?,?,?,?,?)"""
    ordersSQL = """INSERT INTO Orders (ordernum, custID, Cardnum, Cardmonth, Cardyear, Orderdate, Shipdate)
                            VALUES(?,?,?,?,?,?,?)"""
    orderListSQL = """INSERT INTO OrderList (ordernum, isbn, Quantity)
                            VALUES(?,?,?)"""
    customersReportSQL = """SELECT DISTINCT OrderList.ordernum, Orders.custID, Customers.Name, Customers.Address
                            FROM Orders, Customers, OrderList
                            WHERE OrderList.ordernum = Orders.ordernum
	                            AND Orders.custID = Customers.custID""" #To generate reports each field is selected. From indicates every table and where is used to match foreign keys. Otherwise, every record would be selected.
    booksReportSQL = """SELECT DISTINCT OrderList.isbn, Books.title, Books.author, Publishers.PublisherID, Publishers.Name
                        FROM Books, Publishers, OrderList
                        WHERE OrderList.isbn = Books.isbn
	                        AND Books.PublisherID = Publishers.PublisherID"""

    cursor.execute(customersTable)  #These function calls create the tables.
    cursor.execute(publishersTable)
    cursor.execute(booksTable)
    cursor.execute(ordersTable)
    cursor.execute(orderListTable)  

    insertData(customersFile, customersSQL) #These function calls insert data using the file name and corresponding sql command as arguments.
    insertData(publishersFile, publishersSQL)
    insertData(booksFile, booksSQL)
    insertData(ordersFile, ordersSQL)
    insertData(orderListFile, orderListSQL)

    print("REPORTS")
    printData(customersReportSQL) #Print data function is used to print each report.
    print()
    printData(booksReportSQL)
    print()

    conn.commit()

    userInput = 0
    while(userInput != 4): #While loop menu for user to select which table to print.
        userInput = int(input("Enter 1 to print Customers table.\nEnter 2 to print Publishers table.\nEnter 3 to print Books table.\nEnter 4 to quit.\n"))
        userDisplayTable(userInput)
    conn.close()
    

def insertData(textFile, commandSQL):
    with open(textFile) as file:
        reader = csv.reader(file, skipinitialspace=True, delimiter=",", quotechar="'") #File is read as a csv document since its seperated by commas. skipintialspace is changed from false to true and quotechar is given a single quote argument so file can be read as csv.
        for line in reader:
            cursor.execute(commandSQL, line) #execute is given a second argument which is used to insert data from .txt row by row.


def printData(commandSQL):
    cursor.execute(commandSQL)
    rows = cursor.fetchall() #rows is initialized as a list of tuples which fetchall() method returns.
    for row in rows:
        print(row)

def userDisplayTable(userInput): #This function is used for the user input while loop.
    if(userInput == 1):
        print("Customers Table:")
        printData("SELECT * FROM Customers") #This sql command is used to select an entire table and it is passed to printData function.
        print()
    elif(userInput == 2):
        print("Publishers Table:")
        printData("SELECT * FROM Publishers")
        print()
    elif(userInput == 3):
        print("Books Table:")
        printData("SELECT * FROM Books")
        print()
    elif(userInput == 4):
        exit()

if __name__ == '__main__':
    main()
