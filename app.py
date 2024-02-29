from flask import Flask, render_template,request,Response
from main import vm,vm2


detect=vm()
detect2=vm2()

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
def gen(detect):
    while True:
        frame=detect.virtual_mouse()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def gen2(detect2):
    while True:
        frame=detect2.virtual_mouse2()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
@app.route("/home")
def start():
    return Response(gen(detect),mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route("/home2")
def start2():
    return Response(gen2(detect2),mimetype='multipart/x-mixed-replace;boundary=frame')
app.run()