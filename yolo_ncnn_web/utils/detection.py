import cv2
import numpy as np
import ncnn

class YOLOv8NCNN:
    def __init__(self, param_file, bin_file):
        """Load YOLOv8 NCNN model."""
        self.net = ncnn.Net()
        self.net.load_param(param_file)
        self.net.load_model(bin_file)

    def detect(self, frame):
        """Run object detection on a single frame."""
        h, w = frame.shape[:2]
        input_size = 640  # YOLOv8 input size

        # Preprocess frame
        img = cv2.resize(frame, (input_size, input_size))
        img = img.astype(np.float32) / 255.0
        img = img.transpose(2, 0, 1).reshape(1, 3, input_size, input_size)

        input_mat = ncnn.Mat.from_pixels_resize(img, ncnn.Mat.PixelType.PIXEL_RGB, w, h, input_size, input_size)

        # Forward pass
        ex = self.net.create_extractor()
        ex.input("in0", input_mat)
        ret, out = ex.extract("out0")

        # Process detections
        boxes = []
        for i in range(out.h):
            values = out.row(i)
            if len(values) < 6:
                continue  # Skip invalid detections

            x, y, x2, y2, conf, class_id = values[:6]
            if conf > 0.5:  # Confidence threshold
                x, y, x2, y2 = int(x * w), int(y * h), int(x2 * w), int(y2 * h)
                boxes.append((x, y, x2, y2, class_id, conf))

        # Draw detections
        for x, y, x2, y2, class_id, conf in boxes:
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID:{int(class_id)} {conf:.2f}", (x, y - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        return frame
