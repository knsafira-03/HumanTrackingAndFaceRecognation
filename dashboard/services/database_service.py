import sqlite3
from pathlib import Path
from datetime import datetime


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
        """
        DIHITUNG LANGSUNG dari tabel attendance, difilter ke tanggal HARI
        INI saja -- bukan dari room_occupancy.total_in_today/total_out_today
        yang ternyata tidak pernah di-reset harian (terus menumpuk sejak
        database dibuat, itu sebabnya angkanya bisa aneh/tidak masuk akal
        seperti Exit lebih besar dari Entry).
        """

        today = datetime.now().strftime("%Y-%m-%d")

        row_in = self.execute_one("""
            SELECT COUNT(*)
            FROM attendance
            WHERE direction = 'MASUK'
              AND substr(timestamp, 1, 10) = ?
        """, (today,))

        row_out = self.execute_one("""
            SELECT COUNT(*)
            FROM attendance
            WHERE direction = 'KELUAR'
              AND substr(timestamp, 1, 10) = ?
        """, (today,))

        entrance = row_in[0] if row_in else 0
        exit_count = row_out[0] if row_out else 0

        # Occupancy = entry - exit HARI INI, tidak pernah minus
        occupancy = max(entrance - exit_count, 0)

        return {

            "occupancy": occupancy,

            "entrance": entrance,

            "exit": exit_count

        }

    # =====================================
    # UNAUTHORIZED COUNT
    # =====================================

    def get_unauthorized_count(self):
        """
        Sama seperti get_metrics() -- difilter ke HARI INI saja, supaya
        konsisten dengan 3 kartu lain yang juga "Today's ...".
        """

        today = datetime.now().strftime("%Y-%m-%d")

        row = self.execute_one("""
            SELECT COUNT(*)
            FROM attendance
            WHERE status = 'UNAUTHORIZED'
              AND substr(timestamp, 1, 10) = ?
        """, (today,))

        return row[0] if row else 0

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
    # ACTIVITY FEED (dengan filter, dipakai halaman Live Activity)
    # =====================================

    def get_activity_feed(self, limit=20, status=None, direction=None):
        """
        Ambil feed aktivitas dengan filter opsional, dipakai halaman
        Live Activity. status/direction bernilai "All" (atau None)
        berarti tidak difilter.
        """

        query = """
            SELECT
                timestamp,
                track_id,
                name,
                status,
                direction,
                snapshot_path
            FROM attendance
        """

        conditions = []
        params = []

        if status and status != "All":
            conditions.append("status = ?")
            params.append(status)

        if direction and direction != "All":
            conditions.append("direction = ?")
            params.append(direction)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)

        return self.execute(query, tuple(params))

    # =====================================
    # RECENT ACTIVITY
    # =====================================

    def get_recent_activity(self, limit=6):
        """
        limit=None -> dipakai saat tombol "View All" ditekan (di
        activity.py ini akan dipanggil dengan limit=25, bukan None,
        supaya daftarnya tidak kepanjangan). limit=angka -> ambil
        sejumlah itu saja (default 6, dipakai saat tampilan normal).
        """

        if limit is None:

            return self.execute("""
                SELECT
                    timestamp,
                    track_id,
                    name,
                    status,
                    direction,
                    snapshot_path
                FROM attendance
                ORDER BY id DESC
            """)

        return self.execute("""
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
        """, (limit,))

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