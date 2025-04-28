#sol kol ağırlık kaldrıma

import cv2
import mediapipe as mp
import numpy as np
import subprocess
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0
stage = None

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

# Angle calculation function
def calculateAngle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return angle if angle <= 180.0 else 360 - angle

# Setup Mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("ERROR...")
            break

        # Convert image to RGB for Mediapipe processing
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            # Get LEFT arm landmarks (Sol kol koordinatları)
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # Calculate angle for arm movement
            angle_move03 = calculateAngle(left_shoulder, left_elbow, left_wrist)

            # Curl counter logic
            if angle_move03 > 160:
                stage = "down"
            if angle_move03 < 30 and stage == "down":
                stage = "up"
                counter += 1

        except Exception as e:
            print("Hata:", e)
            pass

        # Draw pose landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(139, 0, 139), thickness=3, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(200, 162, 200), thickness=3, circle_radius=4))

        image = cv2.flip(image, 1)
        # Display counter in the top-left corner
        cv2.putText(image, f'Counter: {counter}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 0), 2, cv2.LINE_AA)
        cv2.imshow('Mediapipe Feed', image)

        if counter >= 15:  # Counter 15'e ulaşınca geçiş yap
            print("Tebrikler! Hareketi tamamladınız. Geçiş yapılıyor...")
            cap.release()
            cv2.destroyAllWindows()
            hareket_scripti = r"D:\\pyton-codes2\\mediapipe\\hareket1_gecis.py"
            if os.path.exists(hareket_scripti):
                subprocess.run(["python", hareket_scripti], check=True)
            else:
                print("Hata: hareket1_gecis.py dosyası bulunamadı!")
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
