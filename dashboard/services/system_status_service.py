import json
import time
from pathlib import Path

STATUS_FILE = Path(__file__).resolve().parents[2] / "system_status.json"
STALE_SECONDS = 10  # kalau heartbeat lebih tua dari ini, dianggap main.py mati


def read_heartbeat():
    """
    Baca system_status.json (ditulis main.py lewat app/utils/status_writer.py).
    Return dict-nya (dengan tambahan key "is_alive": bool), atau None kalau
    file belum pernah dibuat / gagal dibaca.
    """

    if not STATUS_FILE.exists():
        return None

    try:
        with open(STATUS_FILE, "r") as f:
            data = json.load(f)

        data["is_alive"] = (time.time() - data.get("timestamp", 0)) < STALE_SECONDS

        return data

    except Exception:
        return None


def is_system_alive():
    """
    True kalau main.py terdeteksi masih hidup (heartbeat masih fresh).
    Dipakai baik oleh header.py (badge SYSTEM ONLINE) maupun sidebar.py
    (panel SYSTEM STATUS) supaya keduanya selalu konsisten.
    """

    heartbeat = read_heartbeat()

    return bool(heartbeat and heartbeat.get("is_alive"))