from main.cache.abstract_weather_cache import AbstractWeatherCache


class WeatherCache(AbstractWeatherCache):

    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key.strip())

    def set(self, date_key, city_key, value):
        if date_key not in self.cache:
            self.cache[date_key] = {}
        self.cache[date_key][city_key] = value

    def load(self):
        return None
