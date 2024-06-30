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
        self.connection = sqlite3.connect(':memory:', check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_weather_table()
        self.load_dummy_data()

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

    def load_dummy_data(self):
        dummy_data = [
            {'date': '2024-06-29', 'city': 'London', 'min_temp': 15.5, 'max_temp': 25.0, 'avg_temp': 20.25,
             'humidity': 60},
            {'date': '2024-06-29', 'city': 'Paris', 'min_temp': 17.0, 'max_temp': 27.0, 'avg_temp': 22.0,
             'humidity': 55},
            {'date': '2024-06-30', 'city': 'New York', 'min_temp': 20.0, 'max_temp': 30.0, 'avg_temp': 25.0,
             'humidity': 70},
            {'date': '2024-06-30', 'city': 'Tokyo', 'min_temp': 22.0, 'max_temp': 32.0, 'avg_temp': 27.0,
             'humidity': 65}
        ]

        insert_sql = """
        INSERT INTO weather (date, city, min_temp, max_temp, avg_temp, humidity)
        VALUES (?, ?, ?, ?, ?, ?)
        """

        for record in dummy_data:
            try:
                self.cursor.execute(insert_sql, (
                    record['date'], record['city'], record['min_temp'], record['max_temp'], record['avg_temp'],
                    record['humidity']))
            except sqlite3.IntegrityError:
                # Handle the case where the record already exists (based on UNIQUE constraint)
                pass

        self.connection.commit()
