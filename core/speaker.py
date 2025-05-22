# core/speaker.py
# Açıklama: Gerçek zamanlı sesli bildirim sistemi.
# Amaç: Kuyruk tabanlı yapı ile pyttsx3 motoru kullanarak konuşmaları yönetmek.

import pyttsx3
import queue
import time
import threading


# --- Başlangıç Ayarları ---
engine = pyttsx3.init()  # Ses motorunu başlat
engine.setProperty('rate', 250)   # Konuşma hızı ayarı (kelime/dakika)
engine.setProperty('volume', 1.0)  # Ses seviyesi (1.0 = maksimum)

# Konuşma sırasını kontrol eden kuyruk ve durum değişkeni
speak_queue = queue.Queue()
currently_speaking = False


def speak(text):
    """
    Yeni bir konuşma mesajı ekler.
    Args:
        text (str): Seslendirilecek metin.
    """
    speak_queue.put(text)  # Mesajı kuyruğa ekle

def speaker_worker():
    """
    Kuyruktaki mesajları sırayla seslendiren işçi thread.
    Her zaman bir mesaj bittiğinde sıradakine geçer.
    """
    global currently_speaking
    while True:
        text = speak_queue.get()  # Kuyruktan mesaj al
        if text is None:
            break  # None gelirse threadi durdur (şu anda kullanılmıyor)
        currently_speaking = True
        print(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
        currently_speaking = False
        speak_queue.task_done()  # Mesajı tamamladı olarak işaretle

#frame box olmadığı durumlarda kuyruğu sıfırlayarak gecikmeli seslerden kurtulan bir fonksiyon
def clear_queue():
    if speak_queue.empty():
        return
    speak_queue.queue.clear()
    print("Queue cleaned!")

# --- Arka planda sürekli çalışan konuşma işçisi thread başlat ---
threading.Thread(target=speaker_worker, daemon=True).start()
