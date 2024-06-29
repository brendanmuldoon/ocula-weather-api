from fastapi import Depends
from main.cache.weather_cache import WeatherCache
from main.cache.abstract_weather_cache import AbstractWeatherCache

# Create a global instance of the cache
weather_cache_instance = WeatherCache()


def get_weather_cache() -> AbstractWeatherCache:
    return weather_cache_instance
