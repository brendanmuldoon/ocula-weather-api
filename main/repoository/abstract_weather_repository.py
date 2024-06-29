from abc import ABC, abstractmethod

from main.entity.weather_response import WeatherResponse


class AbstractWeatherRepository(ABC):

    @abstractmethod
    def store_weather_data(self, data: WeatherResponse):
        raise NotImplementedError
