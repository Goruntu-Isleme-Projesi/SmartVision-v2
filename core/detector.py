# core/detector.py
# Açıklama: YOLOv8 modeli kullanarak nesne algılamayı sağlayan sınıf.

from ultralytics import YOLO


class ObjectDetector:
    """
    YOLOv8 tabanlı nesne algılayıcı sınıfı.
    Verilen bir model yolu üzerinden YOLO modelini yükler ve
    kareler (frame) üzerinden nesne tespiti yapar.
    """

    def __init__(self, model_path):
        """
        Modeli yükler ve temel parametreleri ayarlar.

        Args:
            model_path (str): Eğitilmiş model dosyasının yolu.
        """
        self.model = YOLO(model_path)  # Modeli yükle
        self.names = self.model.names  # Modeldeki sınıf isimleri
        self.focal_length = 615  # TODO: İleri sürümlerde dinamik olarak kalibre edilebilir

    def detect(self, frame):
        """
        Verilen bir kare (frame) üzerinde nesne tespiti yapar.

        Args:
            frame (ndarray): Görüntü karesi.

        Returns:
            results[0]: Algılama sonuçları (boxes, sınıflar vb.)
        """
        results = self.model.predict(
            source=frame,
            imgsz=640,  # Resmi 640x640 çözünürlüğe getir
            conf=0.5,  # %50 güven skorunun üzerindekileri al
            verbose=False,  # Terminale çıktı verme
            device='cpu'  # TODO: Eğer GPU varsa otomatik seçim yapılabilir
        )
        return results[0]  # İlk sonucu döndür
