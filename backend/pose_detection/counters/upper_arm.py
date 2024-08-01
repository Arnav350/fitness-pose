import mediapipe as mp
from ..calc_angle import calculate_angle
import config

mp_pose = mp.solutions.pose

def update_upper_arm_counters(landmarks, exercise_mode):
    left_stage = config.left_stage
    right_stage = config.right_stage
    left_counter = config.left_counter
    right_counter = config.right_counter

    # Left side
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

    left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    config.left_angle = left_angle

    # Right side
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

    right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
    config.right_angle = right_angle

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

    config.left_stage = left_stage
    config.right_stage = right_stage
    config.left_counter = left_counter
    config.right_counter = right_counter
