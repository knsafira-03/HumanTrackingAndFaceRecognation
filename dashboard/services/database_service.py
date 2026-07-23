import sqlite3
from pathlib import Path


class DatabaseService:

    def __init__(self):

        # Path ke database.db di root project
        self.db_path = (
            Path(__file__)
            .resolve()
            .parents[2] / "database.db"
        )

    def connect(self):

        return sqlite3.connect(self.db_path)

    def execute(self, query, params=()):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(query, params)

        rows = cursor.fetchall()

        conn.close()

        return rows

    def execute_one(self, query, params=()):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(query, params)

        row = cursor.fetchone()

        conn.close()

        return row