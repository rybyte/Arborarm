import cv2
import numpy as np
import ncnn
from filterpy.kalman import KalmanFilter

# Load YOLOv8 NCNN model
def load_yolo_model(param_file, bin_file):
    net = ncnn.Net()
    net.load_param(param_file)
    net.load_model(bin_file)
    return net

# Initialize the model
yolo_net = load_yolo_model("models/yolov8n.param", "models/yolov8n.bin")

# Set correct input and output layer names
INPUT_LAYER = "in0"
OUTPUT_LAYER = "out0"

# Load video file
video_path = "test.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Error: Could not open video file.")
    exit()

# Initialize Kalman Filter for object tracking
kf = KalmanFilter(dim_x=4, dim_z=4)
kf.F = np.array([[1, 0, 1, 0],  # Transition matrix
                 [0, 1, 0, 1],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])

kf.H = np.eye(4)  # Measurement function
kf.P *= 1000      # Covariance matrix
kf.R = np.eye(4) * 10  # Measurement noise

tracked_objects = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    h, w = frame.shape[:2]
    input_size = 640  # YOLOv8 input size

    # Preprocess frame
    img = cv2.resize(frame, (input_size, input_size))
    img = img.astype(np.float32) / 255.0
    img = img.transpose(2, 0, 1).reshape(1, 3, input_size, input_size)

    input_mat = ncnn.Mat.from_pixels_resize(img, ncnn.Mat.PixelType.PIXEL_RGB, w, h, input_size, input_size)

    # Forward pass through NCNN model
    ex = yolo_net.create_extractor()
    ex.input(INPUT_LAYER, input_mat)
    ret, out = ex.extract(OUTPUT_LAYER)

    # Process detection output
    detected_boxes = []
    for i in range(out.h):
        values = out.row(i)
        if len(values) < 6:
            continue  # Skip invalid detections

        x, y, x2, y2, conf, class_id = values[:6]
        if conf > 0.6:  # Higher confidence threshold to reduce false positives
            x, y, x2, y2 = int(x * w), int(y * h), int(x2 * w), int(y2 * h)
            detected_boxes.append((x, y, x2, y2, int(class_id), conf))

    # Use Kalman Filter for tracking
    for i, (x, y, x2, y2, class_id, conf) in enumerate(detected_boxes):
        if class_id not in tracked_objects:
            tracked_objects[class_id] = KalmanFilter(dim_x=4, dim_z=4)
            tracked_objects[class_id].F = kf.F
            tracked_objects[class_id].H = kf.H
            tracked_objects[class_id].P *= 1000
            tracked_objects[class_id].R = kf.R
            tracked_objects[class_id].x = np.array([[x], [y], [0], [0]])

        # Predict new position
        tracked_objects[class_id].predict()
        tracked_objects[class_id].update(np.array([[x], [y], [x2], [y2]]))

        x, y, x2, y2 = tracked_objects[class_id].x[:4].flatten().astype(int)

        # Draw tracked bounding box
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{class_id} {conf:.2f}", (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Display frame with detections
    cv2.imshow("YOLOv8 NCNN Detection - Kalman Filter", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
