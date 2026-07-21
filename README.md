# HumanTrackingAndFaceRecognation

# Smart Secure Room Monitoring System

> PKL Project - Diskominfo (Divisi Persandian)

## 📖 Deskripsi

**Smart Secure Room Monitoring System** merupakan sistem monitoring ruangan berbasis **Computer Vision** yang dikembangkan selama Praktik Kerja Lapangan (PKL) di **Dinas Komunikasi dan Informatika (Diskominfo)**, khususnya pada **Divisi Persandian**.

Sistem ini bertujuan membantu petugas dalam memantau aktivitas keluar dan masuk ruangan secara otomatis tanpa harus terus-menerus mengawasi layar CCTV.

Dengan memanfaatkan teknologi **Artificial Intelligence (AI)** dan **Computer Vision**, sistem mampu mendeteksi keberadaan manusia, mencatat aktivitas masuk maupun keluar ruangan, menyimpan riwayat aktivitas ke database, serta mengirimkan notifikasi secara real-time kepada petugas.

Sebagai pengembangan lanjutan, sistem dirancang agar dapat mendukung **Face Recognition** untuk mengenali identitas pengguna apabila diperlukan.

---

# 🎯 Tujuan Proyek

* Mengotomatisasi proses monitoring ruangan menggunakan CCTV.
* Mendeteksi aktivitas manusia yang masuk dan keluar ruangan.
* Mengurangi kebutuhan pengawasan CCTV secara terus-menerus.
* Menyimpan log aktivitas secara otomatis.
* Mengirimkan notifikasi real-time kepada petugas.
* Menyediakan dashboard monitoring aktivitas.
* Membangun sistem yang dapat dikembangkan lebih lanjut untuk kebutuhan keamanan ruangan.

---

# ✨ Fitur

### ✅ Human Detection

Mendeteksi keberadaan manusia menggunakan model YOLO.

### ✅ Human Tracking

Memberikan ID unik pada setiap objek manusia sehingga dapat dilacak.

### ✅ Entry & Exit Detection

Mengidentifikasi apakah seseorang masuk atau keluar ruangan menggunakan virtual line.

### ✅ Activity Logging

Menyimpan seluruh aktivitas ke database beserta waktu kejadian.

### ✅ Snapshot Capture

Mengambil gambar otomatis ketika aktivitas terdeteksi.

### ✅ Real-Time Notification

Mengirimkan notifikasi melalui:

* WhatsApp (prioritas implementasi)
* Telegram (alternatif)

### ✅ Dashboard Monitoring

Menampilkan riwayat aktivitas secara real-time.

### 🚧 Face Recognition (Future Development)

Mengidentifikasi identitas orang yang masuk atau keluar ruangan.

---

# 🏗️ Arsitektur Sistem

```text
                 CCTV Camera
                      │
                      ▼
               Video Streaming
                      │
                      ▼
             Human Detection (YOLO)
                      │
                      ▼
          Object Tracking (ByteTrack)
                      │
                      ▼
          Entry / Exit Detection
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
   Activity Logging          Snapshot Capture
        │                           │
        └─────────────┬─────────────┘
                      ▼
             Notification Service
         (WhatsApp / Telegram)
                      │
                      ▼
            Monitoring Dashboard
```

---

# 🛠️ Tech Stack

## Programming Language

* Python

## IDE

* Visual Studio Code

## Computer Vision

* OpenCV
* Ultralytics YOLO

## Object Tracking

* ByteTrack / BoT-SORT

## Database

* SQLite

## Dashboard

* Flask

## Version Control

* Git

## Hardware

* CCTV Camera
* Windows PC

---

# 📁 Project Structure

```text
HumanDetectionSystem/

│
├── app/
│   ├── detection/
│   ├── tracking/
│   ├── notification/
│   ├── database/
│   ├── dashboard/
│   ├── utils/
│
├── models/
│
├── snapshots/
│
├── database/
│
├── docs/
│
├── testing/
│
├── main.py
│
├── requirements.txt
│
└── README.md
```

---

# 🔄 Workflow

1. CCTV mengirimkan video ke sistem.
2. YOLO mendeteksi manusia.
3. Tracker memberikan ID pada setiap objek.
4. Sistem menentukan aktivitas masuk atau keluar.
5. Snapshot disimpan.
6. Aktivitas dicatat ke database.
7. Notifikasi dikirim melalui WhatsApp atau Telegram.
8. Dashboard diperbarui secara otomatis.

---

# 🔒 Security Considerations

Karena sistem dikembangkan untuk lingkungan **Divisi Persandian Diskominfo**, beberapa aspek keamanan menjadi perhatian utama:

* Penyimpanan log aktivitas.
* Penyimpanan snapshot secara aman.
* Pembatasan hak akses pengguna.
* Audit trail seluruh aktivitas sistem.
* Perlindungan data pribadi apabila Face Recognition diterapkan.
* Desain sistem yang mudah dikembangkan dan dipelihara.

---

# 🚀 Roadmap

## Phase 1

* Human Detection
* Human Tracking
* Entry & Exit Detection

## Phase 2

* Database
* Dashboard
* Snapshot Logging

## Phase 3

* WhatsApp Notification
* Telegram Notification

## Phase 4

* Face Recognition
* Visitor Analytics
* Multi-Camera Support

---

# 👥 Development Team

| Nama                   | Posisi                                | Tanggung Jawab                                                                                                     |
| ---------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Khalisa Nur Safira** | Project Manager & System Analyst      | Mengelola proyek, analisis kebutuhan, desain sistem, koordinasi tim, dokumentasi, dan integrasi sistem.            |
| **Dayinta Raras Apsari**     | AI & Computer Vision Engineer         | Mengembangkan Human Detection, Object Tracking, Face Recognition (opsional), serta optimasi model AI.              |
| **NAqilah Akma**     | Backend & System Integration Engineer | Mengembangkan database, dashboard monitoring, integrasi CCTV, notifikasi WhatsApp/Telegram, dan deployment sistem. |

**Institution**

* Universitas Brawijaya
* Program Studi Teknik Komputer
* Praktik Kerja Lapangan (PKL)
* Dinas Komunikasi dan Informatika (Diskominfo)
* Divisi Persandian

---

### 👨‍💻 Role Description

**Project Manager & System Analyst**

* Menyusun requirement sistem.
* Menyusun timeline dan pembagian tugas.
* Mendesain arsitektur sistem.
* Mengoordinasikan pengembangan proyek.
* Menyusun dokumentasi teknis dan laporan PKL.

**AI & Computer Vision Engineer**

* Implementasi Human Detection menggunakan YOLO.
* Implementasi Object Tracking.
* Pengembangan Entry & Exit Detection.
* Pengembangan Face Recognition (opsional).
* Pengujian performa model AI.

**Backend & System Integration Engineer**

* Mendesain database.
* Mengembangkan Dashboard Monitoring.
* Mengintegrasikan CCTV dengan sistem.
* Mengembangkan modul notifikasi WhatsApp/Telegram.
* Melakukan integrasi seluruh komponen sistem.

---

# 📌 Status Project

🚧 **In Development**

Project ini sedang dikembangkan sebagai bagian dari kegiatan Praktik Kerja Lapangan (PKL) dan akan terus disempurnakan sesuai kebutuhan implementasi di lingkungan Diskominfo.
