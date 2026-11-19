#!/usr/bin/env python3
"""
Computer Vision Singkat — deteksi wajah & tepi (edge) pakai OpenCV.

Contoh:
    python vision.py foto.jpg          # proses 1 foto -> hasil.jpg
    python vision.py kamera            # webcam real-time (tekan Q untuk keluar)
    python vision.py foto.jpg --tanpa-wajah   # hanya deteksi tepi
"""

import argparse
import sys

import cv2


def muat_detektor_wajah():
    """Haar cascade bawaan OpenCV untuk wajah dari depan."""
    path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    detektor = cv2.CascadeClassifier(path)
    if detektor.empty():
        sys.exit("File cascade wajah tidak ditemukan di instalasi OpenCV.")
    return detektor


def proses_frame(frame, detektor=None):
    """Gambar kotak di wajah yang terdeteksi + kembalikan citra tepi Canny."""
    abu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    tepi = cv2.Canny(cv2.GaussianBlur(abu, (5, 5), 0), 50, 150)

    if detektor is not None:
        wajah = detektor.detectMultiScale(abu, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30))
        for (x, y, w, h) in wajah:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "wajah", (x, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        print(f"Wajah terdeteksi: {len(wajah)}")
    return frame, tepi


def mode_foto(path, pakai_wajah=True):
    frame = cv2.imread(path)
    if frame is None:
        sys.exit(f"Foto tidak bisa dibaca: {path}")
    detektor = muat_detektor_wajah() if pakai_wajah else None
    hasil, tepi = proses_frame(frame, detektor)
    cv2.imwrite("hasil.jpg", hasil)
    cv2.imwrite("hasil-tepi.jpg", tepi)
    print("Tersimpan: hasil.jpg (kotak wajah) & hasil-tepi.jpg (deteksi tepi)")


def mode_kamera(pakai_wajah=True):
    kamera = cv2.VideoCapture(0)
    if not kamera.isOpened():
        sys.exit("Webcam tidak bisa dibuka.")
    detektor = muat_detektor_wajah() if pakai_wajah else None
    print("Webcam jalan — tekan Q untuk keluar.")
    while True:
        ok, frame = kamera.read()
        if not ok:
            break
        hasil, tepi = proses_frame(frame, detektor)
        cv2.imshow("Wajah (Q = keluar)", hasil)
        cv2.imshow("Tepi / Canny (Q = keluar)", tepi)
        if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q")):
            break
    kamera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deteksi wajah & tepi singkat.")
    parser.add_argument("sumber", help="'kamera' atau path ke file foto")
    parser.add_argument("--tanpa-wajah", action="store_true",
                        help="lewati deteksi wajah, hanya deteksi tepi")
    args = parser.parse_args()

    if args.sumber.lower() == "kamera":
        mode_kamera(pakai_wajah=not args.tanpa_wajah)
    else:
        mode_foto(args.sumber, pakai_wajah=not args.tanpa_wajah)
