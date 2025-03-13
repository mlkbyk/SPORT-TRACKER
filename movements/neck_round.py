#neck döndürme
import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# Counter variables
counter = 0
stage1 = False
stage2 = False

if not cap.isOpened():
    print("Camera could not be opened!")
    exit()


# Function to calculate the angle between three points
def calculateAngle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Middle point
    c = np.array(c)  # End point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


# Initialize Mediapipe
with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("ERROR...")
            break

        frame=cv2.flip(frame,1)#mirror effect

        # Convert image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Process the frame
        results = pose.process(image)
        image.flags.writeable = True

        # Convert back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # Extract key landmarks
            left_eye = [landmarks[mp_pose.PoseLandmark.LEFT_EYE_OUTER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_EYE_OUTER.value].y]
            left_mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].x,
                          landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_eye = [landmarks[mp_pose.PoseLandmark.RIGHT_EYE_OUTER.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_EYE_OUTER.value].y]
            right_mouth = [landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].x,
                           landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[mp_pose.PoseLandmark.NOSE.value].y]

            # Calculate angles
            angle_move1 = calculateAngle(left_eye, left_mouth, left_shoulder)
            angle_move2 = calculateAngle(right_eye, right_mouth, right_shoulder)

            # Convert normalized coordinates to pixels (for text display)
            coords = tuple(np.multiply(nose, [640, 480]).astype(int))

            # **Loop Logic**: First `angle_move1`, then `angle_move2`
            if 0 < angle_move1 < 125 and not stage1:
                stage1 = True  # First step completed
                stage2 = False  # Reset second step

            if stage1 and 60 < angle_move2 < 120 and not stage2:
                stage2 = True
                counter += 1  # Increase counter
                stage1 = False  # Reset first step

            # **Alternative Loop Logic**: First `angle_move2`, then `angle_move1`
            if 60< angle_move2 < 120 and not stage2:
                stage2 = True
                stage1 = False  # Reset first step

            if stage2 and 30 < angle_move1 < 120 and not stage1:
                stage1 = True
                counter += 1  # Increase counter
                stage2 = False  # Reset second step

            # Display counter value
            cv2.putText(image, f'Counter: {counter}', coords,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        except Exception as e:
            print("Error:", e)
            pass

        # Draw landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(139, 0, 139), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(200, 162, 200), thickness=2, circle_radius=2)
                                      )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
