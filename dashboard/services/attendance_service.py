from .database_service import DatabaseService


class AttendanceService:

    def __init__(self):

        self.db = DatabaseService()

    def get_history(self):

        query = """
        SELECT
            timestamp,
            track_id,
            name,
            event
        FROM attendance
        ORDER BY id DESC
        """

        return self.db.execute(query)

    def get_total_entry(self):

        query = """
        SELECT COUNT(*)
        FROM attendance
        WHERE event='MASUK'
        """

        result = self.db.execute_one(query)

        return result[0]

    def get_total_exit(self):

        query = """
        SELECT COUNT(*)
        FROM attendance
        WHERE event='KELUAR'
        """

        result = self.db.execute_one(query)

        return result[0]

    def get_people_inside(self):

        return (
            self.get_total_entry()
            -
            self.get_total_exit()
        )