import logging
from logging.config import dictConfig
import sqlite3
from threading import Lock

from main.config.log_config import LogConfig
from main.database.abstract_database import AbstractDatabase
from main.decorator.sqlite_database_error_decorator import handle_sqlite_db_exceptions
from main.entity.error_weather_response import ErrorResponse
from main.entity.success_weather_response import SuccessResponse
from main.utils.weather_constants import LOGGER_NAME

dictConfig(LogConfig().model_dump())
logger = logging.getLogger(LOGGER_NAME)


def get_sqlite_database_singleton() -> AbstractDatabase:
    return SQLiteDatabase()


class SQLiteDatabase(AbstractDatabase):

    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SQLiteDatabase, cls).__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
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
                pass

        self.connection.commit()

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor

    @handle_sqlite_db_exceptions
    def insert(self, weather_data: SuccessResponse):
        data = {
            'date': weather_data.date,
            'city': weather_data.city,
            'min_temp': float(weather_data.min_temp),
            'max_temp': float(weather_data.max_temp),
            'avg_temp': float(weather_data.avg_temp),
            'humidity': int(weather_data.humidity)
        }
        self.perform_insert(data)
        return weather_data

    @handle_sqlite_db_exceptions
    def get_all_by_date(self, date: str):
        rows = self.get_rows(date)
        if not rows:
            return self.handle_no_records_found(date)

        columns = [column[0] for column in self.cursor.description]
        results = [
            SuccessResponse(
                city=row[columns.index('city')],
                date=row[columns.index('date')],
                min_temp=str(row[columns.index('min_temp')]),
                max_temp=str(row[columns.index('max_temp')]),
                avg_temp=str(row[columns.index('avg_temp')]),
                humidity=str(row[columns.index('humidity')])
            ) for row in rows
        ]

        return results

    @handle_sqlite_db_exceptions
    def insert(self, weather_data: SuccessResponse):
        data = {
            'date': weather_data.date,
            'city': weather_data.city,
            'min_temp': float(weather_data.min_temp),
            'max_temp': float(weather_data.max_temp),
            'avg_temp': float(weather_data.avg_temp),
            'humidity': int(weather_data.humidity)
        }
        self.perform_insert(data)
        return weather_data

    def get_all(self):
        return

    @handle_sqlite_db_exceptions
    def get_all_by_date(self, date: str):
        rows = self.get_rows(date)
        if not rows:
            return self.handle_no_records_found(date)

        columns = [column[0] for column in self.cursor.description]
        results = [
            SuccessResponse(
                city=row[columns.index('city')],
                date=row[columns.index('date')],
                min_temp=str(row[columns.index('min_temp')]),
                max_temp=str(row[columns.index('max_temp')]),
                avg_temp=str(row[columns.index('avg_temp')]),
                humidity=str(row[columns.index('humidity')])
            ) for row in rows
        ]

        return results

    def perform_insert(self, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        sql = f'INSERT INTO weather ({columns}) VALUES ({placeholders})'
        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()
        logger.info("Record inserted into DB")

    def get_rows(self, date):
        sql = 'SELECT * FROM weather WHERE date = ?'
        self.cursor.execute(sql, (date,))
        return self.cursor.fetchall()

    def handle_no_records_found(self, date):
        error_message = f"No records found for date : {date}"
        logger.error(error_message)
        return ErrorResponse(error_message=error_message, http_code="404")
