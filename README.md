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
