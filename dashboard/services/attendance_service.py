from .database_service import DatabaseService


class AttendanceService:

    def __init__(self):

        self.db = DatabaseService()

    # ==========================================
    # Attendance History
    # ==========================================

    def get_history(self):

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
        """

        return self.db.execute(query)

    # ==========================================
    # Total Entry
    # ==========================================

    def get_total_entry(self):

        query = """
        SELECT COUNT(*)
        FROM attendance
        WHERE direction='MASUK'
        """

        result = self.db.execute_one(query)

        return result[0]

    # ==========================================
    # Total Exit
    # ==========================================

    def get_total_exit(self):

        query = """
        SELECT COUNT(*)
        FROM attendance
        WHERE direction='KELUAR'
        """

        result = self.db.execute_one(query)

        return result[0]

    # ==========================================
    # Current Occupancy
    # ==========================================

    def get_people_inside(self):

        query = """
        SELECT current_occupancy
        FROM room_occupancy
        WHERE id=1
        """

        result = self.db.execute_one(query)

        if result is None:
            return 0

        return result[0]