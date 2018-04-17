#!/usr/bin/env python
from flask import Flask, render_template, Response
from gpiozero import MotionSensor

from camera import Camera

app = Flask(__name__)

pir = MotionSensor(4)

@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        if pir.motion_detected:
            frame = camera.get_frame()
        else:
            frame = open('no_motion.jpg', 'rb').read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
