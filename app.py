from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import cv2
import base64
import subprocess
import time
from ultralytics import YOLO
from twilio.rest import Client
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Music Playback Setup
MUSIC_FILE = "Enter ur mp3 directory"
music_process = None
paused = False
start_time = 0
pause_time = 0

# Twilio Credentials
TWILIO_ACCOUNT_SID = 'Enter ur credentials'
TWILIO_AUTH_TOKEN = 'Enter ur credentials'
TWILIO_PHONE_NUMBER = 'Enter ur credentials'
ALERT_PHONE_NUMBER = 'Enter ur credentials'

# Initialize Twilio Client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

last_alert_time = {"heart_rate": 0, "spo2": 0}
ALERT_COOLDOWN = 60  # Cooldown time in seconds

def send_sms_alert(message, alert_type):
    """ Sends SMS alerts with cooldown prevention. """
    global last_alert_time

    current_time = time.time()
    if current_time - last_alert_time[alert_type] < ALERT_COOLDOWN:
        return  

    try:
        msg = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=ALERT_PHONE_NUMBER
        )
        last_alert_time[alert_type] = current_time
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def check_vitals(heart_rate, spo2):
    """ Checks vitals and triggers SMS alerts if necessary. """
    if 1 < heart_rate < 50:
        send_sms_alert(f"ALERT: Low heart rate detected: {heart_rate} BPM", "heart_rate")
    if 1 < spo2 < 90:
        send_sms_alert(f"ALERT: Low SpO2 detected: {spo2}%", "spo2")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        heart_rate = data.get("heartRate")
        spo2 = data.get("SpO2")

        check_vitals(heart_rate, spo2)
        socketio.emit('update_spo2', {'heart_rate': heart_rate, 'spo2': spo2})

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to process data"}), 500

# Music Controls
@app.route('/toggle_music', methods=['POST'])
def toggle_music():
    global music_process, start_time, paused, pause_time
    if music_process is None:
        try:
            music_process = subprocess.Popen(["mpg123", "-q", MUSIC_FILE], stdin=subprocess.DEVNULL,
                                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            start_time = time.time()
            paused = False
            pause_time = 0
            return jsonify({"status": "playing"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    else:
        music_process.terminate()
        music_process = None
        return jsonify({"status": "stopped"})

@app.route('/pause_resume_music', methods=['POST'])
def pause_resume_music():
    global music_process, paused, pause_time, start_time
    if music_process is not None:
        if not paused:
            subprocess.call(["pkill", "-STOP", "mpg123"])
            paused = True
            pause_time = time.time()
            return jsonify({"status": "paused"})
        else:
            subprocess.call(["pkill", "-CONT", "mpg123"])
            paused = False
            start_time += time.time() - pause_time
            return jsonify({"status": "resumed"})
    return jsonify({"status": "error", "message": "No music playing"})

@app.route('/music_progress', methods=['GET'])
def music_progress():
    global start_time, paused, pause_time
    if music_process is None:
        return jsonify({"status": "stopped", "progress": 0})
    
    progress = (pause_time - start_time) if paused else (time.time() - start_time)
    return jsonify({"status": "playing" if not paused else "paused", "progress": int(progress)})

# Load YOLOv8 Model
model = YOLO("Enter ur pt file directory")

# YOLOv8 Video Processing
def run_yolo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return

    while True:
        success, frame = cap.read()
        if not success:
            continue

        results = model.predict(frame, imgsz=480, conf=0.5, device="cpu")
        detections = []

        for r in results:
            if hasattr(r, 'boxes'):
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf_score = float(box.conf[0])
                    class_name = model.names[cls_id] if cls_id in model.names else "Unknown"
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"{class_name}: {conf_score:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    detections.append({"class": class_name, "confidence": round(conf_score, 2)})

        # Encode frame to Base64
        _, buffer = cv2.imencode('.jpg', frame)
        encoded_frame = base64.b64encode(buffer).decode('utf-8')

        # Emit results with confidence scores
        socketio.emit("update_yolo", {"detections": detections, "frame": encoded_frame})
        
        time.sleep(0.05)  # Standard sleep instead of eventlet.sleep

    cap.release()

def start_yolo_thread():
    """Starts YOLO in a separate thread to avoid blocking Flask."""
    yolo_thread = threading.Thread(target=run_yolo, daemon=True)
    yolo_thread.start()

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    start_yolo_thread()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)
