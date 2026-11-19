# Computer Vision Singkat

Program computer vision singkat pakai **Python + OpenCV**: deteksi wajah
(Haar cascade) dan deteksi tepi (Canny) — dari file foto atau webcam langsung.

## Cara jalan

```bash
pip install -r requirements.txt

python vision.py foto.jpg     # proses foto -> hasil.jpg + hasil-tepi.jpg
python vision.py kamera       # webcam real-time, tekan Q untuk keluar
```

Opsi `--tanpa-wajah` mematikan deteksi wajah (hanya deteksi tepi):

```bash
python vision.py foto.jpg --tanpa-wajah
```

## Isi repo

| File | Fungsi |
| --- | --- |
| `vision.py` | Program utama (±100 baris) |
| `requirements.txt` | Dependensi: `opencv-python` |

## Cara kerja singkat

1. Foto diubah ke grayscale, lalu di-blur ringan (Gaussian) untuk mengurangi noise.
2. **Deteksi tepi** — algoritma Canny (ambang 50/150) menghasilkan citra garis tepi.
3. **Deteksi wajah** — Haar cascade bawaan OpenCV memindai wajah dari depan,
   lalu menggambar kotak hijau + label "wajah" di setiap wajah yang ditemukan.

Lisensi: MIT
