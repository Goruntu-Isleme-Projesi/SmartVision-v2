# core/utils.py
# Açıklama: Nesne konumu belirleme ve nesne mesafesi hesaplama yardımcı fonksiyonları.
# Bu modül, tespit edilen nesnelerin pozisyonunu ve tahmini mesafesini hesaplar.

# --- Nesne türüne göre gerçek genişlikler (metre cinsinden) ---
REAL_WIDTHS = {
    'car': 2.0,        # Ortalama araba genişliği
    'objects': 0.5,    # Genel nesne için yaklaşık orta boyut
    'person': 0.5,     # İnsan genişliği tahmini
    'road': 5.0,       # Yol genişliği tahmini (geniş nesne)
    'stairs': 1.0      # Merdiven genişliği tahmini
}

def calculate_distance(real_width, pixel_width, focal_length):
    """
    Nesnenin tahmini mesafesini hesaplar.

    Args:
        real_width (float): Nesnenin gerçek genişliği (metre cinsinden).
        pixel_width (float): Görüntüdeki nesnenin piksel genişliği.
        focal_length (float): Kameranın odak uzunluğu.

    Returns:
        float: Nesnenin tahmini mesafesi (metre cinsinden).
               Eğer hesaplama yapılamazsa -1 döner.
    """
    if pixel_width > 0:
        return (real_width * focal_length) / pixel_width
    else:
        return -1  # Geçersiz piksel genişliği durumunda

def determine_position(x1, y1, x2, y2, width, height):
    """
    Bir nesnenin görüntü üzerindeki konumunu belirler.

    Args:
        x1, y1, x2, y2 (float): Nesnenin tespit edilen sınır kutusu koordinatları.
        width (int): Görüntü genişliği.
        height (int): Görüntü yüksekliği.

    Returns:
        str: Nesnenin bulunduğu konumu ("left middle", "center top", vb.) döner.
    """
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    if center_x < width / 3:
        horiz = "left"
    elif center_x < 2 * width / 3:
        horiz = "center"
    else:
        horiz = "right"

    if center_y < height / 3:
        vert = "top"
    elif center_y < 2 * height / 3:
        vert = "middle"
    else:
        vert = "bottom"

    return f"{horiz} {vert}"

