# mengelola koneksi SQLite dan membuat tabel

import sqlite3


class Database:

    def __init__(self, db_name="database.db"):

        self.db_path = db_name

        self.create_table()

    def connect(self):

        return sqlite3.connect(self.db_path)

    def create_table(self):

        conn = self.connect()

        cursor = conn.cursor()

        # =====================================
        # Attendance
        # =====================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT NOT NULL,

            track_id INTEGER NOT NULL,

            name TEXT,

            status TEXT,

            direction TEXT,

            snapshot_path TEXT
        )
        """)

        # =====================================
        # Room Occupancy
        # =====================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS room_occupancy (

            id INTEGER PRIMARY KEY,

            current_occupancy INTEGER DEFAULT 0,

            total_in_today INTEGER DEFAULT 0,

            total_out_today INTEGER DEFAULT 0
        )
        """)

        cursor.execute("""
        INSERT OR IGNORE INTO room_occupancy
        (
            id,
            current_occupancy,
            total_in_today,
            total_out_today
        )
        VALUES
        (
            1,
            0,
            0,
            0
        )
        """)

        conn.commit()
        conn.close()

        print("[INFO] Database Ready")