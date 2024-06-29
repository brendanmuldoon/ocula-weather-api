from abc import ABC, abstractmethod


class AbstractWeatherService(ABC):

    @abstractmethod
    def create_weather_data(self, city: str):
        raise NotImplementedError

    @abstractmethod
    def get_weather_data(self, date):
        raise NotImplementedError

    @abstractmethod
    def get_all_data(self):
        raise NotImplementedError

