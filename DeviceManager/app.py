from crypt import methods
import json
from flask import Flask, render_template, Response, redirect, request, session, url_for
import cv2
import time

app = Flask(__name__)
app.config['SECRET_KEY']="asdadvadfsdfs"      #random secret key
app.config['ENV']='development'

def readData():
    path="deviceStats.json"   #here define the path where the file is located, from which the data is to be read
    data=None
    with open(path ,'r') as file:
        data=json.load(file)

    path="/home/attu/Downloads/"  #path for the bhagwat bhaiya's file
    data['temperature']=None
    with open(path+'met' ,'r') as file:
        data['temperature']=file.readlines()

    data['battery_parameters']=None
    with open(path+'battery_parameters' ,'r') as file:
        data['battery_parameters']=file.readlines()

    data['light_intensity']=None
    with open(path+'light_intensity' ,'r') as file:
        data['light_intensity']=file.readlines()[0].split(":")[1:]

    data['gps']=None
    with open("gps.json" ,'r') as file:  #please here define the path of gps file
        data['gps']=json.load(file)

    return data


@app.route('/',methods=["GET","POST"])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('pass')
        credentials=None
        with open('credentials.json') as file:
            credentials=json.load(file)
        if credentials['email']==email and credentials['password']==password:
            session['username']=credentials['username']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

def gen_frames():  # generate frame by frame from camera
    
    camera = cv2.VideoCapture(0)  # use 0 for web camera
    #  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
    # for local webcam use cv2.VideoCapture(0)
    while True:
        print("kuch toh")
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        


@app.route('/video_feed')
def videoFeed():
    if 'username' in  session:
    #Video streaming route. Put this in the src attribute of an img tag
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return redirect(url_for('login'))

@app.route('/video')
def video(): 
    if 'username' in session:
        return render_template('videoFeed.html')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('Dashboard.html',data=readData())
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)