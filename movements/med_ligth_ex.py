from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.uix.video import Video
import subprocess
import os
import sys

# Fontu Kivy'ye tanıtma (font dosyasının doğru yolu)
LabelBase.register(name="PlusJakartaSans", fn_regular="D:/medicine-project/medicine-photos/PlusJakartaSans-VariableFont_wght.ttf")

class BodyEstimationApp(App):
    def __init__(self, **kwargs):
        super(BodyEstimationApp, self).__init__(**kwargs)
        self.script_directory = "D:\\pyton-codes2\\mediapipe"  # Sabit dosya yolu

        # Her bir script için açıklamalar
        self.scripts_descriptions = {
            "hareket1_video.py": "Sağ Kol Ağırlık Kaldırma",
            "hareket2_video.py": "Sağ Kol Yukarı Kaldırma",
            "hareket3_video.py": "Sol Kol Ağırlık Kaldırma",
            "body_estimation4.py": "Sol Kol Yukarı Kaldırma",
            "body_estimation5.oy.py": "Sol Kol Esnetme",
            "body_estimation6.py": "Sağ Kol Esnetme",

            "body_estimation7.py": "Boyun Döndürme",
            "body_estimation8.py": "Sağ Bacak Esnetme",
            "body_estimation9.py": "Sol Bacak Esnetme",
            "hareket10_video.py": "Squat Hareketi",
            "body_estimation11.py": "Sağ Kol Açma ",
            "body_estimation12.py": "Sol Kol Açma "
        }

    def run_script(self, script_name):
        script_path = os.path.join(self.script_directory, script_name)
        if os.path.exists(script_path):
            try:
                subprocess.Popen([sys.executable, script_path])
            except Exception as e:
                self.show_error(f"Komut çalıştırılırken hata oluştu: {e}")
        else:
            self.show_error(f"Hata: {script_path} bulunamadı!")

    def show_error(self, message):
        error_label = Label(text=message, color=(1, 0, 0, 1))  # Kırmızı hata mesajı
        self.root.add_widget(error_label)

    def on_button_enter(self, instance):
        instance.height = 80  # Buton yüksekliğini büyütüyoruz
        instance.width = Window.width  # Buton genişliğini ekran genişliğine göre ayarlıyoruz

        # Kısa video gösterme
        video_path = "D:/path/to/video.mp4"  # Burada kısa video yolunu belirtin
        video_widget = Video(source=video_path, size_hint=(0.5, 0.5), pos=instance.pos)
        self.root.add_widget(video_widget)
        video_widget.play()

    def on_button_leave(self, instance):
        instance.height = 60  # Buton yüksekliğini eski haline getiriyoruz
        instance.width = Window.width * 0.9  # Buton genişliğini eski haline getiriyoruz

        # Video widget'ını kaldırma
        for widget in self.root.children:
            if isinstance(widget, Video):
                self.root.remove_widget(widget)

    def build(self):
        Window.clearcolor = get_color_from_hex('#D3D3D3')  # Arka plan rengi gri
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # ScrollView ile butonları kaydırılabilir hale getirme
        scroll_view = ScrollView()
        button_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter('height'))

        # Başlık etiketini stilize etme
        title_label = Label(
            text="SPOR HAREKETLERİ",
            size_hint_y=None,
            height=60,
            font_size=32,  # Daha büyük başlık fontu
            bold=True,
            font_name="PlusJakartaSans",  # Fontu ayarlama
            color=get_color_from_hex('#ffffff')  # Beyaz renk başlık için
        )
        layout.add_widget(title_label)

        for script_name, description in self.scripts_descriptions.items():
            btn = Button(
                text=f"{description}",
                size_hint=(1, None),
                height=60,
                background_color=get_color_from_hex('#FFD700'),  # Altın sarısı buton rengi
                color=(0, 0, 0, 1),  # Siyah yazı rengi
                bold=True,
                font_size=18,  # Buton yazı boyutu
                font_name="PlusJakartaSans",  # Fontu ayarlama
                background_normal='',  # Varsayılan arka planı kaldır
                background_down='atlas://data/images/defaulttheme/button_pressed',  # Basıldığında farklı arka plan
                # Köşeleri kare yapmak için border özelliği kullanılır
                border=(20, 20, 20, 20),  # 0 yaparak köşeleri kare yapıyoruz
            )
            btn.bind(on_press=lambda instance, s=script_name: self.run_script(s))
            btn.bind(on_enter=self.on_button_enter)  # Fare butona geldiğinde büyütme
            btn.bind(on_leave=self.on_button_leave)  # Fare butondan çıktığında eski haline dönme
            button_layout.add_widget(btn)

        # ScrollView widget'ını layout'a ekle
        scroll_view.add_widget(button_layout)
        layout.add_widget(scroll_view)

        return layout


if __name__ == "__main__":
    BodyEstimationApp().run()
