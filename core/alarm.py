# core/alarm.py
# Açıklama: Belirli bir alarm ses dosyasını çalarak kullanıcıyı uyarır.
# Kullanım: Tehlikeli nesne algılandığında alarm sesi başlatılır.

import threading
import pygame


def play_alarm(sound_path="sounds/alarm.wav"):
    """
    Verilen ses dosyasını (alarm.wav) arka planda çalar.

    Args:
        sound_path (str): Çalınacak alarm sesinin dosya yolu. Varsayılan 'sounds/alarm.wav'.
    """

    def run():
        pygame.mixer.init()  # Pygame ses motorunu başlat
        pygame.mixer.music.load(sound_path)  # Alarm sesini yükle
        pygame.mixer.music.play()  # Alarm sesini çal

    # Alarmı ayrı bir thread içinde çalıştır, ana akışı engelleme
    threading.Thread(target=run, daemon=True).start()


