import cv2
import numpy as np
from flask import Flask, render_template, Response, jsonify
from utils.detection import YOLOv8NCNN

app = Flask(__name__)

# Load the YOLOv8 NCNN model
yolo_model = YOLOv8NCNN("models/yolov8n.param", "models/yolov8n.bin")

# Video source: Change to 0 for webcam or "test.mp4" for a demo video
video_source = "test.mp4"
cap = cv2.VideoCapture(video_source)

streaming = True

def generate_frames():
    """Capture frames and run YOLOv8 NCNN object detection."""
    global cap, streaming
    while streaming:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video when finished
            continue

        frame = yolo_model.detect(frame)  # Run object detection

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Stream the processed video."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_stream', methods=['POST'])
def toggle_stream():
    """Start or stop the video stream."""
    global streaming
    streaming = not streaming
    return jsonify({"streaming": streaming})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
