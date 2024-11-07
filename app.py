from flask import Flask, render_template, request, Response
from main import HardwareController, HandMouseController, DrawingController

app = Flask(__name__)

# Initialize the mouse control objects
hardware_controller = HardwareController()
hand_mouse_controller = HandMouseController()
drawing_controller = DrawingController()

@app.route("/")
def index():
    return render_template("index.html")

def generate_hardware_control_stream(controller):
    while True:
        frame = controller.signal()  
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def generate_hand_mouse_stream(controller):
    while True:
        frame = controller.virtual_mouse() 
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def generate_drawing_stream(controller):
    while True:
        frame = controller.get_drawing_frame() 
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/hardware")
def hardware_stream():
    return Response(generate_hardware_control_stream(hardware_controller), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/hand_mouse")
def hand_mouse_stream():
    return Response(generate_hand_mouse_stream(hand_mouse_controller), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/drawing")
def drawing_stream():
    return Response(generate_drawing_stream(drawing_controller), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
