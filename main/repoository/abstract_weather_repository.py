from abc import ABC, abstractmethod

from main.entity.weather_request import WeatherRequest


class AbstractWeatherRepository(ABC):

    @abstractmethod
    def post_weather_data(self, request: WeatherRequest):
        raise NotImplementedError
