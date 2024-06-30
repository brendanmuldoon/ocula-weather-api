import logging
from logging.config import dictConfig

from main.config.log_config import LogConfig
from main.database.abstract_database import AbstractDatabase
from main.database.sqlite_database_singleton import SQLiteDatabaseSingleton
from main.decorator.database_error_decorator import handle_sqlite_db_exceptions
from main.entity.error_weather_response import ErrorResponse
from main.entity.success_weather_response import SuccessResponse
from main.utils.weather_constants import LOGGER_NAME

dictConfig(LogConfig().model_dump())
logger = logging.getLogger(LOGGER_NAME)


class SQLiteDatabase(AbstractDatabase):

    def __init__(self):
        self.db_singleton = SQLiteDatabaseSingleton()
        self.connection = self.db_singleton.get_connection()
        self.cursor = self.db_singleton.get_cursor()

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
