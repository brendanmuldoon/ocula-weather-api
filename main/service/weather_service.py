from fastapi import Depends

from main.cache.abstract_weather_cache import AbstractWeatherCache
from main.cache.weather_cache_singleton import get_weather_cache
from main.client.abstract_weather_api_client import AbstractWeatherApiClient
from main.client.weather_api_client import WeatherApiClient
from main.entity.final_response import FinalResponse
from main.repoository.abstract_weather_repository import AbstractWeatherRepository
from main.repoository.weather_repository import WeatherRepository
from main.utils import weather_utils


class WeatherService:

    def __init__(self,
                 weather_repo: AbstractWeatherRepository = Depends(WeatherRepository),
                 weather_api_client: AbstractWeatherApiClient = Depends(WeatherApiClient),
                 weather_cache: AbstractWeatherCache = Depends(get_weather_cache)):
        self.weather_repo = weather_repo
        self.weather_api_client = weather_api_client
        self.weather_cache = weather_cache

    def create_weather_data(self, city: str) -> FinalResponse:
        if not weather_utils.valid_weather_request(city):
            return weather_utils.handle_error_response("Invalid payload", "400")

        open_weather_api_response = self.weather_api_client.get_weather(city)

        if not weather_utils.is_successful_weather_api_client_response(open_weather_api_response):
            return weather_utils.handle_error_response(str(open_weather_api_response['message']),
                                                       str(open_weather_api_response['cod']))

        response = weather_utils.create_success_response(open_weather_api_response)

        repo_response = self.weather_repo.store_weather_data(response)

        self.store_in_cache(response)

        return FinalResponse(
            http_code=repo_response.http_code,
            data=repo_response)

    def get_weather_data(self, date):
        return self.weather_cache.get(date)

    def store_in_cache(self, weather_response):
        key_date = weather_utils.create_cache_key_date(weather_response.date)
        key_city = weather_utils.create_cache_key(str(weather_response.city))
        self.weather_cache.set(str(key_date).strip(), key_city, weather_response)
