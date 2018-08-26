#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import pyrebase
import json
import os
app = Flask(__name__)
vc = cv2.VideoCapture(0)
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = vc.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def getNgroxURL():
    try:

        os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

        with open('tunnels.json') as data_file:
            datajson = json.load(data_file)

        msg = 'ngrok URL\'s: \n'

        for i in datajson['tunnels']:
            msg = i['public_url'] + '\n'
        return msg
    except BaseException as e:
        print(e)



def updateURL():
    x = getNgroxURL()
    config = json.load(open('../firebaseConfig.json'))
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child("pistream").update({"djfklejdsjodjsfi":{"pistreamURL": x[:len(x)-1]}})

updateURL()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
