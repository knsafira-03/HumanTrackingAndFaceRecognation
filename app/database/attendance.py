from datetime import datetime


class Attendance:

    def __init__(self, database):

        self.database = database

    def save_event(
        self,
        track_id,
        direction,
        name,
        snapshot_path=None
    ):

        conn = self.database.connect()

        cursor = conn.cursor()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        if name == "Unknown":

            status = "UNAUTHORIZED"

        else:

            status = "AUTHORIZED"

        cursor.execute(
            """
            INSERT INTO attendance
            (
                timestamp,
                track_id,
                name,
                status,
                direction,
                snapshot_path
            )

            VALUES
            (?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                int(track_id),
                name,
                status,
                direction,
                snapshot_path
            )
        )

        # ===============================
        # Update Room Occupancy
        # ===============================

        if direction == "MASUK":

            cursor.execute("""
            UPDATE room_occupancy

            SET

            current_occupancy =
                current_occupancy + 1,

            total_in_today =
                total_in_today + 1

            WHERE id = 1
            """)

        elif direction == "KELUAR":

            cursor.execute("""
            UPDATE room_occupancy

            SET

            current_occupancy =
                MAX(current_occupancy - 1, 0),

            total_out_today =
                total_out_today + 1

            WHERE id = 1
            """)

        conn.commit()

        conn.close()

        print(
            f"[DATABASE] "
            f"{name} "
            f"-> {direction}"
        )