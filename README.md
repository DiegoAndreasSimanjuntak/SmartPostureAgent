# SmartPosture Agent 🧍‍♂️💻

Agen desktop berbasis Python yang memantau postur duduk secara *real-time* lewat webcam,
lalu memberi peringatan (notifikasi + alarm) saat postur buruk terdeteksi.

> Proyek mata kuliah Kecerdasan Buatan — Universitas Singaperbangsa Karawang (UNSIKA).

## Fitur
- Deteksi pose real-time dengan **MediaPipe Pose** + **OpenCV**
- Klasifikasi postur: `normal`, `membungkuk`, `miring`, `dekat` (terlalu dekat layar)
- Notifikasi desktop + alarm suara dengan *cooldown* 30 detik agar tidak spam
- Skrip pengumpulan data sendiri (`collect_data.py`) dan dataset (`dataset_postur.csv`, ±800 sampel)

## Cara Kerja Singkat
1. Webcam menangkap frame, MediaPipe mengekstrak landmark tubuh.
2. Fitur dihitung: sudut telinga–bahu–pinggul, selisih tinggi telinga, jarak antar mata.
3. `posture_detector.py` menilai postur dari fitur tersebut.
4. `agent.py` mengirim peringatan bila postur buruk bertahan.

## Instalasi
Disarankan Python 3.10.

```bash
git clone https://github.com/DiegoAndreasSimanjuntak/SmartPostureAgent.git
cd SmartPostureAgent
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Menjalankan
```bash
python main.py
```
Atau klik dua kali `run.bat` (Windows). Tekan `q` untuk keluar.

## Mengumpulkan Data Sendiri
```bash
python collect_data.py
```
Tekan `s` untuk menyimpan sampel dengan label postur saat ini, `q` untuk keluar.

## Struktur Proyek
```
main.py              # program utama (webcam + deteksi + peringatan)
posture_detector.py  # logika penilaian postur
agent.py             # notifikasi & alarm
utils.py             # hitung sudut & jarak
collect_data.py      # pengumpul dataset
dataset_postur.csv   # dataset postur
assets/alarm.wav     # suara alarm
```

## Catatan
- Butuh webcam yang menghadap pengguna dengan bagian atas tubuh terlihat.
- Akurasi dipengaruhi pencahayaan dan posisi kamera.

## Lisensi
MIT — lihat [LICENSE](LICENSE).

## Penulis
Diego Andreas Simanjuntak — [@DiegoAndreasSimanjuntak](https://github.com/DiegoAndreasSimanjuntak)
