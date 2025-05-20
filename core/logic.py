# core/logic.py
# Açıklama: Algılanan nesneleri sınıflandırma, uyarı mesajları üretme ve öncelik belirleme işlemlerini içerir.

def classify_object(label):
    """
    Nesne etiketine göre nesne tipini belirler.

    Args:
        label (str): Tespit edilen nesnenin etiketi.

    Returns:
        str: "dangerous", "safe", "info" veya "unknown" sınıflandırması.
    """
    dangerous_objects = ['car', 'stairs']
    safe_objects = ['road']
    info_objects = ['person', 'objects']

    if label in dangerous_objects:
        return "dangerous"
    elif label in safe_objects:
        return "safe"
    elif label in info_objects:
        return "info"
    else:
        return "unknown"

def generate_warning_text(label, position, distance_desc):
    """
    Algılanan nesne için uygun uyarı metni oluşturur.

    Args:
        label (str): Nesne etiketi.
        position (str): Nesnenin pozisyonu.
        distance_desc (str): Nesnenin mesafe açıklaması ("nearby", "very close" vb.).

    Returns:
        str: Seslendirilecek veya yazdırılacak uyarı metni.
    """
    obj_type = classify_object(label)

    if obj_type == "dangerous":
        return f"Warning! {label} detected in the {position} region, {distance_desc}."
    elif obj_type == "safe":
        return road_direction_message(position)
    elif obj_type == "info":
        return f"{label} detected in the {position} region, {distance_desc}."
    else:
        return f"{label} detected in the {position}."

def road_direction_message(position):
    """
    Algılanan güvenli yol için uygun yönlendirme mesajı üretir.

    Args:
        position (str): Yolun bulunduğu pozisyon.

    Returns:
        str: Kullanıcıyı yönlendiren mesaj ("left", "right", "straight" vb.).
    """
    if "center middle" in position:
        return "Safe path detected ahead. You can continue straight."
    elif "left" in position:
        return "Safe path detected to your left."
    elif "right" in position:
        return "Safe path detected to your right."
    elif "top" in position:
        return "Safe path detected forward."
    elif "bottom" in position:
        return "Safe path detected behind you."
    else:
        return "Safe path detected nearby."

def determine_wait_time(label, distance, last_distance, threshold=0.3):
    """
    Algılanan nesneye ve mesafe değişimine göre bekleme süresi belirler.

    Args:
        label (str): Nesne etiketi.
        distance (float): Mevcut mesafe.
        last_distance (float): Önceki mesafe.
        threshold (float): Mesafe değişim eşik değeri.

    Returns:
        int: Bekleme süresi (saniye cinsinden).
    """
    obj_type = classify_object(label)

    if last_distance is not None:
        if distance < last_distance - threshold:
            if obj_type == "dangerous":
                return 2
            elif obj_type == "safe":
                return 6
            else:
                return 3
        elif distance > last_distance + threshold:
            return 6
        else:
            return 4
    else:
        return 4

def position_priority(position):
    """
    Nesnenin pozisyonuna göre öncelik sırası belirler.

    Args:
        position (str): Nesnenin görüntüdeki pozisyonu.

    Returns:
        int: Öncelik skoru (1 = en önemli, 10 = en önemsiz).
    """
    if position == "center middle":
        return 1
    elif position == "right middle":
        return 2
    elif position == "left middle":
        return 3
    elif position == "right top":
        return 4
    elif position == "left top":
        return 5
    elif position == "right bottom":
        return 6
    elif position == "left bottom":
        return 7
    elif position == "center top":
        return 8
    elif position == "center bottom":
        return 9
    else:
        return 10  # Bilinmeyen pozisyonlar için en düşük öncelik

def direction_from_position(position):
    """
    Nesnenin konumuna göre yön bilgisi döner.

    Args:
        position (str): Pozisyon bilgisi.

    Returns:
        str: "straight", "left", "right" veya "unknown".
    """
    if "center middle" in position or "center" in position:
        return "straight"
    elif "left" in position:
        return "left"
    elif "right" in position:
        return "right"
    else:
        return "unknown"
#TODO Burada bir kontrol ister gibi bir sorun yokta bir düzenleme olabilir.