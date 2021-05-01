import tkinter as tk
import urllib.request
from tkinter import ttk, messagebox
import mysql.connector
import PIL
from PIL import ImageTk, Image

Image.MAX_IMAGE_PIXELS = None

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ostpl_mp"
)

mycursor = mydb.cursor()


def scroll(name='user10@gmail.com',open_login=print('Hi')):
    import tkinter as tk
    from tkinter import ttk
    movie_cards = []
    class ScrollableFrame(ttk.Frame):
        def __init__(self, container, *args, **kwargs):
            super().__init__(container, *args, **kwargs)
            canvas = tk.Canvas(self,height=709,width=1055)
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
            self.scrollable_frame = ttk.Frame(canvas)

            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

    def addTpFavourites(id,title):
        print('Hi')
        check = "Select * from ostpl_mp.favourites where email=%s and movieId=%s"
        na=(name,id)
        print(na)
        mycursor.execute(check,na)
        myresult=mycursor.fetchall()
        if(len(myresult)>0):
            print(myresult)
            print('Already Exists !')
            messagebox.showinfo('Already Exists !', '{} is already in Your Favourites'.format(title))
        else:
            na=(name,id)
            sql = 'Insert into ostpl_mp.favourites(email,movieId) VALUES({},{})'.format('"{}"'.format(name),id)
            print(sql)
            mycursor.execute(sql)
            mydb.commit()
            messagebox.showinfo('Added', '{} is in Your Favourites'.format(title))
            print("Added")

    def addToLater(id,title):
        print('Hi')
        check = "Select * from ostpl_mp.watchlater where email=%s and movieId=%s"
        na=(name,id)
        print(na)
        mycursor.execute(check,na)
        myresult=mycursor.fetchall()
        if(len(myresult)>0):
            print(myresult)
            print('Already Exists !')
            messagebox.showinfo('Already Exists !', '{} is already in Watch Later'.format(title))
        else:
            na=(name,id)
            sql = 'Insert into ostpl_mp.watchlater(email,movieId) VALUES({},{})'.format('"{}"'.format(name),id)
            print(sql)
            mycursor.execute(sql)
            mydb.commit()
            messagebox.showinfo('Added', '{} is added to watch later'.format(title))
            print("Added")

    class MovieCard:
        def __init__(self,path='images/im1.jpg',tile='',loc='0',desc='',y='',r='4',time='120',genre='',d='None',id=0,show=0):
            self.MC = ttk.Label(frame.scrollable_frame)
            self.path=path
            self.tile=tile
            self.loc = loc
            self.desc = desc
            self.y = y
            self.r =r
            self.time = time
            self.genre = genre
            self.d = d
            self.id = id
            self.show=show

        def updateCard(self):
            #urllib.request.urlretrieve("https://i.imgur.com/ExdKOOz.png", "sample.png")
            #self.image=PIL.Image.open("sample.png")
            self.image = PIL.Image.open(self.path)
            self.image = self.image.resize((175, 205),Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(self.image)
            self.mainLabel = ttk.Label(self.MC,background="black",width="850")
            self.label = tk.Label(self.mainLabel,image=self.photo,bg="black",height=205,width=175)
            self.details = tk.Frame(self.mainLabel,bg="black",height=205,)
            self.features = tk.Frame(self.mainLabel,bg="black",height=205,width=405)
            self.textLabel = tk.Message(self.details,bg="black",fg="white",width=650,text=self.desc,font=("times new roman", 15))
            self.firstRow = tk.Frame(self.details)
            self.secondRow = tk.Frame(self.details)
            self.thirdRow = tk.Frame(self.details)
            self.fouthRow =tk.Frame(self.details)
            self.number = tk.Message(self.firstRow,bg="black",text='{}.'.format(self.loc),font=("times new roman", 16),fg="white")
            self.title = tk.Message(self.firstRow,width=500,bg="black",text =self.tile, font=("times new roman", 16),fg="white")
            self.year = tk.Message(self.firstRow,width=150,bg="black",text=self.y,fg="white",font=("times new roman", 16))
            self.runtime = tk.Message(self.secondRow,width=250,bg="black",text='{} | '.format(self.time),font=("times new roman", 15),fg="white")
            self.rating = tk.Message(self.thirdRow,width=650,bg="black",text=self.r,font=("times new roman", 15),fg="white")
            self.category = tk.Message(self.secondRow, width=550, bg="black", text=self.genre, font=("times new roman", 15), fg="white")
            self.director = tk.Message(self.fouthRow, width=550, bg="black", text=self.d, font=("times new roman", 15), fg="white")
            self.atf = tk.Button(self.mainLabel,bg="green",fg="white",text="Add To Favourites",font=("times new roman", 15),command=lambda:addTpFavourites(self.id,self.tile))
            self.wl = tk.Button(self.mainLabel,bg="#4169e1",fg="white",text="Watch Later",font=("times new roman", 15),command=lambda:addToLater(self.id,self.tile))
            self.rff = tk.Button(self.mainLabel, bg="red", fg="white", text="Remove from Favourites",
                                 font=("times new roman", 11), command=lambda: removeFromFav(self.id,self.tile))
            self.rfwl = tk.Button(self.mainLabel, bg="red", fg="white", text="Remove from Watch Later",
                                 font=("times new roman", 11), command=lambda: removeFromWl(self.id, self.tile))
            self.number.grid(row=0, column=0)
            self.title.grid(row=0, column=1)
            self.year.grid(row=0, column=2)
            self.runtime.grid(row=0,column=0)
            self.category.grid(row=0,column=1)
            self.rating.grid(row=0,column=0)
            self.director.grid(row=0,column=0)
            self.firstRow.pack(anchor="w")
            self.secondRow.pack(anchor="w")
            self.thirdRow.pack(anchor="w")
            self.textLabel.pack(anchor="w")
            self.fouthRow.pack(anchor="w")
            self.label.grid(row=0,column=0)
            self.details.grid(row=0, column=1)
            if self.show == 0 :
                self.atf.place(x=875, y=45, height=45, width=175)
                self.wl.place(x=875, y=105, height=45, width=175)
            self.features.grid(row=0,column=2)
            self.details.grid_propagate(0)
            self.mainLabel.pack()
            self.MC.pack(pady=4.5,anchor="w")

        def changeImage(self,imgPath,heading,desc,y,r,time,genre,d,id,show=0):
            print(show)
            self.show=show
            self.id=id
            self.tile=heading
            self.newImage = Image.open(imgPath)
            self.newImage = self.newImage.resize((175, 205), Image.ANTIALIAS)
            self.newPhoto = ImageTk.PhotoImage(self.newImage)
            self.label.configure(image=self.newPhoto)
            self.label.image = self.newPhoto
            self.title.configure(text=heading)
            self.textLabel.configure(text=desc)
            self.year.configure(text=y)
            self.runtime.configure(text=time)
            self.rating.configure(text=r)
            self.category.configure(text=genre)
            self.director.configure(text=d)
            if(self.show==1):
                self.rff.place(x=875, y=45, height=45, width=175)
                self.wl.place(x=875, y=105, height=45, width=175)
                self.atf.place(x=1150, y=45, height=45, width=175)
                self.rfwl.place(x=1150, y=105, height=45, width=175)
            elif self.show==0 :
                self.rff.place(x=1150,y=45, height=45, width=175)
                self.atf.place(x=875, y=45, height=45, width=175)
                self.wl.place(x=875, y=105, height=45, width=175)
                self.rfwl.place(x=1150, y=105, height=45, width=175)
            else:
                self.atf.place(x=875, y=45, height=45, width=175)
                self.rff.place(x=1150, y=45, height=45, width=175)
                self.rfwl.place(x=875, y=105, height=45, width=175)
                self.wl.place(x=1150, y=105, height=45, width=175)
        def destroy(self):
            print("Destroing")
            self.label = tk.Label(self.MC, image=self.photo, bg="blue", height=0, width=0)
            self.label.pack()
            self.MC.pack(pady=0)

    root = tk.Tk()
    root.geometry("1525x759")
    frame = ScrollableFrame(root)
    y=10

    def changeMovieCard(category):
        na = (category,)
        mycursor.execute("SELECT * FROM ostpl_mp.movies Where type = %s", na)
        myresult = mycursor.fetchall()
        k=0
        for i in movie_cards:
            if(k<len(myresult)):
                i.changeImage('imgs/{}.jpg'.format(myresult[k][0]),myresult[k][1],myresult[k][2][5:],myresult[k][8],'Imdb {}'.format(myresult[k][4]),myresult[k][7],myresult[k][9],'Director : {}'.format(myresult[k][5]),myresult[k][0])
                k=k+1

    def removeFromFav(id,title):
        print('Removing')
        sql='Delete from favourites where email=%s and movieId=%s'
        na=(name,id)
        mycursor.execute(sql,na)
        mydb.commit()
        showFavourites()

    def removeFromWl(id,title):
        print('Removing')
        sql='Delete from watchlater where email=%s and movieId=%s'
        na=(name,id)
        mycursor.execute(sql,na)
        mydb.commit()
        showWatchLater()


    def getMovieDataOfCategory(category):
        na=(category,)
        mycursor.execute("SELECT * FROM ostpl_mp.movies Where type = %s", na)
        myresult=mycursor.fetchall()
        for i in range(len(myresult)):
            print(myresult[i][9])
            movie_cards.append(MovieCard('imgs/{}.jpg'.format(myresult[i][0]),myresult[i][1],str(myresult[i][0]-132),myresult[i][2][5:],myresult[i][8],'Imdb {}'.format(myresult[i][4]),myresult[i][7],myresult[i][9],'Director : {}'.format(myresult[i][5]),myresult[i][0]))

    getMovieDataOfCategory('comedy')

    for obj in movie_cards:
        obj.updateCard()

    def showFavourites():
        sql='SELECT movies.* FROM ostpl_mp.favourites inner join ostpl_mp.movies where favourites.movieId=movies.id and favourites.email=%s order by addedAt DESC;'

        na=(name,)
        mycursor.execute(sql,na)
        myresult=mycursor.fetchall()
        n=len(myresult)
        k = 0
        for i in movie_cards:
            if (k < len(myresult)):
                i.changeImage('imgs/{}.jpg'.format(myresult[k][0]), myresult[k][1], myresult[k][2][5:], myresult[k][8],
                              'Imdb {}'.format(myresult[k][4]), myresult[k][7], myresult[k][9],
                              'Director : {}'.format(myresult[k][5]), myresult[k][0],1)
                k = k + 1
            else:
                i.changeImage('imgs/em3.jpg','-','-','-','-','-','-','-',0)
        #frame.yview_moveto(float(0))

    def showWatchLater():
        sql='SELECT movies.* FROM ostpl_mp.watchlater inner join ostpl_mp.movies where watchlater.movieId=movies.id and watchlater.email=%s order by addedAt DESC;'

        na=(name,)
        mycursor.execute(sql,na)
        myresult=mycursor.fetchall()
        n=len(myresult)
        k = 0
        for i in movie_cards:
            if (k < len(myresult)):
                i.changeImage('imgs/{}.jpg'.format(myresult[k][0]), myresult[k][1], myresult[k][2][5:], myresult[k][8],
                              'Imdb {}'.format(myresult[k][4]), myresult[k][7], myresult[k][9],
                              'Director : {}'.format(myresult[k][5]), myresult[k][0],2)
                k = k + 1
            else:
                i.changeImage('imgs/em3.jpg','-','-','-','-','-','-','-',0)

    frame.place(x=445,y=49)
    comedy=tk.Button(root,text="Comedy",command=lambda : changeMovieCard('comedy'),bg="black",fg="#7fff00",bd=0,font=("times new roman",21))
    comedy.place(x=447,y=1,height=45,width=145)
    mystery = tk.Button(root,text="Mystery",command=lambda : changeMovieCard('mystery'),bg="black",fg="#1da1f2",bd=0,font=("times new roman",21)).place(x=605,y=1,height=45,width=145)
    action = tk.Button(root, text="Action", command=lambda: changeMovieCard('action'), bg="black", fg="#ff4500",
                        bd=0, font=("times new roman", 21)).place(x=765, y=1, height=45, width=145)
    horror = tk.Button(root, text="Horror", command=lambda: changeMovieCard('horror'), bg="black", fg="#dcdcdc",
                       bd=0, font=("times new roman", 21)).place(x=925, y=1, height=45, width=145)
    animation = tk.Button(root, text="Animated", command=lambda: changeMovieCard('animation'), bg="black", fg="#00ffff",
                       bd=0, font=("times new roman", 21)).place(x=1085, y=1, height=45, width=145)
    series = tk.Button(root, text="Series", command=lambda: changeMovieCard('series'), bg="black", fg="#ffd700",
                          bd=0, font=("times new roman", 21)).place(x=1245, y=1, height=45, width=145)
    print(name)
    image2 = PIL.Image.open('imgs/fbg2.jpg')
    image2 = image2.resize((445, 759), Image.ANTIALIAS)
    photo2 = ImageTk.PhotoImage(image2)
    user = tk.Frame(root)
    lbl = tk.Label(user,image=photo2)
    lbl.place(x=0,y=0)
    def logout():
        root.destroy()
        open_login()

    favourites = tk.Button(root, text="My Favourites", bg="black", fg="#e0ffff",command=showFavourites,
                       bd=0, font=("times new roman", 21)).place(x=100, y=405, height=45, width=245)
    watchlater = tk.Button(root, text="Watch Later", bg="black", fg="#e0ffff",command=showWatchLater,
                       bd=0, font=("times new roman", 21)).place(x=100, y=475, height=45, width=245)
    logout = tk.Button(root, text="Logout", bg="black", fg="#e0ffff",command=logout,
                       bd=0, font=("times new roman", 21)).place(x=100, y=545, height=45, width=245)
    usr_lbl = tk.Label(root,text=name,fg='#e0ffff',bd=0, font=("times new roman", 21,),bg='black').place(x=100,y=105,height=45,width=245)
    user.place(x=0, y=0, height=759, width=445)
    root.mainloop()