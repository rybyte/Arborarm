# Objects Detection API

This project is a Flask-based API for detecting Objects in video frames using a pre-trained TensorFlow object detection model.

## Prerequisites

Ensure you have the following installed:

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone this repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not provided, install the dependencies manually:
   ```sh
   pip install opencv-python numpy tensorflow flask requests
   ```

## Running the API

1. Ensure the TensorFlow model file `frozen_inference_graph.pb` is in the project directory.
2. Start the Flask server:
   ```sh
   python app.py
   ```

3. The server will start on `http://0.0.0.0:3000/`.

## API Endpoint

### `POST /detect`

**Description**: Captures a frame from the video feed and detects hands.

**Request**: No body required.

**Response**:
```json
[
    {
        "box": [ymin, xmin, ymax, xmax],
        "score": 0.85
    },
    ...
]
```

## Troubleshooting

- Ensure your camera feed is accessible at `http://172.20.10.4:5000/video_feed`.
- If TensorFlow compatibility issues arise, ensure you are using a compatible version for your environment.
- If OpenCV cannot be found, install it separately using:
  ```sh
  pip install opencv-python
  ```

## License
This project is released under the MIT License.

