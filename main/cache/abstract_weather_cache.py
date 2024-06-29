from abc import ABC, abstractmethod

from main.entity.weather_response import WeatherResponse


class AbstractWeatherCache(ABC):

    @abstractmethod
    def store(self, data: WeatherResponse):
        raise NotImplementedError

    @abstractmethod
    def load(self):
        raise NotImplementedError
