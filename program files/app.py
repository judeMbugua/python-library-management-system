from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image  #to display images
import sqlite3
from datetime import timedelta,date,datetime

#to make sure this program can only be run from this file file not via importing to prevent circular importation
if __name__ == '__main__':
    # Create the root window
    root = Tk()
    root.title("Books management")
    root.geometry("900x600+180+20")
    root.configure(bg="#184769")
    root.iconbitmap(r'C:\Users\judew\Documents\code projects\python\PYTHONPROJECT\icons\books.ico')
    root.resizable(False,False)

    #binding the escape key with the quit event to close the application when clicked
    def close(event):
        root.quit()

    root.bind('<Escape>',close)






    #-------------------NAVIGATION FUNCIONS START---------------------------------------


    #switches between pages(frames) takes from and to page,and context menu for clearing any entries
    def switchPages(fro,to,context_menu):
        fro_children = context_menu.winfo_children()

        fro.pack_forget()
        to.pack(fill='both',expand=True)

        #loops thru all entry children and clears them
        for child_widget in fro_children:
            if child_widget.winfo_class() == 'Entry':
                child_widget.delete(0,'end')
                


    #clears all input in the given frame
    def clear(contextMenu):
        fro_children = contextMenu.winfo_children() 

        #loops thru all entry children and clears them
        for child_widget in fro_children:
            if child_widget.winfo_class() == 'Entry':
                child_widget.delete(0,'end')
                



    #navs back to home Page
    def backToHome(currPage):
        fro = AdminHome_page
        currPage.pack_forget()
        fro.pack(fill='both',expand=True)

        #explicitly setting the defaults text of the options
        user_selected.set('Manage Members')
        book_selected.set('Manage Book')
        checks_selected.set('Check in or out')

    
    #navigates from admin homepage to other pages
    def navFromHome(fro,direction,buttonName):
        
        #handles movement for manage users button
        if direction == 'forward' and buttonName == 'manageUsers':
            fro.pack_forget()
            match user_selected.get():
                case 'Add Member':
                    AddMember_page.pack(fill='both',expand=True)
                    currPage = AddMember_page

                case 'Delete Member':
                    deleteMember_page.pack(fill='both',expand=True)
                    currPage = deleteMember_page
                    
                case 'Edit Member':
                    editMember_page.pack(fill='both',expand=True)
                    currPage = editMember_page

                case 'View Member':
                    viewMember_page.pack(fill='both',expand=True)
                    currPage = viewMember_page

            
        #handles movement for manage books button
        elif direction == 'forward' and buttonName == 'manageBooks':
            fro.pack_forget()
            match book_selected.get():
                case 'Add Book':
                    AddBook_page.pack(fill='both',expand=True)
                    
                    
                case 'Delete Book':
                    deleteBook_page.pack(fill='both',expand=True)
                    
                    
                case 'Edit Book':
                    editBook_page.pack(fill='both',expand=True)
                

                case 'View Book':
                    viewBook_page.pack(fill='both',expand=True)

        #handles movement for book check in\out
        elif direction == 'forward' and buttonName == 'bookBorrow':
            fro.pack_forget()
            match checks_selected.get():
                case 'Borrow Book':
                    borrowBook_page.pack(fill='both',expand=True)

                case 'Return Book':
                    returnBook_page.pack(fill='both',expand=True)
            
               






    #-------------------NAVIGATION FUNCIONS END---------------------------------------













    #++++++++++++++++_____DATABASE FUNCTIONS START_____+++++++++++++++++

    #global variable pointing to the 
    path = r'C:\\Users\\judew\\Documents\\code projects\\python\\PYTHONPROJECT\\database\\pacific_lib_database.db'




    #create a table
    def createTable(command):
        db = sqlite3.connect(path)

        myCursor = db.cursor()
        myCursor.execute(command)
        db.commit()
        db.close()





    #runs every time the program is open,checks whether an admin or master admin exists and enables,disables the various buttons
    def assertMaster():
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        #checking whether a master Admin already exists

        myCursor.execute('SELECT * FROM MasterAdmin')
        existing = myCursor.fetchone()

        #checking for typeerror which will occur when the master admin table is empty(master admin does not exist)
        try:
            if len(existing) > 0:
                create_master_btn.config(state='disabled')

        except(TypeError):
            login_master_btn.config(state='disabled')
            login_admin_btn.config(state='disabled')

        db.close()





    #___________WRITE TO MASTER ADMIN TABLE_________________

    def addMaster(name,paswd,confirmPass):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        
        #checking whether a master Admin already exists

        myCursor.execute('SELECT * FROM MasterAdmin')
        existing = myCursor.fetchone()

        #checking for typeerror which will occur when the master admin table is empty(master admin does not exist)
        try:
            if len(existing) > 0:
                login = messagebox.askokcancel('Master Admin exists','Cannot create another master admin since one already exists,would you like to login to the current one?')
                if login:
                    createMasterAdmin_page.pack_forget()
                    masterLogin_page.pack()
                    return
        except(TypeError):
            pass

        name = name.get().capitalize()
        #check that user has entered both names

        splitName = name.split(' ')
        if len(splitName) < 2:
            messagebox.showerror('Error','Please enter both names')
            return

        paswd = paswd.get()
        #check the length of the password
        if len(paswd) < 6:
            messagebox.showerror('Error','Password too short,should be above 6 characters!')
            return
        elif len(paswd) > 10:
            messagebox.showerror('Error','Password too long')
            return  
        
        confirmPass = confirmPass.get()

        if confirmPass == '' or name == '' or paswd == '':
            messagebox.showerror('Error','Please Fill in all the spaces')
            return

        if paswd == confirmPass:
            myCursor.execute('INSERT INTO MasterAdmin VALUES(null,?,?)',(name,paswd))
            db.commit()
            ans = messagebox.askokcancel('Success','Master Admin created successfully! Login Master Admin?')

            if ans:
                switchPages(createMasterAdmin_page,masterLogin_page,CreateMasterContext_frame)
            else:
                clear(CreateMasterContext_frame)
            
        else:
            db.close()
            messagebox.showwarning('Error',"The passwords don't match!")
        
        #calling the functions which disables creation of master admin
        assertMaster()




    #_______________LOGIN MASTER ADMIN______________

    def loginMaster(name,paswd):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        name = name.get().capitalize()
        paswd = paswd.get()
        

        #retrieving the saved name from database
        try:
            db_name = myCursor.execute('SELECT name from MasterAdmin ').fetchone()[0] #getting the first item in the list
            
            
            #retrieving the saved pass from database
            myCursor.execute('SELECT password from MasterAdmin ')
            db_pass = myCursor.fetchone()[0] #getting the first item in the list

        except(TypeError):
            messagebox.showerror('Error','MasterAdmin does not exist,create one.')
            switchPages(masterLogin_page,createMasterAdmin_page,masterLoginContext_frame)
            return

        if name == db_name and paswd == db_pass:
            
            clear(masterLoginContext_frame)

            #manually unpacking and packing pages since they have packing issues
            masterLogin_page.pack_forget()
            masterOptions_page.pack()
            masterOptionsContext_frame.place(x=240,y=60)
            masterOptionsMenu_frame.place(x=10,y=60)

            #displaying the master admin name
            masterOptsDispName_label.config(text = db_name )


        elif name == '' and paswd == '':
            messagebox.showwarning('Error','Please fill in all spaces')
        
        else:
            messagebox.showwarning('Login','Incorrect information')

        
        
        db.commit()
        db.close() 




    #_______________WRITE TO ADMIN TABLE_________________

    def addAdmin(name,id,password,right):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        name = name.get().capitalize()
        id = id.get()
        password = password.get()
        right = right.get()

        #validating the inputs
        if name == '' or id == '' or password == '':
            messagebox.showwarning('Error','Please fill in all the spaces')
            return
        
        elif len(id) < 8 or len(id)  > 8:
            messagebox.showerror('Error','The ID should be 8 numbers')
            return

        #validate id not start with zero since zero is removed in database
        elif id[0] == '0':
            messagebox.showerror('Error',"The ID can't start with a 0!")
            return         
        
        #converting id to int and checking whether the user input the correct data type
        try:
            id = int(id)

        except(ValueError):
            messagebox.showwarning('Error','The ID should be a number not text')
            return
        
        #check if admin already exists using existing admin ids
        getAdmins = myCursor.execute('SELECT id FROM Admin').fetchall()
        existingAdmin = [admin[0] for  admin in getAdmins]

        if id in existingAdmin:
            messagebox.showwarning('Error','An admin with a similar ID exists')
            return            

        #check if admin with a similar name exists
        getAdminsName = myCursor.execute('SELECT name FROM Admin').fetchall()
        existingAdminName = [admin[0] for  admin in getAdminsName]

        if name in existingAdminName:
            messagebox.showwarning('Error','An admin with a similar name exists')
            return      

        myCursor.execute('INSERT INTO Admin VALUES(?,?,?,?)',(name,id,password,right))
        db.commit()
        messagebox.showinfo('Success','Admin created successfully')
        clear(createAdminContext_frame)
        switchPages(createAdmin_page,startup_page,createAdminContext_frame)
        




    

    #__________LOGIN ADMIN___________________

    def loginAdmin(name,password):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        name = name.get().capitalize()
        password = password.get()

        #holds the id of the currently logged in user
        global loggedInAdm_id

        #validating user input
        if name == '' or password == '':
            messagebox.showerror('Error','Please fill in all the spaces!')
            return


        #retrieving the saved name from database
        myCursor.execute('SELECT name from Admin')
        db_names = myCursor.fetchall() #getting all the names in the database
        names = [name[0] for name in db_names] #adding the names in the list since they are  returned as a turple 
        
        #checking whether the inputted name exists in the database
        if name not in names:
            messagebox.showerror('Error','This admin does not exist')
            clear(loginAdminContext_frame)
            return
        

        #retrieving the saved pass from database with the entered name
        myCursor.execute('SELECT password from Admin WHERE name = ?',(name,))
        db_pass = myCursor.fetchone()[0] #getting the first item in the returned list
        
        
        #comparing entered password with the database one
        if password == db_pass:
            #to always know the current logged in admin
            loggedInAdm_id = myCursor.execute('SELECT id from Admin WHERE name = ?',(name,)).fetchone()[0]

            #set the admin name and id in the admin homepage
             #set name
            loggedAdm_label.configure(text=name)

            #check if this admin has can create admins and disable button if has no rights
            rights = myCursor.execute('SELECT rights FROM Admin WHERE id = ?',(loggedInAdm_id,)).fetchone()[0]
            if rights == "yes":
                createAdmin_btn.config(state='normal')

             #set id
            loggedAdm_idLabel.configure(text=loggedInAdm_id )
            switchPages(loginAdmin_page,AdminHome_page,loginAdminContext_frame)

            

        else:
            messagebox.showerror('Error','You entered the wrong password')


    #to logout the logged in admin by switching pages and and disabling the create adm btn
    def logout():
        switchPages(AdminHome_page,startup_page,context_frame)
        createAdmin_btn.config(state='disabled')



    #function that checks whether an admin has rights to create another admin
    def adminAddAdmin():
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        #check whether current admin has rights to create other admin using logged in admin id
        rights = myCursor.execute('SELECT rights FROM Admin WHERE id = ?',(loggedInAdm_id,)).fetchone()[0]
        name = myCursor.execute('SELECT name FROM Admin WHERE id = ?',(loggedInAdm_id,)).fetchone()[0]

        if rights == 'yes':
            switchPages(AdminHome_page,createAdmin_page,AdminHomepageMenu_frame)
            db.close()
            return
        else:
            messagebox.showerror('Error',f'Admin {name} does not have permission to create other admins!')
            db.close()
            
            



    #__________DELETE ADMIN___________________
    def deleteAdmin(deletedAdm,transferAdm):
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        #get delted admin ID and transfer admin ID
        deletedAdm = deletedAdm.get()
        transferAdm = transferAdm.get()

        getAdmins = myCursor.execute("SELECT id FROM Admin").fetchall()
        existAdmins = [id[0] for id in getAdmins]


        #input validation
        if deletedAdm == '' or transferAdm == '':
            messagebox.showerror('Error',"Please fill in all spaces!")
            return
        elif len(deletedAdm) < 8 or len(deletedAdm) > 8 or len(transferAdm) < 8 or len(transferAdm) > 8:
            messagebox.showerror('Error',"The ID's should be 8 numbers")
            return


        #check that only numbers are input in both fields
        try:
            deletedAdm = int(deletedAdm)
            transferAdm = int(transferAdm)
        
        except(ValueError):
            messagebox.showerror('Error',"Both 'Admin ID' and 'transer ID' should be numbers only!")
            return

        #check if delete admin  and transer admin exist
        getAdmins = myCursor.execute("SELECT id FROM Admin").fetchall()
        existAdmins = [id[0] for id in getAdmins]

         #check that the deleted admin is not the same as transer admin
        if deletedAdm == transferAdm:
            messagebox.showerror('Error','The delete and transfer admin cannot be the same!')
            return            

        elif deletedAdm not in existAdmins:
            messagebox.showerror('Error','The Admin you want to delete does not exist!')
            return
        
        elif transferAdm not in existAdmins:
            messagebox.showerror('Error','The Admin you want to transfer to does not exist!')
            return         
        

        #transfer the deleted admin's record in borrowed table to transer admin
        getBorrowed = myCursor.execute('SELECT borrower_id FROM Borrowed').fetchall()
        existBorrowed = [id[0] for id in getBorrowed]

        #loop through each record and replace the admin_id field in records associated with the deleted admin
         #holds id's of those members associated with the deleted admin
        transRecords = []
        for id in existBorrowed:
            if myCursor.execute('SELECT admin_id FROM Borrowed WHERE borrower_id = ?',(id,)).fetchone()[0] == deletedAdm:
                myCursor.execute('UPDATE Borrowed SET admin_id = ? WHERE borrower_id = ?',(transferAdm,id,))

        #deleting the admin
        myCursor.execute('DELETE FROM Admin WHERE id = ?',(deletedAdm,))

        #get the transfer admin name
        tranName = myCursor.execute('SELECT name FROM Admin WHERE id = ?',(transferAdm,)).fetchone()[0]
        messagebox.showerror('Done',f'Admin deleted.Records transfered to {tranName}')

        clear(deleteAdminContext_frame)  
        

        db.commit()
        db.close()




    #__________WRITE TO MEMBER TABLE__________________

    def addMember(name,id,phone_number,literary_taste,password,isPatrion,isSubbed):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        name = name.get().capitalize()
        id = id.get()
        phone_number = phone_number.get()
        literary_taste = literary_taste.get().capitalize()
        password = password.get()
        isPatrion = isPatrion.get()
        isSubbed = isSubbed.get()

        #validating the inputs
        if name == '' or id == '' or phone_number == '' or literary_taste == '' or password == '':
            messagebox.showwarning('Error','Please fill in all the spaces')
            return
        
        elif len(id) < 8 or len(id)  > 8:
            messagebox.showerror('Error','The ID should be 8 numbers')
            return

        elif len(phone_number) < 10 or len(phone_number)  > 10:
            messagebox.showerror('Error','The phone number should be 10 numbers')
            return
        elif len(password) < 6 or len(password) > 8:
            messagebox.showerror('Error','The password should have 6-8 characters!')
            return 
        
        #validate,ID can't start with zero since zero is ignored in database
        elif id[0] == '0':
            messagebox.showerror('Error',"The ID can't start with a 0!")
            return  
    
        #validate phone number must start with 07
        elif phone_number[0] != '0' and phone_number[1] != '7':
            messagebox.showerror('Error',"The phone number must start 07xxxxxxxx!")
            return  
    


        #converting id and phone number to int and checking whether the user input the correct data type
        try:
            id = int(id)
            phone_number = int(phone_number)

        except(ValueError):
            messagebox.showwarning('Error','The ID and Phone Number should be a number not text')
            return



        #checking whether a member already exists
        myCursor.execute('SELECT id from Member')
        db_ids = myCursor.fetchall() #getting all the id's in the database
        existing_ids = [id[0] for id in db_ids] #adding the id's in the list since they are  returned as a turple

        if id in existing_ids:
            messagebox.showerror('Error','A member with a similar ID already exists!')
            clear(addMemberContext_frame)
            return
        
        #check if pass already in use
        getPaswds = myCursor.execute('SELECT password from Member').fetchall()
        existingPaswds = [paswd[0] for paswd in getPaswds]

        if password in existingPaswds:
            messagebox.showerror('Error','Password exists,choose another one!')
            return
        

        #warning user about similar nameS
        myCursor.execute('SELECT name from Member')
        db_names = myCursor.fetchall() #getting all the names in the database
        names = [name[0] for name in db_names] #adding the names in a list since they are  returned as a turple

        if name in names:
            save = messagebox.askokcancel('Warning','A member with a similar name already exists,Continue and add this member?')

            if not save:
                return
        
        myCursor.execute('INSERT INTO Member VALUES(?,?,?,?,?,?,?)',(name,id,phone_number,literary_taste,password,isPatrion,isSubbed,))

        #adding patrions to patrion table
        if isPatrion == 'yes':
            myCursor.execute('PRAGMA foreign_keys = ON;') #allowing foreign keys since it's not on by default
            myCursor.execute('INSERT INTO Patrion VALUES(?,null,?,?)',(name,phone_number,id))
            messagebox.showinfo('Patrion','This Member will also be added to the patrion table')


        db.commit()
        db.close()
        messagebox.showinfo('Success','Member added successfully!')
        clear(addMemberContext_frame)



    #________________FIND A MEMBER FOR DELETION_________________________________________

    def delFindMember(id):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        id = id.get()

    #input validation
        if id == '':
            messagebox.showerror('Error','Please enter an ID to find member')
            return
        
        elif len(id) < 8 or len(id) > 8:
            messagebox.showwarning('Error','The ID should be 8 numbers')
            return

        try:
            id = int(id)

        except(ValueError):
            messagebox.showerror('Error','The ID should be a number')
            return
        
        #checking whether the member exists in the database
        myCursor.execute('SELECT id from Member')
        db_ids = myCursor.fetchall() #getting all the id's in the database
        existing_ids = [id[0] for id in db_ids] #adding the id's in the list since they are  returned as a turple

        if id not in existing_ids:
            messagebox.showerror('Error','NO member with this ID exists!')
            clear(deleteMemberContext_frame)
            return
    

        
        #getting members's phone number from database
        myCursor.execute('SELECT phone_number FROM Member WHERE id = ?',(id,))
        phone_number = myCursor.fetchone()[0]

        #getting member's membership from database
        myCursor.execute('SELECT isPatrion FROM Member  WHERE id = ?',(id,))
        membership = myCursor.fetchone()[0]

        #getting member's membership from database
        myCursor.execute('SELECT name FROM Member  WHERE id = ?',(id,))
        borrowd_books = myCursor.fetchone()[0]

        #to avoid displaying data twice incase the button is clicked twice clear entries before displaying on them

                #enabling the entries first
        delFoundMemberPhone_entry.config(state='normal')
        delFoundMembership_entry.config(state='normal')
        delFoundBorrowed_entry.config(state='normal') 


        delFoundMemberPhone_entry.delete(0,'end')
        delFoundMembership_entry.delete(0,'end')
        delFoundBorrowed_entry.delete(0,'end')


        #displaying the retrieved information and disabling the entries
        delFoundMemberPhone_entry.insert('0',phone_number)

        if membership == 'yes':
            membership = 'Member is a patrion'
        elif membership == 'no':
            membership = 'Member is not a patrion'

        delFoundMembership_entry.insert('0',membership)

        delFoundBorrowed_entry.insert('0',borrowd_books)


        #disabling the entries
        delFoundMemberPhone_entry.config(state='disabled')
        delFoundMembership_entry.config(state='disabled')
        delFoundBorrowed_entry.config(state='disabled') 



    #_________________DELETE A MEMBER________________________________________

    def deleteMember(id):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        id = id.get()

        if id == '':
            messagebox.showerror('Error','Please enter an ID to find member')
            return

        try:
            id = int(id)

        except(ValueError):
            messagebox.showerror('Error','The ID should be a number')
            return

        #deleting from patrion table if exists
        myCursor.execute('SELECT isPatrion FROM Member WHERE id = ?',(id,))
        patrionStatus = myCursor.fetchone()[0]

        if patrionStatus == 'yes':
            myCursor.execute(f'DELETE FROM Patrion WHERE member_id = {id}')

        myCursor.execute(f'DELETE FROM Member WHERE id = {id}')

        messagebox.showinfo('Deleted','Member has been deleted!')
        clear(deleteMemberContext_frame)
        db.commit()
        db.close()



    #___________________________________DISPLAY MEMBER INFO FOR EDITING___________________________________________

    def editFindMember(id):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        id = id.get()

    #input validation
        if id == '':
            messagebox.showerror('Error','Please enter an ID to find member')
            return
        
        elif len(id) < 8 or len(id) > 8:
            messagebox.showwarning('Error','The ID should be 8 numbers')
            return

        try:
            id = int(id)

        except(ValueError):
            messagebox.showerror('Error','The ID should be a number')
            return
        
        #checking whether the member exists in the database
        myCursor.execute('SELECT id from Member')
        db_ids = myCursor.fetchall() #getting all the id's in the database
        existing_ids = [id[0] for id in db_ids] #adding the id's in the list since they are  returned as a turple

        if id not in existing_ids:
            messagebox.showerror('Error','NO member with this ID exists!')
            clear(deleteMemberContext_frame)
            return
    

        
        #getting members's phone number from database
        myCursor.execute('SELECT phone_number FROM Member WHERE id = ?',(id,))
        phone_number = myCursor.fetchone()[0]

        #getting member's membership from database
        myCursor.execute('SELECT isPatrion FROM Member  WHERE id = ?',(id,))
        membership = myCursor.fetchone()[0] 

        #getting member's membership from database
        myCursor.execute('SELECT name FROM Member  WHERE id = ?',(id,))
        borrowd_books = myCursor.fetchone()[0]

        #to avoid displaying data twice incase the button is clicked twice clear entries before displaying on them
        editMemberName_entry.delete(0,'end')
        editMemberPhone_entry.delete(0,'end')
        editMemberTaste_entry.delete(0,'end')
        editMemberPass_entry.delete(0,'end')


        #displaying the retrieved information for editing
        
        #name
        myCursor.execute('SELECT name FROM Member  WHERE id = ?',(id,))
        name = myCursor.fetchone()[0]

        editMemberName_entry.insert('0',name)

        #phone number
        myCursor.execute('SELECT phone_number FROM Member  WHERE id = ?',(id,))
        phone = myCursor.fetchone()[0]

        editMemberPhone_entry.insert('0',phone)


        #literary taste
        myCursor.execute('SELECT literary_taste FROM Member  WHERE id = ?',(id,))
        taste = myCursor.fetchone()[0]

        editMemberTaste_entry.insert('0',taste)


        #password
        myCursor.execute('SELECT password FROM Member  WHERE id = ?',(id,))
        paswd = myCursor.fetchone()[0]

        #hidding the password for display and editing
        hdnPass = '*' * len(paswd)
        editMemberPass_entry.insert('0',hdnPass)


        #member status
        myCursor.execute('SELECT isPatrion FROM Member  WHERE id = ?',(id,))
        ispat = myCursor.fetchone()[0]

        #setting the value of the checkbox
        editIsPatrion.set(ispat)




    #_________________________________SAVE AFTER EDIT_________________________________________________

    def saveEdit(id):
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        id = id.get()

        #input validation
        if id == '':
            messagebox.showerror('Error','Please enter an ID to find member')
            return
        
        elif len(id) < 8 or len(id) > 8:
            messagebox.showwarning('Error','The ID should be 8 numbers')
            return

        try:
            id = int(id)

        except(ValueError):
            messagebox.showerror('Error','The ID should be a number')
            return
        

        #getting the values of the entries
        eName = editMemberName_entry.get().capitalize()
        ePhone = editMemberPhone_entry.get()
        eTaste = editMemberTaste_entry.get().capitalize()
        ePass = editMemberPass_entry.get()
        ePat = editIsPatrion.get()

        #re assignign the password variable incase its not editted to avoid saving it as *** in the database
        if '*' in ePass:
            myCursor.execute('SELECT password FROM Member WHERE id = ?',(id,))
            ePass = myCursor.fetchone()[0]
    


        askPass = messagebox.askquestion('continue','save changes?')

        if askPass == 'yes':
            #deleting this member's row and re-adding it with the new infomation

            #catching error when user tries editing the ID
            try:
                #getting the subscriptions status of member before deleting
                myCursor.execute('SELECT isSubbed FROM Member WHERE id = ?',(id,))
                subState = myCursor.fetchone()[0]

                myCursor.execute('DELETE FROM Member WHERE id = ?',(id,))
                myCursor.execute('INSERT INTO Member VALUES(?,?,?,?,?,?,?)',(eName,id,ePhone,eTaste,ePass,ePat,subState))
                clear(editMemberContext_frame)
                messagebox.showinfo('Done','saved!')

            except(TypeError):
                messagebox.showerror('Error','cannot change ID!')


        else:
            messagebox.showinfo('canceled','Edit canceled!')
            db.close() 
            return

        db.commit()
        db.close()  





    #_________________________________WRITE TO BOOK TABLE_________________________________________________
    def addBook(title,isbn,author,genre,No_of_copies,yearOfPub,restriction):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        title = title.get().capitalize()
        isbn = isbn.get()
        author = author.get().capitalize()
        genre = genre.get().capitalize()
        No_of_copies = No_of_copies.get()
        yearOfPub = yearOfPub.get()
        restriction = restriction.get()


        if title == '' or isbn == '' or author == '' or genre == '' or No_of_copies == '' or yearOfPub == '':
            messagebox.showerror('Error','Please fill in all the spaces')
            return

        try:
            No_of_copies = int(No_of_copies)
            yearOfPub = int(yearOfPub)

        except(ValueError):
            messagebox.showerror('Error',"The 'No of copies' and 'year of publication' should be a number!")  
            return       


        #check that isbn has correct format;must be 8 chars
        if len(isbn) < 8 or len(isbn) > 9:
            messagebox.showerror('Error','The isbn should be 8 characters!')
            return


        #checking whether a similar book exists
        existingBooks = myCursor.execute('SELECT ISBN FROM Book').fetchall()
        exiting = [book[0] for book in existingBooks]

        if isbn in existingBooks:
            messagebox.showwarning('Error','A book with a similar ISBN already exists')
            return



        
        #checking whether the author being added already exists in the database and assigning their auth_id else adding them in the Author table

        myCursor.execute('SELECT Name FROM Author')
        existingAuthors = myCursor.fetchall()
        existingAuthorNames = [name[0] for name in existingAuthors]


        if author in existingAuthorNames:
            auth_id = myCursor.execute('SELECT id FROM Author WHERE Name = ?',(author,)).fetchone()[0]

        elif author not in existingAuthorNames:  
            myCursor.execute('INSERT INTO Author VALUES(?,null)',(author,))
            auth_id = myCursor.execute('SELECT id FROM Author WHERE Name = ?',(author,)).fetchone()[0]
            messagebox.showinfo('Author Table','Author was added')


        #adding the book to the book table
        myCursor.execute('INSERT INTO Book VALUES(?,?,?,?,?,?,?,?,?,?)',(title,isbn,author,genre,No_of_copies,yearOfPub,1,1,restriction,auth_id))
        messagebox.showinfo('Book Table','Book Added!')
        clear(addBookContext_frame)

        db.commit()
        db.close()



    #_________________________________FIND BOOK TO DELETE_________________________________________________
    def delFindBook(isbn):
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        isbn = isbn.get()
        
        #input validation
        if isbn == '':
            messagebox.showerror('Error','Please enter book ISBN to find book')
            return

        #checking whether the book exists
        getExistingBooks = myCursor.execute('SELECT ISBN FROM Book').fetchall()
        existingBooks = [book[0] for book in getExistingBooks]
       
        if isbn not in existingBooks:
            add = messagebox.askokcancel('Error','Books does not exists,Do you want to add it?')
            if add: 
                #enabling the buttons to clear the text           
                deleteBookTitle_entry.configure(state='normal')
                deleteBookNo_entry.configure(state='normal')
                
                #disabling the delete button
                deleteBook_btn.configure(state='disabled')

                switchPages(deleteBook_page,AddBook_page,deleteBookContext_frame)

                #inserting the non-existent book isbn on the add book isbn field
                addBookISBN_entry.insert('0',isbn)

                #disabling the buttons after clearing their input
                deleteBookTitle_entry.configure(state='disabled')
                deleteBookNo_entry.configure(state='disabled')

                return
            else:
                clear(deleteBookContext_frame)
                return
            
            #displaying the book's info if it exists in the database
        else:
            title = myCursor.execute('SELECT Title FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
            No_of_copies = myCursor.execute('SELECT No_Of_Copies FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]


            #configuring the entries to display the retrieved data and disabling them to avoid user from editing

                        #enabling the fields first to write on them
            deleteBookTitle_entry.configure(state='normal')
            deleteBookNo_entry.configure(state='normal')

                #deleting the fields text to avoid writing to on twice
            deleteBookTitle_entry.delete(0,'end')
            deleteBookNo_entry.delete(0,'end')
            

            deleteBookTitle_entry.insert('0',title)
            deleteBookNo_entry.insert('0',No_of_copies)

            #disbling the fields
            deleteBookTitle_entry.configure(state='disabled')
            deleteBookNo_entry.configure(state='disabled')

            #enabling the delete book button
            deleteBook_btn.configure(state='normal')

        db.commit()
        db.close()





    #_________________________________DELETE A BOOK_________________________________________________
    def deleteBook(isbn):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        isbn = isbn.get()

        title = myCursor.execute('SELECT Title FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]

        if isbn == '':
            messagebox.showerror('Error','Please enter book ISBN to find a book!')
            return
    
        confirm = messagebox.askokcancel('confirm',f'Delete {title}?')
        if confirm:
            myCursor.execute('DELETE FROM Book WHERE isbn = ?',(isbn,))

            #enabling the buttons to clear the text           
            deleteBookTitle_entry.configure(state='normal')
            deleteBookNo_entry.configure(state='normal')

            #clearing the input fields
            clear(deleteBookContext_frame)

            # disabling the buttons after clearing the text           
            deleteBookTitle_entry.configure(state='disabled')
            deleteBookNo_entry.configure(state='disabled')


            messagebox.showinfo('Done!','Book deleted!')

            #disabling the delete button
            deleteBook_btn.configure(state='disabled')
        else:
            messagebox.showinfo('cancelled','operation cancelled!')
            return

        db.commit()
        db.close()
        




    #_________________________________FIND BOOK TO EDIT_________________________________________________
    def editFindBook(isbn):
        db = sqlite3.connect(path)
        myCursor = db.cursor()
        isbn = isbn.get()

        if isbn == '':
            messagebox.showerror('Error','Please enter book ISBN to edit')
            return
        

        #checking whether the book exists and asking user whether to add it
        getAllBooks = myCursor.execute('SELECT ISBN FROM Book').fetchall()
        existingBooks = [book[0] for book in getAllBooks]

        if isbn not in existingBooks:
            add = messagebox.askokcancel('Error','Book does not exist,Do you want to add it?')

            #if user chose add it
            if add:
                  #disabling the save changes button
                editBook_btn.config(state='disabled')
                switchPages(editBook_page,AddBook_page,editBookContext_frame)
                addBookISBN_entry.insert('0',isbn)
                return
            else:
                return


          #clearing the entries to avoid writin on them twice
        editBookTitle_entry.delete(0,'end')
        editBookAuthor_entry.delete(0,'end')
        editBookGenre_entry.delete(0,'end')
        editBookCopies_entry.delete(0,'end')

        #retrieving info from database to display it 

        title = myCursor.execute('SELECT Title FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        author = myCursor.execute('SELECT Author FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        genre = myCursor.execute('SELECT Genre FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        copies = myCursor.execute('SELECT No_Of_Copies FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        res = myCursor.execute('SELECT Restriction FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        
        editBookTitle_entry.insert('0',title)
        editBookAuthor_entry.insert('0',author)
        editBookGenre_entry.insert('0',genre)
        editBookCopies_entry.insert('0',copies)

        isBookRestricted.set(res)

        #enabling the save changes button
        editBook_btn.config(state='normal')





        db.commit()
        db.close()




        #_________________________________SAVE BOOK AFTER _________________________________________________





    #_________________________________SAVE BOOK AFTER EDIT_________________________________________________
    def saveBookEdit(isbn):
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        isbn = isbn.get()

        title = editBookTitle_entry.get().capitalize()
        author = editBookAuthor_entry.get().capitalize()
        genre = editBookGenre_entry.get().capitalize()
        copies = editBookCopies_entry.get()
        res = isBookRestricted.get()


        #input validation
        if title == '' or author == '' or genre == '' or copies == '':
            messagebox.showerror('Error','Please fill in all the spaces')
            return

        try:
            copies = int(copies)


        except(ValueError):
            messagebox.showerror('Error',"The 'No of copies' and 'year of publication' should be a number!")  
            return  


        #deleting the existing book row and re-writing it with the new infomation

        #getting the uneditable columns i.e yearOfPUb and auth_id,rating,number of ratings

        yearOfPub = myCursor.execute('SELECT year_of_publication FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        auth_id = myCursor.execute('SELECT auth_id FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        rating = myCursor.execute('SELECT rating FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        numbOfRatings = myCursor.execute('SELECT number_of_ratings FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]

          #deleting
        myCursor.execute('DELETE FROM Book WHERE ISBN = ?',(isbn,))

        #re writing
        myCursor.execute('INSERT INTO Book VALUES(?,?,?,?,?,?,?,?,?,?)',(title,isbn,author,genre,copies,yearOfPub,rating,numbOfRatings,res,auth_id))
        clear(editBookContext_frame)
        messagebox.showinfo('Done','changes saved!')

        db.commit()
        db.close() 





    #_________________________________VIEW BOOK_________________________________________________
    def viewBook(isbn):
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        isbn = isbn.get()


        #checking whether book exists
        if isbn == '':
            messagebox.showerror('Error','Please enter book ISBN to edit')
            return
        

        #checking whether the book exists and asking user whether to add it
        getAllBooks = myCursor.execute('SELECT ISBN FROM Book').fetchall()
        existingBooks = [book[0] for book in getAllBooks]

        if isbn not in existingBooks:
            add = messagebox.askokcancel('Error','Book does not exist,Do you want to add it?')

            #if user chose add it
            if add:
                 
                switchPages(viewBook_page,AddBook_page,editBookContext_frame)
                addBookISBN_entry.insert('0',isbn)
                return
            else:
                return

        #disabling the entries to allow text deletion
        viewBookTitle_entry.config(state='normal')
        viewBookAuthor_entry.config(state='normal')
        viewBookGenre_entry.config(state='normal')
        viewBookCopies_entry.config(state='normal')
        viewBookYear_entry.config(state='normal')


          #clearing the entries to avoid writin on them twice
        viewBookTitle_entry.delete(0,'end')
        viewBookAuthor_entry.delete(0,'end')
        viewBookGenre_entry.delete(0,'end')
        viewBookCopies_entry.delete(0,'end')
        viewBookYear_entry.delete(0,'end')

        #retrieving info from database to display it 

        title = myCursor.execute('SELECT Title FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        author = myCursor.execute('SELECT Author FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        genre = myCursor.execute('SELECT Genre FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        copies = myCursor.execute('SELECT No_Of_Copies FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        year = myCursor.execute('SELECT year_of_publication FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        res = myCursor.execute('SELECT Restriction FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]


        #inserting retrieved info in the entries
        viewBookTitle_entry.insert('0',title)
        viewBookAuthor_entry.insert('0',author)
        viewBookGenre_entry.insert('0',genre)
        viewBookCopies_entry.insert('0',copies)
        viewBookYear_entry.insert('0',year)
        viewIsBookRestricted.set(res)

        

        #disabling the entries to avoid editing
        viewBookTitle_entry.config(state='disabled')
        viewBookAuthor_entry.config(state='disabled')
        viewBookGenre_entry.config(state='disabled')
        viewBookCopies_entry.config(state='disabled')
        viewBookYear_entry.config(state='disabled')
        viewCheck.config(state='disabled')


        db.commit()
        db.close() 



    #_________________________________BORROW BOOK_________________________________________________
    def borrowBook(name,id,isbn,copies,period,terms):


        db = sqlite3.connect(path)
        myCursor = db.cursor()

        name = name.get().capitalize()
        id = id.get()
        isbn = isbn.get()
        copies = copies.get()
        period = period.get()
        terms = terms.get()


        #get the current date
        dateToday = date.today()

        


        #input validation
        if name == '' or id == '' or isbn == '' or copies == '' or period == '':
            messagebox.showerror('Error','Please fill in all the spaces!')
            return
        
        elif len(id) < 8 or len(id) > 8:
            messagebox.showwarning('Error','The ID should be 8 numbers')
            return


        #check that user enters integers in id,copies and period field
        try:
            id = int(id)
            copies = int(copies)
            period = int(period)

            #convert the period week to days
            converted_period  = period * 7

        except(ValueError):
            messagebox.showerror('Error',"The 'Member ID', 'No. Of Copies' and 'Borrow Period' should contain numbers only!")
            return
        
        #check for 0 input
        if copies == 0 or period == 0:
            messagebox.showerror('Error',"The 'Number Of Copies' and 'period' cannot be 0")
            return


        #check that they agree to terms and conditions
        if terms != 'yes':
            agree = messagebox.askokcancel('Error','You must agree to the terms and conditions,agree and continue?')
            if agree:
                agreeToTerms.set('yes')
                return
            else:
                return


        #checking whether the borrowing person is a member
        getMemberIds = myCursor.execute('SELECT id FROM Member').fetchall()
        existingMembers = [id[0] for id in getMemberIds]


        if id not in existingMembers:
             #ask if to add member
            add = messagebox.askokcancel('confirm','This person is not a member,would you like to add them?')

            if add:
                #inserting the current input in the name and id fields in their respective fields in add member page
                addMemberName_entry.insert('0',name)
                addMemberID_entry.insert('0',id)

                switchPages(borrowBook_page,AddMember_page,borrowBookContext_frame)
                return
            else:
                return
        
        #if id exists,check whether the id corresponds with entered name
        elif id in existingMembers:
            memName = myCursor.execute('SELECT name FROM Member WHERE id = ?',(id,)).fetchone()[0]

            if name != memName:
                messagebox.showerror('Error','This ID does not belong to this member,Please check the name')
                borrowerName_entry.delete(0,'end')
                return







        #checking whether the borrowed book exists and asking whether to add it
        getAllBooks = myCursor.execute('SELECT ISBN FROM Book').fetchall()
        existingBooks = [book[0] for book in getAllBooks]


        if isbn not in existingBooks:
            add = messagebox.askokcancel('Error','Book does not exist,Do you want to add it?')

            #if user chose add it
            if add:
                 
                switchPages(viewBook_page,AddBook_page,editBookContext_frame)
                addBookISBN_entry.insert('0',isbn)
                return
            else:
                return


        #check whether member has any existing borrowed books they've not returned
        getBorrowers = myCursor.execute('SELECT borrower_id FROM Borrowed').fetchall()
        existingBorrowers = [id[0] for id in getBorrowers]

        if id in existingBorrowers:
            #getting the borrowed books info to display to the user
             #getting the book title from Book table using the book ISBN in the Borrowed table
            borrowed_isbn = myCursor.execute('SELECT isbn FROM Borrowed WHERE borrower_id = ?',(id,)).fetchone()[0]
            borrow_title = myCursor.execute('SELECT Title FROM Book WHERE ISBN = ?',(borrowed_isbn,)).fetchone()[0]
            borrow_copies = myCursor.execute('SELECT borrowed_copies FROM Borrowed WHERE borrower_id = ?',(id,)).fetchone()[0]
            
            #displaying the retrieved info in a pop up
            messagebox.showerror('Error',f'cannot borrow since the member has not returned {borrow_copies} copy(s) of {borrow_title} borrowed on {dateToday}.')
            clear(borrowBookContext_frame)
            return
    

        #checking whether book is restricted to patrions only
        bookRestriction = myCursor.execute('SELECT Restriction FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        isBorrowerPatrion = myCursor.execute('SELECT isPatrion FROM Member WHERE id = ?',(id,)).fetchone()[0]
        

        if bookRestriction == 'yes' and isBorrowerPatrion == 'no':
            sign = messagebox.askokcancel('Error','This book is restricted to patrions only,sign up member for patrion?')

            if sign:
                switchPages(borrowBook_page,editMember_page,borrowBookContext_frame)
                editMemberID_entry.insert('0',id)
                return
            else:
                return
            
         #checking whether a non patrion has more than 1 copies
        elif isBorrowerPatrion == 'no' and copies > 1:
            sign2 = messagebox.askokcancel('Error','A non patrion can only borrow 1 copy,sign up member for patrion?')
            
            if sign2:
                editIsPatrion.set('yes')
                switchPages(borrowBook_page,editMember_page,borrowBookContext_frame)
                return
            else:
                borrowedBookCopies_entry.delete(0,'end')
                return
            
         #checking whether a non patrion requests the correct borrow period
        elif isBorrowerPatrion == 'no' and period > 2:
            sign3 = messagebox.askokcancel('Error','A non patrion can only borrow for a maximum of 1 week,sign up member for patrion?')
            
            if sign3:
                editIsPatrion.set('yes')
                switchPages(borrowBook_page,editMember_page,borrowBookContext_frame)
                return
            else:
                borrowedPeriod_entry.delete(0,'end')
                return
            
         #check whether a patrion has overborrowed
        elif isBorrowerPatrion ==  'yes' and copies > 50:
            messagebox.showinfo('Error','You can only only borrow a maximum of 50 books')
            borrowedBookCopies_entry.delete(0,'end')
            return
        
         #check whether a patrion has exceeded period
        elif isBorrowerPatrion ==  'yes' and period > 4:
            messagebox.showinfo('Error','You can only only borrow for maximum of period of 4 weeks.')
            borrowedPeriod_entry.delete(0,'end')
            return

         
        #check whether the library has enough copies of the borrowed books
         #get the number of copies of the book from Book table
        copiesNumber = myCursor.execute('SELECT No_Of_Copies FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
       

          #check if copies are available
        if copies > int(copiesNumber):
            messagebox.showerror('Error',f'cannot borrow {copies} copy(s),at the moment you can only borrow a maximum of {copiesNumber}.')
            return
                

            
        #writing to database

         #get the due date by adding
        #retrieve title of borrowed book for confirmation
        title = myCursor.execute('SELECT Title FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]


         #get the due date
        due_date = dateToday + timedelta(converted_period)

        #getting the remaininng number of copies after borrowing
        oldNo_ofCopies = myCursor.execute('SELECT No_Of_Copies FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        newNo_ofCopies = oldNo_ofCopies - copies


        confirm = messagebox.askokcancel('confirm',f'confirm borrowing {copies} copy(s) of {title} by {name} ID Number {id} for a period of {period} week(s).')

        if confirm:
            myCursor.execute('INSERT INTO Borrowed VALUES(null,?,?,?,?,?,?,?)',(isbn,id,copies,converted_period ,dateToday,due_date,loggedInAdm_id))
            clear(borrowBookContext_frame)
            messagebox.showinfo('done',f'Done,please return the book(s) by {due_date}.')

            #update the Number of copies in Book table
            myCursor.execute('UPDATE Book SET No_Of_Copies = ? WHERE ISBN = ?',(newNo_ofCopies,isbn,))
        
        db.commit()
        db.close() 





     #_________________________________CHECK FOR OVERDUE BOOKS_________________________________________________
      #this functions runs every time the program is ran and checks for overdue books and add them in the overdue table
   
   
   
    #_________________________________CHECKS FOR OVERDUES________________________________________________
    def update_overdue():
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        #get current date
        dateToday = date.today()


        #get all member in borrowed table
        getAllBorrowed = myCursor.execute('SELECT borrower_id FROM Borrowed').fetchall()
        allBorrowed = [id[0] for id in getAllBorrowed]

        #loop through each member in borrowed and check whether they are overdue
        for id in allBorrowed:
            #getting the current member's info
             #getting borrowed book isbn
            isbn = myCursor.execute('SELECT isbn FROM Borrowed WHERE borrower_id = ?',(id,)).fetchone()[0]

            #getting the checkout id
            checkout_id = myCursor.execute('SELECT checkout_id FROM Borrowed WHERE borrower_id = ?',(id,)).fetchone()[0]
             

             #getting the member phone
            phone =  myCursor.execute('SELECT phone_number FROM Member WHERE id = ?',(id,)).fetchone()[0]

             #getting the due date
            due_date =  myCursor.execute('SELECT due_date FROM Borrowed WHERE borrower_id = ?',(id,)).fetchone()[0]


            #converting the text dates to datetime object
            due_date = datetime.strptime(due_date,'%Y-%m-%d').date()
            
            #the fine is 300kes
            fine = 300

            #it the current date is greater than the due date,add member to overdue table
            if dateToday > due_date:

                #get members in overdue to avoid adding a member twice
                getOver = myCursor.execute('SELECT member_id from Overdue').fetchall()
                overExist = [id[0] for id in getOver]

                if id not in overExist:
                    #adding member to overdue table
                    myCursor.execute('INSERT INTO Overdue VALUES(?,?,?,?,?)',(id,phone,isbn,checkout_id,fine,))
                    
            
            db.commit()
            db.close()



    update_overdue()



    #_________________________________RETURN BOOK_________________________________________________
    def returnBook(name,id,isbn,copies,rating):
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        name = name.get().capitalize()
        id = id.get()
        isbn = isbn.get()
        copies = copies.get()
        rating = rating.get()

        #getting todays date
        dateToday = date.today()


        #input validation
        if name == '' or id == '' or isbn == '' or copies == '' or rating == '':
            messagebox.showerror('Error','Please fill in all the spaces!')
            return
        
        elif len(id) < 8 or len(id) > 8:
            messagebox.showwarning('Error','The ID should be 8 numbers')
            return


        #check that user enters integers in id,copies and period field
        try:
            id = int(id)
            copies = int(copies)
            rating = int(rating)

        except(ValueError):
            messagebox.showerror('Error',"The 'Member ID', 'No. Of Copies' and 'rating' should contain numbers only!")
            return
        
        #check for 0 input
        if copies == 0 or rating == 0 or copies == -1 or rating == -1:
            messagebox.showerror('Error',"The 'Number Of Copies' and 'rating' cannot be 0.")
            return


        #check if rating greater than 5
        if rating > 5:
            messagebox.showerror('Error',"The 'rating' cannot be greater than 5.")
            return


        #checking whether the person is a member
        getMemberIds = myCursor.execute('SELECT id FROM Member').fetchall()
        existingMembers = [id[0] for id in getMemberIds]


        if id not in existingMembers:
            messagebox.showerror('Error','This person is not a member!.')
            return 
        
        #if id exists,check whether the id corresponds with entered name
        elif id in existingMembers:
            memName = myCursor.execute('SELECT name FROM Member WHERE id = ?',(id,)).fetchone()[0]

            if name != memName:
                messagebox.showerror('Error','This ID does not belong to this member,Please check the name')
                returnerName_entry.delete(0,'end')
                return



        #checking whether the member had borrowed a book
         #get the borrowed books
        getBorrowedIds = myCursor.execute('SELECT borrower_id FROM Borrowed').fetchall()
        existingBorrowed = [id[0] for id in getBorrowedIds]

        
         #get the book in Books
        getAllBooks = myCursor.execute('SELECT ISBN FROM Book').fetchall()
        existingBooks = [book[0] for book in getAllBooks]


        if id not in existingBorrowed:
            messagebox.showwarning('confirm','This member had not borrowed a book.')
            return 
        
        #checking whether the book exists

        if isbn not in existingBooks:
            messagebox.showerror('Error','Book does not exists.')
            return


        #check whether member has returned the correct book
         #getting the isbn of the book they had borrowed
        borrowed_book_isbn = myCursor.execute('SELECT isbn FROM Borrowed WHERE borrower_id = ?',(id,)).fetchone()[0]
        
         #getting the number of copies they had borrowed
        borrowed_copies = myCursor.execute('SELECT borrowed_copies FROM Borrowed WHERE borrower_id = ?',(id,)).fetchone()[0]

        #check correct book?
        if isbn != borrowed_book_isbn:
            #getting the title of the book they had borrowed and also member name
            title = myCursor.execute('SELECT Title FROM Book WHERE ISBN = ?',(borrowed_book_isbn,)).fetchone()[0]
            messagebox.showerror('Error',f'{name} had not borrowed this book.They had borrowed {borrowed_copies} copies of {title}')
            return

        #check whether its correct no of borrowed copies
        elif copies != borrowed_copies:
            messagebox.showerror('Error',f'{name} had borrowed {borrowed_copies} copies.')
            return


        #check whether member is overdue
          #using a try block  to catch error where the table is empty  
        try:
            #getting all overdue members
            getOverdue = myCursor.execute('SELECT member_id from Overdue').fetchall()
            overdueMembs = [mem[0] for mem in getOverdue]

            #get fine
            fine =  myCursor.execute('SELECT fine from Overdue').fetchone()[0]

            if id in overdueMembs:
                paid = messagebox.askyesno('Error',f'Book borrowed by {name} is overdue,the fine is {fine}.Failure to pay the fine immeadiately will result suspension of membership.Has the user paid the fine?')

                #if fine paid
                if fine:
                    myCursor.execute('DELETE FROM Overdue WHERE member_id = ?',(id,))
                else:
                    messagebox.showwarning('Suspension','Membership has be suspended for {name},ID number {id}.')

        except(TypeError):
            pass #continue since this error means that the table is empty

        #update number of copies of the returned book and also add to returned table and delete fro borrowed table

         #the current number of copies  from book and add it onto the returned number of books
          #update the number of copies in the Book table

        updated_copies = myCursor.execute('SELECT No_Of_Copies FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0] 
        updated_copies += copies

        myCursor.execute('UPDATE Book SET No_Of_Copies = ? WHERE ISBN = ?',(updated_copies,isbn))


        #CALCULATE AND UPDATE BOOK RATING 
         #get current rating and number of ratings
        currRating = myCursor.execute('SELECT rating FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]
        curr_NumbOf_Ratings = myCursor.execute('SELECT number_of_ratings FROM Book WHERE ISBN = ?',(isbn,)).fetchone()[0]

         #add numb of ratings to include this 'rater'
        curr_NumbOf_Ratings += 1

         #calculate rating;total value of ratings divided by the total number of ratings
        updated_rating = (currRating + rating) // ( curr_NumbOf_Ratings)

        #to make sure the rating is not zero
        if updated_rating == 0:
            updated_rating += 1
        

        #update the book table
        myCursor.execute('UPDATE Book SET rating  = ? WHERE ISBN = ?',(updated_rating,isbn))
        myCursor.execute('UPDATE Book SET number_of_ratings  = ? WHERE ISBN = ?',(curr_NumbOf_Ratings,isbn))
        



         #add book to returned table
           #retrieve the required info from other tables
        checkout_id = myCursor.execute('SELECT checkout_id FROM Borrowed WHERE isbn = ?',(isbn,)).fetchone()[0]
        myCursor.execute('INSERT INTO Returned VALUES(null,?,?,?,?,?,?)',(checkout_id,id,isbn,copies,dateToday,rating,))

        #delete book from borrowed table
        myCursor.execute('DELETE FROM Borrowed WHERE isbn = ?',(isbn,))

        #show success and ask user whether to borrow another book
        borrow = messagebox.showinfo('done','Book check-in succesfull.Would you like to borrow another book?')
        db.commit()
        db.close()  

            #clear the input fields
        clear(returnBookContext_frame)

         #if yes
        if borrow:
            switchPages(returnBook_page,borrowBook_page,borrowBookContext_frame)
            return
        else:
            return




    #______________________FILTERED SEARCH___________________________________________
    def filterSearch(filtered,selected,filter_input):
        db = sqlite3.connect(path)
        myCursor = db.cursor()

        #getting what is being filtered;book or member
        filtered = filtered.get()

        #the selected option in the drop down
        selected = selected.get()

        #getting the search input
        filter_input = filter_input.get()
        

        #input validation
        if filter_input == '' and selected != 'Patrion':
            messagebox.showerror('Error','Please enter filter value!')
            return
              
        
       
        #display the various filter results using a case
        match selected:

            #filter book using author
            case 'Author':
                #enabling the Text to insert the search results and then disbaling after to avoid editting
                results_text.config(state='normal')
                results_text.delete('1.0',END)

                filter_input = filter_input.capitalize()
                #get inputted author name
                name = filter_input

                #check whether author exists
                getAuthors = myCursor.execute('SELECT Name FROM Author').fetchall()
                existingAuthors = [id[0] for id in getAuthors]
                
                if name not in existingAuthors:
                    messagebox.showerror('Error','Author does not exist!')
                    return
                
                #display books if author exists using foreign key auth_id in Book
                 #get this author id
                id = myCursor.execute('SELECT id FROM Author WHERE Name = ?',(name,)).fetchone()[0]
                
                #get books under this author
                hisBooks = myCursor.execute('SELECT * FROM Book WHERE auth_id = ?',(id,)).fetchall()
                foundBooks = [book[0] for book in hisBooks]

                #if there are no books
                if len(foundBooks) < 1:
                    messagebox.showerror('Error',f'There are available books authored by {name}.')
                    return

                count = 0
                for book in foundBooks:
                    count += 1
                    results_text.insert('end',f'{count}. {book} \n')

                #disbling the Text to avoid editting
                results_text.config(state='disabled')


        
            #filter book using genre
            case 'Genre':
                #enabling the Text to insert the search results and then disbaling after to avoid editting ,also clearing
                results_text.config(state='normal')
                results_text.delete('1.0',END)



                filter_input = filter_input.capitalize()
                #get inputted author name
                genre = filter_input

                #check whether author exists
                getGenres = myCursor.execute('SELECT Genre FROM Book').fetchall()
                existingAuthors = [id[0] for id in getGenres]
                
                if genre not in existingAuthors:
                    messagebox.showerror('Error',f"We currently don't have any {genre} books!.")
                    return
            
                # get and display books with this genre
                getBooks_genre = myCursor.execute('SELECT * FROM Book WHERE Genre = ?',(genre,)).fetchall()
                genreBooks = [book[0] for book in getBooks_genre]

                count = 0
                for book in genreBooks:
                    count += 1
                    results_text.insert('end',f'{count}. {book} \n')

                #disbling the Text to avoid editting
                results_text.config(state='disabled')


            #filter book using genre
            case 'Rating':
                #enabling the Text to insert the search results and then disbaling after to avoid editting ,also clearing
                results_text.config(state='normal')
                results_text.delete('1.0',END)

                #get inputted author name
                rating = filter_input               

                #validate that the rating is a number
                try:
                    rating = int(rating)

                except(ValueError):
                    messagebox.showerror('Error','The rating should be a number from 1-5!')
                    return

                #check that its not less than 1 or > than 5
                if rating < 1 or rating > 5:
                    messagebox.showerror('Error','The rating should be a number 1-5!')
                    return

                # get and display books with rating above inputted rating
                getBooks_rating = myCursor.execute('SELECT * FROM Book WHERE rating > ?',(rating,)).fetchall()
                ratingBooks = [book[0] for book in getBooks_rating]

                #check if there is no such rated book
                if len(ratingBooks) < 1:
                    messagebox.showerror('Error','There is no book with such rating!')
                    return
                
                count = 0
                for book in ratingBooks:
                    count += 1
                    results_text.insert('end',f'{count}. {book} \n')

                #disabling the Text to avoid editting
                results_text.config(state='disabled')



            #filter patrion members
            case 'Patrion':
                #enabling the Text to insert the search results and then disbaling after to avoid editting ,also clearing
                results_text.config(state='normal')
                results_text.delete('1.0',END)

                #get patrions from Member table
                getPatrions = myCursor.execute('SELECT * FROM Member WHERE isPatrion = ?',('yes',)).fetchall()
                patrionMembers = [member[0] for member in getPatrions]
                
                #counter number
                count = 0 

                for member in patrionMembers:
                    count += 1
                    results_text.insert('end',f'{count}. {member} \n')
                    

                #disabling the Text to avoid editting
                results_text.config(state='disabled')


            
            #filter members by ID
            case 'ID':
                #enabling the Text to insert the search results and then disbaling after to avoid editting ,also clearing
                results_text.config(state='normal')
                results_text.delete('1.0',END)

                id = filter_input


                #check that its not less than 1 or > than 5
                if len(id) < 8 or len(id) > 8:
                    messagebox.showerror('Error','The ID should be a maximum of 8 numbers!')
                    return


                #validate that the rating is a number
                try:
                    id = int(id)

                except(ValueError):
                    messagebox.showerror('Error','The id should be a number')
                    return


                #check if member exists
                getMembs = myCursor.execute('SELECT id FROM Member').fetchall()
                existingMembs = [id[0] for id in getMembs]

                if id not in existingMembs:
                    messagebox.showerror('Error','Member does not exist!')
                    return
                
                #get the member
                member = myCursor.execute('SELECT name FROM Member WHERE id = ?',(id,)).fetchone()[0]

                results_text.insert('end',f'1. {member}')

                #disabling the Text to avoid editting
                results_text.config(state='disabled')            

               


        db.close()





    #______________________ALERT THE OVERDUE MEMBERS ABOUT RETURNING BOOKS___________________________________________
    def alertOverdue():
        db = sqlite3.connect(path)
        myCursor = db.cursor()
                                

        #get the phone numbers of members in overdue table
        getOverdue = myCursor.execute('SELECT member_phone FROM Overdue').fetchall()
        overduePhone = [phone[0] for phone in getOverdue]

        #if there are no overdues
        if len(overduePhone) < 1:
            messagebox.showerror('No overdues','There are no overdues!')
            return


        #loop through the numbers sending messages to them
        for number in overduePhone:

            #used to send messages using twilio's API
            from twilio.rest import Client

            #get member name
            name = myCursor.execute('SELECT name FROM Member WHERE phone_number = ?',(number,)).fetchone()[0]

            #get title of borrowed book
            getISBN = myCursor.execute('SELECT isbn FROM Overdue WHERE member_phone = ?',(number,)).fetchone()[0]
            title = myCursor.execute('SELECT Title FROM Book WHERE ISBN = ?',(getISBN,)).fetchone()[0]

            #THE API KEYS
            account_sid = 'AC6eb53912dda5989286106e405c7c3a8b'
            auth_token = '91458d00380ba01d61e63f9cd5cf92ac'
            client = Client(account_sid, auth_token)

            #number to send message to,prefixing the country code since the api required it
            to_number = '+254' + str(number)

            #the number used to send the messages,(trial number)
            from_number = '+12545002268'


            message_body = f'Greetings {name},this is a reminder to return the book {title}.A fine of kes 300 will be charged during check in.Good day!.'


            message = client.messages.create(
                to=to_number,
                from_=from_number,
                body=message_body)

        messagebox.showinfo('Done','Members alerted!')

        db.close() 




    #++++++++++++++++_____DATABASE FUNCTIONS END_____+++++++++++++++++








    #the background for the content window,using pillow to open,resize and convert the image to tkinter's photo image
    image_path = r"C:\Users\judew\Documents\code projects\python\PYTHONPROJECT\libraryImage.png"
    bg_image = Image.open(image_path).resize((400,400),Image.LANCZOS)
    converted_image_startup = ImageTk.PhotoImage(bg_image)
    converted_image = ImageTk.PhotoImage(bg_image)




    LoadLogo = Image.open(image_path).resize((80,80),Image.LANCZOS)
    logoImage = ImageTk.PhotoImage(LoadLogo)


    #function to display tkinter message boxes
    def displayMessage(head,msg):
        messagebox.showinfo(head,msg)

 
    #-------------------MASTER LOGIN PAGE START-----------------------------------
    masterLogin_page = Frame(root,width=900,height=600,background='#184769')
    
    masterLoginStartup_label = Label(masterLogin_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)


    

    #----THE MENU FRAME START------------------------------
    masterLoginMenu_frame = Frame(masterLogin_page,background='#0C173F',width=200,height=530).place(x=10,y=60)

    masterCr_tools_text = Label(masterLogin_page,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=20,y=60)

    masterLoginExit_btn = Button(masterLogin_page,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=30,y=110)


    #----THE MENU FRAME END------------------------------


    #----THE CONTEXT FRAME START------------------------------

    masterLoginContext_frame = Frame(masterLogin_page,background='#001345',width=650,height=530)
    masterLoginContext_frame.place(x=220,y=60)

    
    #the label holding the logo image
    image_label = Label(masterLogin_page,width=80,height=80,image=logoImage)
    image_label.place(x=270,y=90)

    loginMasterTop_label = Label(masterLogin_page,text='Login Master Admin',foreground='white',background='#001345',font=('Arial',20)).place(x=420,y=100)


    #name fields
    masterLoginName_label = Label(masterLogin_page,text='Master Name',font=('Arial',15),background='#001345',foreground='white').place(x=230,y=240)
    masterLoginName_entry = Entry(masterLogin_page,bg='#0080ff',width=25,font=('Arial',20))
    masterLoginName_entry.place(x=420,y=240,)


    #password fields
    masterLoginPass_label = Label(masterLogin_page,text='Master Password',font=('Arial',15),background='#001345',foreground='white').place(x=230,y=310)
    masterLoginPass_entry = Entry(masterLogin_page,bg='#0080ff',width=25,font=('Arial',20))
    masterLoginPass_entry.place(x=420,y=310)


    #login button
    masterCreate_btn = Button(masterLogin_page,text='Login',background='#3acaff',width=20,font=('Arial',10),command= lambda : loginMaster(masterLoginName_entry,masterLoginPass_entry)).place(x=500,y=400)

    #----THE CONTEXT FRAME END------------------------------



    #masterLogin_page.pack(fill='both',expand=True)


    #-------------------MASTER LOGIN PAGE END-------------------------------------













    #-------------------MASTER ADMIN OPTIONS PAGE START-------------------------------------

    masterOptions_page = Frame(root,width=900,height=600,background='#184769')
    
    masterOptStartup_label = Label(masterOptions_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)



    
    #----THE MENU FRAME START------------------------------
    masterOptionsMenu_frame = Frame(masterOptions_page,background='#0C173F',width=200,height=530)#packed bottom of page creation course errors

    masteropt_tools_text = Label(masterOptionsMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=20,y=20)

    #buttons
    masterOptsNewAdmn_btn = Button(masterOptionsMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Create Admin',borderwidth=4,command = lambda : switchPages(masterOptions_page,createAdmin_page,masterOptionsContext_frame)).place(x=35,y=70)

    masterOptsEditAdmn_btn = Button(masterOptionsMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Delete an Admin',borderwidth=4,command = lambda : switchPages(masterOptions_page,deleteAdmin_page,masterOptionsContext_frame)).place(x=35,y=130)

    masterOptsDelAdmn_btn = Button(masterOptionsMenu_frame,activebackground='brown',background='#80ff7b',width=15,font=('ARIAL',10),text='Startup page',borderwidth=4,command=lambda : switchPages(masterOptions_page,startup_page,masterOptionsContext_frame)).place(x=35,y=190)


    masterOptsDelAdmn_btn = Button(masterOptionsMenu_frame,activebackground='brown',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=35,y=250)





    #----THE MENU FRAME END------------------------------



    #-------CONTEXT FRAME START---------------------
    
    
    masterOptionsContext_frame = Frame(masterOptions_page,background='#001345',width=650,height=530)#packed bottom of page creation course errors

    masterOptsTop_label = Label(masterOptionsContext_frame,text='Edit self or other admins',foreground='white',background='#001345',font=('Arial',20)).place(x=150,y=50)

    
    #master admin name
    masterOptsDispName_label = Label(masterOptionsContext_frame,width=10,text='John Doe',foreground='white',background='blue',font=('Arial',15))
    masterOptsDispName_label.place(x=490,y=30)

    #the label holding the logo image,defined in the creation of the homepage
    image_label = Label(masterOptionsContext_frame,width=400,height=400,image=converted_image_startup)
    image_label.place(x=120,y=120)


    #packing the diffrent frames individually since they have some errors while packing together.

    #masterOptions_page.pack() 
    #masterOptionsContext_frame.place(x=240,y=60)
    #masterOptionsMenu_frame.place(x=10,y=60)





    #-------------------MASTER ADMIN OPTIONS PAGE END---------------------------------------














    #-------------------CREATE MASTER ADMIN PAGE START---------------------------------------



    createMasterAdmin_page = Frame(root,background='#184769')
    

    masterAdmin_label = Label(createMasterAdmin_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    masterCreateMenu_frame = Frame(createMasterAdmin_page,background='#0C173F',width=200,height=530)

    masterCreateMenu_tools_text = Label(masterCreateMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=15,y=30)

    #-------MENU FRAME BUTTONS START-------------------
    createMaster_startup_btn = Button(masterCreateMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Startup page',borderwidth=4,command=lambda : switchPages(createMasterAdmin_page,startup_page,CreateMasterContext_frame)).place(x=40,y=100)



    master_exit_btn = Button(masterCreateMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=5,command=quit).place(x=40,y=160)




    #-------CONTEXT FRAME START---------------------

    #the background for the content window,using pillow to open,resize and convert the image to tkinter's photo image
    bg_logo_image = Image.open(r"C:\Users\judew\Documents\code projects\python\PYTHONPROJECT\libraryImage.png").resize((80,80),Image.LANCZOS)
    converted_image = ImageTk.PhotoImage(bg_logo_image)
    

    CreateMasterContext_frame = Frame(createMasterAdmin_page,background='#001345',width=650,height=530)

    createMasterTop_label = Label(CreateMasterContext_frame,text='Create Master Admin',foreground='white',background='#001345',font=('Arial',20)).place(x=180,y=60)

    #the label holding the logo image
    image_label = Label(CreateMasterContext_frame,width=80,height=80,image=converted_image)
    image_label.place(x=20,y=30)


    masterCreateName_label = Label(CreateMasterContext_frame,text='Master Admin Full Name',font=('Arial',15),background='#001345',foreground='white').place(x=20,y=170)
    masterCreateName_entry = Entry(CreateMasterContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    masterCreateName_entry.place(x=260,y=170,)


    masterCreatePass_label = Label(CreateMasterContext_frame,text='Master Password',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=250)
    masterCreatePass_entry = Entry(CreateMasterContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    masterCreatePass_entry.place(x=260,y=250)


    #password confirmation
    masterCreateConfirmPass_label = Label(CreateMasterContext_frame,text='Confirm Password',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=340)
    masterCreateConfirmPass_entry = Entry(CreateMasterContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    masterCreateConfirmPass_entry.place(x=260,y=340)


    masterCreate_btn = Button(CreateMasterContext_frame,text='Create',background='#3acaff',width=20,font=('Arial',10),command= lambda : addMaster(name=masterCreateName_entry,paswd=masterCreatePass_entry,confirmPass=masterCreateConfirmPass_entry)).place(x=260,y=410)




    #createMasterAdmin_page.pack(fill='both',expand=True)
    CreateMasterContext_frame.place(x=220,y=60)
    masterCreateMenu_frame.place(x=10,y=60)
    








    #-------------------CREATE MASTER ADMIN PAGE END---------------------------------------











    #-------------------DELETE ADMIN PAGE START---------------------------------------



    deleteAdmin_page = Frame(root,background='#184769')
    

    deleteAdmin_label = Label(deleteAdmin_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    deleteAdminMenu_frame = Frame(deleteAdmin_page,background='#0C173F',width=200,height=530)

    masterCreateMenu_tools_text = Label(deleteAdminMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=13,y=20)

    deleteAdmin_startup_btn = Button(deleteAdminMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Startup page',borderwidth=4,command=lambda : switchPages(masterOptions_page,startup_page,masterOptionsContext_frame)).place(x=30,y=80)

    delAdm_exit_btn = Button(deleteAdminMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=5,command=quit).place(x=30,y=130)




    #----THE CONTEXT MENU FRAME START------------------------------
    deleteAdminContext_frame = Frame(deleteAdmin_page,background='#001345',width=650,height=530)#packed bottom of page creation course errors

    delAdmTop_label = Label(deleteAdminContext_frame,text='Delete an admin',foreground='white',background='#001345',font=('Arial',20)).place(x=230,y=50)



    delAdminName_label = Label(deleteAdminContext_frame,text='Admin ID',font=('Arial',15),background='#001345',foreground='white').place(x=30,y=140)
    delAdminName_entry = Entry(deleteAdminContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    delAdminName_entry.place(x=180,y=140)


    trasnferAdminName_label = Label(deleteAdminContext_frame,text='Transfer their records\nto this admin;ID',font=('Arial',10),background='#001345',foreground='white').place(x=30,y=220)
    transfer_entry = Entry(deleteAdminContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    transfer_entry.place(x=180,y=220)


    deleteAdmin_btn = Button(deleteAdminContext_frame,text='Delete',background='#3acaff',width=20,font=('Arial',10),command = lambda : deleteAdmin(delAdminName_entry,transfer_entry))
    deleteAdmin_btn.place(x=240,y=290)





    #deleteAdmin_page.pack(fill='both',expand=True)
    deleteAdminMenu_frame.place(x=10,y=50)
    deleteAdminContext_frame.place(x=220,y=50)

    #-------------------DELETE ADMIN PAGE END---------------------------------------













    #-------------------CREATE ADMIN PAGE START---------------------------------------


    createAdmin_page = Frame(root,background='#184769')
    

    createAdmin_label = Label(createAdmin_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    createAdminMenu_frame = Frame(createAdmin_page,background='#0C173F',width=200,height=530)

    masterCreateMenu_tools_text = Label(createAdminMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)

    #-------MENU FRAME BUTTONS-------------------
    createAdmin_startup_btn = Button(createAdminMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(createAdmin_page)).place(x=25,y=80)

    createAdmin_exit_btn = Button(createAdminMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)



    #---------CONTEXT WINDOW-----------------------------------
    createAdminContext_frame = Frame(createAdmin_page,background='#001345',width=650,height=530)

    createAdminTop_label = Label(createAdminContext_frame,text='Create Admin',foreground='white',background='#001345',font=('Arial',20)).place(x=250,y=60)


    createAdminName_label = Label(createAdminContext_frame,text='Admin Name',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=150)
    CreateAdminName_entry = Entry(createAdminContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    CreateAdminName_entry.place(x=230,y=150,)

    createAdminId_label = Label(createAdminContext_frame,text='Admin ID Number',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=220)
    CreateAdminId_entry = Entry(createAdminContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    CreateAdminId_entry.place(x=230,y=220,)


    createAdminPass_label = Label(createAdminContext_frame,text='Admin Password',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=290)
    CreateAdminPass_entry = Entry(createAdminContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    CreateAdminPass_entry.place(x=230,y=290)


    #checkbox
    #checkbox variable
    rights = StringVar()
    rights.set('no')#setting the value of the checkbox to off after loading

    Checkbutton(createAdminContext_frame,text='This admin can create or edit other admins.',variable=rights,onvalue='yes',offvalue='no',font=('Arial',10),background='#001345',bg='white').place(x=250,y=350)


    addAdmin_btn = Button(createAdminContext_frame,text='Create',background='#3acaff',width=20,font=('Arial',10),command = lambda : addAdmin(name=CreateAdminName_entry,id=CreateAdminId_entry,password=CreateAdminPass_entry,right=rights))
    addAdmin_btn.place(x=260,y=420)




    #createAdmin_page.pack(fill='both',expand=True)
    createAdminMenu_frame.place(x=10,y=50)
    createAdminContext_frame.place(x=220,y=50)

    #-------------------CREATE ADMIN PAGE END---------------------------------------













    #-------------------LOGIN ADMIN PAGE START---------------------------------------

    loginAdmin_page = Frame(root,background='#184769')
    

    loginAdmin_label = Label(loginAdmin_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    loginAdminMenu_frame = Frame(loginAdmin_page,background='#0C173F',width=200,height=530)

    masterCreateMenu_tools_text = Label(loginAdminMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)

    #-------MENU FRAME BUTTONS-------------------
    loginAdmin_startup_btn = Button(loginAdminMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Startup page',borderwidth=4,command=lambda : switchPages(loginAdmin_page,startup_page,loginAdminContext_frame)).place(x=25,y=80)

    loginAdmin_exit_btn = Button(loginAdminMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)


    #---------CONTEXT WINDOW-----------------------------------
    loginAdminContext_frame = Frame(loginAdmin_page,background='#001345',width=650,height=530)

    loginAdminTop_label = Label(loginAdminContext_frame,text='Login Admin',foreground='white',background='#001345',font=('Arial',20)).place(x=250,y=60)


    loginAdminName_label = Label(loginAdminContext_frame,text='Admin Name',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=150)
    loginAdminName_entry = Entry(loginAdminContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    loginAdminName_entry.place(x=230,y=150,)

    loginAdminPass_label = Label(loginAdminContext_frame,text='Password',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=220)
    loginAdminPass_entry = Entry(loginAdminContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    loginAdminPass_entry.place(x=230,y=220,)


    LoginAdmin_btn = Button(loginAdminContext_frame,text='Log In',background='#3acaff',width=20,font=('Arial',10),command= lambda : loginAdmin(loginAdminName_entry,loginAdminPass_entry))
    LoginAdmin_btn.place(x=260,y=320)






    #loginAdmin_page.pack(fill='both',expand=True)
    loginAdminMenu_frame.place(x=10,y=50)
    loginAdminContext_frame.place(x=220,y=50)

    #-------------------LOGIN ADMIN PAGE END---------------------------------------








    #-------------------ADMIN HOMEPAGE START---------------------------------------
    
    AdminHome_page = Frame(root,background='#184769')
    

    AdminHome_label = Label(AdminHome_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    AdminHomepageMenu_frame = Frame(AdminHome_page,background='#0C173F',width=200,height=530)

    admHomepageMenu_tools_text = Label(AdminHomepageMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)



    #----CONTEXT FRAME START-----------------------------
    adminHomepageContext_frame = Frame(AdminHome_page,background='#001345',width=650,height=530)

    admHomepagetop_label = Label(adminHomepageContext_frame,text='Welcome',foreground='white',background='#001345',font=('Arial',30)).place(x=230,y=25)

    
    #the admin icon
    ico_path = r'icons\admin.ico'
    admin_ico =  Image.open(ico_path).resize((30,30),Image.LANCZOS)
    admin_icon = ImageTk.PhotoImage(admin_ico)


        #the label holding the admin icon
    admIcon_label = Label(adminHomepageContext_frame,width=30,height=30,image=admin_icon).place(x=480,y=20)

    loggedAdm_label = Label(adminHomepageContext_frame,text='Admin Name',foreground='white',background='#001345',font=('Arial',15))
    loggedAdm_label.place(x=520,y=13)

    loggedAdm_idLabel = Label(adminHomepageContext_frame,text='278187287',foreground='white',background='#001345',font=('Arial',10))
    loggedAdm_idLabel.place(x=525,y=40)


    #the label holding the logo image
    admHomeimage_label = Label(adminHomepageContext_frame,width=400,height=400,image=converted_image_startup).place(x=130,y=90)



    #the drop down buttons

    #the manage members icon
    ico_path = r'icons\members.ico'
    members_ico =  Image.open(ico_path).resize((30,30),Image.LANCZOS)
    member_ico = ImageTk.PhotoImage(members_ico)


        #the label holding the admin icon
    memberIcon_label = Label(AdminHomepageMenu_frame,width=30,height=30,image=member_ico).place(x=10,y=70)

    #manage users
    userOpts = ['Add Member','Edit Member','Delete Member']
    user_selected = StringVar()
    user_selected.set('Manage Members')
    #command added later
    manageUsers_dropBtn = OptionMenu(AdminHomepageMenu_frame,user_selected,*userOpts,command= lambda _: navFromHome(AdminHome_page,'forward','manageUsers'))
    manageUsers_dropBtn.place(x=50,y=70)


    #the manage books icon
    ico_path = r'icons\books.ico'
    books_ico =  Image.open(ico_path).resize((30,30),Image.LANCZOS)
    books_ico = ImageTk.PhotoImage(books_ico)

        #the label holding the admin icon
    memberIcon_label = Label(AdminHomepageMenu_frame,width=30,height=30,image=books_ico).place(x=10,y=120)


    #manage books
    booksOpts = ['Add Book','Edit Book','Delete Book','View Book']
    book_selected = StringVar()
    book_selected.set('Manage Books')
    
    #command added later
    manageBooks_dropBtn = OptionMenu(AdminHomepageMenu_frame,book_selected,*booksOpts,command = lambda _: navFromHome(AdminHome_page,'forward','manageBooks')).place(x=50,y=120)


    #the manage checkins and outs icon
    ico_path = r'icons\checks.ico'
    checks_ico =  Image.open(ico_path).resize((30,30),Image.LANCZOS)
    checks_ico = ImageTk.PhotoImage(checks_ico)


        #the label holding the admin icon
    memberIcon_label = Label(AdminHomepageMenu_frame,width=30,height=30,image=checks_ico).place(x=10,y=170)


    #manage check-in and out
    checksOpts = ['Borrow Book','Return Book']
    checks_selected = StringVar()
    checks_selected.set('Check-in or out')
    
    #command added later
    manageChecks_dropBtn = OptionMenu(AdminHomepageMenu_frame,checks_selected,*checksOpts,command = lambda _: navFromHome(AdminHome_page,'forward','bookBorrow')).place(x=50,y=170)



    #the filter search icon
    ico_path = r'icons\search.ico'
    reports_ico =  Image.open(ico_path).resize((30,30),Image.LANCZOS)
    reports_ico = ImageTk.PhotoImage(reports_ico)


        #the label holding the admin icon
    memberIcon_label = Label(AdminHomepageMenu_frame,width=30,height=30,image=reports_ico).place(x=10,y=220)



    filterSearch_btn = Button(AdminHomepageMenu_frame,text='Filter Search',background='#3acaff',width=15,font=('Arial',10),command = lambda : switchPages(AdminHome_page,filterBook_page,AdminHomepageMenu_frame))
    filterSearch_btn.place(x=50,y=220)



    #alert members icon
    ico_path = r'icons\alert.ico'
    alert_ico =  Image.open(ico_path).resize((30,30),Image.LANCZOS)
    alert_ico = ImageTk.PhotoImage(alert_ico)


        #the label holding the admin icon
    alertIcon_label = Label(AdminHomepageMenu_frame,width=30,height=30,image=alert_ico).place(x=10,y=260)

    alertOverdue_btn = Button(AdminHomepageMenu_frame,text='Alert Overdues',background='#3acaff',width=15,font=('Arial',10),command = alertOverdue)
    alertOverdue_btn.place(x=50,y=260)


    #create admin icon
    ico_path = r'icons\createAdmin.ico'
    adm_ico =  Image.open(ico_path).resize((30,30),Image.LANCZOS)
    adm_ico = ImageTk.PhotoImage(adm_ico)


        #the label holding the admin icon
    admIcon_label = Label(AdminHomepageMenu_frame,width=30,height=30,image=adm_ico).place(x=10,y=340)

    createAdmin_btn = Button(AdminHomepageMenu_frame,text='Create Admin',background='#3acaff',width=15,font=('Arial',10),state='disabled',command = adminAddAdmin)
    createAdmin_btn.place(x=50,y=340)


    #logout  icon
    ico_path = r'icons\logout.ico'
    log_ico =  Image.open(ico_path).resize((30,30),Image.LANCZOS)
    log_ico = ImageTk.PhotoImage(log_ico)


        #the label holding the admin icon
    logIcon_label = Label(AdminHomepageMenu_frame,width=30,height=30,image=log_ico).place(x=10,y=380)





    adminHomeLogout_btn = Button(AdminHomepageMenu_frame,background='#d22d2d',width=15,font=('ARIAL',10),text='Log Out',command= logout).place(x=50,y=380)


    #exit icon
    ico_path = r'icons\exit.ico'
    exit_ico =  Image.open(ico_path).resize((30,30),Image.LANCZOS)
    exit_ico = ImageTk.PhotoImage(exit_ico)


        #the label holding the admin icon
    exitIcon_label = Label(AdminHomepageMenu_frame,width=30,height=30,image=exit_ico).place(x=10,y=420)


    adminHomeExit_btn = Button(AdminHomepageMenu_frame,background='#3acaff',width=15,font=('ARIAL',10),text='Exit',command=quit).place(x=50,y=420)






    #AdminHome_page.pack(fill='both',expand=True)
    AdminHomepageMenu_frame.place(x=10,y=60)
    adminHomepageContext_frame.place(x=220,y=60)

    #-------------------ADMIN HOMEPAGE END---------------------------------------









    #-------------------ADD USER PAGE START---------------------------------------


    AddMember_page = Frame(root,background='#184769')
    

    addMember_label = Label(AddMember_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    addMemberMenu_frame = Frame(AddMember_page,background='#0C173F',width=200,height=530)

    addMemberMenu_tools_text = Label(addMemberMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)




        #-------MENU FRAME BUTTONS-------------------
    addMember_home_btn = Button(addMemberMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(AddMember_page)).place(x=25,y=80)

    addMember_exit_btn = Button(addMemberMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)


    #help info text,!!
    addmem_info = ' IF THE MEMBER IS A \n PATRION,CHECK THE\n "MEMBER IS A PATRION" \n CHECKBOX.'
    addMembertext_box = Text(addMemberMenu_frame,height=5,width=27,font=('Arial',10),background='#0C173F',fg='white',border=NO)
    addMembertext_box.insert('end',addmem_info)
    addMembertext_box.config(state='disabled')#making it non editable after inserting the text
    addMembertext_box.place(x=0,y=350)




    #---------CONTEXT WINDOW-----------------------------------
    addMemberContext_frame = Frame(AddMember_page,background='#001345',width=650,height=530)

    addMemberTop_label = Label(addMemberContext_frame,text='Register New Member',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=10)


    addMemberName_label = Label(addMemberContext_frame,text='Name',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=70)
    addMemberName_entry = Entry(addMemberContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    addMemberName_entry.place(x=220,y=70)


    addMemberID_label = Label(addMemberContext_frame,text='ID Number',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=140)
    addMemberID_entry = Entry(addMemberContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    addMemberID_entry.place(x=220,y=140)


    addMemberPhone_label = Label(addMemberContext_frame,text='Phone Number',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=210)
    addMemberPhone_entry = Entry(addMemberContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    addMemberPhone_entry.place(x=220,y=210)


    addMemberTaste_label = Label(addMemberContext_frame,text='Literary taste',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=280)
    addMemberTaste_entry = Entry(addMemberContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    addMemberTaste_entry.place(x=220,y=280)


    addMemberPass_label = Label(addMemberContext_frame,text='Password',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=350)
    addMemberPass_entry = Entry(addMemberContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    addMemberPass_entry.place(x=220,y=350)


    #checkboxes

    #checkbox variable
    isPatrion = StringVar()
    isPatrion.set('no')#setting the value of the checkbox to off after loading

    Checkbutton(addMemberContext_frame,width=20,text='This member is a patrion.',variable=isPatrion,onvalue='yes',offvalue='no',font=('Arial',10),background='#001345',bg='white').place(x=250,y=410)


    #checkbox variable
    subToMail = StringVar()
    subToMail.set('yes')#setting the value of the checkbox to off after loading

    Checkbutton(addMemberContext_frame,width=30,text='Receive notifications about new books.',variable=subToMail,onvalue='yes',offvalue='no',font=('Arial',10),border=NO,bg='white').place(x=250,y=440)



    addUser_btn = Button(addMemberContext_frame,text='Register',background='#3acaff',width=15,font=('Arial',10),command = lambda : addMember(addMemberName_entry,addMemberID_entry,addMemberPhone_entry,addMemberTaste_entry,addMemberPass_entry,isPatrion=isPatrion,isSubbed=subToMail)).place(x=260,y=480)



    #AddMember_page.pack(fill='both', expand=True)
    addMemberMenu_frame.place(x=10,y=60)
    addMemberContext_frame.place(x=220,y=60)

    #-------------------ADD MEMBER PAGE END---------------------------------------







    #-------------------DELETE MEMBER PAGE START---------------------------------------


    deleteMember_page = Frame(root,background='#184769')
    

    deleteMember_label = Label(deleteMember_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    deleteMemberMenu_frame = Frame(deleteMember_page,background='#0C173F',width=200,height=530)

    deleteMemberMenu_tools_text = Label(deleteMemberMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)


    #-------MENU FRAME BUTTONS-------------------
    delMember_home_btn = Button(deleteMemberMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(deleteMember_page)).place(x=25,y=80)

    delMember_exit_btn = Button(deleteMemberMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)




    #---------CONTEXT WINDOW-----------------------------------
    deleteMemberContext_frame = Frame(deleteMember_page,background='#001345',width=650,height=530)

    delMemberTop_label = Label(deleteMemberContext_frame,text='Delete Member',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=10)


    delMemberInfo_label = Label(deleteMemberContext_frame,text='Enter the ID Number of the user to delete',font=('Arial',15),background='#001345',foreground='white').place(x=140,y=70)


    delMemberID_label = Label(deleteMemberContext_frame,text='ID',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=120)

    delMemberID_entry = Entry(deleteMemberContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    delMemberID_entry.place(x=170,y=120)



    delGetMember_btn = Button(deleteMemberContext_frame,text='Find Member',background='#3acaff',width=15,font=('Arial',10),command = lambda : delFindMember(id=delMemberID_entry))
    delGetMember_btn.place(x=285,y=170)






    delFoundMemberPhone_label = Label(deleteMemberContext_frame,text='Phone Number',font=('Arial',15),background='#001345',foreground='white').place(x=40,y=230)

    delFoundMemberPhone_entry = Entry(deleteMemberContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    delFoundMemberPhone_entry.place(x=230,y=230)



    delFoundMembership_label = Label(deleteMemberContext_frame,text='Membership',font=('Arial',15),background='#001345',foreground='white').place(x=40,y=300)

    delFoundMembership_entry = Entry(deleteMemberContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    delFoundMembership_entry.place(x=230,y=300)



    delFoundBorrowed_label = Label(deleteMemberContext_frame,text='No. of Borrowed\n Books',font=('Arial',15),background='#001345',foreground='white').place(x=40,y=370)

    delFoundBorrowed_entry = Entry(deleteMemberContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    delFoundBorrowed_entry.place(x=230,y=370)



    delMember_btn = Button(deleteMemberContext_frame,text='Delete',background='#3acaff',width=15,font=('Arial',10),command = lambda : deleteMember(delMemberID_entry)).place(x=260,y=450)







    #deleteMember_page.pack(fill='both',expand=True)
    deleteMemberMenu_frame.place(x=10,y=60)
    deleteMemberContext_frame.place(x=220,y=60)

    #-------------------DELETE MEMBER PAGE END---------------------------------------







    #-------------------EDIT MEMBER PAGE START-----------------------------------------


    editMember_page = Frame(root,background='#184769')
    

    editMember_label = Label(editMember_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    editMemberMenu_frame = Frame(editMember_page,background='#0C173F',width=200,height=530)

    editMemberMenu_tools_text = Label(editMemberMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)


    #-------MENU FRAME BUTTONS-------------------
    editMember_home_btn = Button(editMemberMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(editMember_page)).place(x=25,y=80)


    editMember_exit_btn = Button(editMemberMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)


    #help info text,!!
    editmem_info = " YOU CAN ALSO EDIT A \n MEMBER'S MEMBERSHIP,\n CHECK OR UNCHECK THE\n CHECKBOX."
    editMembertext_box = Text(editMemberMenu_frame,height=13,width=27,font=('Arial',10),background='#0C173F',fg='white',border=NO,)
    editMembertext_box.insert('end',editmem_info)
    editMembertext_box.config(state='disabled') #making it non editable after inserting the text
    editMembertext_box.place(x=0,y=320)



    #---------CONTEXT WINDOW-----------------------------------
    editMemberContext_frame = Frame(editMember_page,background='#001345',width=650,height=530)

    editMemberTop_label = Label(editMemberContext_frame,text='Edit Member',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=8)


    editMemberInfo_label = Label(editMemberContext_frame,text='Enter the ID Number of the user to edit.',font=('Arial',15),background='#001345',foreground='white').place(x=140,y=55)


    editMemberID_label = Label(editMemberContext_frame,text='ID',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=100)

    editMemberID_entry = Entry(editMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editMemberID_entry.place(x=170,y=100)


    editMember_btn = Button(editMemberContext_frame,text='Find Member',background='#3acaff',width=15,font=('Arial',10),command = lambda : editFindMember(editMemberID_entry))
    editMember_btn.place(x=275,y=140)


    editMemberName_label = Label(editMemberContext_frame,text='Name',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=180)

    editMemberName_entry = Entry(editMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editMemberName_entry.place(x=200,y=180)



    editMemberPhone_label = Label(editMemberContext_frame,text='Phone Number',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=240)

    editMemberPhone_entry = Entry(editMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editMemberPhone_entry.place(x=200,y=240)



    editMemberTaste_label = Label(editMemberContext_frame,text='Literary Taste',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=300)

    editMemberTaste_entry = Entry(editMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editMemberTaste_entry.place(x=200,y=300)




    editMemberPass_label = Label(editMemberContext_frame,text='Password',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=360)

    editMemberPass_entry = Entry(editMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editMemberPass_entry.place(x=200,y=360)



    editMembership_label = Label(editMemberContext_frame,text='Membership',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=400)



        #checkbox variable
    editIsPatrion = StringVar()
    editIsPatrion.set('no')

    Checkbutton(editMemberContext_frame,width=20,text='This member is a patrion.',variable=editIsPatrion,onvalue='yes',offvalue='no',font=('Arial',10),border=NO,bg='white').place(x=200,y=405)



    editMember_btn = Button(editMemberContext_frame,text='Save Changes',background='#3acaff',width=15,font=('Arial',10),command = lambda : saveEdit(editMemberID_entry))
    editMember_btn.place(x=260,y=460)



    #editMember_page.pack(fill='both',expand=True)
    editMemberMenu_frame.place(x=10,y=60)
    editMemberContext_frame.place(x=220,y=60)

    #-------------------EDIT MEMBER PAGE END-----------------------------------------









    #-------------------VIEW MEMBER PAGE START-----------------------------------------


    viewMember_page = Frame(root,background='#184769')
    

    viewMember_label = Label(viewMember_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    viewMemberMenu_frame = Frame(viewMember_page,background='#0C173F',width=200,height=530)

    viewMemberMenu_tools_text = Label(viewMemberMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)


    #-------MENU FRAME BUTTONS-------------------
    viewMember_home_btn = Button(viewMemberMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(viewMember_page)).place(x=25,y=80)


    viewMember_exit_btn = Button(viewMemberMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)



    #---------CONTEXT WINDOW-----------------------------------
    viewMemberContext_frame = Frame(viewMember_page,background='#001345',width=650,height=530)

    viewMemberTop_label = Label(viewMemberContext_frame,text='View Member',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=8)


    viewMemberInfo_label = Label(viewMemberContext_frame,text='Enter the ID Number of the user to view.',font=('Arial',15),background='#001345',foreground='white').place(x=140,y=55)


    viewMemberID_label = Label(viewMemberContext_frame,text='ID',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=100)

    viewMemberID_entry = Entry(viewMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15)).place(x=170,y=100)


    viewMember_btn = Button(viewMemberContext_frame,text='Find Member',background='#3acaff',width=15,font=('Arial',10))
    viewMember_btn.place(x=275,y=140)



    viewMemberName_label = Label(viewMemberContext_frame,text='Name',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=180)

    viewMemberName_entry = Entry(viewMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewMemberName_entry.place(x=200,y=180)



    viewMemberPhone_label = Label(viewMemberContext_frame,text='Phone Number',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=250)

    viewMemberPhone_entry = Entry(viewMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewMemberPhone_entry.place(x=200,y=250)



    viewMemberTaste_label = Label(viewMemberContext_frame,text='Literary Taste',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=320)

    viewMemberTaste_entry = Entry(viewMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewMemberTaste_entry.place(x=200,y=320)




    viewMemberBorrowed_label = Label(viewMemberContext_frame,text='No. of borrowed\nbooks',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=370)

    viewMemberTaste_entry = Entry(viewMemberContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewMemberTaste_entry.place(x=200,y=380)



    viewMembership_label = Label(viewMemberContext_frame,text='Membership',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=435)



        #checkbox variable
    viewIsPatrion = StringVar()
    viewIsPatrion.set('no')#read from database

    Checkbutton(viewMemberContext_frame,width=20,text='This member is a patrion.',variable=viewIsPatrion,onvalue='yes',offvalue='no',font=('Arial',10),border=NO,bg='white').place(x=200,y=440)



    viewMember_btn = Button(viewMemberContext_frame,text='Done',background='#3acaff',width=15,font=('Arial',10)).place(x=260,y=480)




    #viewMember_page.pack(fill='both',expand=True)
    viewMemberMenu_frame.place(x=10,y=60)
    viewMemberContext_frame.place(x=220,y=60)

    #-------------------VIEW MEMBER PAGE END-----------------------------------------  









    #-------------------ADD BOOK PAGE START---------------------------------------


    AddBook_page = Frame(root,background='#184769')
    

    addBook_label = Label(AddBook_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    addBookMenu_frame = Frame(AddBook_page,background='#0C173F',width=200,height=530)

    addBookMenu_tools_text = Label(addBookMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)




        #-------MENU FRAME BUTTONS-------------------
    addBook_home_btn = Button(addBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(AddBook_page)).place(x=25,y=80)

    addBook_exit_btn = Button(addBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)


    #help info text,!!
    addBook_info = ' CHECK THE CHECKBOX IF\n THE BOOK BEING ADDED \n CAN ONLY BE BORROWED \n BY PATRIONS.'
    addBooktext_box = Text(addBookMenu_frame,height=10,width=27,font=('Arial',10),background='#0C173F',fg='white',border=NO)
    addBooktext_box.insert('end',addBook_info)
    addBooktext_box.config(state='disabled')#making it non editable after inserting the text
    addBooktext_box.place(x=0,y=350)



        #---------CONTEXT WINDOW-----------------------------------
    addBookContext_frame = Frame(AddBook_page,background='#001345',width=650,height=530)

    addBookTop_label = Label(addBookContext_frame,text='Add a Book',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=10)


    addBookTitle_label = Label(addBookContext_frame,text='Title',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=70)
    addBookTitle_entry = Entry(addBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    addBookTitle_entry.place(x=220,y=70)



    addBookISBN_label = Label(addBookContext_frame,text='ISBN',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=130)
    addBookISBN_entry = Entry(addBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    addBookISBN_entry.place(x=220,y=130)



    addBookAuthor_label = Label(addBookContext_frame,text='Author',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=190)
    addBookAuthor_entry = Entry(addBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    addBookAuthor_entry.place(x=220,y=190)



    addBookGenre_label = Label(addBookContext_frame,text='Genre',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=250)
    addBookGenre_entry = Entry(addBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    addBookGenre_entry.place(x=220,y=250)



    addBookCopies_label = Label(addBookContext_frame,text='No. of Copies',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=310)
    addBookCopies_entry = Entry(addBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    addBookCopies_entry.place(x=220,y=310)



    addBookYear_label = Label(addBookContext_frame,text='Year Of \n Publication',font=('Arial',15),background='#001345',foreground='white').place(x=80,y=370)
    addBookYear_entry = Entry(addBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    addBookYear_entry.place(x=220,y=370)



    #checkbox variable
    bookIsRestricted = StringVar()
    bookIsRestricted.set('no')# setting the default value to no

    Checkbutton(addBookContext_frame,width=35,text='This book can only be borrowed by patrions.',variable=bookIsRestricted,onvalue='yes',offvalue='no',font=('Arial',10),border=NO,bg='white').place(x=230,y=420)



    addBook_btn = Button(addBookContext_frame,text='ADD',background='#3acaff',width=15,font=('Arial',10),command = lambda : addBook(addBookTitle_entry,addBookISBN_entry,addBookAuthor_entry,addBookGenre_entry,addBookCopies_entry,addBookYear_entry,bookIsRestricted))
    addBook_btn.place(x=260,y=480)





    #AddBook_page.pack(fill='both',expand=True)
    addBookMenu_frame.place(x=10,y=60)
    addBookContext_frame.place(x=220,y=60)

    #-------------------ADD BOOK PAGE END----------------------------------------- 









    #-------------------EDIT BOOK PAGE START-----------------------------------------


    editBook_page = Frame(root,background='#184769')
    

    editBook_label = Label(editBook_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    editBookMenu_frame = Frame(editBook_page,background='#0C173F',width=200,height=530)

    editBookMenu_tools_text = Label(editBookMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)


    #-------MENU FRAME BUTTONS-------------------
    editBook_home_btn = Button(editBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(editBook_page)).place(x=25,y=80)


    editBook_exit_btn = Button(editBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)


    #help info text,!!
    editBook_info = " TO EDIT A RECORD,FILL IN \n THE SPACES WITH THE NEW  VALUES.\n\n TO LEAVE A RECORD AS IS,\n LEAVE IT BLANK.\n\n YOU CAN ALSO EDIT A \n BOOK'S RESTRICTION,\n CHECK OR UNCHECK THE\n CHECKBOX."
    editBooktext_box = Text(editBookMenu_frame,height=13,width=27,font=('Arial',10),background='#0C173F',fg='white',border=NO,)
    editBooktext_box.insert('end',editBook_info)
    editBooktext_box.config(state='disabled') #making it non editable after inserting the text
    editBooktext_box.place(x=0,y=320)




    #---------CONTEXT WINDOW-----------------------------------
    editBookContext_frame = Frame(editBook_page,background='#001345',width=650,height=530)

    editBookTop_label = Label(editBookContext_frame,text='Edit Book',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=8)


    editBookInfo_label = Label(editBookContext_frame,text='Enter the ISBN Number of the book to edit.',font=('Arial',15),background='#001345',foreground='white').place(x=140,y=55)


    editBookISBN_label = Label(editBookContext_frame,text='ISBN',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=100)

    editBookISBN_entry = Entry(editBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editBookISBN_entry.place(x=170,y=100)


    editBook_btn = Button(editBookContext_frame,text='Find Book',background='#3acaff',width=15,font=('Arial',10),command = lambda : editFindBook(editBookISBN_entry))
    editBook_btn.place(x=275,y=140)



    editBookName_label = Label(editBookContext_frame,text='Title',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=180)

    editBookTitle_entry = Entry(editBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editBookTitle_entry.place(x=200,y=180)



    editBookAuthor_label = Label(editBookContext_frame,text='Author',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=240)

    editBookAuthor_entry = Entry(editBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editBookAuthor_entry.place(x=200,y=240)



    editBookGenre_label = Label(editBookContext_frame,text='Genre',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=300)

    editBookGenre_entry = Entry(editBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editBookGenre_entry.place(x=200,y=300)



    editBookCopies_label = Label(editBookContext_frame,text='No Of Copies',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=360)

    editBookCopies_entry = Entry(editBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    editBookCopies_entry.place(x=200,y=360)



    editBookRestriction_label = Label(editBookContext_frame,text='Restriction',font=('Arial',15),background='#001345',foreground='white').place(x=50,y=405)



        #checkbox variable
    isBookRestricted = StringVar()
    isBookRestricted.set('no')#read from database

    Checkbutton(editBookContext_frame,width=35,text='This book can only be borrowed by patrions.',variable=isBookRestricted,onvalue='yes',offvalue='no',font=('Arial',10),border=NO,bg='white').place(x=210,y=410)



    editBook_btn = Button(editBookContext_frame,text='Save Changes',background='#3acaff',width=15,state='disabled',font=('Arial',10),command = lambda : saveBookEdit(editBookISBN_entry))
    editBook_btn.place(x=260,y=450)


    #editBook_page.pack(fill='both',expand=True)
    editBookMenu_frame.place(x=10,y=60)
    editBookContext_frame.place(x=220,y=60)

    #-------------------EDIT BOOK PAGE END-----------------------------------------








    #-------------------DELETE BOOK PAGE START-----------------------------------------


    deleteBook_page = Frame(root,background='#184769')
    

    deleteBook_label = Label(deleteBook_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    deleteBookMenu_frame = Frame(deleteBook_page,background='#0C173F',width=200,height=530)

    deleteBookMenu_tools_text = Label(deleteBookMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)


    #-------MENU FRAME BUTTONS-------------------
    deleteBook_home_btn = Button(deleteBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(deleteBook_page)).place(x=25,y=80)


    deleteBook_exit_btn = Button(deleteBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)



    #---------CONTEXT WINDOW-----------------------------------
    deleteBookContext_frame = Frame(deleteBook_page,background='#001345',width=650,height=530)

    deleteBookTop_label = Label(deleteBookContext_frame,text='Delete Book',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=8)


    deleteBookInfo_label = Label(deleteBookContext_frame,text='Enter the ISBN Number of the book to delete.',font=('Arial',15),background='#001345',foreground='white').place(x=140,y=55)


    deleteBookISBN_label = Label(deleteBookContext_frame,text='ISBN',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=100)

    deleteBookISBN_entry = Entry(deleteBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    deleteBookISBN_entry.place(x=170,y=100)


    deleteBook_btn = Button(deleteBookContext_frame,text='Find Book',background='#3acaff',width=15,font=('Arial',10),command = lambda : delFindBook(deleteBookISBN_entry))
    deleteBook_btn.place(x=275,y=140)



    deleteBookName_label = Label(deleteBookContext_frame,text='Title',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=205)

    deleteBookTitle_entry = Entry(deleteBookContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    deleteBookTitle_entry.place(x=200,y=200)



    deleteBookNo_label = Label(deleteBookContext_frame,text='No Of\nCopies',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=250)

    deleteBookNo_entry = Entry(deleteBookContext_frame,bg='#0080ff',width=25,font=('Arial',20))
    deleteBookNo_entry.place(x=200,y=260)




    deleteBook_btn = Button(deleteBookContext_frame,text='Delete',background='#3acaff',width=15,state='disabled',font=('Arial',10),command = lambda : deleteBook(deleteBookISBN_entry))
    deleteBook_btn.place(x=260,y=350)



    #deleteBook_page.pack(fill='both',expand=True)
    deleteBookMenu_frame.place(x=10,y=60)
    deleteBookContext_frame.place(x=220,y=60)


    #-------------------DELETE BOOK PAGE END-----------------------------------------







    #-------------------VIEW BOOK PAGE START-----------------------------------------


    viewBook_page = Frame(root,background='#184769')
    

    viewBook_label = Label(viewBook_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    viewBookMenu_frame = Frame(viewBook_page,background='#0C173F',width=200,height=530)

    viewBookMenu_tools_text = Label(viewBookMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)


    #-------MENU FRAME BUTTONS-------------------
    viewBook_home_btn = Button(viewBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(viewBook_page)).place(x=25,y=80)


    viewBook_exit_btn = Button(viewBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)



    #---------CONTEXT WINDOW-----------------------------------
    viewBookContext_frame = Frame(viewBook_page,background='#001345',width=650,height=530)

    viewBookTop_label = Label(viewBookContext_frame,text='View Book',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=8)


    viewBookInfo_label = Label(viewBookContext_frame,text='Enter the ISBN Number of the book to view.',font=('Arial',15),background='#001345',foreground='white').place(x=140,y=55)


    viewBookISBN_label = Label(viewBookContext_frame,text='ISBN',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=100)

    viewBookISBN_entry = Entry(viewBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewBookISBN_entry.place(x=170,y=100)


    viewBook_btn = Button(viewBookContext_frame,text='Find Book',background='#3acaff',width=15,font=('Arial',10),command = lambda : viewBook(viewBookISBN_entry))
    viewBook_btn.place(x=275,y=140)




    viewBookTitle_label = Label(viewBookContext_frame,text='Title',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=185)

    viewBookTitle_entry = Entry(viewBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewBookTitle_entry.place(x=200,y=180)



    viewBookAuthor_label = Label(viewBookContext_frame,text='Author',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=245)

    viewBookAuthor_entry = Entry(viewBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewBookAuthor_entry.place(x=200,y=240)



    viewBookGenre_label = Label(viewBookContext_frame,text='Genre',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=305)

    viewBookGenre_entry = Entry(viewBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewBookGenre_entry.place(x=200,y=300)




    viewBookCopies_label = Label(viewBookContext_frame,text='No. Of \nCopies',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=355)

    viewBookCopies_entry = Entry(viewBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewBookCopies_entry.place(x=200,y=360)




    viewBookYear_label = Label(viewBookContext_frame,text='Year Of \nPublication',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=415)

    viewBookYear_entry = Entry(viewBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    viewBookYear_entry.place(x=200,y=420)




    viewBookRestriction_label = Label(viewBookContext_frame,text='Restriction',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=475)



        #checkbox variable
    viewIsBookRestricted = StringVar()
    viewIsBookRestricted.set('no')#read from database

    viewCheck = Checkbutton(viewBookContext_frame,width=35,text='This book can only be borrowed by patrions.',variable=viewIsBookRestricted,onvalue='yes',offvalue='no',font=('Arial',10),border=NO,bg='white')
    viewCheck.place(x=230,y=480)



    #viewBook_page.pack(fill='both',expand=True)
    viewBookMenu_frame.place(x=10,y=60)
    viewBookContext_frame.place(x=220,y=60)

    #-------------------VIEW BOOK PAGE END-----------------------------------------








    #-------------------BORROW BOOK PAGE START---------------------------------------


    borrowBook_page = Frame(root,background='#184769')
    

    borrowBook_label = Label(borrowBook_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    borrowBookMenu_frame = Frame(borrowBook_page,background='#0C173F',width=200,height=530)

    borrowBookMenu_tools_text = Label(borrowBookMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)



        #-------MENU FRAME BUTTONS-------------------
    borrowBook_home_btn = Button(borrowBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(borrowBook_page)).place(x=25,y=80)

    borrowBook_exit_btn = Button(borrowBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)


    #help info text,!!
    borrowBook_info = ' THE BORROW PERIOD IS IN \n WEEKS.\n\n NORMAL MEMBERS CAN \n BORROW ONLY 1 COPY FOR  A MAXIMUM PERIOD OF 1 \n WEEK.\n\n PATRIONS CAN BORROW \n UPTO 50 COPIES FOR A \n MAXIMUM PERIOD OF 4 \n WEEKS.'
    borrowBooktext_box = Text(borrowBookMenu_frame,height=15,width=27,font=('Arial',10),background='#0C173F',fg='white',border=NO)
    borrowBooktext_box.insert('end',borrowBook_info)
    borrowBooktext_box.config(state='disabled')#making it non editable after inserting the text
    borrowBooktext_box.place(x=0,y=300)



    #---------CONTEXT WINDOW-----------------------------------
    borrowBookContext_frame = Frame(borrowBook_page,background='#001345',width=650,height=530)

    borrowBookTop_label = Label(borrowBookContext_frame,text='Book Check-Out',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=10)


    borrowerName_label = Label(borrowBookContext_frame,text='Member Name',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=70)
    borrowerName_entry = Entry(borrowBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    borrowerName_entry.place(x=220,y=70)



    borrowerID_label = Label(borrowBookContext_frame,text='Member ID',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=140)
    borrowerID_entry = Entry(borrowBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    borrowerID_entry.place(x=220,y=140)



    borrowedBookISBN_label = Label(borrowBookContext_frame,text='Book ISBN',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=210)
    borrowedBookISBN_entry = Entry(borrowBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    borrowedBookISBN_entry.place(x=220,y=210)




    borrowedBookCopies_label = Label(borrowBookContext_frame,text='No. Of Copies',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=280)
    borrowedBookCopies_entry = Entry(borrowBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    borrowedBookCopies_entry.place(x=220,y=280)




    borrowPeriod_label = Label(borrowBookContext_frame,text='Borrow Period',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=350)
    borrowedPeriod_entry = Entry(borrowBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    borrowedPeriod_entry.place(x=220,y=350)



    #checkbox variable
    agreeToTerms = StringVar()
    agreeToTerms.set('yes')#set default to yes

    Checkbutton(borrowBookContext_frame,width=35,text='I agree to being fined due to late book returns.',variable=agreeToTerms,onvalue='yes',offvalue='no',font=('Arial',10),border=NO,bg='white').place(x=230,y=400)



    borrowBook_btn = Button(borrowBookContext_frame,text='Check-out',background='#3acaff',width=15,font=('Arial',10),command = lambda : borrowBook(borrowerName_entry,borrowerID_entry,borrowedBookISBN_entry,borrowedBookCopies_entry,borrowedPeriod_entry,agreeToTerms))
    borrowBook_btn.place(x=260,y=450)


    #borrowBook_page.pack(fill='both',expand=True)
    borrowBookMenu_frame.place(x=10,y=60)
    borrowBookContext_frame.place(x=220,y=60)


    #-------------------BORROW BOOK PAGE END---------------------------------------







    #-------------------RETURN BOOK PAGE START---------------------------------------


    returnBook_page = Frame(root,background='#184769')
    

    returnBook_label = Label(returnBook_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    returnBookMenu_frame = Frame(returnBook_page,background='#0C173F',width=200,height=530)

    returnBookMenu_tools_text = Label(returnBookMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)



        #-------MENU FRAME BUTTONS-------------------
    returnBook_home_btn = Button(returnBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : backToHome(returnBook_page)).place(x=25,y=80)

    returnBook_exit_btn = Button(returnBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)


    #help info text,!!
    returnBook_info = ' TO RATE A BOOK,GIVE A \n NUMBER OF STARS 1-5 .\n\n 1 IS THE WORST AND 5 IS \n THE BEST.'
    returnBooktext_box = Text(returnBookMenu_frame,height=15,width=27,font=('Arial',10),background='#0C173F',fg='white',border=NO)
    returnBooktext_box.insert('end',returnBook_info)
    returnBooktext_box.config(state='disabled')#making it non editable after inserting the text
    returnBooktext_box.place(x=0,y=300)


    #---------CONTEXT WINDOW-----------------------------------
    returnBookContext_frame = Frame(returnBook_page,background='#001345',width=650,height=530)

    returnBookTop_label = Label(returnBookContext_frame,text='Book Check-In',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=10)


    returnerName_label = Label(returnBookContext_frame,text='Member Name',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=70)
    returnerName_entry = Entry(returnBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    returnerName_entry.place(x=220,y=70)



    returnerID_label = Label(returnBookContext_frame,text='Member ID',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=140)
    returnerID_entry = Entry(returnBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    returnerID_entry.place(x=220,y=140)



    returnedBookISBN_label = Label(returnBookContext_frame,text='Book ISBN',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=210)
    returnedBookISBN_entry = Entry(returnBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    returnedBookISBN_entry.place(x=220,y=210)



    returnedBookCopies_label = Label(returnBookContext_frame,text='No. Of Copies',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=280)
    returnedBookCopies_entry = Entry(returnBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    returnedBookCopies_entry.place(x=220,y=280)



    rateBook_label = Label(returnBookContext_frame,text='Rate Book',font=('Arial',15),background='#001345',foreground='white').place(x=60,y=350)
    rateBook_entry = Entry(returnBookContext_frame,bg='#0080ff',width=30,font=('Arial',15))
    rateBook_entry.place(x=220,y=350)




    returnBook_btn = Button(returnBookContext_frame,text='Check-in',background='#3acaff',width=15,font=('Arial',10),
    command = lambda : returnBook(returnerName_entry,returnerID_entry,returnedBookISBN_entry, returnedBookCopies_entry,rateBook_entry))
    returnBook_btn.place(x=260,y=450)



    #returnBook_page.pack(fill='both',expand=True)
    returnBookMenu_frame.place(x=10,y=60)
    returnBookContext_frame.place(x=220,y=60)

    #-------------------RETURN BOOK PAGE END---------------------------------------









    #-------------------FILTER BOOK PAGE START---------------------------------------


    filterBook_page = Frame(root,background='#184769')
    

    filterBook_label = Label(filterBook_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    filterBookMenu_frame = Frame(filterBook_page,background='#0C173F',width=200,height=530,highlightbackground='darkblue',highlightthickness=6)

    filterBookMenu_tools_text = Label(filterBookMenu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15)).place(x=14,y=20)



        #-------MENU FRAME BUTTONS-------------------
    filterBook_home_btn = Button(filterBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Main Menu',borderwidth=4,command = lambda : switchPages(filterBook_page,AdminHome_page,filterBookContext_frame)).place(x=25,y=80)

    filterBook_exit_btn = Button(filterBookMenu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Exit',borderwidth=4,command=quit).place(x=25,y=140)


    #---------CONTEXT WINDOW-----------------------------------
    filterBookContext_frame = Frame(filterBook_page,background='#001345',width=650,height=530,highlightbackground='darkblue',highlightthickness=6)

    filterBookTop_label = Label(filterBookContext_frame,text='Filter Books or Members',foreground='white',background='#001345',font=('Arial',20)).place(x=240,y=10)


    filterName_label = Label(filterBookContext_frame,text='Filter:',font=('Arial',15),background='#001345',foreground='white').place(x=150,y=90)




    #filter query
    #this options are displayed if filter books is selected in the above drop down
    bookQueryOpts = ['Author','Genre','Rating']

    #this options are displayed if filter members is selected in the above drop down
    memberQueryOpts = ['Patrion','ID']



    #this functions checks what is selected in the filter dropdown and configures what options are displayed in the filter using dropdown

                  
       
     #value changes according to the options selected in filter option
    def checkSet(event):
  
        if filterOpts_selected.get() == 'Members':
            bookQueryOpts_dropBtn.place_forget()
            memberQueryOpts_dropBtn.place(x=520,y=200)

        elif filterOpts_selected.get() == 'Books':
            memberQueryOpts_dropBtn.place_forget()
            bookQueryOpts_dropBtn.place(x=520,y=200)


    #matching the selected filter field to change the filter input text to 'make it make sense'
    def setInput(event):
        #clearing the entry and results field
        filterInput_entry.delete(0,'end')

        results_text.config(state='normal')
        results_text.delete('1.0',END)
        results_text.config(state='disabled')

        match bothOpts_selected.get():
            case 'Author':
                filterInput_label.config(text='Author Name:')
                info_label.config(text='Filtered search results using Author.')

            case 'Genre':
                filterInput_label.config(text='Filter Genre:')
                info_label.config(text='Filtered search results using Genre.')

            case 'Rating':
                filterInput_label.config(text='Filter Rating\n(greate than):')
                info_label.config(text='Filtered search results using rating.')

            case 'ID':
                filterInput_label.config(text='Enter ID:')
                info_label.config(text='Filtered search results using ID.')

            case 'Patrion':
                filterInput_label.config(text='Patrions')
                info_label.config(text='All patrion members')



            
            

        
        
    bothOpts_selected = StringVar()         #the currently selected option
    bothOpts_selected.set('Author') 

    bookQueryOpts_dropBtn = OptionMenu(filterBook_page,bothOpts_selected,*bookQueryOpts,command = setInput)
    bookQueryOpts_dropBtn.place(x=520,y=200)
    memberQueryOpts_dropBtn = OptionMenu(filterBook_page,bothOpts_selected,*memberQueryOpts,command = setInput)
       

    #filter books or members?
    filterOpts = ['Books','Members']
    filterOpts_selected = StringVar()
    filterOpts_selected.set(filterOpts[0])
    
    #command added later
    filterOpts_dropBtn = OptionMenu(filterBook_page,filterOpts_selected,*filterOpts,command=checkSet).place(x=520,y=150)


    #filter books or members?
    filterInputOpts = ['Books','Members']
    filterOpts_selected = StringVar()
    filterOpts_selected.set(filterOpts[0])
    
    #command added later
    filterOpts_dropBtn = OptionMenu(filterBook_page,filterOpts_selected,*filterOpts,command=checkSet).place(x=520,y=150)


    filterQuery_label = Label(filterBookContext_frame,text='Filter Using:',font=('Arial',15),background='#001345',foreground='white').place(x=100,y=150)
  
    filterInput_label = Label(filterBookContext_frame,text='Filter Input:',font=('Arial',15),background='#001345',foreground='white')
    filterInput_label.place(x=100,y=200)

    filterInput_entry = Entry(filterBookContext_frame,bg='#0080ff',width=20,font=('Arial',20))
    filterInput_entry.place(x=270,y=200)

    
    filter_btn = Button(filterBookContext_frame,text='Search',background='#3acaff',width=15,font=('Arial',10),command = lambda : filterSearch(filtered=filterOpts_selected,selected=bothOpts_selected,filter_input=filterInput_entry))
    filter_btn.place(x=300,y=250)

    info_label = Label(filterBookContext_frame,text='Filter Info',font=('Arial',10),background='#001345',foreground='white')
    info_label.place(x=120,y=300)

    results_text = Text(filterBookContext_frame,width=75,height=10,bg='white',fg='black',font=('Arial',15))
    results_text.place(x=20,y=340)

    #scrollbar for the results Text
    sb = Scrollbar(filterBookContext_frame)
    sb.place(x=600,y=350)

    results_text.config(yscrollcommand=sb.set,state='disabled')
    sb.config(command=results_text.yview)


    #filterBook_page.pack(fill='both',expand=True) 
    filterBookMenu_frame.place(x=10,y=60)
    filterBookContext_frame.place(x=220,y=60)

    #-------------------FILTER  PAGE END---------------------------------------








    #-----------------------START UP PAGE START------------------------------------------------------
    startup_page = Frame(root,width=900,height=600,background='#184769')
   

    startup_label = Label(startup_page,text='PACIFIC LIBRARY MANAGEMENT SYSTEM.',width=40,font=('Arial',20),background='#184769',foreground='white').place(x=180,y=10)

    #----THE MENU FRAME START------------------------------
    menu_frame = Frame(startup_page,background='#0C173F',width=200,height=530)
    menu_frame.place(x=10,y=60)

    menu_tools_text = Label(menu_frame,background='#00ffff',text='TOOLS',width=15,font=('Arial',15))
    menu_tools_text.place(x=15,y=10)

    login_admin_btn = Button(menu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Admin Login',borderwidth=4,command=lambda : switchPages(startup_page,loginAdmin_page,context_frame))
    login_admin_btn.place(x=30,y=60)


    #IS DISABLED
    login_master_btn = Button(menu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Master Admin Login',borderwidth=5,command=lambda : switchPages(startup_page,masterLogin_page,masterLoginContext_frame))
    login_master_btn.place(x=30,y=120)


    create_master_btn = Button(menu_frame,activebackground='green',background='#80ff7b',width=15,font=('ARIAL',10),text='Create Master Admin',borderwidth=5,command=lambda : switchPages(startup_page,createMasterAdmin_page,CreateMasterContext_frame))
    create_master_btn.place(x=30,y=180)


    exit_btn = Button(menu_frame,activebackground='green',background='#ff9999',width=15,font=('ARIAL',10),text='Exit',borderwidth=5,command=quit).place(x=30,y=240)


    info_text = 'A master admin is used to create or delete admins ,if one already exists,it cannot be created again.'

    login_help_text = Label(menu_frame,background='#0C173F',foreground='white',text=info_text,width=18,justify='left',wraplength=150,font=('Arial',10))
    login_help_text.place(x=10,y=400)

    #-------MENU FRAME BUTTONS END---------------------



    #-------CONTEXT FRAME START---------------------


    

    context_frame = Frame(startup_page,background='#001345',width=650,height=530)
    context_frame.place(x=220,y=60)

    top_label = Label(context_frame,text='Please Log In',foreground='white',background='#001345',font=('Arial',30))
    top_label.place(x=190,y=10)

    #the label holding the logo image
    image_label = Label(context_frame,width=400,height=400,image=converted_image_startup)
    image_label.place(x=120,y=80)



    startup_page.pack(fill='both',expand=True)

    #-----------------------START UP PAGE END------------------------------------------------------

    assertMaster()

    root.mainloop()




