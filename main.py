from flask import Flask, render_template, Response,redirect,abort,request,url_for
from camera import VideoCamera

from werkzeug import secure_filename
import os


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

global videoaddr
global imageaddr

global flag

@app.route('/')

def index():
    return render_template('index.html')



#live webcamera stream
@app.route('/livewebcam')

def livewebcam():
    global flag
    flag=0
    return render_template('livewebcam.html')
















@app.route('/uploadimage')

def uploadimage():
    return render_template('uploadimage.html')


@app.route("/uploadimg", methods=['POST'])
def uploadimg():
    target = os.path.join(APP_ROOT, 'image')
    #print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        #print(file)
        filename = file.filename
        destination = "/".join([target, filename])
       # print(destination)
        global imageaddr
        imageaddr=destination
        fname=filename
        global flag
        flag=2
        file.save(destination)
        
    return render_template('imagesentiment.html')



#video sentiment 
@app.route('/uploadvideo')

def uploadvideo():
    return render_template('uploadvideo.html')


@app.route("/uploadvido", methods=['POST'])
def uploadvido():
    target = os.path.join(APP_ROOT, 'video')
    #print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        #print(file)
        filename = file.filename
        destination = "/".join([target, filename])
       # print(destination)
        global videoaddr
        videoaddr=destination
        global flag
        flag=1
        file.save(destination)
        
    return render_template('videosentiment.html')
    #return redirect(url_for('videosentiment')
    #obj = VideoCamera('images/alpha1.mp4')
    #return render_template("data.html")
    

@app.route('/videosentiment')
def videosentiment():
    """Video streaming home page."""
    
    return render_template('videosentiment.html')













def gen():    
    global videoaddr
    if flag==1:
        obj = VideoCamera(videoaddr)
    if flag==0:
        obj = VideoCamera(0)
    
    
    while True:
        frame = obj.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')

def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')








def genimage():    
    global imageaddr
    if flag==2:
        obj = VideoCamera(imageaddr)
    
    
    
    while True:
        frame = obj.get_image()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/image_feed')

def image_feed():
    return Response(genimage(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')







if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=False)


