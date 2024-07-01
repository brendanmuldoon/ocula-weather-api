from abc import ABC, abstractmethod


class AbstractWeatherApiClient(ABC):

    @abstractmethod
    def get_weather(self, city: str):
        raise NotImplementedError
