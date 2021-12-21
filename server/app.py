#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, send_from_directory
from flask_cors import *
import traceback
import sys


# import camera driver

try:
    from camera_opencv import Camera
except:
    print("An exception occurred cannot load camera cannot improt Camera")
    print(traceback.format_exc())



import threading

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)
CORS(app, supports_credentials=True)

camera = "" 
try:
    camera = Camera()
    print(traceback.format_exc())

except:
    print("An exception occurred cannot load camera cannot create object")

def gen(camera):
    """Video streaming generator function."""
    while True:
        try:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            continue
             
              

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

dir_path = os.path.dirname(os.path.realpath(__file__))

@app.route('/api/img/<path:filename>')
def sendimg(filename):
    print("sendimg")
    print(dir_path)
    print(filename)
    return send_from_directory(dir_path+'/dist/img', filename)

@app.route('/js/<path:filename>')
def sendjs(filename):
    print("sendjs")
    print(dir_path)
    print(filename)
    return send_from_directory(dir_path+'/dist/js', filename)

@app.route('/css/<path:filename>')
def sendcss(filename):
    print("sendcss")
    print(dir_path)
    print(filename)
    return send_from_directory(dir_path+'/dist/css', filename)

@app.route('/api/img/icon/<path:filename>')
def sendicon(filename):
    print("sendicon")
    print(dir_path)
    print(filename)
    return send_from_directory(dir_path+'/dist/img/icon', filename)

@app.route('/fonts/<path:filename>')
def sendfonts(filename):
    return send_from_directory(dir_path+'/dist/fonts', filename)

@app.route('/<path:filename>')
def sendgen(filename):
    print("sendgen")
    print(dir_path)
    print(filename)
    return send_from_directory(dir_path+'/dist', filename)

@app.route('/')
def index():
    print("index")
    return send_from_directory(dir_path+'/dist', 'index.html')

class webapp:
    def __init__(self):
        self.camera = camera

    def modeselect(self, modeInput):
        Camera.modeSelect = modeInput

    def colorFindSet(self, H, S, V):
        camera.colorFindSet(H, S, V)

    def thread(self):
        app.run(host='0.0.0.0', threaded=True)

    def startthread(self):
        fps_threading=threading.Thread(target=self.thread)         #Define a thread for FPV and OpenCV
        fps_threading.setDaemon(False)                             #'True' means it is a front thread,it would close when the mainloop() closes
        fps_threading.start()                                     #Thread starts


