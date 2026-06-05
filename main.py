import cv2
import mediapipe as mp
import time

from posture_detector import cek_postur
from agent import beri_peringatan

# =========================
# MediaPipe
# =========================
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

# =========================
# Webcam
# =========================
cap = cv2.VideoCapture(0)

waktu_mulai_buruk = None

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        result = pose.process(rgb)

        score = 100
        status_text = "NORMAL"
        durasi_buruk = 0
        border = (0, 255, 0)

        if result.pose_landmarks:

            landmarks = result.pose_landmarks.landmark

            hasil, sudut = cek_postur(
                landmarks
            )

            ada_masalah = False

            # =========================
            # Hitung Score
            # =========================

            for status, warna in hasil:

                ada_masalah = True

                if status == "MEMBUNGKUK":
                    score -= 40

                elif status == "KEPALA MIRING":
                    score -= 30

                elif status == "TERLALU DEKAT":
                    score -= 30

                beri_peringatan(status)

            score = max(score, 0)

            # =========================
            # Status
            # =========================

            if ada_masalah:

                status_text = "BURUK"

                if waktu_mulai_buruk is None:
                    waktu_mulai_buruk = time.time()

                durasi_buruk = int(
                    time.time() -
                    waktu_mulai_buruk
                )

            else:

                waktu_mulai_buruk = None

            # =========================
            # Warna Border
            # =========================

            if score >= 80:

                border = (0, 255, 0)

            elif score >= 50:

                border = (0, 255, 255)

            else:

                border = (0, 0, 255)

            # =========================
            # Border Kamera
            # =========================

            cv2.rectangle(
                frame,
                (0, 0),
                (frame.shape[1], frame.shape[0]),
                border,
                3
            )

            # =========================
            # Panel Mini
            # =========================

            cv2.rectangle(
                frame,
                (10, 10),
                (240, 120),
                (35, 35, 35),
                -1
            )

            cv2.putText(
                frame,
                "SmartPosture",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Score : {score}%",
                (20, 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                f"Sudut : {sudut:.0f}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                f"Status : {status_text}",
                (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                border,
                1
            )

            # =========================
            # Progress Bar Mini
            # =========================

            cv2.rectangle(
                frame,
                (20, 105),
                (170, 112),
                (255, 255, 255),
                1
            )

            cv2.rectangle(
                frame,
                (20, 105),
                (
                    20 + int(score * 1.5),
                    112
                ),
                border,
                -1
            )

            # =========================
            # Status Aktif
            # =========================

            posisi_y = 145

            for status, warna in hasil:

                cv2.putText(
                    frame,
                    f"- {status}",
                    (20, posisi_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    warna,
                    1
                )

                posisi_y += 22

            # =========================
            # Timer
            # =========================

            if durasi_buruk > 0:

                cv2.putText(
                    frame,
                    f"Buruk {durasi_buruk}s",
                    (20, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    border,
                    2
                )

            # =========================
            # Skeleton Pose
            # =========================

            mp_draw.draw_landmarks(
                frame,
                result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )

        cv2.imshow(
            "SmartPosture Agent",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()