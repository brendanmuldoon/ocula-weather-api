from logging.config import dictConfig
import logging
from main.config.log_config import LogConfig
from main.cache.abstract_weather_cache import AbstractWeatherCache
from main.database.sqlite_database_singleton import SQLiteDatabaseSingleton
from main.entity.success_weather_response import SuccessResponse

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("weather-api")


class WeatherCache(AbstractWeatherCache):

    def __init__(self):
        self.cache = {}

    def get(self, key: str):
        date_key = key.strip()
        result = self.cache.get(date_key, {})
        success_responses = []

        # Loop through the city-to-response mappings
        for city, response in result.items():
            sr = SuccessResponse(
                http_code=response.http_code,
                city=response.city,
                date=response.date,
                min_temp=response.min_temp,
                max_temp=response.max_temp,
                avg_temp=response.avg_temp,
                humidity=response.humidity
            )
            success_responses.append(sr)

        return success_responses

    def set(self, date_key, city_key, value):
        if date_key not in self.cache:
            self.cache[date_key] = {}
        self.cache[date_key][city_key] = value
        logger.info("Record inserted into cache")

    def load(self):
        db_singleton = SQLiteDatabaseSingleton()
        cursor = db_singleton.get_cursor()
        cursor.execute("SELECT date, city, min_temp, max_temp, avg_temp, humidity FROM weather")
        rows = cursor.fetchall()
        for row in rows:
            date_key = row[0]
            city_key = row[1]
            response = SuccessResponse(
                http_code='200',
                city=row[1],
                date=row[0],
                min_temp=str(row[2]),
                max_temp=str(row[3]),
                avg_temp=str(row[4]),
                humidity=str(row[5])
            )
            self.set(date_key, city_key, response)

    def print_cache(self):
        print("Cache contents --> ")
        for date_key, cities in self.cache.items():
            print(f"Date: {date_key}")
            for city_key, value in cities.items():
                print(f"  City: {city_key}, Data: {value}")
