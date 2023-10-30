import sqlite3
from tkinter import messagebox


if __name__ == '__main__':

    path = r'database\pacific_lib_database.db'





    #create a table
    def createTable(command):
        db = sqlite3.connect(path)

        myCursor = db.cursor()
        myCursor.execute(command)
        db.commit()
        db.close()
        print('table created!')




    #create masterAdmin table
    createMasterTable = '''CREATE TABLE IF NOT EXISTS MasterAdmin(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                password TEXT)'''




    #create Admin table
    createAdminTable = '''CREATE TABLE IF NOT EXISTS Admin(
                name TEXT NOT NULL UNIQUE,
                id INTEGER NOT NULL PRIMARY KEY,
                password TEXT NOT NULL UNIQUE,
                rights TEXT)'''



    #create member table
    createMemberTable = '''CREATE TABLE IF NOT EXISTS Member(
                name TEXT NOT NULL,
                id INTEGER NOT NULL PRIMARY KEY,
                phone_number INTEGER NOT NULL UNIQUE,
                literary_taste TEXT NOT NULL,
                password TEXT NOT NULL UNIQUE,
                isPatrion TEXT,
                isSubbed TEXT)'''



    #create patrion table
    createPatrionTable = '''CREATE TABLE IF NOT EXISTS Patrion(
                name TEXT NOT NULL,
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                phone_number INTEGER NOT NULL UNIQUE,
                member_id INTEGER NOT NULL UNIQUE,
                FOREIGN KEY(member_id) REFERENCES Member(id))'''



    #create book table
    createBookTable = '''
                    CREATE TABLE IF NOT EXISTS Book(
                    Title TEXT NOT NULL,
                    ISBN TEXT NOT NULL UNIQUE PRIMARY KEY,
                    Author TEXT NOT NULL,
                    Genre TEXT NOT NULL,
                    No_Of_Copies INTEGER NOT NULL,
                    year_of_publication INTEGER NOT NULL,
                    rating INTEGER,
                    number_of_ratings INTEGER,
                    Restriction TEXT NOT NULL,
                    auth_id INTEGER NOT NULL,
                    FOREIGN KEY(auth_id) REFERENCES Author(id))
                    

    '''


    createAuthorTable = '''
                        CREATE TABLE IF NOT EXISTS Author(
                        Name TEXT NOT NULL UNIQUE,
                        id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT  
                        )

    '''

    createBorrowedTable = '''
                    CREATE TABLE IF NOT EXISTS Borrowed(
                    checkout_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
                    isbn TEXT NOT NULL,
                    borrower_id INTEGER NOT NULL UNIQUE,
                    borrowed_copies INTEGER NOT NULL,
                    borrow_period_days INTEGER NOT NULL,
                    date_borrowed TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    admin_id INTEGER NOT NULL,
                    FOREIGN KEY(admin_id) REFERENCES Admin(id))
                    
    '''
    createReturnedTable = '''
                    CREATE TABLE IF NOT EXISTS Returned(
                    checkin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    checkout_id INTEGER NOT NULL,
                    returner_id INTEGER NOT NULL,
                    isbn TEXT NOT NULL,
                    returned_copies INTEGER NOT NULL,
                    return_date TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    FOREIGN KEY(checkout_id) REFERENCES Borrowed(checkout_id))
    '''

    createDeletedBookTable = '''
                    CREATE TABLE IF NOT EXISTS DeletedBook(
                    isbn TEXT NOT NULL UNIQUE PRIMARY KEY,
                    delete_date TEXT NOT NULL,
                    logged_admin_id INTEGER NOT NULL
                    )


    '''

    createOverdueTable = '''
                    CREATE TABLE IF NOT EXISTS Overdue(
                    member_id INTEGER NOT NULL PRIMARY KEY,
                    member_phone INTEGER NOT NULL,
                    isbn TEXT NOT NULL,
                    checkout_id TEXT NOT NULL,
                    fine INTEGER NOT NULL
                    )
    '''
    
    #runs every time the program is open,checks whether an admin or master admin exists and enables,disables the buttons
    def assertAdmins(masterBTN,adminBTN):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        result = myCursor.fetchall()
        print(result)
        db.commit()
        db.close()



    #add data to master admin table
    def addMaster(name,paswd,confirmPass):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        name = name.get()
        paswd = paswd.get()
        confirmPass = confirmPass.get()
        if paswd == confirmPass:
            myCursor.execute('INSERT INTO MasterAdmin VALUES(?,?)',(name,paswd))
            db.commit()
            messagebox.showinfo('Success','Master Admin created successfully!')
        else:
            db.close()
            messagebox.showwarning('Error',"The passwords don't match!")




    #login master admin
    def loginMaster(name,paswd):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        name = name.get()
        paswd = paswd.get()

        #retrieving the saved name from database
        myCursor.execute('SELECT name from MasterAdmin ')
        db_name = myCursor.fetchone()[0] #getting the first item in the list
        
        #retrieving the saved pass from database
        myCursor.execute('SELECT password from MasterAdmin ')
        db_pass = myCursor.fetchone()[0] #getting the first item in the list 
        
        db.commit()
        db.close() 





    #delete all rows in table
    def deleteAll(table):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        id=1
        for row in table:
            myCursor.execute(f'DELETE FROM {table}')
        print('done')
        db.commit()
        db.close()  




    #delete a table from the database
    def deleteTable(table):
        db = sqlite3.connect(path)

        myCursor = db.cursor()
        delTable = f'DROP TABLE IF EXISTS {table}'
        myCursor.execute(delTable)
        print('done')
        db.commit()
        db.close()


    #delete a row using an id
    def deleteSpecific(table,id):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        myCursor.execute(f'DELETE FROM {table} WHERE name = {id}')
        print('done')
        db.commit()
        db.close()


