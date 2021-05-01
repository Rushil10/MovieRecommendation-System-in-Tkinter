import cv2
from fer import FER
from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP

def getMoviethroughEmotion():
    global clicked
    def back(*args):
        clicked = True

    cap = cv2.VideoCapture(0)

    def mouse_click(event, x, y,
                    flags, param):
        global clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            print("clicked")
            clicked = True

    clicked = False
    while True:
        ret, image = cap.read()

        if not ret:
            break

        cv2.imshow("image", image)
        cv2.setMouseCallback("image", mouse_click)

        if clicked:
            break

        k = cv2.waitKey(1)
        if k == ord("q"):
            break

    detector = FER()
    emotion = detector.top_emotion(image)
    print(emotion)
    cv2.destroyAllWindows()
    cap.release()

    # Main Function for scraping
    def main(emotion):
        print("Emotion is here : ")
        print(emotion)
        # IMDb Url for Drama genre of
        # movie against emotion Sad
        if (emotion == "sad"):
            urlhere = 'http://www.imdb.com/search/title?genres=drama&title_type=feature&sort=moviemeter, asc'

        # IMDb Url for Musical genre of
        # movie against emotion Disgust
        elif (emotion == "disgust"):
            urlhere = 'http://www.imdb.com/search/title?genres=musical&title_type=feature&sort=moviemeter, asc'

        # IMDb Url for Family genre of
        # movie against emotion Anger
        elif (emotion == "angry"):
            urlhere = 'http://www.imdb.com/search/title?genres=family&title_type=feature&sort=moviemeter, asc'

        # IMDb Url for Sport genre of
        # movie against emotion Fear
        elif (emotion == "fear"):
            urlhere = 'http://www.imdb.com/search/title?genres=sport&title_type=feature&sort=moviemeter, asc'

        # IMDb Url for Thriller genre of
        # movie against emotion Enjoyment
        elif (emotion == "happy"):
            urlhere = 'http://www.imdb.com/search/title?genres=thriller&title_type=feature&sort=moviemeter, asc'

        # IMDb Url for Film_noir genre of
        # movie against emotion Surprise
        elif (emotion == "surprise"):
            urlhere = 'http://www.imdb.com/search/title?genres=film_noir&title_type=feature&sort=moviemeter, asc'

        else:
            urlhere = 'http://www.imdb.com/search/title?genres=western&title_type=feature&sort=moviemeter, asc'
        # HTTP request to get the data of
        # the whole page
        response = HTTP.get(urlhere)
        data = response.text

        # Parsing the data using
        # BeautifulSoup
        soup = SOUP(data, "lxml")

        # Extract movie titles from the
        # data using regex
        title = soup.find_all("a", attrs={"href": re.compile(r'\/title\/tt+\d*\/')})
        return title

    a = main(emotion[0])
    count = 0

    if (emotion == "Disgust" or emotion == "Anger"
            or emotion == "Surprise"):

        for i in a:

            # Splitting each line of the
            # IMDb data to scrape movies
            tmp = str(i).split('>;')

            if (len(tmp) == 3):
                print(tmp[1][:-3])

            if (count > 13):
                break
            count += 1
    else:
        for i in a:
            tmp = str(i).split('>')

            if (len(tmp) == 3):
                print(tmp[1][:-3])

            if (count > 11):
                break
            count += 1