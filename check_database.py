import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
SELECT id,
       timestamp,
       track_id,
       name,
       event
FROM attendance
ORDER BY id DESC
""")

rows = cursor.fetchall()

print("=" * 70)
print("Attendance History")
print("=" * 70)

if len(rows) == 0:
    print("Belum ada data.")
else:

    for row in rows:

        print(f"ID        : {row[0]}")
        print(f"Waktu     : {row[1]}")
        print(f"Track ID  : {row[2]}")
        print(f"Nama      : {row[3]}")
        print(f"Event     : {row[4]}")
        print("-" * 70)

conn.close()