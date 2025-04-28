import cv2
import numpy as np
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.button import Button
import os
import sys

# Plus Jakarta fontunu kaydetme
LabelBase.register(name="PlusJakartaSans", fn_regular="med_pro_sport_videos/PlusJakartaSans-VariableFont_wght.ttf")

class VideoPlayerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Estetik video kutusu: video etrafında bir çerçeve
        self.video_frame = BoxLayout(size_hint=(1, 0.8), orientation='horizontal', padding=20, spacing=10)

        # Kivy Image widget
        self.image = Image()
        self.video_frame.add_widget(self.image)

        # Başlık
        self.title_label = Label(text="Egzersiz Hareketi", font_name="PlusJakartaSans", font_size=32,
                                 color=(1, 1, 1, 1), size_hint=(1, 0.1), bold=True)
        self.layout.add_widget(self.title_label)

        # Video dosyasının yolu
        self.video_path = "med_pro_sport_videos/hareket2.mp4"
        self.cap = cv2.VideoCapture(self.video_path)

        # FPS ayarlama
        self.timer_event = Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS

        # Başlangıçta videonun başını al
        self.layout.add_widget(self.video_frame)

        # Buton ekleme (Örn: "Başlat" butonu)
        self.play_button = Button(text="Başlat", size_hint=(None, None), size=(200, 50), pos_hint={"center_x": 0.5})
        self.play_button.bind(on_press=self.start_video)
        self.layout.add_widget(self.play_button)

        return self.layout

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Video bitince başa sar

        # Videoyu düzgün şekilde göster
        frame = cv2.flip(frame, 0)  # Dikey döndürme
        frame = cv2.resize(frame, (600, 550), interpolation=cv2.INTER_AREA)

        # Renk dönüşümü
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Kivy Image widget'ına gösterme
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        self.image.texture = texture

    def start_video(self, instance):
        # Başlat butonuna basıldığında video oynatmayı başlat
        self.play_button.disabled = True  # Butonu devre dışı bırak
        self.timer_event()  # Video oynatmayı başlat

        # Video oynatımı bittikten sonra ekranı kapat
        Clock.schedule_once(self.stop_video, 1)  # 1 saniye sonra stop_video fonksiyonu çalışacak

    def stop_video(self, dt):
        # Video bittiğinde video ekranını kapat
        self.cap.release()  # Video kaynağını serbest bırak
        self.image.texture = None  # Ekran görüntüsünü temizle

        # "body_estimation2.py" dosyasını başlat
        os.system("python body_estimation2.py")  # Alternatif olarak, subprocess kullanılabilir.
        self.stop()  # Kivy uygulamasını durdur ve pencereyi kapat

    def on_stop(self):
        self.cap.release()

if __name__ == "__main__":
    VideoPlayerApp().run()
