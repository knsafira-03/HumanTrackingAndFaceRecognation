import json
import time
from pathlib import Path

# system_status.json ditaruh di root project (sejajar dengan main.py & database.db)
BASE_DIR = Path(__file__).resolve().parents[2]
STATUS_FILE = BASE_DIR / "system_status.json"


def write_status(**kwargs):
    """
    Tulis status komponen sistem (yolo_engine, face_recognition, whatsapp, dll)
    beserta timestamp saat ini ke file JSON.

    Dashboard membaca file ini untuk menampilkan status real (bukan dummy).
    Kalau timestamp-nya sudah lebih dari beberapa detik, dashboard akan
    menganggap main.py sudah berhenti/crash dan menandai status jadi offline.

    Contoh pemakaian di main.py:
        write_status(yolo_engine=True, face_recognition=True, whatsapp=True)
    """

    data = {
        "timestamp": time.time(),
        **kwargs,
    }

    try:
        with open(STATUS_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"[STATUS] Gagal menulis status: {e}")