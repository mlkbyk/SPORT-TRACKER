#right arm raise
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0
stage = None

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()


# Angle calculate function
def calculateAngle(a, b, c):
    a = np.array(a)  # first
    b = np.array(b)  # mid
    c = np.array(c)  # end

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


# Setup Mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("ERROR...")
            break


        # Recoloring image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)
        image.flags.writeable = True

        # Recolor back to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract Landmarks
        try:
            landmarks = results.pose_landmarks.landmark

            # Get coordinates
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            # Calculate angle
            angle_move02 = calculateAngle(right_hip,right_shoulder,right_elbow)



            # curl counter logic
            if angle_move02 > 160:
                stage = "open"
            if angle_move02 < 30 and stage == "open":
                stage = "down"
                counter += 1



        except Exception as e:
            print("Hata:", e)
            pass

        # Rendering detections
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(139, 0, 139), thickness=3, circle_radius=4),
                                      # change the color of point
                                      mp_drawing.DrawingSpec(color=(200, 162, 200), thickness=3, circle_radius=4)
                                      # change the color of line
                                      )

        image = cv2.flip(image, 1)
        # Display counter in the top-left corner
        cv2.putText(image, f'Counter: {counter}', (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 0), 2, cv2.LINE_AA)
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("Çıkış yapılıyor...")
            break

cap.release()
cv2.destroyAllWindows()
