import cv2
from flask import Flask, render_template, request, redirect, session, Response
from requests import post
from datetime import datetime
import webbrowser

app = Flask(__name__)
cam = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('C:/Users/vikto/Documents/CODE/python/fun/fd/web/static/shiiid.xml')
cooldown = datetime.now().strftime('%m%d%H' + str(int(datetime.now().strftime('%M'))-2))
webbrowser.open_new_tab('10.11.46.120:5000')


def gen_frames():
    global cooldown
    while True:
        success, frame = cam.read()
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.5, 5)
            if len(faces)!=0:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    if datetime.now().strftime('%m%d%H%M') > cooldown:
                        post('https://maker.ifttt.com/trigger/yuh/with/key/fmO4phgnKpiYkrEqbhuYbo2MHAK2LGasy2_2nyBMDOH')
                        cooldown = datetime.now().strftime('%m%d%H' + str(int(datetime.now().strftime('%M'))+2))
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True, host='10.11.46.120')
