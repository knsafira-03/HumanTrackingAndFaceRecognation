# Smart Server Room Access Monitoring

Sistem pemantauan akses ruang server berbasis deteksi orang (YOLOv8),
pengenalan wajah (FaceNet), dan penghitungan MASUK/KELUAR otomatis,
dilengkapi dashboard web (Streamlit) dan notifikasi WhatsApp.

Dibuat untuk Dinas Komunikasi dan Informatika Kota Probolinggo.

---

## 1. Struktur Proyek

```
├── main.py                     # Program utama -- jalankan kamera & deteksi
├── app_config.py                # Semua pengaturan (kamera, model, threshold, dll)
│
├── app/                         # Logic inti sistem
│   ├── detector/
│   │   ├── detector.py          # Deteksi & tracking ORANG (YOLOv8 + ByteTrack)
│   │   └── face_detector.py     # Deteksi WAJAH (YOLOv8-face)
│   │
│   ├── event/
│   │   ├── line_counter.py      # Hitung MASUK/KELUAR berdasarkan garis virtual
│   │   └── track_resolver.py    # Sambungkan track_id yang "putus" akibat oklusi
│   │
│   ├── recognition/
│   │   ├── face_database.py     # Bangun database wajah dari folder photos/
│   │   ├── face_matcher.py      # Cocokkan kotak wajah ke kotak badan orang
│   │   ├── face_recognizer.py   # Bandingkan wajah ke database (FaceNet)
│   │   └── track_registry.py    # Sistem "lock" identitas per track (voting)
│   │
│   ├── services/
│   │   └── recognition_service.py  # Orkestrasi: deteksi wajah + lock + cache
│   │
│   ├── database/
│   │   ├── database.py          # Koneksi SQLite + skema tabel
│   │   └── attendance.py        # Simpan event MASUK/KELUAR ke database
│   │
│   ├── notification/
│   │   ├── notification_manager.py  # Susun pesan notifikasi
│   │   └── whatsapp_service.py      # Kirim WhatsApp lewat Fonnte API
│   │
│   ├── snapshot/
│   │   └── snapshot_service.py  # Simpan foto snapshot tiap event
│   │
│   ├── tracker/
│   │   └── tracker.py           # Wrapper tracking (dipakai detector.py)
│   │
│   └── utils/
│       ├── status_writer.py     # Tulis heartbeat (system_status.json) untuk dashboard
│       └── hud.py               # Gambar panel Person/Masuk/Keluar/FPS di window kamera
│
├── config/
│   ├── bytetrack.yaml           # Parameter tracker ByteTrack (track_buffer dkk)
│   └── settings.py              # (TIDAK ADA DI REPO, WAJIB DIBUAT SENDIRI -- lihat Bagian 3)
│
├── dashboard/                   # Aplikasi web (Streamlit)
│   ├── dashboard_v2.py          # Entry point dashboard -- jalankan file ini
│   │
│   ├── views/                   # 1 file = 1 halaman
│   │   ├── dashboard.py         # Halaman utama (4 kartu ringkasan + Live Activity)
│   │   ├── live_activity.py     # Halaman Live Activity lengkap (dengan filter)
│   │   └── audit_log.py         # Halaman Audit Log (tabel lengkap + export CSV)
│   │
│   ├── components/              # Potongan UI yang dipakai ulang antar halaman
│   │   ├── sidebar.py           # Sidebar kiri (menu + System Status)
│   │   ├── header.py            # Judul halaman + badge SYSTEM ONLINE
│   │   ├── metrics.py           # 4 kartu (Occupancy, Entry, Exit, Unauthorized)
│   │   ├── activity.py          # Kartu Live Activity (dipakai dashboard & live_activity)
│   │   ├── footer.py            # Footer halaman
│   │   └── audit/               # Komponen khusus halaman Audit Log
│   │       ├── table.py         # Tabel + logic filter
│   │       ├── filters.py       # Widget filter (search/tanggal/status/dll)
│   │       ├── header.py        # Judul + tombol Export CSV
│   │       └── detail.py        # Panel detail di kanan (saat baris dipilih)
│   │
│   ├── services/
│   │   ├── database_service.py       # Semua query SQL ke database.db
│   │   └── system_status_service.py  # Baca heartbeat dari main.py
│   │
│   └── assets/
│       ├── style.css             # Semua styling dashboard
│       └── logo_diskominfo.png   # Logo di sidebar
│
├── models/
│   ├── yolo/yolov8n.pt          # Model deteksi ORANG
│   └── face/yolov8n-face.pt     # Model deteksi WAJAH
│
├── photos/                      # Database wajah -- 1 folder per orang
│   └── <nama>/foto1.jpg, foto2.jpg, ...
│
├── static/live.jpg              # Preview kamera terbaru (auto-update tiap 0.5 detik)
├── database.db                  # Database SQLite (dibuat otomatis saat main.py pertama jalan)
├── system_status.json           # Heartbeat main.py (dibuat otomatis, dibaca dashboard)
└── requirements.txt
```

---

## 2. Persiapan (sekali saja)

### a. Buat virtual environment & install dependency

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`requirements.txt` bawaan repo ini belum lengkap -- tambahkan juga:

```powershell
pip install keras-facenet scipy streamlit-autorefresh
```

- `keras-facenet` + `scipy` -- dipakai `face_recognizer.py` untuk pengenalan wajah
- `streamlit-autorefresh` -- dipakai dashboard supaya angka ter-update sendiri tanpa refresh manual

### b. Download model YOLO (kalau folder `models/` kosong atau file corrupt)

```powershell
python download_model.py
```

Pastikan juga `models/face/yolov8n-face.pt` ada (model deteksi wajah) -- download manual dari sumber project kalau belum ada.

### c. Siapkan token WhatsApp (Fonnte)

Buat file baru `config/settings.py` (file ini **sengaja tidak ada di repo**, berisi token rahasia):

```python
FONNTE_TOKEN = "ISI_TOKEN_DARI_AKUN_FONNTE_KAMU"
WHATSAPP_TARGET = "62812xxxxxxxx"
```

Token didapat dari dashboard [fonnte.com](https://fonnte.com) setelah connect nomor WhatsApp sebagai device.

### d. Siapkan database wajah

Buat 1 folder per orang di `photos/`, isi 3-5 foto (variasi sudut/pencahayaan):

```
photos/
  aqil/
    foto1.jpg
    foto2.jpg
    ...
  raras/
    foto1.jpg
    foto2.jpg
```

### e. Cek kamera & posisi garis (kalau kamera baru/posisi berubah)

```powershell
python camera_test.py       # cari CAMERA_INDEX yang benar
python door_cordinate.py    # klik di video buat cari koordinat garis pintu
```

Update hasilnya di `app_config.py` (`CAMERA_INDEX`) dan `app/event/line_counter.py` (koordinat garis).

---

## 3. Menjalankan Sistem

Butuh **2 terminal terpisah**, dua-duanya harus aktifkan venv dulu (`.\.venv\Scripts\Activate.ps1`).

**Terminal 1 -- mesin deteksi (kamera, YOLO, face recognition):**
```powershell
python main.py
```
Tekan `q` di window kamera untuk berhenti dengan aman.

**Terminal 2 -- dashboard web:**
```powershell
streamlit run dashboard/dashboard_v2.py
```
Buka `http://localhost:8501` di browser.

> Dashboard bisa dibuka meski `main.py` belum/tidak jalan -- semua panel status akan otomatis menunjukkan offline/0, bukan error.

---

## 4. Konfigurasi Penting (`app_config.py`)

| Variabel | Kegunaan |
|---|---|
| `CAMERA_INDEX` | Index kamera yang dipakai |
| `YOLO_MODEL` | Path model deteksi orang |
| `CONFIDENCE` | Ambang percaya diri deteksi orang (turunkan kalau bounding box sering hilang) |
| `FACE_MODEL` | Path model deteksi wajah |
| `FACE_CONFIDENCE` | Ambang percaya diri deteksi wajah |
| `FACE_LOCK_VOTES` | Berapa kali nama yang sama harus muncul sebelum identitas dikunci |
| `FACE_VOTE_HISTORY` | Dari berapa tebakan terakhir voting dihitung |
| `TRACKER` | Path config ByteTrack (`config/bytetrack.yaml`) |

---

## 5. Fitur Utama

- **Deteksi & tracking orang** real-time dengan penomoran ID yang stabil, tahan terhadap oklusi singkat dan perubahan pose (duduk/berdiri).
- **Pengenalan wajah** dengan sistem voting (toleran ke kesalahan baca sesekali) dan lock permanen begitu identitas cukup yakin.
- **Hitung MASUK/KELUAR otomatis** lewat garis virtual, dengan mekanisme anti-dobel-hitung saat ID tracking berubah.
- **Notifikasi WhatsApp** otomatis tiap ada event masuk/keluar, dengan status kirim yang dilaporkan balik ke dashboard.
- **Dashboard real-time**: ringkasan okupansi live, riwayat aktivitas dengan foto, audit log lengkap dengan filter & export CSV, dan status kesehatan sistem (YOLO/Face Recognition/Database/WhatsApp) berbasis heartbeat dari `main.py`.

---

## 6. Catatan Pemeliharaan

- File `system_status.json` dan `static/live.jpg` dibuat otomatis oleh `main.py` saat berjalan -- aman dihapus manual, akan dibuat ulang otomatis.
- `database.db` dibuat otomatis oleh `Database()` di `app/database/database.py`, termasuk migrasi skema (menambah kolom baru) kalau ada perubahan struktur tabel.
- Kalau menambah/mengurangi foto di `photos/`, database wajah akan otomatis dibangun ulang setiap `main.py` start -- tidak perlu langkah tambahan.