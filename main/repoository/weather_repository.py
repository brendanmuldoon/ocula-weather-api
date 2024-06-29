from fastapi import Depends

from main.database.abstract_database import AbstractDatabase
from main.database.sqlite_database import SQLiteDatabase
from main.entity.error_weather_response import ErrorResponse
from main.entity.success_weather_response import SuccessResponse
from main.repoository.abstract_weather_repository import AbstractWeatherRepository


class WeatherRepository(AbstractWeatherRepository):

    def __init__(self, database: AbstractDatabase = Depends(SQLiteDatabase)):
        self.database = database

    def store_weather_data(self, data: SuccessResponse):
        return self.database.insert(data)

    def get_all_data(self):
        self.database.get_all()
