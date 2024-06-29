from fastapi import Depends

from main.cache.weather_cache import WeatherCache
from main.cache.abstract_weather_cache import AbstractWeatherCache
from main.client.abstract_weather_api_client import AbstractWeatherApiClient
from main.client.weather_api_client import WeatherApiClient
from main.entity.weather_request import WeatherRequest
from main.entity.weather_response import WeatherResponse
from main.repoository.abstract_weather_repository import AbstractWeatherRepository
from main.repoository.weather_repository import WeatherRepository
from main.utils import weather_utils


class WeatherService:

    def __init__(self, weather_repo: AbstractWeatherRepository = Depends(WeatherRepository),
                 weather_api_client: AbstractWeatherApiClient = Depends(WeatherApiClient),
                 weather_cache: AbstractWeatherCache = Depends(WeatherCache)):
        self.weather_repo = weather_repo
        self.weather_api_client = weather_api_client
        self.weather_cache = weather_cache

    def create_weather_data(self, request: WeatherRequest) -> WeatherResponse:
        if not weather_utils.valid_weather_request(request):
            return weather_utils.handle_error_response("Invalid payload", "400")

        open_weather_api_response = self.weather_api_client.get_weather(request)
        if not weather_utils.is_successful_weather_api_client_response(open_weather_api_response):
            return weather_utils.handle_error_response(str(open_weather_api_response.__getattribute__('error_message')),
                                                       str(open_weather_api_response.__getattribute__('http_code')))

        self.store_in_cache_and_db(data=open_weather_api_response)

        return self.weather_repo.store_weather_data(data=open_weather_api_response)

    def store_in_cache_and_db(self, data):
        self.weather_cache.store(data)
