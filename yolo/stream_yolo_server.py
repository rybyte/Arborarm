from flask import Flask, Response, render_template
import cv2
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLO model
model = YOLO("yolo11n_ncnn_model", task="detect")

# Open webcam (adjust index if needed)
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        # Run detection
        results = model(frame, verbose=False)
        detections = results[0].boxes

        # Draw bounding boxes
        for det in detections:
            xyxy = det.xyxy.cpu().numpy().squeeze().astype(int)
            conf = det.conf.item()
            classidx = int(det.cls.item())
            if conf > 0.5:
                cv2.rectangle(frame, tuple(xyxy[:2]), tuple(xyxy[2:]), (0, 255, 0), 2)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')  # Shows the web page with stream

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
