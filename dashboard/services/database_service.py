import sqlite3
from pathlib import Path


class DatabaseService:

    def __init__(self):

        self.db_path = (
            Path(__file__)
            .resolve()
            .parents[2] / "database.db"
        )

    # =====================================
    # CONNECT
    # =====================================

    def connect(self):

        return sqlite3.connect(self.db_path)

    # =====================================
    # GENERIC QUERY
    # =====================================

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

    # =====================================
    # DASHBOARD METRICS
    # =====================================

    def get_metrics(self):

        row = self.execute_one("""
            SELECT
                current_occupancy,
                total_in_today,
                total_out_today
            FROM room_occupancy
            WHERE id = 1
        """)

        if row:

            return {

                "occupancy": row[0],

                "entrance": row[1],

                "exit": row[2]

            }

        return {

            "occupancy": 0,

            "entrance": 0,

            "exit": 0

        }

    # =====================================
    # UNAUTHORIZED COUNT
    # =====================================

    def get_unauthorized_count(self):

        row = self.execute_one("""
            SELECT COUNT(*)
            FROM attendance
            WHERE status='UNAUTHORIZED'
        """)

        return row[0]

    # =====================================
    # ALL LOGS
    # =====================================

    def get_logs(self):

        return self.execute("""
            SELECT *

            FROM attendance

            ORDER BY id DESC
        """)

    # =====================================
    # DISTINCT USERS (dropdown filter "All Users" di Audit Log)
    # =====================================

    def get_distinct_users(self):

        rows = self.execute("""
            SELECT DISTINCT name
            FROM attendance
            WHERE name IS NOT NULL AND name != 'Unknown'
            ORDER BY name
        """)

        return [row[0] for row in rows]

    # =====================================
    # DIRECTION CHART
    # =====================================

    def get_direction_chart(self):

        return self.execute("""
            SELECT

                direction,

                COUNT(*)

            FROM attendance

            GROUP BY direction
        """)

    # =====================================
    # STATUS CHART
    # =====================================

    def get_status_chart(self):

        return self.execute("""
            SELECT

                status,

                COUNT(*)

            FROM attendance

            GROUP BY status
        """)

    def get_recent_activity(self, limit=10):

        query = """
        SELECT
            timestamp,
            track_id,
            name,
            status,
            direction,
            snapshot_path
        FROM attendance
        ORDER BY id DESC
        LIMIT ?
        """

        return self.execute(query, (limit,))
