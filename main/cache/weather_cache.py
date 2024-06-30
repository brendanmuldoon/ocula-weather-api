from logging.config import dictConfig
import logging

from fastapi import Depends

from main.config.log_config import LogConfig
from main.cache.abstract_weather_cache import AbstractWeatherCache
from main.database.abstract_database import AbstractDatabase
from main.database.sqlite_database import SQLiteDatabase
from main.decorator.cache_error_decorator import handle_cache_db_exceptions
from main.entity.success_weather_response import SuccessResponse
from main.utils.weather_constants import LOGGER_NAME

dictConfig(LogConfig().model_dump())
logger = logging.getLogger(LOGGER_NAME)


class WeatherCache(AbstractWeatherCache):

    def __init__(self, db_singleton: AbstractDatabase = Depends(SQLiteDatabase)):
        self.cache = {}
        self.db_singleton = db_singleton

    def get(self, key: str):
        date_key = key.strip()
        result = self.cache.get(date_key, {})
        data = self.get_data(result)
        return data

    def set(self, date_key, city_key, value):
        if date_key not in self.cache:
            self.cache[date_key] = {}
        self.cache[date_key][city_key] = value
        logger.info("Record inserted into cache")

    def load(self):
        rows = self.get_database_rows()
        self.set_rows(rows)

    def get_data(self, result):
        data = []
        for city, response in result.items():
            sr = SuccessResponse(
                city=response.city,
                date=response.date,
                min_temp=response.min_temp,
                max_temp=response.max_temp,
                avg_temp=response.avg_temp,
                humidity=response.humidity
            )
            data.append(sr)
        return data

    def set_rows(self, rows):
        for row in rows:
            date_key = row[0]
            city_key = row[1]
            response = SuccessResponse(
                city=row[1],
                date=row[0],
                min_temp=str(row[2]),
                max_temp=str(row[3]),
                avg_temp=str(row[4]),
                humidity=str(row[5])
            )
            self.set(date_key, city_key, response)

    @handle_cache_db_exceptions
    def get_database_rows(self):
        cursor = self.db_singleton.get_cursor()
        cursor.execute("SELECT date, city, min_temp, max_temp, avg_temp, humidity FROM weather")
        return cursor.fetchall()
