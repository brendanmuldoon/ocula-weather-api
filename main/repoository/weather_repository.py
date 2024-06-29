from main.entity.weather_response import WeatherResponse
from main.repoository.abstract_weather_repository import AbstractWeatherRepository


class WeatherRepository(AbstractWeatherRepository):

    def store_weather_data(self, data: WeatherResponse):
        return data
