from fastapi import Depends
from logging.config import dictConfig
import logging

from main.cache.weather_cache import get_weather_cache
from main.config.log_config import LogConfig
from main.cache.abstract_weather_cache import AbstractWeatherCache
# from main.cache.weather_cache_singleton import get_weather_cache
from main.client.abstract_weather_api_client import AbstractWeatherApiClient
from main.client.weather_api_client import WeatherApiClient
from main.entity.final_response import FinalResponse
from main.entity.success_weather_response import SuccessResponse
from main.repoository.abstract_weather_repository import AbstractWeatherRepository
from main.repoository.weather_repository import WeatherRepository
from main.service.abstract_weather_service import AbstractWeatherService
from main.utils import weather_utils
from main.utils.weather_constants import LOGGER_NAME

dictConfig(LogConfig().model_dump())
logger = logging.getLogger(LOGGER_NAME)


class WeatherService(AbstractWeatherService):

    def __init__(self,
                 weather_repo: AbstractWeatherRepository = Depends(WeatherRepository),
                 weather_api_client: AbstractWeatherApiClient = Depends(WeatherApiClient),
                 weather_cache: AbstractWeatherCache = Depends(get_weather_cache)):
        self.weather_repo = weather_repo
        self.weather_api_client = weather_api_client
        self.weather_cache = weather_cache

    def create_weather_data(self, city: str):
        logger.info("Validating request ...")
        if not weather_utils.valid_weather_request(city):
            return weather_utils.handle_error_response("Invalid request", "400")

        open_weather_api_response = self.weather_api_client.get_weather(city)

        if not weather_utils.is_successful_weather_api_client_response(open_weather_api_response):
            return weather_utils.handle_error_response(str(open_weather_api_response['message']),
                                                       str(open_weather_api_response['cod']))

        response = weather_utils.create_dto_object(open_weather_api_response)

        data = self.weather_repo.store_weather_data(response)

        return self.handle_response(data)

    def get_weather_data(self, date):
        cache_data = self.weather_cache.get(date)
        if len(cache_data) > 0:
            return self.return_cache_data(cache_data)
        logger.info("Nothing in the cache for that date, going to the database")
        db_data = self.weather_repo.get_all_by_date(date)
        return FinalResponse(
            http_code=weather_utils.get_http_code_from_db_response(db_data),
            data=db_data)

    def store_in_cache(self, weather_response):
        logger.info("Inserting into cache")
        key_date = weather_response.date
        key_city = weather_response.city
        self.weather_cache.set(str(key_date).strip(), key_city, weather_response)

    def get_all_data(self):
        self.weather_repo.get_all_data()

    def handle_response(self, data):
        # if weather_utils.status_code_2xx(data):
        if isinstance(data, SuccessResponse):
            self.store_in_cache(data)
            return FinalResponse(
                http_code="201",
                data=[data])
        return FinalResponse(
            http_code=data.http_code,
            data=data)

    def return_cache_data(self, cache_data):
        logger.info("Returning data from cache")
        return FinalResponse(
            http_code="200",
            data=cache_data)
