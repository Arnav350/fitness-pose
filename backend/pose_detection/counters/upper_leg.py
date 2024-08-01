import mediapipe as mp
from ..calc_angle import calculate_angle
import config

mp_pose = mp.solutions.pose

def update_upper_leg_counters(landmarks, exercise_mode):
    left_stage = config.left_stage
    right_stage = config.right_stage
    left_counter = config.left_counter
    right_counter = config.right_counter

    # Left side
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    left_angle = calculate_angle(left_hip, left_knee, left_ankle)
    config.left_angle = left_angle

    # Right side
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

    right_angle = calculate_angle(right_hip, right_knee, right_ankle)
    config.right_angle = right_angle

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

    config.left_stage = left_stage
    config.right_stage = right_stage
    config.left_counter = left_counter
    config.right_counter = right_counter
