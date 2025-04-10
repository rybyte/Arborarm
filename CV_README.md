# YOLO Streaming Web Interface

This project streams live video from a Raspberry Pi using a YOLO-based object detection model and serves it via a web interface.

## 📡 Getting Started

### 🔗 Connect to Raspberry Pi

1. **Ensure both your laptop and Raspberry Pi are connected to the same Wi-Fi network.**
2. **Ping the Pi to get its IP address:**


'''bash
ping bmopi.local

SSH into the Raspberry Pi:

ssh bmopi@<ip_address>

Replace <ip_address> with the one from the ping command.

Enter your Pi's password when prompted.

🧪 Run the YOLO Web Stream
Navigate to the project directory:


cd yolo
Activate the virtual environment:


source venv/bin/activate
Run the streaming script:


python yolo_streamin_web.py
Copy the printed web link and open it in your browser to view the live video stream.

📌 Notes
Ensure your camera is connected and recognized by the Raspberry Pi.

The web server should automatically bind to a local IP; make sure firewall settings allow access if needed.

