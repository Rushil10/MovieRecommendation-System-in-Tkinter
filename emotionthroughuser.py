import cv2
from fer import FER
from bs4 import BeautifulSoup as SOUP
import re
import requests as HTTP

#GEtting Emotion Of User
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
    return emotion

