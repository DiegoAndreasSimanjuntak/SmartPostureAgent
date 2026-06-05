from plyer import notification
from playsound import playsound
import time

waktu_terakhir = 0

def beri_peringatan(pesan):

    global waktu_terakhir

    sekarang = time.time()

    # cooldown 30 detik
    if sekarang - waktu_terakhir > 30:

        notification.notify(
            title="SmartPosture Agent ⚠️",
            message=pesan,
            timeout=5
        )

        try:
            playsound("assets/alarm.wav")
        except:
            pass

        waktu_terakhir = sekarang