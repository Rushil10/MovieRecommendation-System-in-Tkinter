import requests
from bs4 import BeautifulSoup
import mysql.connector
import urllib.request

from PIL import Image

#Parsing Imdb page to get movies information

#Change genre name to get data related to different genre
horror_url = "https://www.imdb.com/search/title/?genres=Animation&title_type=feature&explore=genres"

#Url to get top series from imdb site
series_url = "https://www.imdb.com/list/ls025873927/?sort=moviemeter,asc&st_dt=&mode=detail&page=1"

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ostpl_mp"
)

mycursor = mydb.cursor()

def getSeriesData():
    titles = []
    years = []
    genres = []
    runtimes = []
    imdb_ratings = []
    urls = []
    descriptions = []
    codes = []

    r = requests.get(series_url)

    # create a BeautifulSoup object
    soup = BeautifulSoup(r.text, 'html.parser')

    movie_containers = soup.findAll('div', class_='lister-item mode-detail')
    for container in movie_containers:

        #Get title
        title=container.h3.a.text
        titles.append(title)

        #Get Year
        year = container.h3.find('span', class_='lister-item-year text-muted unbold').text
        years.append(year)
        print(year)

        #Get Genre
        genre = container.p.find('span', class_='genre').text
        genres.append(genre[1:(len(genre) - 11)])

        #Get Description
        description = container.findAll('p', class_="")
        descriptions.append(description[len(description) - 1].text)

        #Get runtime
        time = container.p.find('span', class_='runtime').text
        runtimes.append(time)

        #Get Imdb Rating
        imdb_rating=container.find('span',class_='ipl-rating-star__rating').text
        imdb_ratings.append(imdb_rating)

        #Get Image Url
        im = container.find('div', class_="lister-item-image ribbonize")
        k = im.a.img['loadlate']
        code = im.a['href']
        urls.append(k) # Image urls
        codes.append(code)

    #Inserting into table
    sql = "INSERT INTO movies (title,description,type,imdb,director,image,runtime,years,genres,code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    # Storing Every Series in sql database
    # Maximum 44 Series
    # Keep genre name to series
    for i in range(44):
        try:
            na = (
                titles[i], descriptions[i], 'series', imdb_ratings[i], '-', urls[i], runtimes[i], years[i],
                genres[i],codes[i])
            mycursor.execute(sql, na)
            mydb.commit()
        except:
            print("--------------")
            print(titles[i])
            print(i)


def getMovieData(url):

    #Parses Movie Data Of Imdb Pages of Top 50 Movies according to genres
    titles=[]
    years=[]
    genres = []
    runtimes = []
    imdb_ratings=[]
    votes=[]
    urls=[]
    metascores=[]
    descriptions = []
    directors = []
    codes = []

    r = requests.get(url)

    # create a BeautifulSoup object
    soup = BeautifulSoup(r.text, 'html.parser')

    movie_containers = soup.findAll('div', class_ = 'lister-item mode-advanced')

    for container in movie_containers:

        if container.find('div', class_='ratings-metascore') is not None:

            #Get Title
            title = container.h3.a.text
            titles.append(title)

            #Get Year
            year = container.h3.find('span', class_='lister-item-year text-muted unbold').text
            years.append(year)

            #Get Image Url and Code to get on particular movie page
            im = container.find('div', class_="lister-item-image float-left")
            k = im.a.img['loadlate']
            code = im.a['href']
            urls.append(k) # Image urls
            codes.append(code)

            # genre
            genre = container.p.find('span', class_='genre').text
            genres.append(genre[1:(len(genre)-11)])

            # runtime
            time = container.p.find('span', class_='runtime').text
            runtimes.append(time)

            # IMDB ratings
            imdb = float(container.strong.text)
            imdb_ratings.append(imdb)

            # Metascore
            m_score = container.find('span', class_='metascore').text
            metascores.append(int(m_score))

            # Number of votes
            vote = container.find('span', attrs={'name': 'nv'})['data-value']
            votes.append(int(vote))

            #Description
            description = container.findAll('p',class_="text-muted")
            descriptions.append(description[len(description)-1].text)

            #Director Name
            allDs = container.findAll('p',class_="")
            directors.append(allDs[len(allDs)-1].a.text)

    sql = "INSERT INTO movies (title,description,type,imdb,director,image,runtime,years,genres,code) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    #Storing Every Category in sql database
    #Maximum 44 Movies of each category
    #Change genre name according to category url

    for i in range(44):
        try:
            na = (
                titles[i], descriptions[i], 'animation', imdb_ratings[i], directors[i], urls[i], runtimes[i], years[i],
                genres[i],codes[i])
            #Adding movie details to database
            mycursor.execute(sql, na)
            mydb.commit()
        except:
            #On Error get title name
            print("--------------")
            print(titles[i])
            print(i)


def parseMovieData():
    #Parses Movie Data according to url and inserts into mysql database
    getMovieData(horror_url)

#Downloading Images through url stored in database into this file
def downloadHighQualityImages():

    sql = "SELECT id,image,code FROM ostpl_mp.movies';"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)

    for i in range(len(myresult)):
        url = myresult[i][1]
        id = myresult[i][0]
        print(url)
        print(str(id))
        #url[:-20] is done to get high quality images as lasto 20 characters of imdb page url compress the image
        #Images are downloaded and stored in allImages Folder
        #We map every movie's image name with it's id so it's easy to access them
        urllib.request.urlretrieve(url[:-20], "allImages/{}.jpg".format(str(id)))

#After downloading all Images we need to reduce image size
#So wee call this function and store reduced images in imgs folder
#Small images take less time to render in tkinter frame
def reduceImageSize():
    for i in range(133,378):
        foo=Image.open("allImages/{}.jpg".format(str(i)))
        foo=foo.resize((175,205),Image.ANTIALIAS)
        foo.save('imgs/{}.jpg'.format(str(i)),quality=95)


