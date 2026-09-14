import json
import time
from pathlib import Path

STATUS_FILE = Path(__file__).resolve().parent / "system_status.json"

print(f"Mencari file di: {STATUS_FILE}")
print(f"File ada? {STATUS_FILE.exists()}")

if STATUS_FILE.exists():
    with open(STATUS_FILE, "r") as f:
        data = json.load(f)

    age = time.time() - data.get("timestamp", 0)

    print(f"Isi file: {data}")
    print(f"Umur heartbeat: {age:.1f} detik (dianggap mati kalau > 10 detik)")
    print(f"Status dianggap ALIVE? {age < 10}")
else:
    print(">> File belum pernah dibuat sama sekali oleh main.py")