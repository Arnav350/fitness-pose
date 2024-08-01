import mediapipe as mp
from ..calc_angle import calculate_angle
import config

mp_pose = mp.solutions.pose

def update_chest_counters(landmarks):
    left_stage = config.left_stage
    right_stage = config.right_stage
    left_counter = config.left_counter
    right_counter = config.right_counter

    # Left side (Left Shoulder as the middle joint)
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

    left_angle = calculate_angle(right_shoulder, left_shoulder, left_elbow)
    config.left_angle = left_angle

    # Right side (Right Shoulder as the middle joint)
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

    right_angle = calculate_angle(left_shoulder, right_shoulder, right_elbow)
    config.right_angle = right_angle

    # Logic for chest exercise
    if left_angle > 180:
        left_stage = "isometric bottom"
    elif left_angle < 100:
        if left_stage == "concentric":
            left_counter += 1
            print("Left reps:", left_counter)
        left_stage = "isometric top"
    elif 100 <= left_angle <= 180:
        if left_stage == "isometric bottom":
            left_stage = "concentric"
        elif left_stage == "isometric top":
            left_stage = "eccentric"

    if right_angle > 180:
        right_stage = "isometric bottom"
    elif right_angle < 100:
        if right_stage == "concentric":
            right_counter += 1
            print("Right reps:", right_counter)
        right_stage = "isometric top"
    elif 100 <= right_angle <= 180:
        if right_stage == "isometric bottom":
            right_stage = "concentric"
        elif right_stage == "isometric top":
            right_stage = "eccentric"

    config.left_stage = left_stage
    config.right_stage = right_stage
    config.left_counter = left_counter
    config.right_counter = right_counter
