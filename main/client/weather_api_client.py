import os
from logging.config import dictConfig
import logging
from main.config.log_config import LogConfig
import requests
from dotenv import load_dotenv

from main.client.abstract_weather_api_client import AbstractWeatherApiClient
from main.utils.weather_constants import LOGGER_NAME

load_dotenv()

dictConfig(LogConfig().model_dump())
logger = logging.getLogger(LOGGER_NAME)


class WeatherApiClient(AbstractWeatherApiClient):
    def __init__(self):
        self.base_url = os.getenv("OPENWEATHER_API_URL")
        self.appid = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self, city: str):
        logger.info("Making api request to " + self.base_url)
        params = {
            "q": city,
            "appid": self.appid
        }
        return requests.get(self.base_url, params=params).json()
