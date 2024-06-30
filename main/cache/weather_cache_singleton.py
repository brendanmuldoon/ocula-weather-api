from main.cache.abstract_weather_cache import AbstractWeatherCache
from main.cache.weather_cache import WeatherCache
from main.database.sqlite_database import get_sqlite_database_singleton

# weather_cache_instance = WeatherCache(SQLiteDatabaseSingleton())
weather_cache_instance = WeatherCache(get_sqlite_database_singleton())


def get_weather_cache() -> AbstractWeatherCache:
    return weather_cache_instance
