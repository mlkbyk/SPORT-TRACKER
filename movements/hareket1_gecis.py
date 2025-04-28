import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
from kivy.uix.label import Label
from kivy.clock import Clock
import os

# Kivy sürümünü kontrol edelim
kivy.require('2.0.0')  # Kivy sürümünü belirtiyoruz (sizin versiyonunuz farklı olabilir)

# Fontun kaydedilmesi (med_pro_sport_videos klasöründeki fontu kullanıyoruz)
LabelBase.register(name="Plus Jakarta", fn_regular="med_pro_sport_videos/PlusJakartaSans-VariableFont_wght.ttf")

class TransitionScreen(Widget):
    def __init__(self, **kwargs):
        super(TransitionScreen, self).__init__(**kwargs)
        # Ekran boyutlarını video boyutunda ayarlıyoruz (örneğin 600x550)
        self.size = (600, 550)

        # Grafik bileşenlerini oluşturuyoruz
        with self.canvas:
            Color(1, 215/255, 0, 1)  # #FFD700 rengi (altın sarısı arka plan)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Tebrik mesajını yazdıracak Label
        self.label = Label(text="Tebrikler!\nHareket tamamlandı", font_name="Plus Jakarta",
                           font_size=40, color=(1, 0, 0, 1),
                           size_hint=(None, None), size=(self.width, self.height),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.label)

        # 3 saniye sonra başka bir sayfaya geçmesini sağlıyoruz
        Clock.schedule_once(self.switch_screen, 3)

    def on_size(self, *args):
        # Ekran boyutunu güncelleme işlemi
        if hasattr(self, 'rect'):  # 'rect' öğesinin mevcut olup olmadığını kontrol et
            self.rect.size = self.size
        if hasattr(self, 'label'):  # 'label' öğesinin mevcut olup olmadığını kontrol et
            self.label.size = self.size

    def switch_screen(self, dt):
        # Geçiş ekranını kapatıp, med_light_ex.py dosyasını çalıştırıyoruz
        App.get_running_app().stop()  # Uygulamayı kapatıyoruz
        os.system("python med_light_ex.py")  # med_light_ex.py dosyasını çalıştırıyoruz

class MyApp(App):
    def build(self):
        return TransitionScreen()

if __name__ == '__main__':
    MyApp().run()
