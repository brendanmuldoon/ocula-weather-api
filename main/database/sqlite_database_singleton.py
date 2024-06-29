import sqlite3
from threading import Lock


class SQLiteDatabaseSingleton:
    instance = None
    lock = Lock()

    def __new__(cls):
        with cls.lock:
            if cls.instance is None:
                cls.instance = super(SQLiteDatabaseSingleton, cls).__new__(cls)
                cls.instance._initialize()
        return cls.instance

    def _initialize(self):
        # Create an in-memory SQLite database
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()
        self.create_weather_table()

    def create_weather_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            city TEXT NOT NULL,
            min_temp REAL NOT NULL,
            max_temp REAL NOT NULL,
            avg_temp REAL NOT NULL,
            humidity INTEGER NOT NULL,
            UNIQUE(date, city)
        )
        """
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
