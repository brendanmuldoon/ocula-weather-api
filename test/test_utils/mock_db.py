from main.database.sqlite_database import SQLiteDatabase


class MockDatabase(SQLiteDatabase):
    def __init__(self):
        self.data = [
            ('2024-06-29', 'London', 15.5, 25.0, 20.25, 60),
            ('2024-06-29', 'Paris', 17.0, 27.0, 22.0, 55)
        ]

    def get_cursor(self):
        return self

    def execute(self, sql, params=None):
        # Simulate the execution of SQL command
        pass

    def fetchall(self):
        # Return the mock data
        return self.data
