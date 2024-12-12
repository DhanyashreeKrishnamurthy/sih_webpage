import airsim
import time
import base64
from flask import Flask, render_template, Response

app = Flask(__name__)

# Connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()

def gen():
    while True:
        # Capture the image from the drone's camera
        response = client.simGetImage("0", airsim.ImageType.Scene)  # Assuming camera 0
        if response:
            # Convert image to base64 encoding
            img_str = base64.b64encode(response).decode('utf-8')
            # Convert base64 back to image and send it as a MJPEG stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + base64.b64decode(img_str) + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
