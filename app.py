from crypt import methods
import json
from multiprocessing import dummy
from flask import Flask, render_template, Response, redirect, request, session, url_for, abort, send_file
import cv2
import time
import os
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY']="asdadvadfsdfs"      #random secret key
app.config['ENV']='development'
app.config['UPLOAD_FOLDER']='/media/mmcblk1p1'
app.config['RANA_FOLDER']='/usr/sbin/rana'

def readFile(fileName):
    path="/tmp/"+fileName
    data={}
    try:
        with open(path ,'r') as file:
            data=json.load(file)
    except FileNotFoundError:
        data={"error":"File not found"}
    except json.decoder.JSONDecodeError:
        data={"error":"File is passed instead of json file"}
    except Exception as e:
        data={"error":str(e)}
    return data

def readData():
    data={}
    tmp=readFile("devicestats")
    if "error" in tmp:
        data={
            "cpuInfo":{"usage":tmp["error"]},
            "gpuInfo":{"memoryUsage":404},
            "internet":{"connectivity":tmp["error"],"signal":tmp["error"]},
            "ramInfo":{"total":tmp["error"],"usage":tmp["error"],"free":tmp["error"]},
            "generalInfo":{"board_serial":tmp["error"],"board_type":"NRF","board_revision":tmp["error"]}
        }
    else:
        data=tmp

    tmp=readFile("met")
    if "error" in tmp:
        data['temperature']={"Relative_humidity":tmp["error"],"Temperature_c":tmp["error"],"Temperature_f":tmp["error"]}
    else:
        data['temperature']=tmp

    tmp=readFile("battery_parameters")
    if "error" in tmp:
        data['battery_parameters']={"Voltage":tmp["error"],"Internal_temperature":tmp["error"],"Average_current":tmp["error"]}
    else:
        data['battery_parameters']=tmp

    tmp=readFile("light_intensity")
    if "error" in tmp:
        data['light_intensity']={"Light_Intensity":tmp["error"]}
    else:
        data['light_intensity']=tmp

    tmp=readFile("gps")
    if "error" in tmp:
        data['gps']={"location":{"longitude":tmp["error"],"latitude":tmp["error"],"altitude":tmp["error"]}}
    else:
        data['gps']=tmp
                
    return data

@app.route('/upd')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        #f.save(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return render_template("success.html", name = f.filename)  

@app.route('/',methods=["GET","POST"])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('pass')
        credentials=None
        with open('/usr/sbin/device-manager/DeviceManager/credentials.json') as file:
            credentials=json.load(file)
        if credentials['email']==email and credentials['password']==password:
            session['username']=credentials['username']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

def gen_frames():  # generate frame by frame from camera
    
    subprocess.call(["systemctl","stop","rana"])
    camera = cv2.VideoCapture(2)  # use 0 for web camera
    camera.set(cv2.CAP_PROP_FPS,120)
    #  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
    # for local webcam use cv2.VideoCapture(0)
    while True:
        #print("kuch toh")
        # Capture frame-by-frame
        success1, frame1 = camera.read()  # read the first camera frame
        success2, frame2 = camera.read()  # read the second camera frame
        
        if (success1 and success2):
            diff1 = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours1, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
            for contour in contours1:
                (x, y, w, h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) < 8000:
                    continue
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #resizedframe11 = rescale_frame(frame11, percent=75)
        
            #cv2.imshow("cam", resizedframe11)
            ret, buffer = cv2.imencode('.jpg', frame1)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        else:
            break


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
        dummyData={
            "cpuInfo":{"usage":5.6},
            "gpuInfo":{"memoryUsage":2.3},
            "light_intensity":{"Light_Intensity":6.6},
            "internet":{"connectivity":True,"signal":2.3},
            "ramInfo":{"total":4,"usage":3,"free":1},
            "gps":{"location":{"longitude":1,"latitude":2,"altitude":3}},
            "temperature":{"Relative_humidity":32,"Temperature_c":21,"Temperature_f":37},
            "battery_parameters":{"Voltage":2.5,"Internal_temperature":38,"Average_current":2.7},
            "generalInfo":{"board_serial":34534,"board_type":"NRF","board_revision":2.3}
        }
        return render_template('Dashboard.html',data=readData())
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/files')
def files():
    path="/media/mmcblk1p1/upload/"  #path for the directory's of file
    if not os.path.exists(path):
        return abort(404)

    files = os.listdir(path)
    return render_template('files.html',files=files)

@app.route('/files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    dir="/media/mmcblk1p1/upload/"+filename  #path for the directory's of file
    # Returning file from appended path
    return send_file(dir)

@app.route('/configurations')
def configurations():
    return render_template('configurations.html')

@app.route('/configurations/file', methods=['GET', 'POST'])
def downloadConfFile():
    dir="/usr/sbin/rana/ranacore.conf"  #defing the path for conf file
    # Returning file from appended path
    return send_file(dir)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        #f.save(f.filename)  #path where the file has to be saved
        f.save(os.path.join(app.config['RANA_FOLDER'], f.filename))
        return 'file uploaded successfully'
    return 'Something went wrong'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
