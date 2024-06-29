from main.cache.abstract_weather_cache import AbstractWeatherCache
from main.entity.weather_response import WeatherResponse


class WeatherCache(AbstractWeatherCache):

    def store(self, data: WeatherResponse):
        print('cache: ')
        print(data)

    def load(self):
        return None
