import logging
from logging.config import dictConfig

from fastapi import Depends

from main.config.log_config import LogConfig
from main.database.abstract_database import AbstractDatabase
from main.database.sqlite_database import SQLiteDatabase
from main.entity.success_weather_response import SuccessResponse
from main.repoository.abstract_weather_repository import AbstractWeatherRepository

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("weather-api")


class WeatherRepository(AbstractWeatherRepository):

    def __init__(self, database: AbstractDatabase = Depends(SQLiteDatabase)):
        self.database = database

    def store_weather_data(self, data: SuccessResponse):
        logger.info("Inserting record into DB")
        return self.database.insert(data)

    def get_all_data(self):
        self.database.get_all()

    def get_all_by_date(self, date):
        logger.info("Retrieving records from database")
        return self.database.get_all_by_date(date)
