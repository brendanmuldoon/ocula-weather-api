from main.entity.success_weather_response import SuccessResponse
from main.repoository.abstract_weather_repository import AbstractWeatherRepository
import sqlite3

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()


class WeatherRepository(AbstractWeatherRepository):

    def store_weather_data(self, data: SuccessResponse):
        data.http_code = "201"

        conn.commit()
        conn.close()
        return data
