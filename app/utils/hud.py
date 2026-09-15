import cv2
import numpy as np


# ============================================================
# WARNA (format BGR -- kebalik dari RGB/hex biasa, karena OpenCV)
# Senada dengan tema dashboard Streamlit (navy sidebar, hijau/merah dsb)
# ============================================================

COLOR_PANEL_BG = (35, 24, 15)     # navy gelap (mirip #0F172A)
COLOR_ACCENT   = (221, 147, 0)    # biru terang (mirip #0093DD)
COLOR_GREEN    = (94, 197, 34)    # hijau (mirip #22C55E)
COLOR_RED      = (38, 38, 220)    # merah (mirip #DC2626)
COLOR_WHITE    = (255, 255, 255)
COLOR_GRAY     = (150, 145, 140)
COLOR_LINE     = (80, 70, 60)


def _rounded_rect(img, pt1, pt2, color, radius):

    x1, y1 = pt1
    x2, y2 = pt2

    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, -1)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, -1)

    cv2.ellipse(img, (x1 + radius, y1 + radius), (radius, radius), 180, 0, 90, color, -1)
    cv2.ellipse(img, (x2 - radius, y1 + radius), (radius, radius), 270, 0, 90, color, -1)
    cv2.ellipse(img, (x1 + radius, y2 - radius), (radius, radius), 90, 0, 90, color, -1)
    cv2.ellipse(img, (x2 - radius, y2 - radius), (radius, radius), 0, 0, 90, color, -1)


def draw_hud(frame, person_count, in_count, out_count, fps):
    """
    Gambar panel "dashboard mini" di pojok kiri atas frame -- semi
    transparan, rounded corner, dengan ikon kecil untuk tiap baris.
    Dipanggil SEKALI tiap frame, menggantikan cv2.rectangle/putText
    manual yang sebelumnya ada di main.py.
    """

    x1, y1 = 16, 16
    x2, y2 = 246, 198  # 230x182 -- lebih ringkas dari versi sebelumnya

    # ---- panel semi-transparan ----
    overlay = frame.copy()
    _rounded_rect(overlay, (x1, y1), (x2, y2), COLOR_PANEL_BG, radius=14)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

    # ---- garis aksen di kiri panel ----
    cv2.rectangle(frame, (x1, y1 + 14), (x1 + 4, y2 - 14), COLOR_ACCENT, -1)

    # ---- judul ----
    cv2.putText(
        frame, "MONITORING", (x1 + 18, y1 + 24),
        cv2.FONT_HERSHEY_DUPLEX, 0.48, COLOR_ACCENT, 1, cv2.LINE_AA
    )
    cv2.line(frame, (x1 + 18, y1 + 32), (x2 - 14, y1 + 32), COLOR_LINE, 1, cv2.LINE_AA)

    row_y = y1 + 58
    row_gap = 28

    # ---- PERSON ----
    cv2.circle(frame, (x1 + 28, row_y - 6), 5, COLOR_WHITE, -1)
    cv2.putText(
        frame, "Person", (x1 + 44, row_y),
        cv2.FONT_HERSHEY_SIMPLEX, 0.48, COLOR_GRAY, 1, cv2.LINE_AA
    )
    cv2.putText(
        frame, str(person_count), (x2 - 36, row_y),
        cv2.FONT_HERSHEY_DUPLEX, 0.58, COLOR_WHITE, 1, cv2.LINE_AA
    )

    # ---- MASUK (segitiga ke atas) ----
    row_y += row_gap
    tri_up = np.array([
        [x1 + 28, row_y - 12],
        [x1 + 22, row_y - 3],
        [x1 + 34, row_y - 3],
    ])
    cv2.fillPoly(frame, [tri_up], COLOR_GREEN)
    cv2.putText(
        frame, "Masuk", (x1 + 44, row_y),
        cv2.FONT_HERSHEY_SIMPLEX, 0.48, COLOR_GRAY, 1, cv2.LINE_AA
    )
    cv2.putText(
        frame, str(in_count), (x2 - 36, row_y),
        cv2.FONT_HERSHEY_DUPLEX, 0.58, COLOR_GREEN, 1, cv2.LINE_AA
    )

    # ---- KELUAR (segitiga ke bawah) ----
    row_y += row_gap
    tri_down = np.array([
        [x1 + 22, row_y - 12],
        [x1 + 34, row_y - 12],
        [x1 + 28, row_y - 3],
    ])
    cv2.fillPoly(frame, [tri_down], COLOR_RED)
    cv2.putText(
        frame, "Keluar", (x1 + 44, row_y),
        cv2.FONT_HERSHEY_SIMPLEX, 0.48, COLOR_GRAY, 1, cv2.LINE_AA
    )
    cv2.putText(
        frame, str(out_count), (x2 - 36, row_y),
        cv2.FONT_HERSHEY_DUPLEX, 0.58, COLOR_RED, 1, cv2.LINE_AA
    )

    # ---- separator + FPS ----
    row_y += 16
    cv2.line(frame, (x1 + 16, row_y), (x2 - 16, row_y), COLOR_LINE, 1, cv2.LINE_AA)

    row_y += 26
    cv2.putText(
        frame, f"FPS {fps:.1f}", (x1 + 18, row_y),
        cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLOR_GRAY, 1, cv2.LINE_AA
    )