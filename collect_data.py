import cv2
import mediapipe as mp
import csv
import os

from utils import hitung_sudut, hitung_jarak

# ==================================
# GANTI LABEL SESUAI DATA YANG DIREKAM
# ==================================
LABEL = "dekat"

# normal
# membungkuk
# miring
# dekat

mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# ==================================
# Lokasi file CSV
# ==================================
file_csv = os.path.join(
    os.path.dirname(__file__),
    "dataset_postur.csv"
)

# ==================================
# Buat file jika belum ada
# ==================================
if not os.path.exists(file_csv):

    with open(file_csv, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "sudut",
            "selisih_telinga",
            "jarak_mata",
            "label"
        ])

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Webcam gagal dibaca")
            break

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        result = pose.process(rgb)

        if result.pose_landmarks:

            lm = result.pose_landmarks.landmark

            # ==========================
            # Landmark yang dipakai
            # ==========================

            telinga_kiri = [
                lm[7].x,
                lm[7].y
            ]

            telinga_kanan = [
                lm[8].x,
                lm[8].y
            ]

            bahu_kiri = [
                lm[11].x,
                lm[11].y
            ]

            pinggul_kiri = [
                lm[23].x,
                lm[23].y
            ]

            mata_kiri = [
                lm[2].x,
                lm[2].y
            ]

            mata_kanan = [
                lm[5].x,
                lm[5].y
            ]

            # ==========================
            # Hitung fitur
            # ==========================

            sudut = hitung_sudut(
                telinga_kiri,
                bahu_kiri,
                pinggul_kiri
            )

            selisih_telinga = abs(
                telinga_kiri[1] -
                telinga_kanan[1]
            )

            jarak_mata = hitung_jarak(
                mata_kiri,
                mata_kanan
            )

            # ==========================
            # Status sementara
            # ==========================

            status = "NORMAL"

            if sudut < 140:
                status = "MEMBUNGKUK"

            elif selisih_telinga > 0.04:
                status = "KEPALA MIRING"

            elif jarak_mata > 0.10:
                status = "TERLALU DEKAT"

            # ==========================
            # Tampilkan informasi
            # ==========================

            cv2.putText(
                frame,
                f"Label Dataset : {LABEL}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Tekan S = Simpan",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Sudut : {sudut:.2f}",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Selisih Telinga : {selisih_telinga:.4f}",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Jarak Mata : {jarak_mata:.4f}",
                (20, 200),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Status : {status}",
                (20, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            # Gambar skeleton
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        cv2.imshow(
            "Dataset Collector",
            frame
        )

        key = cv2.waitKey(1)

        # ==========================
        # Simpan data
        # ==========================
        if key == ord('s') and result.pose_landmarks:

            with open(
                file_csv,
                "a",
                newline=""
            ) as f:

                writer = csv.writer(f)

                writer.writerow([
                    round(sudut, 3),
                    round(selisih_telinga, 4),
                    round(jarak_mata, 4),
                    LABEL
                ])

            print(
                f"Data tersimpan -> "
                f"{LABEL}"
            )

        # ==========================
        # Keluar
        # ==========================
        elif key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()