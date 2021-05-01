from tkinter import *
from tkinter import messagebox
import mysql.connector
import re
from PIL import ImageTk, Image
import scroll_example

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ostpl_mp"
)

mycursor = mydb.cursor()

def window():
    #from signup import signup_window

    def goToSignup():
        form.destroy()
        signup_window()

    def checkUsername(name):
        check1 = 'Username must be atleast 5 charcters long !'
        if (len(name) < 5):
            return check1
        else:
            return ''

    def checkPassword(password):
        check1 = 'Password must be greater than 8 characters and less than 15 characters'
        check2 = 'Password must contain atleast lowerCase letter'
        check3 = 'Password must contain atleast upperCase letter'
        check4 = 'Password must contain atleast one digit '
        check5 = 'Password must contain atlease one special symbol '
        special = ['$', '#', '@']
        x = re.findall(".*[a-z].*", password)
        y = re.findall(".*[A-Z].*", password)
        z = re.findall(".*\d.*", password)
        if (len(password) < 8 or len(password) > 15):
            return check1
        elif len(x) == 0:
            return check2
        elif len(y) == 0:
            return check3
        elif (len(z) == 0):
            return check4
        else:
            return ''

    def open_login():
        window()

    def login():
        name = txt_email.get()
        credential = txt_password.get()
        sql = "Select * from users where email = %s and password = %s "
        prop = (name, credential)
        mycursor.execute(sql, prop)
        myresult = mycursor.fetchall()
        if (len(name) == 0 or len(credential) == 0):
            messagebox.showinfo('Failed', 'Username and password must not be empty !')
        else:
            if (len(myresult) == 1):
                form.destroy()
                scroll_example.scroll(name, open_login)
                # messagebox.showinfo('Success', 'Login Successfull ! ')
                # form.destroy()
            else:
                messagebox.showinfo('Failed', 'Login Unsuccessfull !')

    form = Tk()
    form.geometry("2000x795")
    image = Image.open('imgs/bg7.jpg')
    image = image.resize((1920, 795), Image.ANTIALIAS)
    bg = ImageTk.PhotoImage(image)
    bg_image = Label(form, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    Frame_login = Frame(form, bg="black")
    Frame_login.place(x=150, y=150, height=355, width=500)

    title = Label(Frame_login, text="Login", font=("Impact", 35,), fg="#1da1f2", bg="black").place(x=90, y=30)

    lbl_email = Label(Frame_login, text="Email", font=("Goudy old style", 25,), fg="#1da1f2", bg="black").place(x=90,
                                                                                                                y=97)
    txt_email = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
    txt_email.place(x=90, y=139, width=255, height=35)

    lbl_password = Label(Frame_login, text="Password", font=("Goudy old style", 25,), fg="#1da1f2", bg="black").place(
        x=90, y=185)
    txt_password = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
    txt_password.place(x=90, y=225, width=255, height=35)

    signup_btn = Button(Frame_login, command=goToSignup, text="Don't have an account? Signup", bg="black", fg="#1da1f2",
                        bd=0, font=("times new roman", 15)).place(x=90, y=275)

    login_btn = Button(form, text="Login", bg="#1da1f2", fg="black", command=login, font=("times new roman", 20)).place(
        x=305, y=479, height=40, width=175)

    # Frame_login.configure(bg='green')
    form.title('Ostpl Login Form')
    form.mainloop()

def signup_window():
    #from main import window

    def open_login():
        window()

    def goToLogin():
        form.destroy()
        window()

    def checkUsername(name):
        check1 = 'Email must be atleast 5 charcters long !'
        check0 = 'Email cannot be empty'
        if (len(name) < 1):
            return check0
        else:
            return ''

    def checkPassword(password):
        check1 = 'Password must be greater than 8 characters and less than 15 characters'
        check2 = 'Password must contain atleast lowerCase letter'
        check3 = 'Password must contain atleast upperCase letter'
        check4 = 'Password must contain atleast one digit '
        check5 = 'Password must contain atlease one special symbol '
        special = ['$', '#', '@']
        x = re.findall(".*[a-z].*", password)
        y = re.findall(".*[A-Z].*", password)
        z = re.findall(".*\d.*", password)
        if (len(password) < 8 or len(password) > 15):
            return check1
        elif len(x) == 0:
            return check2
        elif len(y) == 0:
            return check3
        elif (len(z) == 0):
            return check4
        else:
            return ''

    def signup():
        err = ''
        email = txt_email.get()
        credential = txt_password.get()
        username = txt_username.get()
        if (checkUsername(email) != '' or checkPassword(credential) != ''):
            if (checkUsername(email) != ''):
                err = checkUsername(email)
            else:
                err = checkPassword(credential)
            messagebox.showinfo('Failed', err)
        else:
            sql = "INSERT INTO users (email,username,password) VALUES(%s,%s,%s)"
            check = "SELECT * FROM users where email=%s"
            try:
                na = (email,)
                mycursor.execute("SELECT * FROM users Where email = %s", na)
                stop = 0
                myresult = mycursor.fetchall()
                if (len(myresult) == 0):
                    val = (email,username, credential)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    if (mycursor.lastrowid):
                        #messagebox.showinfo('Success', 'Signup Successfull')
                        form.destroy()
                        scroll_example.scroll(email, open_login)
                else:
                    messagebox.showinfo('Failed', 'Account Already Exists ! Pls Login')
            except:
                messagebox.showinfo('Failed', 'Signup Unsuccessfull !')
        print("Hi")
        print(credential)

    def login():
        name = txt_email.get()
        credential = txt_password.get()
        sql = "Select * from login_details where username = %s and password = %s "
        prop = (name, credential)
        mycursor.execute(sql, prop)
        myresult = mycursor.fetchall()
        if (len(name) == 0 or len(credential) == 0):
            messagebox.showinfo('Failed', 'Username and password must not be empty !')
        else:
            if (len(myresult) == 1):
                form.destroy()
                # messagebox.showinfo('Success', 'Login Successfull ! ')
                # form.destroy()
            else:
                messagebox.showinfo('Failed', 'Login Unsuccessfull !')

    form = Tk()
    form.geometry("2000x795")
    image = Image.open('imgs/bg7.jpg')
    image = image.resize((1920, 795), Image.ANTIALIAS)
    bg = ImageTk.PhotoImage(image)
    bg_image = Label(form, image=bg).place(x=0, y=0, relwidth=1, relheight=1)

    Frame_login = Frame(form, bg="black")
    Frame_login.place(x=150, y=75, height=475, width=500)

    title = Label(Frame_login, text="Signup", font=("Impact", 35,), fg="#1da1f2", bg="black").place(x=90, y=30)

    lbl_email = Label(Frame_login, text="Email", font=("Goudy old style", 25,), fg="#1da1f2", bg="black").place(x=90,
                                                                                                                y=97)
    txt_email = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
    txt_email.place(x=90, y=139, width=255, height=35)

    lbl_password = Label(Frame_login, text="Password", font=("Goudy old style", 25,), fg="#1da1f2", bg="black").place(
        x=90, y=185)
    txt_password = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
    txt_password.place(x=90, y=225, width=255, height=35)

    lbl_username = Label(Frame_login, text="Username", font=("Goudy old style", 25,), fg="#1da1f2", bg="black").place(
        x=90, y=275)
    txt_username = Entry(Frame_login, font=("times new roman", 15), bg="lightgray")
    txt_username.place(x=90, y=315, width=255, height=35)

    login_btn = Button(Frame_login,command=goToLogin,text="Already have an account? Login",bg="black",fg="#1da1f2",bd=0,font=("times new roman",15)).place(x=90,y=365)

    signup_btn = Button(form, text="Signup", bg="#1da1f2", fg="black", command=signup, font=("times new roman", 20)).place(
        x=305, y=531, height=40, width=175)

    # Frame_login.configure(bg='green')
    form.title('Ostpl Login Form')
    form.mainloop()



window()
#mainpage.mainScreen()
#scroll_example.scroll()
#movie_data_parse.exec()
