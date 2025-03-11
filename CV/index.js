import * as handTrack from 'handtrackjs';
import mqtt from 'mqtt';

import mqtt from 'mqtt';

// AWS IoT Core Configuration
const options = {
    host: 'iot.ap-southeast-1.amazonaws.com', // Replace with your AWS IoT Core endpoint
    protocol: 'wss', // WebSocket Secure
    port: 443,
    clientId: 'WebApp',
    username: '', // Leave empty for AWS IoT
    password: '', // Leave empty for AWS IoT
};

// Connect to AWS IoT Core
const client = mqtt.connect(options);

client.on('connect', () => {
    console.log('Connected to AWS IoT Core');
});

// Send motor commands
function sendMotorCommand(command) {
    const topic = 'robot/motor_control';
    client.publish(topic, command);
    console.log(`Command sent: ${command}`);
}

// Example usage
document.getElementById('forwardButton').addEventListener('click', () => {
    sendMotorCommand('forward');
});
document.getElementById('stopButton').addEventListener('click', () => {
    sendMotorCommand('stop');
});

document.addEventListener('DOMContentLoaded', async () => {
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    const streamUrl = 'http://172.20.10.4:5000/video_feed'; // MJPEG stream URL
    const img = new Image();
    img.crossOrigin = 'Anonymous'; // Allow cross-origin requests

    // Set Handtrack.js options
    const options = {
        flipHorizontal: true, // Flip the image for mirrored view
        maxNumBoxes: 1,       // Detect one hand
        scoreThreshold: 0.6,  // Confidence threshold
    };

    // Load the Handtrack.js model
    const model = await handTrack.load(options);
    console.log("Handtrack.js model loaded.");

    // Set canvas size dynamically based on the video stream
    img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
    };

    // Fetch and draw MJPEG frames
    const fetchStream = () => {
        img.src = `${streamUrl}?time=${Date.now()}`; // Add timestamp to prevent caching
    };

    // Process each frame
    img.onload = async () => {
        context.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
        context.drawImage(img, 0, 0, canvas.width, canvas.height); // Draw the MJPEG frame

        // Detect hands using Handtrack.js
        const predictions = await model.detect(canvas);
        console.log(predictions);

        // Draw bounding boxes for each detected hand
        predictions.forEach(prediction => {
            const [x, y, width, height] = prediction.bbox;
            context.strokeStyle = 'red';
            context.lineWidth = 2;
            context.strokeRect(x, y, width, height);
            context.font = '16px Arial';
            context.fillStyle = 'red';
            context.fillText(
                `${prediction.label} (${Math.round(prediction.score * 100)}%)`,
                x,
                y - 10
            );
        });

        fetchStream(); // Fetch the next frame
    };

    img.onerror = () => {
        console.error('Error loading MJPEG frame.');
        setTimeout(fetchStream, 1000); // Retry after 1 second
    };

    // Start fetching the MJPEG stream
    fetchStream();
});
