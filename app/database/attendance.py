# menyimpan event (MASUK/KELUAR) dan nanti juga membaca riwayat jika dibutuhkan

from datetime import datetime


class Attendance:

    def __init__(self, database):

        self.database = database

    def save_event(self, track_id, event, name=None):

        conn = self.database.connect()

        cursor = conn.cursor()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        track_id = int(track_id)

        cursor.execute(
            """
            INSERT INTO attendance
            (timestamp, track_id, name, event)
            VALUES (?, ?, ?, ?)
            """,
            (
                timestamp,
                track_id,
                name,
                event
            )
        )

        conn.commit()

        conn.close()

        print(f"[DATABASE] {track_id} -> {event} disimpan")