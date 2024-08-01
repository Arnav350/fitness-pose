import cv2
import mediapipe as mp
from .counters import update_upper_arm_counters, update_upper_leg_counters, update_chest_counters
import config

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def pose_detection():
    config.running = True
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened() and config.running:
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
                    if config.exercise_mode in ['biceps', 'triceps']:
                        update_upper_arm_counters(landmarks, config.exercise_mode)
                    elif config.exercise_mode in ['quads', 'hamstrings']:
                        update_upper_leg_counters(landmarks, config.exercise_mode)
                    elif config.exercise_mode == 'chest':
                        update_chest_counters(landmarks)

                    if config.exercise_mode in ['biceps', 'triceps']:
                        left_position = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
                        right_position = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
                    elif config.exercise_mode in ['quads', 'hamstrings']:
                        left_position = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
                        right_position = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
                    elif config.exercise_mode == 'chest':
                        left_position = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                        right_position = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

                    cv2.putText(image, str(int(config.left_angle)),
                                (int(left_position.x * 640), int(left_position.y * 480)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                                )

                    cv2.putText(image, str(int(config.right_angle)),
                                (int(right_position.x * 640), int(right_position.y * 480)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA
                                )

                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                except Exception as e:
                    print(e)
                    continue

            cv2.imshow('MediaPipe Pose', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    config.running = False
