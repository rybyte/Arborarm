import cv2
import requests
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the inference graph
PATH_TO_CKPT = "frozen_inference_graph.pb"
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

sess = tf.compat.v1.Session(graph=detection_graph)

@app.route('/detect', methods=['POST'])
def detect_hands():
    # Capture a frame from the video stream
    response = requests.get('hhttp://172.20.10.4:5000/video_feed', stream=True)
    bytes = b''
    for chunk in response.iter_content(chunk_size=1024):
        bytes += chunk
        a = bytes.find(b'\xff\xd8')  # JPEG start
        b = bytes.find(b'\xff\xd9')  # JPEG end
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]

            # Decode the frame
            image_np = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

            # Expand dimensions for TensorFlow
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name("image_tensor:0")
            detection_boxes = detection_graph.get_tensor_by_name("detection_boxes:0")
            detection_scores = detection_graph.get_tensor_by_name("detection_scores:0")
            detection_classes = detection_graph.get_tensor_by_name("detection_classes:0")
            num_detections = detection_graph.get_tensor_by_name("num_detections:0")

            # Run detection
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded}
            )

            # Filter results with high confidence
            results = []
            for i in range(int(num[0])):
                if scores[0][i] > 0.5:  # Confidence threshold
                    box = [float(v) for v in boxes[0][i]]
                    results.append({"box": box, "score": float(scores[0][i])})

            return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
