from flask import Flask, Response
import cv2
from ultralytics import YOLO

app = Flask(__name__)
model = YOLO("yolo11n.pt")  # Path to your model
cap = cv2.VideoCapture(0)    # 0 = USB webcam

def generate():
    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame, verbose=False)[0]
        annotated = results.plot()
        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return "<h1>YOLOv11n Stream</h1><img src='/video'>"

@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
