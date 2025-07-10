# 🍼 IoT Baby Monitoring System with Real-time Alerts and Video Feed

This project is an **IoT-based baby monitoring system** built with **Flask**, **YOLOv8**, **Twilio**, and **OpenCV**. It enables **real-time health monitoring**, **video-based detection**, and **SMS alerting** for abnormal vitals, along with **music playback** for comfort.

---

## 🌟 Key Features

- 🎯 Real-time object detection using **YOLOv8**
- 📈 Vital signs monitoring (Heart Rate & SpO2) via API
- 📩 **Twilio SMS alerts** for abnormal vitals
- 🎶 Music playback control (start/stop/pause/resume)
- 📡 Live video stream using **Socket.IO** with detection overlays
- 🌐 Web-based dashboard using Flask & HTML

---

## 🖼️ System Overview

- Backend: Python + Flask
- Real-time Communication: Flask-SocketIO
- Detection: YOLOv8 via `ultralytics`
- Alerts: Twilio API for SMS
- Media: mp3 playback using `mpg123` (Linux required)
- Frontend: HTML + JavaScript + WebSocket

---

## ⚙️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/baby-monitoring-system.git
   cd baby-monitoring-system
2. Create a virtual environment (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
3. Install required packages
   ```bash
   pip install -r requirements.txt

4.Edit the following in app.py:

Your .mp3 file path (MUSIC_FILE)
Twilio credentials (TWILIO_ACCOUNT_SID, etc.)
YOLO model path (model = YOLO("path/to/your/model.pt"))

5. Run the application
   ```bash
   python app.py

📦 Dependencies
Listed in requirements.txt, major ones include:
-Flask
-Flask-SocketIO
-OpenCV-Python
-Ultralytics (YOLOv8)
-Twilio
-Eventlet (for SocketIO)

📱 How it Works
-Sensor sends heart rate and SpO2 via POST to /receive_data
-If vitals are low, SMS is triggered
-YOLOv8 runs in background thread on webcam frames
-Detected frames are sent to frontend via Socket.IO
-Music can be played/stopped via web buttons

🔗 Connect
Author: Sridhar prakash
LinkedIn: https://www.linkedin.com/in/sridhar-prakash-631343239/
GitHub: https://github.com/Sridharprakash
