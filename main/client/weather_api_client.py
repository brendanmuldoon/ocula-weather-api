import os

import requests
from dotenv import load_dotenv

from main.client.abstract_weather_api_client import AbstractWeatherApiClient

load_dotenv()


class WeatherApiClient(AbstractWeatherApiClient):
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.appid = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self, city: str):
        url = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.appid
        }
        return requests.get(url, params=params).json()

    def response_is_2xx(self, response):
        return bool(response.status_code == 200)
