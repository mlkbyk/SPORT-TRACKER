#squat
import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

#Curl counter variables
counter=0
stage=None


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

        frame = cv2.flip(frame, 1)  # mirror effect

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
            #Left arm
            left_elbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
            left_shoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
            left_hip=[landmarks[mp_pose.PoseLandmark.LEFT_HIP].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
            #Right arm
            right_elbow=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]

            right_shoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]

            right_hip=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y]

            #left leg
            left_knee=[landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]

            left_ankle=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]


            #right leg
            right_knee=[landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y]

            right_ankle=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y]

            # Calculate angle
            angle_mv1=calculateAngle(right_elbow,right_shoulder,right_hip) #angle between right arm
            angle_mv2=calculateAngle(left_elbow,left_shoulder,left_hip)#angle between left arm
            angle_mv3=calculateAngle(right_hip,right_knee,right_ankle)#angle between right leg
            angle_mv4=calculateAngle(left_hip,left_knee,left_ankle)#angle between left leg


            #logic
            if 50 < angle_mv1 < 160 and 50 < angle_mv2 < 160:
                if 0 < angle_mv3 < 160 and 0 < angle_mv4 < 160:
                    if stage != "squat":
                        stage = "squat"


            if stage == "squat" and 165 < angle_mv3 < 250 and 165 < angle_mv4 < 250:  #
                stage = "up"
                counter += 1


            # Visualize angle
            cv2.putText(image, str(int(counter)), (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,100,0), 2, cv2.LINE_AA)




        except Exception as e:
            print("Hata:", e)
            pass

        # Rendering detections
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(139, 0, 139), thickness=3, circle_radius=4),  # change the color of point
                                      mp_drawing.DrawingSpec(color=(200, 162, 200), thickness=3, circle_radius=4)  # change the color of line
                                      )

        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
