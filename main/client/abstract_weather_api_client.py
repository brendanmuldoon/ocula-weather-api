from abc import ABC, abstractmethod

from main.entity.weather_request import WeatherRequest
from main.entity.weather_response import WeatherResponse


class AbstractWeatherApiClient(ABC):

    @abstractmethod
    def get_weather(self, request: WeatherRequest) -> WeatherResponse:
        raise NotImplementedError
