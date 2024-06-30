from main.database.abstract_database import AbstractDatabase
from main.database.sqlite_database_singleton import SQLiteDatabaseSingleton
from main.entity.error_weather_response import ErrorResponse
from main.entity.success_weather_response import SuccessResponse
from logging.config import dictConfig
import logging
from main.config.log_config import LogConfig

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("weather-api")


class SQLiteDatabase(AbstractDatabase):

    def __init__(self):
        self.db_singleton = SQLiteDatabaseSingleton()
        self.connection = self.db_singleton.get_connection()
        self.cursor = self.db_singleton.get_cursor()

    def insert(self, weather_data: SuccessResponse):
        data = {
            'date': weather_data.date,
            'city': weather_data.city,
            'min_temp': float(weather_data.min_temp),
            'max_temp': float(weather_data.max_temp),
            'avg_temp': float(weather_data.avg_temp),
            'humidity': int(weather_data.humidity)
        }

        check_sql = 'SELECT 1 FROM weather WHERE date = ? AND city = ?'
        self.cursor.execute(check_sql, (data['date'], data['city']))
        if self.cursor.fetchone() is not None:
            error_message = "Record already exists"
            logger.error(error_message)
            return ErrorResponse(error_message=error_message, http_code="400")

        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        sql = f'INSERT INTO weather ({columns}) VALUES ({placeholders})'

        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()
        weather_data.http_code = "201"
        logger.info("Record inserted into DB")
        return weather_data

    def get_all(self):
        sql = f'SELECT * FROM weather'

    def get_all_by_date(self, date: str):
        sql = 'SELECT * FROM weather WHERE date = ?'
        self.cursor.execute(sql, (date,))
        rows = self.cursor.fetchall()
        if not rows:
            return ErrorResponse(error_message=f"No records found for date : {date}", http_code="404")

        columns = [column[0] for column in self.cursor.description]
        results = [
            SuccessResponse(
                http_code="200",
                city=row[columns.index('city')],
                date=row[columns.index('date')],
                min_temp=str(row[columns.index('min_temp')]),
                max_temp=str(row[columns.index('max_temp')]),
                avg_temp=str(row[columns.index('avg_temp')]),
                humidity=str(row[columns.index('humidity')])
            ) for row in rows
        ]

        return results
