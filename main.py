# main.py
# Proje: SmartVisionAssist - Görme Engelliler İçin Akıllı Nesne Tanıma ve Sesli Uyarı Sistemi
# Açıklama:
# Bu kod, bir videodan alınan görüntülerde nesne algılaması yapar.
# Arabalar, insanlar, yollar, merdivenler gibi nesneleri tespit eder.
# Algılanan nesnelere göre sesli uyarı verir ve tehlike durumlarında alarm çalar.

# --- Kütüphane İçe Aktarımları ---
import cv2
import time
import threading
from core.detector import ObjectDetector
from core.speaker import speak, currently_speaking,clear_queue
from core.alarm import play_alarm
from core.utils import calculate_distance, determine_position, REAL_WIDTHS
from core.logic import classify_object, generate_warning_text

speak_lock = threading.Lock()

# --- Başlangıç Ayarları ---
model_path = "models/my_model.pt"  
video_path = "videos/video.mp4"    # Kullanılacak video dosyasının yolu

detector = ObjectDetector(model_path)  # Nesne algılayıcı başlat
url = "http://192.168.1.40:4747/video"
cap = cv2.VideoCapture(video_path)
 # Video kaynağını başlat
paused = False  # Başlangıçta video oynuyor


speech_enabled = True  # Sesli bildirimler açık
fps = cap.get(cv2.CAP_PROP_FPS)  # Video FPS bilgisi
skip_seconds = 5  # Fast-forward/backward süresi
frame = None  # Güncel video karesi
threshold = 0.5  # Mesafe değişim eşiği (0.5 metre)

# --- Son Algı Bilgileri ---
last_detected_text = None
last_spoken_time = 0
last_warn_time=0
last_label = None
last_position = None
last_distance = None
draw_lines = False  # 9 bölge çizgilerini aç/kapat


# --- Ana Döngü ---
while True:
    # Video oynuyorsa yeni kare oku
    if not paused:
        ret, new_frame = cap.read()
        if not ret:
            break  # Video biterse çık
        frame = new_frame

    if frame is None:
        continue  # Eğer kare yoksa döngüyü atla          

    # --- Nesne Algılama ve İşleme ---
    height, width, _ = frame.shape
    result = detector.detect(frame)

    boxes = result.boxes

    if len(boxes) == 0:
        clear_queue()
        #ekranda bir şey olmadıgında konuşma kısmını sıfırlıyor
    if boxes is not None and len(boxes) > 0:
        classes = boxes.cls.cpu().numpy().astype(int)

        closest_obj = None
        closest_distance = float('inf')
        closest_info = None

        for cls_idx, box in zip(classes, boxes.xyxy):
            label = detector.names[cls_idx]
            x1, y1, x2, y2 = box.cpu().numpy()

            position = determine_position(x1, y1, x2, y2, width, height)
            real_width = REAL_WIDTHS.get(label, 0.5)
            pixel_width = x2 - x1
            distance = calculate_distance(real_width, pixel_width, detector.focal_length)


            if distance != -1 and distance < closest_distance:
                closest_distance = distance
                closest_obj = label
                closest_info = (position, distance)

        # --- En Yakın Nesne Seçimi ---
        if closest_obj:
            position, distance = closest_info

            similar = (
                closest_obj == last_label and
                position == last_position and
                last_distance is not None and
                abs(distance - last_distance) < threshold
            )

            if not similar:
                if distance>25.0:
                    continue

                distance_desc = ("very close" if distance < 2 else
                                 "nearby" if distance < 5 else
                                 f"approximately {distance:.1f} meters away")

                last_detected_text=generate_warning_text(closest_obj, position, distance_desc)

                # --- Tehlikeli nesne varsa alarm çal ---
                if (classify_object(closest_obj) == "dangerous" or distance_desc == "very close") and (time.time()-last_warn_time > .5):
                    threading.Thread(target=play_alarm).start()
                    last_warn_time = time.time()
                last_label = closest_obj
                last_position = position
                last_distance = distance

    # --- Sesli Uyarı Yap ---
    if not currently_speaking and last_detected_text and (time.time() - last_spoken_time > 2):
        print(last_detected_text)
        if speech_enabled:
            #speak(last_detected_text)
            threading.Thread(target=speak, args=(last_detected_text,)).start()

            last_spoken_time = time.time()
            last_detected_text = None

    # --- Ekrana Sonuçları Çiz ---
    annotated_frame = result.plot()

    if draw_lines:
        cv2.line(annotated_frame, (width // 3, 0), (width // 3, height), (255, 0, 0), 2)
        cv2.line(annotated_frame, (2 * width // 3, 0), (2 * width // 3, height), (255, 0, 0), 2)
        cv2.line(annotated_frame, (0, height // 3), (width, height // 3), (255, 0, 0), 2)
        cv2.line(annotated_frame, (0, 2 * height // 3), (width, 2 * height // 3), (255, 0, 0), 2)

    cv2.imshow('SmartVisionAssist', annotated_frame)

    # --- Klavye Kontrolleri ---
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break  # Çıkış
    elif key == ord('s'):
        speech_enabled = False
        print("Speech disabled.")
    elif key == ord('r'):
        speech_enabled = True
        print("Speech enabled.")
    elif key == ord('p'):
        paused = not paused
        print("Video paused." if paused else "Video resumed.")
    elif key == ord('d'):
        draw_lines = not draw_lines
        print("Draw Lines on." if draw_lines else "Draw Lines off.")
    elif key == ord('f'):
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + fps * skip_seconds)
        print(f"Fast forward {skip_seconds} seconds.")
    elif key == ord('b'):
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        new_frame = max(current_frame - fps * skip_seconds, 0)
        cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
        print(f"Rewind {skip_seconds} seconds.")


# --- Temizlik ---
cap.release()
cv2.destroyAllWindows()
