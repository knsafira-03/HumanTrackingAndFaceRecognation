# mengelola koneksi SQLite dan membuat tabel

import sqlite3
import os


class Database:

    def __init__(self, db_name="database.db"):

        self.db_path = db_name

        self.create_table()

    def connect(self):

        return sqlite3.connect(self.db_path)

    def create_table(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                timestamp TEXT NOT NULL,

                track_id INTEGER NOT NULL,

                name TEXT,

                event TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

        print("[INFO] Database Ready")