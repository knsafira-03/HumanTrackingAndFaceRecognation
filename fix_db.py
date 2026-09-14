import sqlite3
from pathlib import Path

# path ini SAMA PERSIS dengan yang dipakai dashboard/services/database_service.py:
# Path(__file__).resolve().parents[2] / "database.db"  <- dari dashboard/services/
# Kalau fix_db.py ini ditaruh di root project, path-nya jadi:
db_path = Path(__file__).resolve().parent / "database.db"

print(f"Membuka database di: {db_path}")
print(f"File ada? {db_path.exists()}")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("PRAGMA table_info(attendance)")
columns = [c[1] for c in cur.fetchall()]
print(f"Kolom saat ini: {columns}")

if "confidence" not in columns:
    cur.execute("ALTER TABLE attendance ADD COLUMN confidence REAL")
    conn.commit()
    print(">> Kolom 'confidence' BERHASIL ditambahkan.")
else:
    print(">> Kolom 'confidence' sudah ada, tidak ada yang perlu diubah.")

cur.execute("PRAGMA table_info(attendance)")
print(f"Kolom sekarang: {[c[1] for c in cur.fetchall()]}")

conn.close()