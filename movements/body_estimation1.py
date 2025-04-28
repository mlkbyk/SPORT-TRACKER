#sağ kol ağırlık kaldırma 
import cv2
import mediapipe as mp
import numpy as np
import os
import time
import sys

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Sayım değişkenleri
counter = 0
stage = None

# Video ve script yolları
final_script_path = "hareket1_gecis.py"

# Kamerayı başlat ve çözünürlüğü al
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

cap.release()

# Kamera açılana kadar ekranı kapatma yerine açık tut
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

time.sleep(2)  # 2 saniye bekle
cv2.destroyAllWindows()

# Açı hesaplama fonksiyonu
def calculateAngle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Mediapipe Pose modeli
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Hata! Kamera verisi alınamıyor.")
            break

        frame = cv2.flip(frame, 1)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            angle_move01 = calculateAngle(left_shoulder, left_elbow, left_wrist)

            if angle_move01 > 160:
                stage = "Aşağı"
            if angle_move01 < 30 and stage == "Aşağı":
                stage = "Yukarı"
                counter += 1

        except Exception as e:
            print("Hata:", e)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(139, 0, 139), thickness=3, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(200, 162, 200), thickness=3, circle_radius=4))

        # Sayım bilgisini ekrana yazdır
        overlay = image.copy()
        cv2.rectangle(overlay, (20, 20), (270, 90), (0, 0, 0), -1)  # Arka plan kutusu
        image = cv2.addWeighted(overlay, 0.5, image, 0.5, 0)

        cv2.putText(image, f'Sayac: {counter}', (30, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Egzersiz Takip', image)

        if counter >= 15:
            break

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

# Sayım 15'e ulaşınca hareket1_geçiş sayfasına yönlendir
print("Tebrikler! Hareketi tamamladınız. Geçiş yapılıyor...")

# Dosyanın mevcut olup olmadığını kontrol et ve çalıştır
if os.path.exists(final_script_path):
    os.system(f"{sys.executable} {final_script_path}")
else:
    print(f"Hata: {final_script_path} dosyası bulunamadı!")
