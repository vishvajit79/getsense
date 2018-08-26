# Face Recognition
# Importing the libraries
from collections import deque
from http.server import HTTPServer
from multiprocessing.pool import ThreadPool




from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import requests
import json
# add multiple images with concepts


import cv2
from threading import Thread
import time
camera_type = 'local'
# Loading the cascades
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')


# Defining a function that will do the detections
def detect(gray, frame, counter, modvar):
    print(counter)
    if counter % modvar == 0:
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            Thread(target=makeImage(frame,counter), args=()).start()

    return frame


def makeImage(frame, counter):
    img_name = "opencv_frame_{}.png".format(counter)
    cv2.imwrite("./images/" + img_name, frame)
    predictImage("./images/" + img_name)
    print("{} written!".format(img_name))

# Doing some Face Recognition with the webcam
def runCam():
    video_capture = cv2.VideoCapture(0)
    modvar = 20
    counter = 0
    while True:
        _, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canvas = detect(gray, frame, counter, modvar)
        cv2.imshow('Video', canvas)
        counter+=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()

# generic routine to grab one frame from camera


def predictImage(imageUrl):
    app = ClarifaiApp(api_key='API_KEY')
    model = app.models.get('getsense')
    image = ClImage(filename=imageUrl)
    prediction = model.predict([image])
    print(prediction['outputs'][0]['input']['data']['image']['url'])
    print("PREDICTION IS: " + str(prediction['outputs'][0]['data']['concepts'][0]['value']))
    if prediction['outputs'][0]['data']['concepts'][0]['value'] < 0.95:
        print(prediction['outputs'][0]['input']['data']['image']['url'][8:])
        requests.get("https://vishvajit79.lib.id/getsense@dev/alertSlack/?url=" + prediction['outputs'][0]['input']['data']['image']['url'])


Thread(target=runCam(), args=()).start()
