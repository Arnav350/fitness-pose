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
exercise_mode = 'biceps'  # Default mode

def pose_detection():
    global left_counter, right_counter, left_stage, right_stage, running, exercise_mode
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

            if results.pose_landmarks is not None:
                try:
                    landmarks = results.pose_landmarks.landmark

                    if exercise_mode in ['biceps', 'triceps']:
                        # Left side
                        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

                        # Right side
                        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                        if exercise_mode == 'biceps':
                            # Logic for biceps
                            if left_angle > 160:
                                left_stage = "isometric bottom"
                            elif left_angle < 40:
                                if left_stage == "concentric":
                                    left_counter += 1
                                    print("Left reps:", left_counter)
                                left_stage = "isometric top"
                            elif 40 <= left_angle <= 160:
                                if left_stage == "isometric bottom":
                                    left_stage = "concentric"
                                elif left_stage == "isometric top":
                                    left_stage = "eccentric"

                            if right_angle > 160:
                                right_stage = "isometric bottom"
                            elif right_angle < 40:
                                if right_stage == "concentric":
                                    right_counter += 1
                                    print("Right reps:", right_counter)
                                right_stage = "isometric top"
                            elif 40 <= right_angle <= 160:
                                if right_stage == "isometric bottom":
                                    right_stage = "concentric"
                                elif right_stage == "isometric top":
                                    right_stage = "eccentric"
                        elif exercise_mode == 'triceps':
                            # Logic for triceps
                            if left_angle < 40:
                                left_stage = "isometric bottom"
                            elif left_angle > 160:
                                if left_stage == "concentric":
                                    left_counter += 1
                                    print("Left reps:", left_counter)
                                left_stage = "isometric top"
                            elif 40 <= left_angle <= 160:
                                if left_stage == "isometric top":
                                    left_stage = "eccentric"
                                elif left_stage == "isometric bottom":
                                    left_stage = "concentric"

                            if right_angle < 40:
                                right_stage = "isometric bottom"
                            elif right_angle > 160:
                                if right_stage == "concentric":
                                    right_counter += 1
                                    print("Right reps:", right_counter)
                                right_stage = "isometric top"
                            elif 40 <= right_angle <= 160:
                                if right_stage == "isometric top":
                                    right_stage = "eccentric"
                                elif right_stage == "isometric bottom":
                                    right_stage = "concentric"
                    elif exercise_mode in ['quads', 'hamstrings']:
                        # Left side
                        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                        left_angle = calculate_angle(left_hip, left_knee, left_ankle)

                        # Right side
                        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                        right_angle = calculate_angle(right_hip, right_knee, right_ankle)

                        if exercise_mode == 'quads':
                            # Logic for quads
                            if left_angle < 60:
                                left_stage = "isometric bottom"
                            elif left_angle > 160:
                                if left_stage == "concentric":
                                    left_counter += 1
                                    print("Left reps:", left_counter)
                                left_stage = "isometric top"
                            elif 60 <= left_angle <= 160:
                                if left_stage == "isometric top":
                                    left_stage = "eccentric"
                                elif left_stage == "isometric bottom":
                                    left_stage = "concentric"

                            if right_angle < 60:
                                right_stage = "isometric bottom"
                            elif right_angle > 160:
                                if right_stage == "concentric":
                                    right_counter += 1
                                    print("Right reps:", right_counter)
                                right_stage = "isometric top"
                            elif 60 <= right_angle <= 160:
                                if right_stage == "isometric top":
                                    right_stage = "eccentric"
                                elif right_stage == "isometric bottom":
                                    right_stage = "concentric"
                        elif exercise_mode == 'hamstrings':
                            # Logic for hamstrings
                            if left_angle > 160:
                                left_stage = "isometric bottom"
                            elif left_angle < 60:
                                if left_stage == "concentric":
                                    left_counter += 1
                                    print("Left reps:", left_counter)
                                left_stage = "isometric top"
                            elif 60 <= left_angle <= 160:
                                if left_stage == "isometric bottom":
                                    left_stage = "concentric"
                                elif left_stage == "isometric top":
                                    left_stage = "eccentric"

                            if right_angle > 160:
                                right_stage = "isometric bottom"
                            elif right_angle < 60:
                                if right_stage == "concentric":
                                    right_counter += 1
                                    print("Right reps:", right_counter)
                                right_stage = "isometric top"
                            elif 60 <= right_angle <= 160:
                                if right_stage == "isometric bottom":
                                    right_stage = "concentric"
                                elif right_stage == "isometric top":
                                    right_stage = "eccentric"

                    # Draw angle on the image
                    if exercise_mode in ['biceps', 'triceps']:
                        left_position = left_elbow
                        right_position = right_elbow
                    else:
                        left_position = left_knee
                        right_position = right_knee

                    cv2.putText(image, str(int(left_angle)),
                                tuple(np.multiply(left_position, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                                )

                    cv2.putText(image, str(int(right_angle)),
                                tuple(np.multiply(right_position, [640, 480]).astype(int)),
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
    global left_counter, right_counter, left_stage, right_stage, exercise_mode
    left_counter = 0
    right_counter = 0
    left_stage = None
    right_stage = None
    exercise_mode = request.json.get('mode', 'biceps')
    threading.Thread(target=pose_detection).start()
    return jsonify({'message': 'Pose detection started', 'mode': exercise_mode})

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
