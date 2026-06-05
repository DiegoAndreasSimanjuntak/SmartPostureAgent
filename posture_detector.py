from utils import hitung_sudut, hitung_jarak

# =========================
# Deteksi Postur
# =========================
def cek_postur(landmarks):

    hasil = []

    # =========================
    # Ambil Titik
    # =========================
    telinga_kiri = [
        landmarks[7].x,
        landmarks[7].y
    ]

    telinga_kanan = [
        landmarks[8].x,
        landmarks[8].y
    ]

    bahu_kiri = [
        landmarks[11].x,
        landmarks[11].y
    ]

    pinggul_kiri = [
        landmarks[23].x,
        landmarks[23].y
    ]

    mata_kiri = [
        landmarks[2].x,
        landmarks[2].y
    ]

    mata_kanan = [
        landmarks[5].x,
        landmarks[5].y
    ]

    # =========================
    # 1. Membungkuk
    # =========================

    sudut = hitung_sudut(
        telinga_kiri,
        bahu_kiri,
        pinggul_kiri
    )

    if sudut < 150:

        hasil.append(
            ("MEMBUNGKUK", (0, 0, 255))
        )

    # =========================
    # 2. Kepala Miring
    # =========================

    selisih = abs(
        telinga_kiri[1] -
        telinga_kanan[1]
    )

    if selisih > 0.03:

        hasil.append(
            ("KEPALA MIRING", (0, 255, 255))
        )

    # =========================
    # 3. Terlalu Dekat
    # =========================

    jarak_mata = hitung_jarak(
        mata_kiri,
        mata_kanan
    )

    if jarak_mata > 0.08:

        hasil.append(
            ("TERLALU DEKAT", (255, 0, 0))
        )

    return hasil, sudut