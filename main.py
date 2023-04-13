#ARA PASSWORD MANAGER 1.11
from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk

import pandas as pd

import mysql.connector as sqltr
from mysql.connector import Error

from PIL import ImageTk

import matplotlib.pyplot as plt

import numpy as np 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------


#definitions----------------------------------------------------------------------------
def LOGIN():
    """ Connect to MySQL database """
    p1=pwd_entry.get()
    myco= None
    try:
        myco= sqltr.connect(host='localhost',user='root',password=p1)
        if myco.is_connected():
            a=mb.showinfo('CONNECTION ESTABLISHED !','MySQL connection successfully installed')

            correct_label=Label(root,text="MySQL connection Successful")
            correct_label.place(x=0,y=450)
            continue_but=Button(root,text='Continue',font=("bold",30),bg="gold",fg="white",bd=1,command=ACTION)
            continue_but.place(x=300,y=400,relwidth=0.35)
            cursor = myco.cursor()
            cursor.execute('create database if  not exists Project;')
            mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
            cursor = mycon.cursor()
            cursor.execute('create table if not exists password(Username varchar(50),Platform varchar(50),Password varchar(50) not null);')
    except Error as e:
        b=mb.showerror('DENIED !','Wrong Password Entered')
        incorrect_label=Label(root,text="MySQL connection Failed           ")
        incorrect_label.place(x=0,y=450)
	#Connection is succesful----------------------


#-------------------------------------------------------------------------------------------------------------------------------------------------------
def ADD():
    def MYSQLADD():
        uname=ADD_uname_entry.get()
        pform=ADD_pform_entry.get()
        pword=ADD_pword_entry.get()
        qry="insert into password values('%s','%s','%s');"%(uname,pform,pword)
        p1=pwd_entry.get()
        mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
        cursor = mycon.cursor()
        cursor.execute(qry)
        mycon.commit()
        ADD_Success_label=Label(add,text="PASSWORD SUCCESSFULY ADDED")
        ADD_Success_label.place(x=0,y=450)

    def CLOSEADD():
        add.destroy()


    add=Toplevel(root)
    add.title('ADD A PASSWORD')
    add.geometry('500x500')
    add.iconbitmap('icon.ico')
    add.configure(background ='#FFE260')

    ADD_uname_label=Label(add,text=' USERNAME  :',font=("times new roman",22,"bold"),bg="white",fg="#FF7400",bd=1)
    ADD_uname_label.place(x=20,y=180,relwidth=0.4)
    ADD_uname_entry=Entry(add,font=("bold",22),bg="white",fg="black",bd=1)
    ADD_uname_entry.place(x=220,y=180,relwidth=0.5)

    ADD_pform_label=Label(add,text=' PLATFORM  :',font=("times new roman",22,"bold"),bg="white",fg="#FF7400",bd=1)
    ADD_pform_label.place(x=20,y=220,relwidth=0.4)
    ADD_pform_entry=Entry(add,font=("bold",22),bg="white",fg="black",bd=1)
    ADD_pform_entry.place(x=220,y=220,relwidth=0.5)

    ADD_pword_label=Label(add,text=' PASSWORD  :',font=("times new roman",22,"bold"),bg="white",fg="#FF7400",bd=1)
    ADD_pword_label.place(x=20,y=260,relwidth=0.4)
    ADD_pword_entry=Entry(add,font=("bold",22),bg="white",fg="black",bd=1)
    ADD_pword_entry.place(x=220,y=260,relwidth=0.5)

    ADD_button=Button(add,text='ADD',font=("bold",22),bg="gold",fg="white",bd=1,command=MYSQLADD)
    ADD_button.place(x=220,y=300,relwidth=0.5)

    ADD_CLOSE_but=Button(add,text="BACK",font=("bold",22),bg="gold",fg="white",bd=1,command=CLOSEADD)
    ADD_CLOSE_but.place(x=300,y=400,relwidth=0.35)


#-------------------------------------------------------------------------------------------------------------------------------------------------------
def VIEW():
    def MYSQLVIEW():
        pform=VIEW_pform_entry.get()
        qry=("SELECT * FROM password where platform='%s';"%(pform,))
        p1=pwd_entry.get()
        mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
        cursor = mycon.cursor()
        data = pd.read_sql(qry,mycon)
        data_frame=pd.DataFrame(data)

        VEIW_DATA_Label=Label(view,text=data_frame)
        VEIW_DATA_Label.place(x=0,y=400,relwidth=0.5)

        mycon.commit()

    def CLOSEVIEW():
        view.destroy()

    view=Toplevel(root)
    view.title('VIEW PASSWORDS')
    view.geometry('500x500')
    view.iconbitmap('icon.ico')
    view.configure(background ='#FFE260')

    p1=pwd_entry.get()
    mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
    cursor = mycon.cursor()
    qry3=("select distinct(platform) from password;")
    output2=""
    cursor.execute("select distinct(platform) from password;")
    rows=cursor.fetchall()
    for row in rows:
        output2 += ' ' + str(row[0:8]) + ' ' + ','
    output2 = output2[:-1]

    VIEW_available_label=Label(view,text='Available Platforms :-',font=("times new roman",22,"bold"),bg="white",fg="#FF7400",bd=1)
    VIEW_available_label.place(x=20,y=5,relwidth=0.6)
    VIEW_available_pforms_label=Label(view,text=output2)
    VIEW_available_pforms_label.place(x=20,y=50)

    VIEW_Label=Label(view,text=' Platform  :',font=("times new roman",22,"bold"),bg="white",fg="#FF7400",bd=1)
    VIEW_Label.place(x=20,y=180,relwidth=0.4)

    VIEW_pform_entry=Entry(view,font=("bold",22),bg="white",fg="black",bd=1)
    VIEW_pform_entry.place(x=220,y=180,relwidth=0.5)

    VIEW_but=Button(view,text='VIEW',font=("bold",22),bg="gold",fg="white",bd=1,command=MYSQLVIEW)
    VIEW_but.place(x=220,y=300,relwidth=0.5)    
    VIEW_CLOSE_but=Button(view,text="BACK",font=("bold",22),bg="gold",fg="white",bd=1,command=CLOSEVIEW)
    VIEW_CLOSE_but.place(x=300,y=400,relwidth=0.35)


#-------------------------------------------------------------------------------------------------------------------------------------------------------
def DELETE():
    def CLOSEDELETE():
        delete.destroy()
    #-------------------------------------------------------------------------------------------------------------------------------------------------------

    def DEL_USERNAMEFIND():
        def USERNAMESEARCH():
            q1='username'
            q2=DELETE_entry1.get()
            p1=pwd_entry.get()
            mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
            cursor = mycon.cursor()
            qry=("SELECT * FROM password where %s='%s';"%(q1,q2,))
            data = pd.read_sql(qry,mycon)
            data_=pd.DataFrame(data)
            mycon.commit()
            answer=mb.askokcancel('Warning!',('Entry',data_,'Is going to be deleted and cannot cannot be undone .Do you want to proceed ?'))
            if answer==1:
                q1='username'
                q2=DELETE_entry1.get()
                p1=pwd_entry.get()
                mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
                cursor = mycon.cursor()
                qry2=("DELETE FROM password WHERE %s='%s';"%(q1,q2,))
                cursor.execute(qry2)
                mycon.commit()
                a=mb.showinfo('Success','The entry has been deleted')

        DELETE_label3=Label(delete,text="FINDING INFO IN USERNAME")
        DELETE_label3.place(x=0,y=450)
        DELETE_label4=Label(delete,text="Enter Username",font=("times new roman",20,"bold"),bg="white",fg="#FF7400",bd=1)
        DELETE_label4.place(x=20,y=200,relwidth=0.5)
        DELETE_entry1=Entry(delete,font=("bold",22),bg="white",fg="black",bd=1)
        DELETE_entry1.place(x=250,y=200,relwidth=0.45)
        DELETE_SEARCH_but=Button(delete,text='Enter',font=("bold",30),bg="gold",fg="white",bd=1,command=USERNAMESEARCH)
        DELETE_SEARCH_but.place(x=175,y=240,relwidth=0.3)
        
        p1=pwd_entry.get()
        mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
        cursor = mycon.cursor()
        qry3=("select distinct(platform) from password;")
        output2=""
        cursor.execute("select distinct(username) from password;")
        rows=cursor.fetchall()
        for row in rows:
           output2 += ' ' + str(row[0:8]) + ' ' + ','
        output2 = output2[:-1]

        DELETE_available_label=Label(delete,text='Available Usernames :-',font=("times new roman",12,"bold"),bg="white",fg="#FF7400",bd=1)
        DELETE_available_label.place(x=0,y=135,relwidth=0.4)
        DELETE_available_username_label=Label(delete,text=output2)
        DELETE_available_username_label.place(x=0,y=160)
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    def DEL_PLATFORMFIND():
        def PLATFORMSEARCH():
            q1='platform'
            q2=DELETE_entry2.get()
            p1=pwd_entry.get()
            mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
            cursor = mycon.cursor()
            qry=("SELECT * FROM password where %s='%s';"%(q1,q2,))
            data = pd.read_sql(qry,mycon)
            data_=pd.DataFrame(data)
            mycon.commit()
            answer=mb.askokcancel('Warning!',('Entry',data_,'Is going to be deleted and cannot cannot be undone .Press OK to proceed'))
            if answer==1:
                q1='platform'
                q2=DELETE_entry2.get()
                p1=pwd_entry.get()
                mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
                cursor = mycon.cursor()
                qry2=("DELETE FROM password WHERE %s='%s';"%(q1,q2,))
                cursor.execute(qry2)
                mycon.commit()
                a=mb.showinfo('Success','The entry has been deleted')            
            mycon.commit()
            #-------------------------------------------------------------------------------------------------------------------------------------------------------
        
        
        DELETE_label3=Label(delete,text="FINDING INFO IN PLATFORM")
        DELETE_label3.place(x=0,y=450)
        DELETE_label5=Label(delete,text="Enter Platform",font=("times new roman",20,"bold"),bg="white",fg="#FF7400",bd=1)
        DELETE_label5.place(x=20,y=200,relwidth=0.5)
        DELETE_entry2=Entry(delete,font=("bold",22),bg="white",fg="black",bd=1)
        DELETE_entry2.place(x=250,y=200,relwidth=0.45)
        DELETE_SEARCH_but=Button(delete,text='Enter',font=("bold",30),bg="gold",fg="white",bd=1,command=PLATFORMSEARCH)
        DELETE_SEARCH_but.place(x=175,y=240,relwidth=0.3)

        p1=pwd_entry.get()
        mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
        cursor = mycon.cursor()
        qry3=("select distinct(platform) from password;")
        output2=""
        cursor.execute("select distinct(platform) from password;")
        rows=cursor.fetchall()
        for row in rows:
           output2 += ' ' + str(row[0:8]) + ' ' + ','
        output2 = output2[:-1]

        DELETE_available_label=Label(delete,text='Available Platforms :-',font=("times new roman",12,"bold"),bg="white",fg="#FF7400",bd=1)
        DELETE_available_label.place(x=0,y=135,relwidth=0.4)
        DELETE_available_pforms_label=Label(delete,text=output2)
        DELETE_available_pforms_label.place(x=0,y=160)




    delete=Toplevel(root)
    delete.title('DELETE A PASSWORD')
    delete.geometry('500x500')
    delete.iconbitmap('icon.ico')
    delete.configure(background ='#FFE260')

    DELETE_label1=Label(delete,text='Search by Username or Platform ',font=("times new roman",20,"bold"),bg="white",fg="#FF7400",bd=1)
    DELETE_label1.place(x=20,y=20,relwidth=0.9)
    DELETE_USERNAME_but1=Button(delete,text="USERNAME",font=("bold",22),bg="gold",fg="white",bd=1,command=DEL_USERNAMEFIND)
    DELETE_USERNAME_but1.place(x=20,y=70,relwidth=0.45)
    DELETE_USERNAME_but2=Button(delete,text="PLATFORM",font=("bold",22),bg="gold",fg="white",bd=1,command=DEL_PLATFORMFIND)
    DELETE_USERNAME_but2.place(x=250,y=70,relwidth=0.45)
    DELETE_CLOSE_but=Button(delete,text="BACK",font=("bold",22),bg="gold",fg="white",bd=1,command=CLOSEDELETE)
    DELETE_CLOSE_but.place(x=300,y=400,relwidth=0.35)

#-------------------------------------------------------------------------------------------------------------------------------------------------------
def UPDATE():
    def CLOSEUPDATE():
        update.destroy()

    def UPDATE_USERNAMEFIND():
        def UPDATE_CHANGEUSERNAME():
            okcancel=mb.askokcancel("WARNING","The username cannot be undone after this process. Click OK to accept")
            if okcancel==1:                
                q1='username'
                q2=UPDATE_USERNAME_entry.get()
                q3=UPDATE_NEWUSERNAME_entry.get()
                p1=pwd_entry.get()
                mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
                cursor = mycon.cursor()
                qry4=("UPDATE password SET %s='%s'WHERe %s='%s';"%(q1,q3,q1,q2,))

                cursor.execute(qry4)
                mycon.commit()
                b=mb.showinfo("Success","The Username has been updated !")

        UPDATE_USERNAME_label=Label(update,text="Enter Username",font=("times new roman",18,"bold"),bg="white",fg="#FF7400",bd=1)
        UPDATE_USERNAME_label.place(x=10,y=225,relwidth=0.45)
        UPDATE_USERNAME_entry=Entry(update,font=("bold",20),bg="white",fg="black",bd=1)
        UPDATE_USERNAME_entry.place(x=220,y=225,relwidth=0.5)

        UPDATE_NEWUSERNAME_label=Label(update,text="New Username",font=("times new roman",18,"bold"),bg="white",fg="#FF7400",bd=1)
        UPDATE_NEWUSERNAME_label.place(x=10,y=275,relwidth=0.45)
        UPDATE_NEWUSERNAME_entry=Entry(update,font=("bold",20),bg="white",fg="black",bd=1)
        UPDATE_NEWUSERNAME_entry.place(x=220,y=275,relwidth=0.5)

        UPDATE_NEWUSERNAMECHANGE_but=Button(update,text='CHANGE',font=("bold",18),bg="gold",fg="white",bd=1,command=UPDATE_CHANGEUSERNAME)
        UPDATE_NEWUSERNAMECHANGE_but.place(x=220,y=315,relwidth=0.5)

        p1=pwd_entry.get()
        mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
        cursor = mycon.cursor()
        qry3=("select distinct(username) from password;")
        output2=""
        cursor.execute(qry3)
        rows=cursor.fetchall()
        for row in rows:
           output2 += ' ' + str(row[0:100]) + ' ' + ','
        output2 = output2[:-1]

        UPDATE_available_label=Label(update,text='Available Usernames :-',font=("times new roman",12,"bold"),bg="white",fg="#FF7400",bd=1)
        UPDATE_available_label.place(x=0,y=135,relwidth=0.4)
        UPDATE_available_pforms_label=Label(update,text=output2)
        UPDATE_available_pforms_label.place(x=0,y=160)


    def UDPATE_PLATFORMFIND():
        def UPDATE_CHANGEPLATFORM():
            okcancel=mb.askokcancel("WARNING","The username cannot be undone after this process. Click OK to accept")
            if okcancel==1:                
                q1='platform'
                q2=UPDATE_PLATFORM_entry.get()
                q3=UPDATE_NEWPLATFORM_entry.get()
                p1=pwd_entry.get()
                mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
                cursor = mycon.cursor()
                qry4=("UPDATE password SET %s='%s'WHERe %s='%s';"%(q1,q3,q1,q2,))

                cursor.execute(qry4)
                mycon.commit()
                b=mb.showinfo("Success","The Username has been updated !")

        UPDATE_PLATFORM_label=Label(update,text="Enter Platform",font=("times new roman",18,"bold"),bg="white",fg="#FF7400",bd=1)
        UPDATE_PLATFORM_label.place(x=10,y=225,relwidth=0.45)
        UPDATE_PLATFORM_entry=Entry(update,font=("bold",20),bg="white",fg="black",bd=1)
        UPDATE_PLATFORM_entry.place(x=220,y=225,relwidth=0.5)

        UPDATE_NEWPLATFORM_label=Label(update,text="New Platform",font=("times new roman",18,"bold"),bg="white",fg="#FF7400",bd=1)
        UPDATE_NEWPLATFORM_label.place(x=10,y=275,relwidth=0.45)
        UPDATE_NEWPLATFORM_entry=Entry(update,font=("bold",20),bg="white",fg="black",bd=1)
        UPDATE_NEWPLATFORM_entry.place(x=220,y=275,relwidth=0.5)

        UPDATE_NEWPLATFORMCHANGE_but=Button(update,text='CHANGE',font=("bold",18),bg="gold",fg="white",bd=1,command=UPDATE_CHANGEPLATFORM)
        UPDATE_NEWPLATFORMCHANGE_but.place(x=220,y=315,relwidth=0.5)

        p1=pwd_entry.get()
        mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
        cursor = mycon.cursor()
        qry3=("select distinct(platform) from password;")
        output2=""
        cursor.execute(qry3)
        rows=cursor.fetchall()
        for row in rows:
           output2 += ' ' + str(row[0:100]) + ' ' + ','
        output2 = output2[:-1]

        UPDATE_available_label=Label(update,text='Available Platforms :-',font=("times new roman",12,"bold"),bg="white",fg="#FF7400",bd=1)
        UPDATE_available_label.place(x=0,y=135,relwidth=0.4)
        UPDATE_available_pforms_label=Label(update,text=output2)
        UPDATE_available_pforms_label.place(x=0,y=160)

    def UPDATE_PASSWORDFIND():
        def UPDATE_CHANGEPASSWORD():
            okcancel=mb.askokcancel("WARNING","The password cannot be undone after this process. Click OK to accept")
            if okcancel==1:                
                q1='password'
                q2=UPDATE_PASSWORD_entry.get()
                q3=UPDATE_NEWPASSWORD_entry.get()
                p1=pwd_entry.get()
                mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
                cursor = mycon.cursor()
                qry4=("UPDATE password SET %s='%s'WHERe %s='%s';"%(q1,q3,q1,q2,))

                cursor.execute(qry4)
                mycon.commit()
                b=mb.showinfo("Success","The Password has been updated !")

        UPDATE_PASSWORD_label=Label(update,text="Enter Password",font=("times new roman",18,"bold"),bg="white",fg="#FF7400",bd=1)
        UPDATE_PASSWORD_label.place(x=10,y=225,relwidth=0.45)
        UPDATE_PASSWORD_entry=Entry(update,font=("bold",20),bg="white",fg="black",bd=1)
        UPDATE_PASSWORD_entry.place(x=220,y=225,relwidth=0.5)

        UPDATE_NEWPASSWORD_label=Label(update,text="New Password",font=("times new roman",18,"bold"),bg="white",fg="#FF7400",bd=1)
        UPDATE_NEWPASSWORD_label.place(x=10,y=275,relwidth=0.45)
        UPDATE_NEWPASSWORD_entry=Entry(update,font=("bold",20),bg="white",fg="black",bd=1)
        UPDATE_NEWPASSWORD_entry.place(x=220,y=275,relwidth=0.5)

        UPDATE_NEWPASSWORDCHANGE_but=Button(update,text='CHANGE',font=("bold",18),bg="gold",fg="white",bd=1,command=UPDATE_CHANGEPASSWORD)
        UPDATE_NEWPASSWORDCHANGE_but.place(x=220,y=315,relwidth=0.5)

        p1=pwd_entry.get()
        mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
        cursor = mycon.cursor()
        qry3=("select distinct(password) from password;")
        output2=""
        cursor.execute(qry3)
        rows=cursor.fetchall()
        for row in rows:
           output2 += ' ' + str(row[0:100]) + ' ' + ','
        output2 = output2[:-1]

        UPDATE_available_label=Label(update,text='Available Passwords :-',font=("times new roman",12,"bold"),bg="white",fg="#FF7400",bd=1)
        UPDATE_available_label.place(x=0,y=135,relwidth=0.4)
        UPDATE_available_pforms_label=Label(update,text=output2)
        UPDATE_available_pforms_label.place(x=0,y=160)
        





    update=Toplevel(root)
    update.title('UPDATE A PASSWORD')
    update.geometry('500x500')
    update.iconbitmap('icon.ico')
    update.configure(background ='#FFE260')


    UPDATE_label1=Label(update,text='Search by Username or Platform or Password',font=("times new roman",19,"bold"),bg="white",fg="#FF7400",bd=1)
    UPDATE_label1.place(x=0,y=20,relwidth=1)


    UPDATE_USERNAME_but1=Button(update,text="USERNAME",font=("bold",18),bg="gold",fg="white",bd=1,command=UPDATE_USERNAMEFIND)
    UPDATE_USERNAME_but1.place(x=10,y=70,relwidth=0.3)
    UPDATE_PLATFORM_but1=Button(update,text="PLATFORM",font=("bold",18),bg="gold",fg="white",bd=1,command=UDPATE_PLATFORMFIND)
    UPDATE_PLATFORM_but1.place(x=170,y=70,relwidth=0.3)
    UPDATE_PASSWORD_but1=Button(update,text="PASSWORD",font=("bold",18),bg="gold",fg="white",bd=1,command=UPDATE_PASSWORDFIND)
    UPDATE_PASSWORD_but1.place(x=330,y=70,relwidth=0.3)
    ACTION_CLOSE_but=Button(update,text="BACK",font=("bold",22),bg="gold",fg="white",bd=1,command=CLOSEUPDATE)
    ACTION_CLOSE_but.place(x=300,y=400,relwidth=0.35)
#------------------------------------------------------------------------------------------------
def GRAPH():
    p1=pwd_entry.get()
    mycon=sqltr.connect(host='localhost',user='root',passwd=(p1),database='Project')
    cursor = mycon.cursor()
    qry=(" select length(password) as length from password;")
    d1 = pd.read_sql(qry,mycon) 
    mycon.commit()
    a=np.array(d1)
    qry2=(" select platform from password;")
    d2 = pd.read_sql(qry2,mycon)  
    b=np.array(d2)     
    mycon.commit()
    c = a.flatten() 
    d=b.flatten()
    plt.plot(d,c)
    plt.xlabel('platform')
    plt.ylabel('password length')
    plt.show()




def ACTION():
    def CLOSEACTION():
        action.destroy()
    action=Toplevel(root)
    action.title('Choose The Options Below')
    action.geometry('500x500')
    action.iconbitmap('icon.ico')
    action.configure(background ='#FFE260')
    #ADD------------------------------------------------------------------------------------------
    add_but=Button(action,text='ADD',font=("bold",30),bg="gold",fg="white",bd=1,command=ADD)
    add_but.place(x=15,y=20,relwidth=0.4)
    #VIEW-----------------------------------------------------------------------------------------
    View_but=Button(action, text='VIEW', font=('bold', 30),bg='gold', fg='white', bd=1,command=VIEW)
    View_but.place(x=285,y=20,relwidth=0.4)
    #DELETE--------------------------------------------------------------------------------------
    Del_but=Button(action, text='DELETE', font=('bold', 30),bg='gold', fg='white', bd=1,command=DELETE)
    Del_but.place(x=15,y=200,relwidth=0.4)
    #UPDATE-------------------------------------------------------------------------------------
    Update_but=Button(action, text='UPDATE', font=('bold', 30),bg='gold', fg='white', bd=1,command=UPDATE)
    Update_but.place(x=285,y=200,relwidth=0.4)
    #CLOSE---------------------------------------------------------------------------------------------
    ACTION_CLOSE_but=Button(action,text="BACK",font=("bold",22),bg="gold",fg="white",bd=1,command=CLOSEACTION)
    ACTION_CLOSE_but.place(x=300,y=400,relwidth=0.35)
    #SHOW_GRAPH------------------------------------------------------------------------------------
    SHOW_GRAPH_but=Button(action,text="SHOW GRAPH",font=("bold",22),bg="gold",fg="white",bd=1,command=GRAPH)
    SHOW_GRAPH_but.place(x=15,y=400,relwidth=0.45)
#-------------------------------------------------------------------------------------------------
#MAIN WINDOW----------------------------------------------------------------------------------------
root=Tk()
root.title('MK Password Manager 1.11')
root.geometry('500x500')
root.iconbitmap('icon.ico')
root.configure(background ='#FFE260')
#variables---------------------------------------------------------------------------------------
pass_=StringVar()
#title-------------------------------------------------------------------------------------------
title=Label(root,text="Login",font=("times new roman",60,"bold"),bg="orange",fg="white",bd=20)
title.place(x=0,y=0,relwidth=1)
#login password label---------------------------
login_pwd_label=Label(root,text='Enter MySQL Password',font=("times new roman",20,"bold"),bg="white",fg="#FF7400",bd=1)
login_pwd_label.place(x=0,y=140,relwidth=1)
#login password entry---------------------------
pwd_entry=Entry(root,textvariable=pass_,show='*',font=("bold",20),bg="white",fg="orange",bd=1)
pwd_entry.place(x=0,y=180,relwidth=1)
#login button-----------------------------------
log_but=Button(root,text='Enter',font=("bold",30),bg="gold",fg="white",bd=1,command=LOGIN)
log_but.place(x=175,y=240,relwidth=0.3)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
root.mainloop()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
