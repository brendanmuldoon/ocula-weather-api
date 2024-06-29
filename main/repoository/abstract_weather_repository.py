from abc import ABC, abstractmethod

from main.entity.success_weather_response import SuccessResponse


class AbstractWeatherRepository(ABC):

    @abstractmethod
    def store_weather_data(self, data: SuccessResponse):
        raise NotImplementedError
