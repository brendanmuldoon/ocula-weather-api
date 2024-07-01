from abc import ABC, abstractmethod


class AbstractWeatherCache(ABC):

    @abstractmethod
    def get(self, key: str):
        raise NotImplementedError

    @abstractmethod
    def set(self, date_key, city_key, value):
        raise NotImplementedError

    @abstractmethod
    def load(self):
        raise NotImplementedError
