from main.cache.abstract_weather_cache import AbstractWeatherCache
from main.cache.weather_cache import WeatherCache

weather_cache_instance = WeatherCache()


def get_weather_cache() -> AbstractWeatherCache:
    return weather_cache_instance
