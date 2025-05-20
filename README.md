# SmartVisionAssist

Görme engelliler için geliştirilmiş nesne tanıma ve sesli uyarı sistemi.  
Video üzerinden araba, insan, yol gibi nesneleri algılar ve sesli bildirim yapar.

## Özellikler
- Gerçek zamanlı nesne algılama (YOLOv8)
- Sesli bildirim (pyttsx3 ile)
- Tehlike durumlarında alarm sesi
- Yol yönlendirme (left, right, straight)

## Gereksinimler
- Python 3.10 veya üstü
- ultralytics
- opencv-python
- pyttsx3
- pygame

Kurmak için:

```bash
pip install -r requirements.txt
```

Kullanım:
```bash
python main.py
```
Varsayılan olarak videos/video.mp4 dosyasını kullanır.

Model dosyası models/my_model.pt içinde olmalıdır.


## Önemli Not

Video dosyası (videos/video.mp4) büyük olduğu için GitHub'a yüklenmemiştir.  
Kendi test videonuzu `videos/` klasörüne yerleştirerek projeyi çalıştırabilirsiniz.
