from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import pyautogui
import mediapipe as mp
import threading
import base64
from io import BytesIO

app = Flask(__name__)
socketio = SocketIO(app)

# Video capturing thread and flag
thread = None
thread_lock = threading.Lock()
capture_flag = True

# MediaPipe hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

# Initialize music_playing and hand_gesture
music_playing = False
hand_gesture = None

def detect_hand_gesture(index_finger_y, middle_finger_y):
    # Check if both index and middle fingers are up
    if index_finger_y < 0.8 and middle_finger_y < 0.8:
        return 'both fingers up'
    elif index_finger_y < middle_finger_y:
        return 'pointing up'
    elif index_finger_y > middle_finger_y:
        return 'pointing down'
    else:
        return 'other'

def hand_gesture_thread():
    global capture_flag, music_playing, hand_gesture

    while capture_flag:
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                middle_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                # Update hand_gesture based on hand landmarks
                hand_gesture = detect_hand_gesture(index_finger_y, middle_finger_y)

                # Your original logic for handling hand gestures
                if hand_gesture == 'both fingers up':
                    if music_playing:
                        pyautogui.press('mediapause')
                    else:
                        pyautogui.press('mediaplaypause')
                    music_playing = not music_playing
                elif hand_gesture == 'pointing up':
                    pyautogui.press('volumeup')
                elif hand_gesture == 'pointing down':
                    pyautogui.press('volumedown')

        # Encode the frame to base64 and emit it to the client
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('update_frame', frame_data)

    cap.release()

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on('connect')
def handle_connect():
    global thread
    with thread_lock:
        if thread is None:
            # Start the hand gesture recognition thread
            thread = threading.Thread(target=hand_gesture_thread)
            thread.start()

@socketio.on('disconnect')
def handle_disconnect():
    global thread, capture_flag
    with thread_lock:
        if thread is not None:
            # Stop the hand gesture recognition thread
            capture_flag = False
            thread.join()
            thread = None

if __name__ == "__main__":
    # OpenCV video capture setup
    cap = cv2.VideoCapture(0)

    # Run the Flask app with SocketIO support
    socketio.run(app, debug=True)
