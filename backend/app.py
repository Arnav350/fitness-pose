from flask import Flask, jsonify, request
import cv2
import mediapipe as mp
import numpy as np
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

left_counter = 0
right_counter = 0
left_stage = None
right_stage = None
running = False

def pose_detection():
    global left_counter, right_counter, left_stage, right_stage, running
    running = True
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened() and running:
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark

                # Left side
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

                if left_angle > 160:
                    left_stage = "isometric bottom"
                elif left_angle < 40:
                    left_stage = "isometric top"
                elif 40 <= left_angle <= 160:
                    if left_stage == "isometric bottom":
                        left_stage = "concentric"
                    elif left_stage == "isometric top":
                        left_stage = "eccentric"
                        left_counter += 1
                        print("Left reps:", left_counter)

                # Draw angle on the image
                cv2.putText(image, str(int(left_angle)),
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            )

                # Right side
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                if right_angle > 160:
                    right_stage = "isometric bottom"
                elif right_angle < 40:
                    right_stage = "isometric top"
                elif 40 <= right_angle <= 160:
                    if right_stage == "isometric bottom":
                        right_stage = "concentric"
                    elif right_stage == "isometric top":
                        right_stage = "eccentric"
                        right_counter += 1
                        print("Right reps:", right_counter)

                # Draw angle on the image
                cv2.putText(image, str(int(right_angle)),
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                            )

                # Draw landmarks and connections on the image
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            except Exception as e:
                print(e)
                continue

            # Display the image
            cv2.imshow('MediaPipe Pose', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    running = False

@app.route('/start', methods=['POST'])
def start_pose_detection():
    global left_counter, right_counter, left_stage, right_stage
    left_counter = 0
    right_counter = 0
    left_stage = None
    right_stage = None
    threading.Thread(target=pose_detection).start()
    return jsonify({'message': 'Pose detection started'})

@app.route('/stop', methods=['POST'])
def stop_pose_detection():
    global running
    running = False
    return jsonify({'message': 'Pose detection stopped'})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        'left_stage': left_stage,
        'right_stage': right_stage,
        'left_reps': left_counter,
        'right_reps': right_counter
    })

if __name__ == '__main__':
    app.run(debug=True)
