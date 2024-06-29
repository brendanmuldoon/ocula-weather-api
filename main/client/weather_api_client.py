import os

import requests
from dotenv import load_dotenv

from main.client.abstract_weather_api_client import AbstractWeatherApiClient
from main.entity.weather_request import WeatherRequest
from main.entity.weather_response import WeatherResponse

load_dotenv()


class WeatherApiClient(AbstractWeatherApiClient):
    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.appid = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self, request: WeatherRequest) -> WeatherResponse:
        url = f"{self.base_url}/weather"

        params = {
            "q": request.city,
            "appid": self.appid
        }
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            print(data)
            min_temp = data['main']['temp_min'] - 273.15
            max_temp = data['main']['temp_max'] - 273.15
            avg_temp = (min_temp + max_temp) / 2
            min_temp_formatted = f"{min_temp:.2f}"
            max_temp_formatted = f"{max_temp:.2f}"
            avg_temp_formatted = f"{avg_temp:.2f}"
            return WeatherResponse.get(
                city=request.city,
                date=request.date,
                min_temp=str(min_temp_formatted),
                max_temp=str(max_temp_formatted),
                avg_temp=str(avg_temp_formatted),
                humidity=str(data['main']['humidity']),
                http_code="200"
            )
        else:
            print('Error fetching weather data')
            return WeatherResponse.error(data['message'], str(data['cod']))
